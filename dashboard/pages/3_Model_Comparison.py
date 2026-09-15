# dashboard/pages/3_Model_Comparison.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from configs.constants import *
from configs.color_palette import *

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from theme import apply_theme

st.set_page_config(page_title="Model Comparison", page_icon="◈", layout="wide")
apply_theme()

st.title("Algorithmic Comparison")
st.markdown("Evaluasi 6 model Supervised Machine Learning dengan **Spatial Block GroupKFold (5-fold)** untuk menghindari spatial data leakage.")

@st.cache_data
def load_metrics():
    path = os.path.join(CLASSIFICATION_DIR, 'model_comparison.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

@st.cache_data
def load_summary(model_name):
    import json
    path = os.path.join(CLASSIFICATION_DIR, f'summary_{model_name}.json')
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

df_metrics = load_metrics()

if df_metrics is None:
    st.error("File model_comparison.csv tidak ditemukan.")
    st.stop()

# ── Highlight Best Model ──
chosen_model = 'lgbm'
chosen_row = df_metrics[df_metrics['model'] == chosen_model].iloc[0]

st.markdown(f"""
<div class="forest-card" style="margin-bottom: 1.5rem;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
        <div>
            <span class="step-badge">MODEL OPERASIONAL FINAL</span>
            <h3 style="margin: 0.2rem 0 0.4rem 0; font-size: 1.35rem; color: #16281C;">
                LightGBM (Light Gradient Boosting Machine)
            </h3>
            <p style="color: #4B5A50; font-size: 0.88rem; margin: 0; max-width: 720px; line-height: 1.55;">
                Meskipun SVM mencapai akurasi sedikit lebih tinggi (+0,67%), LightGBM dipilih sebagai model operasional utama 
                karena efisiensi komputasi <strong>6,5× lebih cepat</strong> (116,6 detik vs 759,9 detik). Kecepatan eksekusi ini mutlak diperlukan 
                untuk memprediksi jutaan titik pada skala pulau makro 500m dan presisi mikro 10m.
            </p>
        </div>
        <div style="display: flex; gap: 0.6rem; margin-top: 0.5rem;">
            <div class="stat-pill">OA: <strong>{chosen_row['accuracy']*100:.2f}%</strong></div>
            <div class="stat-pill">F1-Macro: <strong>{chosen_row['f1_macro']:.4f}</strong></div>
            <div class="stat-pill">Waktu: <strong>{chosen_row['time_s']:.1f}s</strong></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Summary Table ──
st.subheader("Tabel Perbandingan Metrik")
st.caption("Semua model dilatih dengan 30.000 sampel kecuali MLP (10.000 sampel karena keterbatasan komputasi). Semua dievaluasi menggunakan Spatial Block GroupKFold untuk menghindari data leakage spasial.")

display_cols = ['model', 'n_samples', 'accuracy', 'f1_macro', 'f1_weighted', 'kappa', 'time_s']
df_display = df_metrics[display_cols].copy()
df_display['model'] = df_display['model'].map(lambda x: MODEL_DISPLAY_NAMES.get(x, x))
df_display.columns = ['Model', 'N Sampel', 'Overall Accuracy', 'F1 Macro', 'F1 Weighted', 'Kappa', 'Waktu (detik)']
df_display = df_display.sort_values('Overall Accuracy', ascending=False).reset_index(drop=True)
df_display.index += 1

st.dataframe(
    df_display.style
        .highlight_max(subset=['Overall Accuracy', 'F1 Macro', 'Kappa'], color=DASHBOARD_THEME['bg_tertiary'])
        .format({'Overall Accuracy': '{:.4f}', 'F1 Macro': '{:.4f}', 'F1 Weighted': '{:.4f}', 'Kappa': '{:.4f}', 'Waktu (detik)': '{:.1f}'}),
    use_container_width=True
)

# ── Bar Charts ──
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(df_metrics.sort_values('accuracy', ascending=True),
                 x='accuracy', y='model', orientation='h',
                 color='model', color_discrete_map=MODEL_COLORS,
                 title='Overall Accuracy (Spatial Block CV)',
                 template=PLOTLY_TEMPLATE,
                 text='accuracy')
    fig.update_traces(texttemplate='%{text:.4f}', textposition='outside', cliponaxis=False)
    fig.update_layout(xaxis_range=[0.6, 0.9], showlegend=False,
                      paper_bgcolor=PLOTLY_PAPER_COLOR,
                      plot_bgcolor=PLOTLY_PLOT_COLOR,
                      font_color=PLOTLY_FONT_COLOR,
                      yaxis_title='', xaxis_title='Overall Accuracy')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(df_metrics.sort_values('f1_macro', ascending=True),
                 x='f1_macro', y='model', orientation='h',
                 color='model', color_discrete_map=MODEL_COLORS,
                 title='Macro F1-Score (Spatial Block CV)',
                 template=PLOTLY_TEMPLATE,
                 text='f1_macro')
    fig.update_traces(texttemplate='%{text:.4f}', textposition='outside', cliponaxis=False)
    fig.update_layout(xaxis_range=[0.6, 0.9], showlegend=False,
                      paper_bgcolor=PLOTLY_PAPER_COLOR,
                      plot_bgcolor=PLOTLY_PLOT_COLOR,
                      font_color=PLOTLY_FONT_COLOR,
                      yaxis_title='', xaxis_title='F1 Macro')
    st.plotly_chart(fig, use_container_width=True)

# ── Kappa vs Time Trade-off ──
st.subheader("Efisiensi vs Performa")
fig_scatter = px.scatter(df_metrics, x='time_s', y='accuracy',
                         color='model', color_discrete_map=MODEL_COLORS,
                         size='f1_macro', text='model',
                         labels={'time_s': 'Waktu Training (detik)', 'accuracy': 'Overall Accuracy'},
                         title='Trade-off: Waktu Training vs Akurasi',
                         template=PLOTLY_TEMPLATE)
fig_scatter.update_traces(textposition='top center')
fig_scatter.update_layout(
    paper_bgcolor=PLOTLY_PAPER_COLOR,
    plot_bgcolor=PLOTLY_PLOT_COLOR,
    font_color=PLOTLY_FONT_COLOR
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ── Per-class accuracy for best model ──
st.subheader(f"Akurasi Per Kelas — {MODEL_DISPLAY_NAMES.get(chosen_model, chosen_model)}")
summary = load_summary(chosen_model)
if summary and 'per_class' in summary:
    per_class = summary['per_class']
    pc_rows = []
    for cls_name, metrics in per_class.items():
        pc_rows.append({
            'Kelas': cls_name,
            "Producer's Accuracy": round(metrics.get('producers_accuracy', 0), 4),
            "User's Accuracy": round(metrics.get('users_accuracy', 0), 4),
            'IoU': round(metrics.get('iou', 0), 4)
        })
    df_pc = pd.DataFrame(pc_rows)
    st.dataframe(
        df_pc.style.format({"Producer's Accuracy": '{:.4f}', "User's Accuracy": '{:.4f}', 'IoU': '{:.4f}'})
            .bar(subset=["Producer's Accuracy", "User's Accuracy", 'IoU'], color=DASHBOARD_THEME['accent'], vmin=0.5),
        use_container_width=True, hide_index=True
    )

st.info("""**Catatan Metodologis:** Akurasi yang dilaporkan berasal dari Spatial Block Cross-Validation (5-fold), 
         bukan *random split* biasa. Blok spasial berukuran 0.5° (~55km) memastikan titik-titik bertetangga tidak bocor 
         antara set train dan test. Ini menyebabkan akurasi lebih rendah dari yang biasanya dilaporkan (~93–98%) 
         karena tidak ada *spatial autocorrelation leakage*.""")
