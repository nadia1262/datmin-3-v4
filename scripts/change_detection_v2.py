"""
change_detection_v2.py — Scientifically Valid Temporal Change Detection
========================================================================
Implements Steps 3-8 of the temporal pipeline rebuild:
  Step 3: Land-cover composition on common spatial domain
  Step 4: Consecutive change detection (5 intervals)
  Step 5: Long-term change (2019→2024)
  Step 6: Temporal consistency classification
  Step 7: Confidence/uncertainty evaluation
  Step 8: Forest loss/gain persistence evaluation

KEY PRINCIPLE: All comparisons use the SAME 118,943-point common domain
so that denominators are identical across years.
"""

import os
import sys
import time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *


# ============================================================
# STEP 2: Load & Filter to Common Spatial Domain
# ============================================================

def load_common_domain():
    """Load the precomputed common domain coordinates."""
    if not os.path.exists(COMMON_DOMAIN_FILE):
        print(f"  [FAIL] Common domain file not found: {COMMON_DOMAIN_FILE}")
        print("  Run step1b_overlap.py first to generate it.")
        sys.exit(1)

    common = pd.read_csv(COMMON_DOMAIN_FILE)
    print(f"  Common domain: {len(common):,} points")
    return common


def load_predictions_common_domain(model_name, years, common_domain):
    """Load predictions for all years, filtered to common domain only."""
    all_dfs = {}
    common_set = set(zip(common_domain['lon'].round(4), common_domain['lat'].round(4)))

    for year in years:
        fpath = os.path.join(PREDICTIONS_DIR, f'predictions_{model_name}_{year}.csv')
        if not os.path.exists(fpath):
            print(f"  [SKIP] {fpath} not found")
            continue

        df = pd.read_csv(fpath)
        df['lon_r'] = df['lon'].round(4)
        df['lat_r'] = df['lat'].round(4)

        # Filter to common domain
        df['in_common'] = list(zip(df['lon_r'], df['lat_r']))
        df['in_common'] = df['in_common'].apply(lambda x: x in common_set)
        df_filtered = df[df['in_common']].drop(columns=['in_common', 'lon_r', 'lat_r']).copy()

        all_dfs[year] = df_filtered
        print(f"  {year}: {len(df):,} total -> {len(df_filtered):,} in common domain")

    return all_dfs


def build_temporal_profile(all_dfs, common_domain):
    """Build unified temporal profile by matching on coordinates."""
    profile = common_domain[['lon', 'lat']].copy()
    profile['lon'] = profile['lon'].round(4)
    profile['lat'] = profile['lat'].round(4)

    for year in sorted(all_dfs.keys()):
        df = all_dfs[year].copy()
        df['lon'] = df['lon'].round(4)
        df['lat'] = df['lat'].round(4)

        # Columns to merge: predicted_class, max_prob, entropy
        merge_cols = ['lon', 'lat', 'predicted_class']
        if 'max_prob' in df.columns:
            merge_cols.append('max_prob')
        if 'entropy' in df.columns:
            merge_cols.append('entropy')

        # Rename for year-specific columns
        rename_map = {
            'predicted_class': f'class_{year}',
        }
        if 'max_prob' in df.columns:
            rename_map['max_prob'] = f'prob_{year}'
        if 'entropy' in df.columns:
            rename_map['entropy'] = f'entropy_{year}'

        df_merge = df[merge_cols].rename(columns=rename_map)

        # Remove duplicates before merge (keep first)
        df_merge = df_merge.drop_duplicates(subset=['lon', 'lat'], keep='first')

        profile = profile.merge(df_merge, on=['lon', 'lat'], how='left')

    # Drop rows with any missing year
    class_cols = [f'class_{y}' for y in sorted(all_dfs.keys())]
    before = len(profile)
    profile = profile.dropna(subset=class_cols)
    after = len(profile)

    if before != after:
        print(f"  [WARN] Dropped {before - after} rows with missing predictions")

    for col in class_cols:
        profile[col] = profile[col].astype(int)

    print(f"  Temporal profile: {len(profile):,} matched points across {len(all_dfs)} years")
    return profile


# ============================================================
# STEP 3: Land-Cover Composition on Common Domain
# ============================================================

