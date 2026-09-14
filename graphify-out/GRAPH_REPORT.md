# Graph Report - .  (2026-09-12)

## Corpus Check
- 1 files · ~98,781 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 281 nodes · 328 edges · 48 communities (28 shown, 20 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 31 edges (avg confidence: 0.8)
- Token cost: 0 input · 65,077 output

## Community Hubs (Navigation)
- Cited Literature & Methods
- Dashboard & SHAP Pipeline
- Change Detection Pipeline
- Research Gaps & Audit
- Mixed Pixel & Driver Rationale
- GEE Utility Functions
- Spectral Indices & Land Cover Classes
- Dashboard Data Prep
- Dual Driver Logistic Analysis
- Model Training Pipeline
- Prediction Grid Export
- Kepler Export Script
- Stratified Sampling (GEE)
- Temporal Trends Chart
- Multi-Year Prediction Script
- Raster Classification Export
- 2022-2023 Transition Matrix
- 2023-2024 Transition Matrix
- 10m IKN Prediction Script
- Random Forest Confusion Matrix
- CRISP-DM Flowchart
- Mining Proximity Script (GEE)
- Prediction Confidence Chart
- 2019-2020 Transition Matrix
- 2019-2024 Transition Matrix
- 2020-2021 Transition Matrix
- 2021-2022 Transition Matrix
- LightGBM Confusion Matrix
- Logistic Regression Confusion Matrix
- MLP Confusion Matrix
- SVM Confusion Matrix
- XGBoost Confusion Matrix
- IKN 10m Map 2019
- IKN 10m Map 2024
- Driver Effects Chart
- Maus Mining Polygons Map
- SHAP Interaction Plot
- Spectral Temporal Drift Chart

## God Nodes (most connected - your core abstractions)
1. `BAB 2: Materi dan Metode (Draft)` - 35 edges
2. `main()` - 11 edges
3. `getFeatureStack()` - 10 edges
4. `apply_theme()` - 9 edges
5. `Report & Research Gap Blueprint` - 8 edges
6. `BAB 4: Pembahasan (Draft)` - 8 edges
7. `Spatiotemporal Land Cover Transformation in Kalimantan (README)` - 7 edges
8. `Research Gap vs Prior IKN Studies` - 7 edges
9. `run_consecutive_transitions()` - 6 edges
10. `run_long_term_change()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Python Requirements (Dual-Driver Land Cover Classification)` --shares_data_with--> `Six ML Models Comparison Table`  [INFERRED]
  requirements.txt → README.md
- `Python Requirements (Dual-Driver Land Cover Classification)` --shares_data_with--> `Hyperparameter Grid Search Optimization`  [INFERRED]
  requirements.txt → reports/draft_bab2_metodologi.md
- `6-Model Comparison Metrics (OA/F1/Kappa)` --shares_data_with--> `Six ML Models Comparison Table`  [INFERRED]
  reports/01_FINAL_TECHNICAL_AUDIT.md → README.md
- `Land Cover Classes (5-class Schema)` --shares_data_with--> `Land Cover Target Classes (5-class Schema)`  [INFERRED]
  README.md → reports/variabel_penelitian.md
- `DOCX Dump (Proposal Template Extract)` --references--> `BAB 2: Materi dan Metode (Draft)`  [INFERRED]
  reports/_docx_dump.txt → reports/draft_bab2_metodologi.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Dual-Driver Spatial Analysis Pipeline** — reports_draft_bab2_metodologi_spatial_block_cv, reports_draft_bab2_metodologi_common_spatial_domain, reports_draft_bab2_metodologi_logistic_regression_driver_model, reports_variabel_penelitian_driver_variables [INFERRED 0.85]
- **Mixed Pixel Anomaly and Defense Narrative** — reports_05_defense_mixed_pixels_mixed_pixels_effect, reports_draft_bab2_metodologi_domain_shift, reports_draft_bab4_pembahasan_forest_gain_anomaly [INFERRED 0.90]
- **Research Gap Positioning vs Prior Work** — reports_03_report_blueprint_research_gap, paper_kurniawan2024, paper_habibie2025, reports_draft_bab2_metodologi_spatial_block_cv [INFERRED 0.80]

## Communities (48 total, 20 thin omitted)

### Community 0 - "Cited Literature & Methods"
Cohesion: 0.06
Nodes (36): Alamgir et al. 2019 - Infrastructure Expansion Challenges Biodiversity Hotspots, Breiman 2001 - Random Forests, Chen & Guestrin 2016 - XGBoost, Cohen 1960 - A Coefficient of Agreement for Nominal Scales, Cortes & Vapnik 1995 - Support-Vector Networks, Farr et al. 2007 - The Shuttle Radar Topography Mission (SRTM), Funk et al. 2015 - CHIRPS Precipitation Dataset, Gao 1996 - NDMI Normalized Difference Water Index (+28 more)

### Community 1 - "Dashboard & SHAP Pipeline"
Cohesion: 0.10
Nodes (10): color_palette.py — Visual design system for Land Cover Classification Dashboard, constants.py — Shared constants for Dual-Driver Land Cover Classification =====, image_to_base64(), Convert PIL Image to base64 data URI string., apply_theme(), Inject Instrument Panel CSS into the current Streamlit page.      Hard-edged,, shap_classifier.py — SHAP Feature Importance Analysis =========================, Run SHAP analysis on trained model. (+2 more)

### Community 2 - "Change Detection Pipeline"
Cohesion: 0.10
Nodes (29): build_temporal_profile(), classify_temporal_consistency(), compute_composition(), compute_transition_matrix(), detect_transitions(), evaluate_confidence(), evaluate_forest_persistence(), load_common_domain() (+21 more)

### Community 3 - "Research Gaps & Audit"
Cohesion: 0.09
Nodes (25): Habibie et al. 2025 - Integrating Sentinel-2 and ESA WorldCover for LULC Assessment, Six ML Models Comparison Table, Final Technical Audit (Updated), Use 'Association' Not 'Causation' Language, Change Detection Results (Common Domain, Forest Gain/Loss), 6-Model Comparison Metrics (OA/F1/Kappa), Final Pipeline Architecture (Audited), Risk Register (P0/P1/P2 Issues) (+17 more)

### Community 4 - "Mixed Pixel & Driver Rationale"
Cohesion: 0.13
Nodes (19): Abood et al. 2015 - Relative Contributions of Logging, Fiber, Oil Palm and Mining to Forest Loss in Indonesia, Gomez, White & Wulder 2016 - Optical Remotely Sensed Time Series Data Review, Lu & Weng 2007 - Survey of Image Classification Methods, Wu 2004 - Effects of Changing Scale on Landscape Pattern Analysis (MAUP), LightGBM Chosen Over SVM (Speed Trade-off), Defense Guide: Mixed Pixels Attack, Acknowledge & Reframe Defense Script, Mixed Pixel Effect (10m vs 500m Resolution) (+11 more)

### Community 5 - "GEE Utility Functions"
Cohesion: 0.29
Nodes (12): addIndices(), getBlockId(), getComposite(), getElevation(), getFeatureStack(), getIKNBufferZone(), getIKNDistance(), getLabels() (+4 more)

### Community 6 - "Spectral Indices & Land Cover Classes"
Cohesion: 0.15
Nodes (13): Spatiotemporal Land Cover Transformation in Kalimantan (README), Cloud Masking Requirement (Critical Note), Key Configuration (constants.py), Land Cover Classes (5-class Schema), Project Pipeline Architecture, Temporal Transfer Assumption (Critical Note), Spatial Block Cross-Validation Strategy, BAB III: Variabel Penelitian dan Justifikasi Ilmiah (+5 more)

### Community 7 - "Dashboard Data Prep"
Cohesion: 0.25
Nodes (10): main(), prepare_change_summary(), prepare_classification_summary(), prepare_driver_summary(), prepare_temporal_data(), prepare_dashboard_data.py — Pre-compute Dashboard Data ========================, Aggregate model comparison data., Prepare year-by-year class distribution for dashboard. (+2 more)

### Community 8 - "Dual Driver Logistic Analysis"
Cohesion: 0.27
Nodes (9): load_change_data(), plot_driver_effects(), dual_driver_analysis.py — IKN x Mining Dual-Driver Analysis ===================, Plot marginal effects of IKN distance and mining density on deforestation., Main dual-driver analysis pipeline., Load change points with ancillary driver variables., Run logistic regression to test driver significance., run_analysis() (+1 more)

### Community 9 - "Model Training Pipeline"
Cohesion: 0.32
Nodes (7): get_model_and_params(), quick_cv_score(), train_classification.py — Multi-Model Land Cover Classification ===============, Return model instance and hyperparameter grid., Quick 3-fold CV to find best hyperparameters., Train a single model with full pipeline., train_model()

### Community 10 - "Prediction Grid Export"
Cohesion: 0.52
Nodes (6): addIndices(), exportYearGrid(), getComposite(), getIKNDistance(), getMiningDensity10km(), maskS2clouds()

### Community 11 - "Kepler Export Script"
Cohesion: 0.33
Nodes (6): extract_lon_lat(), prepare_all_years_combined(), prepare_kepler_csv(), prepare_kepler_export.py Menyiapkan file CSV bersih untuk visualisasi di Kepler, Parse kolom .geo dari GEE output ke lon/lat, Gabung semua tahun ke satu file untuk animasi temporal di Kepler.gl

### Community 13 - "Temporal Trends Chart"
Cohesion: 0.40
Nodes (6): Bare/Mining-like Land Cover Class, Built-up Land Cover Class, Forest Land Cover Class, Shrubland/Agriculture Land Cover Class, Land Cover Composition Over Time Chart, Water Land Cover Class

### Community 14 - "Multi-Year Prediction Script"
Cohesion: 0.50
Nodes (4): main(), predict_year(), predict_all_years.py — Apply trained model to prediction grids (2018-2024) ====, Predict land cover for a single year's grid.

### Community 16 - "2022-2023 Transition Matrix"
Cohesion: 0.50
Nodes (4): Bare/Mining-like Class (2022-2023), Forest Class (2022-2023), Shrubland/Agriculture Class (2022-2023), Land Cover Transition Matrix 2022 to 2023

### Community 17 - "2023-2024 Transition Matrix"
Cohesion: 0.67
Nodes (4): Bare/Mining-like Land Cover Class, Forest Land Cover Class, Shrubland/Agriculture Land Cover Class, Land Cover Transition Matrix 2023-2024

### Community 18 - "10m IKN Prediction Script"
Cohesion: 0.67
Nodes (3): main(), parse_geo(), predict_ikn_10m.py — Apply trained LGBM model to 10m IKN grids and generate maps

### Community 19 - "Random Forest Confusion Matrix"
Cohesion: 0.67
Nodes (3): Confusion Matrix: Random Forest, Land Cover Classes (Forest, Shrubland/Agriculture, Built-up, Bare/Mining-like, Water), Random Forest Classifier

## Knowledge Gaps
- **71 isolated node(s):** `Flowchart Alur Penelitian`, `Team Storyline Guide`, `DOCX Dump (Proposal Template Extract)`, `Project Pipeline Architecture`, `Spatial Block Cross-Validation Strategy` (+66 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BAB 2: Materi dan Metode (Draft)` connect `Cited Literature & Methods` to `Research Gaps & Audit`, `Mixed Pixel & Driver Rationale`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `Six ML Models Comparison Table` connect `Research Gaps & Audit` to `Spectral Indices & Land Cover Classes`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `Spatiotemporal Land Cover Transformation in Kalimantan (README)` connect `Spectral Indices & Land Cover Classes` to `Research Gaps & Audit`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `BAB 2: Materi dan Metode (Draft)` (e.g. with `DOCX Dump (Proposal Template Extract)` and `DOCX Dump Top (Proposal Template Outline)`) actually correct?**
  _`BAB 2: Materi dan Metode (Draft)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Flowchart Alur Penelitian`, `Team Storyline Guide`, `DOCX Dump (Proposal Template Extract)` to the rest of the system?**
  _71 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Cited Literature & Methods` be split into smaller, more focused modules?**
  _Cohesion score 0.05873015873015873 - nodes in this community are weakly interconnected._
- **Should `Dashboard & SHAP Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.10483870967741936 - nodes in this community are weakly interconnected._