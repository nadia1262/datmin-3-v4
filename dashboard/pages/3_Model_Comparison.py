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
best_idx = df_metrics['accuracy'].idxmax()
best_model = df_metrics.loc[best_idx, 'model']
best_acc = df_metrics.loc[best_idx, 'accuracy']
best_f1 = df_metrics.loc[best_idx, 'f1_macro']
best_kappa = df_metrics.loc[best_idx, 'kappa']

st.success(f"🏆 **Model Terpilih: {MODEL_DISPLAY_NAMES.get(best_model, best_model)}** — OA={best_acc:.4f} | F1-Macro={best_f1:.4f} | Kappa={best_kappa:.4f}")

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
        .highlight_max(subset=['Overall Accuracy', 'F1 Macro', 'Kappa'], color='#c8e6c9')
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
    fig.update_traces(texttemplate='%{text:.4f}', textposition='outside')
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
    fig.update_traces(texttemplate='%{text:.4f}', textposition='outside')
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
st.subheader(f"Akurasi Per Kelas — {MODEL_DISPLAY_NAMES.get(best_model, best_model)}")
summary = load_summary(best_model)
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
            .bar(subset=["Producer's Accuracy", "User's Accuracy", 'IoU'], color='#799368', vmin=0.5),
        use_container_width=True, hide_index=True
    )

st.info("""**Catatan Metodologis:** Akurasi yang dilaporkan berasal dari Spatial Block Cross-Validation (5-fold), 
         bukan *random split* biasa. Blok spasial berukuran 0.5° (~55km) memastikan titik-titik bertetangga tidak bocor 
         antara set train dan test. Ini menyebabkan akurasi lebih rendah dari yang biasanya dilaporkan (~93–98%) 
         karena tidak ada *spatial autocorrelation leakage*.""")