def compute_composition(profile, years, output_dir):
    """Compute land-cover composition for each year on the common domain."""
    print(f"\n{'='*60}")
    print("  STEP 3: LAND-COVER COMPOSITION (Common Domain)")
    print(f"{'='*60}")

    rows = []
    for year in sorted(years):
        col = f'class_{year}'
        if col not in profile.columns:
            continue

        n_total = len(profile)
        counts = profile[col].value_counts()
        for cls_id, count in counts.items():
            pct = 100 * count / n_total
            rows.append({
                'year': year,
                'class_id': int(cls_id),
                'class_name': CLASS_NAMES.get(int(cls_id), f'Unknown_{cls_id}'),
                'count': int(count),
                'percentage': round(pct, 4),
                'n_total': n_total,
            })

    comp_df = pd.DataFrame(rows)
    comp_df = comp_df.sort_values(['year', 'class_id']).reset_index(drop=True)

    # Print table
    print(f"\n  {'Year':>6} {'Forest':>10} {'Shrub/Ag':>10} {'Built-up':>10} {'Bare/Mine':>10} {'Water':>10} {'N':>10}")
    print(f"  {'-'*72}")
    for year in sorted(years):
        yr_data = comp_df[comp_df['year'] == year]
        vals = {}
        for _, row in yr_data.iterrows():
            vals[row['class_id']] = row['percentage']
        n = yr_data['n_total'].iloc[0] if len(yr_data) > 0 else 0
        print(f"  {year:>6} {vals.get(0,0):>9.2f}% {vals.get(1,0):>9.2f}% {vals.get(2,0):>9.2f}% {vals.get(3,0):>9.2f}% {vals.get(4,0):>9.2f}% {n:>10,}")

    # Save
    comp_file = os.path.join(output_dir, 'common_domain_composition.csv')
    comp_df.to_csv(comp_file, index=False)
    print(f"\n  [OK] Saved {comp_file}")

    # Plot temporal trends
    plot_composition_trends(comp_df, years, output_dir)

    return comp_df


def plot_composition_trends(comp_df, years, output_dir):
    """Plot class proportions over time."""
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = {
        'Forest': '#2d6a4f',
        'Shrubland/Agriculture': '#e9c46a',
        'Built-up': '#e76f51',
        'Bare/Mining-like': '#8d6e63',
        'Water': '#219ebc',
    }

    for cls_name in CLASS_LABELS:
        subset = comp_df[comp_df['class_name'] == cls_name].sort_values('year')
        if not subset.empty:
            ax.plot(subset['year'], subset['percentage'], 'o-',
                    label=cls_name, linewidth=2.5, markersize=7,
                    color=colors.get(cls_name, None))

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Proportion (%)', fontsize=12)
    ax.set_title('Land Cover Composition Over Time\n(Common Spatial Domain, N=118,943)',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(sorted(years))
    plt.tight_layout()

    fig_path = os.path.join(output_dir, 'temporal_trends_v2.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved {fig_path}")


# ============================================================
# STEP 4: Consecutive Change Detection
# ============================================================

def compute_transition_matrix(profile, start_year, end_year):
    """Compute NxN transition matrix between two years."""
    col_start = f'class_{start_year}'
    col_end = f'class_{end_year}'

    cm = pd.crosstab(
        profile[col_start].map(CLASS_NAMES),
        profile[col_end].map(CLASS_NAMES),
        margins=True
    )
    return cm


def detect_transitions(profile, start_year, end_year):
    """Detect and summarize transitions between two years."""
    col_start = f'class_{start_year}'
    col_end = f'class_{end_year}'

    n_total = len(profile)
    changed_mask = profile[col_start] != profile[col_end]
    n_changed = changed_mask.sum()
    pct_changed = 100 * n_changed / n_total

    # Specific transitions
    forest_loss = ((profile[col_start] == 0) & (profile[col_end] != 0)).sum()
    forest_gain = ((profile[col_start] != 0) & (profile[col_end] == 0)).sum()
    urbanization = ((profile[col_start] != 2) & (profile[col_end] == 2)).sum()
    mining_expansion = ((profile[col_start] != 3) & (profile[col_end] == 3)).sum()

    print(f"\n  --- {start_year} -> {end_year} ---")
    print(f"  Total: {n_total:,}  Changed: {n_changed:,} ({pct_changed:.2f}%)")
    print(f"  Forest loss: {forest_loss:,}  Forest gain: {forest_gain:,}")
    print(f"  Urbanization: {urbanization:,}  Mining expansion: {mining_expansion:,}")

    # Top transitions
    transition_codes = (profile[col_start].astype(str) + '->' + profile[col_end].astype(str))
    changed_transitions = transition_codes[changed_mask].value_counts().head(10)
    print(f"  Top transitions:")
    for code, count in changed_transitions.items():
        from_cls, to_cls = int(code.split('->')[0]), int(code.split('->')[1])
        from_name = CLASS_NAMES.get(from_cls, '?')
        to_name = CLASS_NAMES.get(to_cls, '?')
        print(f"    {from_name} -> {to_name}: {count:,} ({100*count/n_total:.3f}%)")

    return {
        'start_year': start_year,
        'end_year': end_year,
        'n_total': n_total,
        'n_changed': int(n_changed),
        'change_rate_pct': round(pct_changed, 4),
        'forest_loss': int(forest_loss),
        'forest_gain': int(forest_gain),
        'urbanization': int(urbanization),
        'mining_expansion': int(mining_expansion),
    }


def plot_transition_matrix(cm, start_year, end_year, output_dir):
    """Plot heatmap of transition matrix."""
    cm_plot = cm.drop('All', axis=0, errors='ignore').drop('All', axis=1, errors='ignore')

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        cm_plot, annot=True, fmt='d', cmap='YlOrRd',
        ax=ax, linewidths=0.5
    )
    ax.set_title(f'Land Cover Transition: {start_year} -> {end_year}\n(Common Domain, N={cm_plot.values.sum():,})',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel(f'Class in {end_year}', fontsize=11)
    ax.set_ylabel(f'Class in {start_year}', fontsize=11)
    plt.tight_layout()

    fig_path = os.path.join(output_dir, f'transition_matrix_{start_year}_{end_year}.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()


def run_consecutive_transitions(profile, years, output_dir):
    """Run consecutive transitions for all adjacent year pairs."""
    print(f"\n{'='*60}")
    print("  STEP 4: CONSECUTIVE CHANGE DETECTION")
    print(f"{'='*60}")

    all_summaries = []
    consecutive_pairs = [(years[i], years[i+1]) for i in range(len(years)-1)]

    for start_yr, end_yr in consecutive_pairs:
        # Transition matrix
        cm = compute_transition_matrix(profile, start_yr, end_yr)
        cm.to_csv(os.path.join(output_dir, f'transition_matrix_{start_yr}_{end_yr}.csv'))
        plot_transition_matrix(cm, start_yr, end_yr, output_dir)

        # Summary
        summary = detect_transitions(profile, start_yr, end_yr)
        all_summaries.append(summary)

    # Save all summaries
    summary_df = pd.DataFrame(all_summaries)
    summary_df.to_csv(os.path.join(output_dir, 'consecutive_change_summary.csv'), index=False)
    print(f"\n  [OK] Saved consecutive change summary ({len(consecutive_pairs)} intervals)")

    return summary_df


# ============================================================
# STEP 5: Long-Term Change
# ============================================================

def run_long_term_change(profile, start_year, end_year, output_dir):
    """Compute long-term transition (baseline -> endline)."""
    print(f"\n{'='*60}")
    print(f"  STEP 5: LONG-TERM CHANGE ({start_year} -> {end_year})")
    print(f"{'='*60}")

    # Transition matrix
    cm = compute_transition_matrix(profile, start_year, end_year)
    cm.to_csv(os.path.join(output_dir, f'transition_matrix_{start_year}_{end_year}.csv'))
    plot_transition_matrix(cm, start_year, end_year, output_dir)

    print(f"\n  Transition Matrix ({start_year} -> {end_year}):")
    print(cm.to_string())

    # Summary
    summary = detect_transitions(profile, start_year, end_year)

    # Build change points for driver analysis
    col_start = f'class_{start_year}'
    col_end = f'class_{end_year}'
    change_df = profile[['lon', 'lat', col_start, col_end]].copy()
    change_df.columns = ['lon', 'lat', 'class_start', 'class_end']
    change_df['is_changed'] = (change_df['class_start'] != change_df['class_end']).astype(int)
    change_df['forest_loss'] = ((change_df['class_start'] == 0) & (change_df['class_end'] != 0)).astype(int)
    change_df['forest_gain'] = ((change_df['class_start'] != 0) & (change_df['class_end'] == 0)).astype(int)
    change_df['urbanization'] = ((change_df['class_start'] != 2) & (change_df['class_end'] == 2)).astype(int)
    change_df['mining_expansion'] = ((change_df['class_start'] != 3) & (change_df['class_end'] == 3)).astype(int)

    change_file = os.path.join(output_dir, f'change_points_{start_year}_{end_year}.csv')
    change_df.to_csv(change_file, index=False)
    print(f"\n  [OK] Saved {change_file}")

    return summary, change_df


# ============================================================
# STEP 6: Temporal Consistency Classification
# ============================================================

def classify_temporal_consistency(profile, years):
    """
    Classify each point's temporal trajectory into:
      A. Stable — same class all years
      B. Persistent transition — changed once, stayed changed
      C. Temporary transition — changed and reverted
      D. Oscillating — flipped >=3 times
    """
    print(f"\n{'='*60}")
    print("  STEP 6: TEMPORAL CONSISTENCY CLASSIFICATION")
    print(f"{'='*60}")

    class_cols = [f'class_{y}' for y in sorted(years)]
    trajectory = profile[class_cols].values

    n = len(trajectory)
    labels = []

    for i in range(n):
        seq = trajectory[i]
        unique_classes = len(set(seq))

        if unique_classes == 1:
            labels.append('Stable')
            continue

        # Count transitions (number of class changes between consecutive years)
        n_transitions = sum(1 for j in range(len(seq)-1) if seq[j] != seq[j+1])

        if n_transitions == 1:
            # Changed once — check if it stayed changed
            # Find the change point
            change_idx = next(j for j in range(len(seq)-1) if seq[j] != seq[j+1])
            # Check if everything after the change is the same
            if len(set(seq[change_idx+1:])) == 1:
                labels.append('Persistent transition')
            else:
                labels.append('Temporary transition')
        elif n_transitions == 2:
            # Two transitions — could be temporary (A->B->A) or complex
            if seq[0] == seq[-1] and unique_classes == 2:
                labels.append('Temporary transition')
            else:
                labels.append('Temporary transition')
        elif n_transitions >= 3:
            labels.append('Oscillating')
        else:
            labels.append('Temporary transition')

    profile['temporal_consistency'] = labels

    # Summary
    consistency_counts = profile['temporal_consistency'].value_counts()
    total = len(profile)

    print(f"\n  {'Category':<30s} {'Count':>10s} {'Percentage':>12s}")
    print(f"  {'-'*54}")
    for cat in ['Stable', 'Persistent transition', 'Temporary transition', 'Oscillating']:
        count = consistency_counts.get(cat, 0)
        pct = 100 * count / total
        print(f"  {cat:<30s} {count:>10,} {pct:>11.2f}%")

    # Save summary
    summary_rows = []
    for cat in ['Stable', 'Persistent transition', 'Temporary transition', 'Oscillating']:
        count = int(consistency_counts.get(cat, 0))
        summary_rows.append({
            'category': cat,
            'count': count,
            'percentage': round(100 * count / total, 4),
        })

    return profile, pd.DataFrame(summary_rows)


# ============================================================
# STEP 7: Confidence / Uncertainty Evaluation
# ============================================================

def evaluate_confidence(profile, years, output_dir):
    """Evaluate prediction confidence for different transition types."""
    print(f"\n{'='*60}")
    print("  STEP 7: CONFIDENCE / UNCERTAINTY EVALUATION")
    print(f"{'='*60}")

    prob_cols = [f'prob_{y}' for y in sorted(years)]
    has_probs = all(col in profile.columns for col in prob_cols)

    if not has_probs:
        print("  [WARN] Probability columns not available. Skipping confidence analysis.")
        print("  Using temporal consistency as minimum uncertainty check instead.")
        return None

    # Mean probability per consistency category
    profile['mean_prob'] = profile[prob_cols].mean(axis=1)
    profile['min_prob'] = profile[prob_cols].min(axis=1)
    profile['prob_std'] = profile[prob_cols].std(axis=1)

    print(f"\n  Confidence by Temporal Consistency:")
    print(f"  {'Category':<30s} {'Mean Prob':>10s} {'Min Prob':>10s} {'Prob Std':>10s} {'N':>10s}")
    print(f"  {'-'*72}")

    confidence_rows = []
    for cat in ['Stable', 'Persistent transition', 'Temporary transition', 'Oscillating']:
        subset = profile[profile['temporal_consistency'] == cat]
        if len(subset) > 0:
            mean_p = subset['mean_prob'].mean()
            min_p = subset['min_prob'].mean()
            std_p = subset['prob_std'].mean()
            n = len(subset)
            print(f"  {cat:<30s} {mean_p:>10.4f} {min_p:>10.4f} {std_p:>10.4f} {n:>10,}")
            confidence_rows.append({
                'category': cat,
                'mean_max_prob': round(mean_p, 4),
                'mean_min_prob': round(min_p, 4),
                'mean_prob_std': round(std_p, 4),
                'n': n,
            })

    # Also compare stable vs changed for the long-term transition
    col_start = f'class_{sorted(years)[0]}'
    col_end = f'class_{sorted(years)[-1]}'
    if col_start in profile.columns and col_end in profile.columns:
        stable_mask = profile[col_start] == profile[col_end]
        changed_mask = ~stable_mask

        print(f"\n  Long-term ({sorted(years)[0]}->{sorted(years)[-1]}) Confidence:")
        for label, mask in [('Stable (long-term)', stable_mask), ('Changed (long-term)', changed_mask)]:
            subset = profile[mask]
            if len(subset) > 0:
                print(f"    {label}: mean_prob={subset['mean_prob'].mean():.4f}, "
                      f"min_prob={subset['min_prob'].mean():.4f}, "
                      f"prob_std={subset['prob_std'].mean():.4f}, "
                      f"n={len(subset):,}")

    conf_df = pd.DataFrame(confidence_rows)
    conf_file = os.path.join(output_dir, 'confidence_evaluation.csv')
    conf_df.to_csv(conf_file, index=False)
    print(f"\n  [OK] Saved {conf_file}")

    # Plot confidence distribution by consistency
    fig, ax = plt.subplots(figsize=(10, 6))
    cats = ['Stable', 'Persistent transition', 'Temporary transition', 'Oscillating']
    cat_colors = ['#2d6a4f', '#e9c46a', '#e76f51', '#d62828']
    for cat, color in zip(cats, cat_colors):
        subset = profile[profile['temporal_consistency'] == cat]['mean_prob']
        if len(subset) > 0:
            ax.hist(subset, bins=50, alpha=0.5, label=f'{cat} (n={len(subset):,})',
                    color=color, density=True)

    ax.set_xlabel('Mean Prediction Probability', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title('Prediction Confidence by Temporal Consistency', fontsize=14, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    fig_path = os.path.join(output_dir, 'confidence_distribution.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved {fig_path}")

    return conf_df


# ============================================================
# STEP 8: Forest Loss/Gain Persistence Evaluation
# ============================================================

def evaluate_forest_persistence(profile, years, output_dir):
    """
    Evaluate whether forest loss and gain are persistent, temporary, or isolated.
    This determines whether they are suitable as headline results.
    """
    print(f"\n{'='*60}")
    print("  STEP 8: FOREST LOSS/GAIN PERSISTENCE EVALUATION")
    print(f"{'='*60}")

    class_cols = [f'class_{y}' for y in sorted(years)]
    first_year = sorted(years)[0]
    last_year = sorted(years)[-1]

    col_first = f'class_{first_year}'
    col_last = f'class_{last_year}'

    # Forest loss (was forest at start, not forest at end)
    forest_loss_mask = (profile[col_first] == 0) & (profile[col_last] != 0)
    # Forest gain (was not forest at start, forest at end)
    forest_gain_mask = (profile[col_first] != 0) & (profile[col_last] == 0)

    print(f"\n  Forest Loss ({first_year}->{last_year}): {forest_loss_mask.sum():,} points")
    print(f"  Forest Gain ({first_year}->{last_year}): {forest_gain_mask.sum():,} points")

    results = []

    for label, mask in [('Forest Loss', forest_loss_mask), ('Forest Gain', forest_gain_mask)]:
        subset = profile[mask]
        if len(subset) == 0:
            print(f"\n  {label}: No observations")
            continue

        # Evaluate consistency of these observations
        consistency_counts = subset['temporal_consistency'].value_counts()

        print(f"\n  {label} — Temporal Consistency Breakdown:")
        for cat in ['Persistent transition', 'Temporary transition', 'Oscillating', 'Stable']:
            count = consistency_counts.get(cat, 0)
            pct = 100 * count / len(subset) if len(subset) > 0 else 0
            if count > 0:
                print(f"    {cat}: {count:,} ({pct:.1f}%)")
                results.append({
                    'transition_type': label,
                    'consistency': cat,
                    'count': int(count),
                    'percentage': round(pct, 2),
                })

        # Recommendation
        persistent = consistency_counts.get('Persistent transition', 0)
        total = len(subset)
        persistent_pct = 100 * persistent / total if total > 0 else 0

        if persistent_pct >= 60:
            recommendation = "SUITABLE as headline result"
        elif persistent_pct >= 30:
            recommendation = "USE WITH CAUTION — report with persistence qualifier"
        else:
            recommendation = "NOT RECOMMENDED as headline — mostly classification instability"

        print(f"\n  {label} Recommendation: {recommendation}")
        print(f"    Persistent: {persistent:,}/{total:,} ({persistent_pct:.1f}%)")

    results_df = pd.DataFrame(results)
    results_file = os.path.join(output_dir, 'forest_loss_gain_persistence.csv')
    results_df.to_csv(results_file, index=False)
    print(f"\n  [OK] Saved {results_file}")

    return results_df


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():
    """Run the full temporal change detection pipeline (Steps 3-8)."""
    t0 = time.time()

    print(f"\n{'='*60}")
    print("  TEMPORAL CHANGE DETECTION v2")
    print(f"  Primary Window: {BASELINE_YEAR}-{ENDLINE_YEAR}")
    print(f"  Model: LightGBM (lgbm)")
    print(f"{'='*60}")

    model_name = 'lgbm'
    years = PRIMARY_YEARS
    output_dir = CHANGE_DIR_V2
    os.makedirs(output_dir, exist_ok=True)

    # Step 2: Load common domain
    print(f"\n--- Loading Common Spatial Domain ---")
    common_domain = load_common_domain()

    # Load predictions
    print(f"\n--- Loading Predictions ---")
    all_dfs = load_predictions_common_domain(model_name, years, common_domain)

    if len(all_dfs) < 2:
        print("  [FAIL] Need at least 2 years")
        sys.exit(1)

    # Build temporal profile
    print(f"\n--- Building Temporal Profile ---")
    profile = build_temporal_profile(all_dfs, common_domain)

    # Step 3: Composition
    comp_df = compute_composition(profile, years, output_dir)

    # Step 4: Consecutive transitions
    consec_df = run_consecutive_transitions(profile, sorted(years), output_dir)

    # Step 5: Long-term transition
    lt_summary, change_df = run_long_term_change(profile, BASELINE_YEAR, ENDLINE_YEAR, output_dir)

    # Step 6: Temporal consistency
    profile, consistency_df = classify_temporal_consistency(profile, years)
    consistency_df.to_csv(os.path.join(output_dir, 'temporal_consistency_summary.csv'), index=False)

    # Step 7: Confidence evaluation
    conf_df = evaluate_confidence(profile, years, output_dir)

    # Step 8: Forest persistence
    persistence_df = evaluate_forest_persistence(profile, years, output_dir)

    # Save full profile
    profile_file = os.path.join(output_dir, f'temporal_profile_{model_name}_v2.csv')
    profile.to_csv(profile_file, index=False)
    print(f"\n  [OK] Saved full temporal profile: {profile_file}")
    print(f"       {len(profile):,} points x {len(profile.columns)} columns")

    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print(f"  PIPELINE COMPLETE — {elapsed:.1f}s")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
