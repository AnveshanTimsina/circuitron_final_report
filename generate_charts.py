#!/usr/bin/env python3
"""
Generate publication-quality comparison charts for the CIRCUITRON report.
All charts use Times New Roman, 12pt base font, matching the LaTeX report style.
Outputs go to src/images/figures/ as high-DPI PNGs.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ============================================================
# GLOBAL STYLE — Times New Roman, 12pt, publication quality
# ============================================================
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
rcParams['font.size'] = 12
rcParams['axes.labelsize'] = 12
rcParams['axes.titlesize'] = 13
rcParams['xtick.labelsize'] = 11
rcParams['ytick.labelsize'] = 11
rcParams['legend.fontsize'] = 10
rcParams['figure.titlesize'] = 14
rcParams['axes.linewidth'] = 0.8
rcParams['grid.linewidth'] = 0.5
rcParams['lines.linewidth'] = 1.5
rcParams['savefig.dpi'] = 300
rcParams['savefig.bbox'] = 'tight'
rcParams['savefig.pad_inches'] = 0.1
rcParams['mathtext.fontset'] = 'stix'

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'src', 'images', 'figures')
os.makedirs(OUT, exist_ok=True)

# ============================================================
# 1. YOLO MODEL COMPARISON (15-class, retrained models)
# ============================================================
# Final metrics from comparison_summary.csv
yolo_models_15 = ['YOLOv7\n(retrained)', 'YOLOv11', 'YOLOv8', 'YOLOv26']
yolo_precision_15 = [0.97468, 0.96174, 0.90729, 0.89193]
yolo_recall_15 = [0.93496, 0.92093, 0.80578, 0.78011]
yolo_map50_15 = [0.95623, 0.95309, 0.86195, 0.85370]
yolo_map5095_15 = [0.72662, 0.70326, 0.59688, 0.57379]

# Original 61-class models from existing report
yolo_models_61 = ['YOLOv7\n(61-class)', 'YOLOv5\n(61-class)']
yolo_precision_61 = [0.93, 0.84]
yolo_recall_61 = [0.78, 0.62]
yolo_map50_61 = [0.83, 0.61]
yolo_map5095_61 = [0.60, 0.41]

# Combined data for the big comparison
all_models = ['YOLOv5\n(61-class)', 'YOLOv7\n(61-class)', 'YOLOv8\n(15-class)', 'YOLOv26\n(15-class)',
              'YOLOv11\n(15-class)', 'YOLOv7\n(15-class)']
all_precision = [0.84, 0.93, 0.90729, 0.89193, 0.96174, 0.97468]
all_recall = [0.62, 0.78, 0.80578, 0.78011, 0.92093, 0.93496]
all_map50 = [0.61, 0.83, 0.86195, 0.85370, 0.95309, 0.95623]
all_map5095 = [0.41, 0.60, 0.59688, 0.57379, 0.70326, 0.72662]

# Colors: lighter for 61-class, darker for 15-class
colors_all = ['#c0c0c0', '#888888', '#2ca02c', '#1f77b4', '#ff7f0e', '#d62728']

# --- Chart 1: Complete YOLO Comparison Bar Chart (all 6 models, 4 metrics) ---
def chart_yolo_full_comparison():
    fig, ax = plt.subplots(figsize=(12, 6))
    metrics_labels = ['Precision', 'Recall', 'mAP@0.5', 'mAP@0.5:0.95']
    metrics_data = [all_precision, all_recall, all_map50, all_map5095]

    n_models = len(all_models)
    n_metrics = len(metrics_labels)
    x = np.arange(n_metrics) * 1.4  # wider spacing between metric groups
    width = 0.14

    for i in range(n_models):
        vals = [m[i] for m in metrics_data]
        bars = ax.bar(x + i * width, vals, width, label=all_models[i].replace('\n', ' '),
                      color=colors_all[i], edgecolor='black', linewidth=0.4)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                    f'{v:.2f}', ha='center', va='bottom', fontsize=6.5,
                    rotation=90, fontweight='bold')

    ax.set_xticks(x + width * (n_models - 1) / 2)
    ax.set_xticklabels(metrics_labels, fontsize=12)
    ax.set_ylabel('Score')
    ax.set_ylim(0, 1.18)
    ax.legend(loc='upper center', ncol=3, framealpha=0.9, bbox_to_anchor=(0.5, 1.12),
             fontsize=9)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    fig.savefig(os.path.join(OUT, 'yolo_full_comparison_bar.png'))
    plt.close(fig)
    print('Saved yolo_full_comparison_bar.png')


# --- Chart 2: 15-class model training curves (4 subplots) ---
def chart_15class_training_curves():
    import pandas as pd

    COMP = os.path.join(BASE, '..', 'yolocomparision')
    csv_paths = {
        'YOLOv7 (retrained)': os.path.join(COMP, 'circuitron_yolov7new', 'results.csv'),
        'YOLOv11': os.path.join(COMP, 'runsyolo11', 'detect', 'circuitron_yolov13', 'results.csv'),
        'YOLOv8': os.path.join(COMP, 'runsyolo8ramro', 'detect', 'circuitron_yolov83', 'results.csv'),
        'YOLOv26': os.path.join(COMP, 'runs26withval', 'detect', 'circuitron_yolov262', 'results.csv'),
    }
    colors = {'YOLOv7 (retrained)': '#d62728', 'YOLOv11': '#ff7f0e', 'YOLOv8': '#2ca02c', 'YOLOv26': '#1f77b4'}

    dfs = {}
    for name, path in csv_paths.items():
        if os.path.exists(path):
            df = pd.read_csv(path)
            df.columns = df.columns.str.strip()
            dfs[name] = df
        else:
            print(f'WARNING: {path} not found')

    if not dfs:
        print('No CSV data found, skipping training curves')
        return

    metrics = {
        'metrics/precision(B)': 'Precision',
        'metrics/recall(B)': 'Recall',
        'metrics/mAP50(B)': 'mAP@0.5',
        'metrics/mAP50-95(B)': 'mAP@0.5:0.95',
    }

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, (col, label) in zip(axes.flatten(), metrics.items()):
        for name, df in dfs.items():
            ax.plot(df['epoch'], df[col], label=name, color=colors[name])
        ax.set_xlabel('Epoch')
        ax.set_ylabel(label)
        ax.set_title(label)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
    fig.tight_layout(pad=2.0)
    fig.savefig(os.path.join(OUT, 'yolo_15class_training_curves.png'))
    plt.close(fig)
    print('Saved yolo_15class_training_curves.png')

    # Also: loss curves comparison (train vs val)
    loss_cols = {
        'Box Loss': ('train/box_loss', 'val/box_loss'),
        'Classification Loss': ('train/cls_loss', 'val/cls_loss'),
        'DFL Loss': ('train/dfl_loss', 'val/dfl_loss'),
    }

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, (title, (tcol, vcol)) in zip(axes, loss_cols.items()):
        for name, df in dfs.items():
            ax.plot(df['epoch'], df[tcol], color=colors[name], label=name)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss')
        ax.set_title(f'Training {title}')
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
    fig.tight_layout(pad=2.0)
    fig.savefig(os.path.join(OUT, 'yolo_15class_train_loss.png'))
    plt.close(fig)
    print('Saved yolo_15class_train_loss.png')

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, (title, (tcol, vcol)) in zip(axes, loss_cols.items()):
        for name, df in dfs.items():
            ax.plot(df['epoch'], df[vcol], color=colors[name], label=name)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss')
        ax.set_title(f'Validation {title}')
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
    fig.tight_layout(pad=2.0)
    fig.savefig(os.path.join(OUT, 'yolo_15class_val_loss.png'))
    plt.close(fig)
    print('Saved yolo_15class_val_loss.png')


# --- Chart 3: 15-class final metrics grouped bar ---
def chart_15class_final_bar():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    models = ['YOLOv7\n(retrained)', 'YOLOv11', 'YOLOv8', 'YOLOv26']
    metrics_labels = ['Precision', 'Recall', 'mAP@0.5', 'mAP@0.5:0.95']
    data = np.array([
        yolo_precision_15, yolo_recall_15, yolo_map50_15, yolo_map5095_15
    ])
    colors_bar = ['#2166ac', '#67a9cf', '#ef8a62', '#b2182b']

    x = np.arange(len(models)) * 1.2  # wider spacing between model groups
    width = 0.20
    for i, (met, color) in enumerate(zip(metrics_labels, colors_bar)):
        vals = data[i]
        bars = ax.bar(x + i * width, vals, width, label=met, color=color, edgecolor='black', linewidth=0.4)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                    f'{v:.3f}', ha='center', va='bottom', fontsize=7, rotation=45)

    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models, fontsize=11)
    ax.set_ylabel('Score')
    ax.set_ylim(0, 1.14)
    ax.legend(loc='lower right', framealpha=0.9, fontsize=10)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    fig.savefig(os.path.join(OUT, 'yolo_15class_final_bar.png'))
    plt.close(fig)
    print('Saved yolo_15class_final_bar.png')


# --- Chart 4: OCR Model Comparison (CRNN vs TrOCR) ---
def chart_ocr_comparison():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    # 4a: Accuracy / CER / WER comparison
    ax = axes[0]
    models = ['Custom\nCRNN', 'Fine-tuned\nTrOCR']
    accuracy = [65.96, 84.5]  # TrOCR shows improved accuracy from fine-tuning
    cer = [0.25, 0.12]
    wer = [0.34, 0.18]

    x = np.arange(len(models)) * 1.2  # wider spacing
    width = 0.25
    bars1 = ax.bar(x - width, accuracy, width, label='Accuracy (%)', color='#2166ac', edgecolor='black', linewidth=0.4)
    # For CER/WER, scale to percentage for visual comparison
    bars2 = ax.bar(x, [c * 100 for c in cer], width, label='CER (\u00d7100)', color='#ef8a62', edgecolor='black', linewidth=0.4)
    bars3 = ax.bar(x + width, [w * 100 for w in wer], width, label='WER (\u00d7100)', color='#b2182b', edgecolor='black', linewidth=0.4)

    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                    f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=10,
                    fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=11)
    ax.set_ylabel('Value')
    ax.set_ylim(0, 100)
    ax.set_title('OCR Performance Metrics')
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # 4b: Qualitative comparison table as text
    ax2 = axes[1]
    ax2.axis('off')
    table_data = [
        ['Feature', 'Custom CRNN', 'Fine-tuned TrOCR'],
        ['Architecture', 'CNN+BiLSTM+CTC', 'ViT Encoder+\nTransformer Decoder'],
        ['Training', 'From scratch\n(50 epochs)', 'Fine-tuned\n(3 epochs)'],
        ['Batch Inference', 'Sequential', 'Parallel (GPU)'],
        ['Accuracy', '65.96%', '84.5%'],
        ['CER', '0.25', '0.12'],
        ['WER', '0.34', '0.18'],
        ['Inference Speed', 'Moderate', 'Fast (float16)'],
    ]
    table = ax2.table(cellText=table_data[1:], colLabels=table_data[0],
                      loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 1.6)
    # Style header
    for j in range(3):
        table[0, j].set_facecolor('#d4e6f1')
        table[0, j].set_text_props(fontweight='bold')
    # Alternate row colors
    for i in range(1, len(table_data)):
        for j in range(3):
            if i % 2 == 0:
                table[i, j].set_facecolor('#f5f5f5')
    ax2.set_title('Feature Comparison', pad=20)

    fig.tight_layout(pad=2.0)
    fig.savefig(os.path.join(OUT, 'ocr_model_comparison.png'))
    plt.close(fig)
    print('Saved ocr_model_comparison.png')


# --- Chart 5: Evolution timeline — mAP@0.5 across all iterations ---
def chart_evolution_timeline():
    fig, ax = plt.subplots(figsize=(11, 5.5))

    stages = [
        'YOLOv5\n(61-class)\n200 epochs',
        'YOLOv7\n(61-class)\n100 epochs',
        'YOLOv8\n(15-class)\n100 epochs',
        'YOLOv26\n(15-class)\n100 epochs',
        'YOLOv11\n(15-class)\n100 epochs',
        'YOLOv7 retrained\n(15-class)\n100 epochs',
    ]
    map50_vals = [0.61, 0.83, 0.86195, 0.85370, 0.95309, 0.95623]
    map5095_vals = [0.41, 0.60, 0.59688, 0.57379, 0.70326, 0.72662]
    x = np.arange(len(stages))

    line1, = ax.plot(x, map50_vals, 'o-', color='#d62728', markersize=8, label='mAP@0.5')
    line2, = ax.plot(x, map5095_vals, 's--', color='#1f77b4', markersize=8, label='mAP@0.5:0.95')

    # Offset annotations to avoid overlap on close values
    # mAP@0.5 labels above, mAP@0.5:0.95 labels below
    map50_offsets = [(0, 12), (0, 12), (12, 12), (-12, 12), (0, 12), (0, 12)]
    map5095_offsets = [(0, -16), (0, -16), (12, -16), (-12, -16), (0, -16), (0, -16)]

    for i, (v1, v2) in enumerate(zip(map50_vals, map5095_vals)):
        ax.annotate(f'{v1:.3f}', (x[i], v1), textcoords="offset points",
                    xytext=map50_offsets[i], ha='center', fontsize=8,
                    color='#d62728', fontweight='bold')
        ax.annotate(f'{v2:.3f}', (x[i], v2), textcoords="offset points",
                    xytext=map5095_offsets[i], ha='center', fontsize=8,
                    color='#1f77b4', fontweight='bold')

    # Draw a vertical dashed line separating 61-class from 15-class
    ax.axvline(x=1.5, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax.text(0.75, 1.03, '61-class', transform=ax.get_xaxis_transform(),
            ha='center', fontsize=9, color='gray', style='italic')
    ax.text(3.75, 1.03, '15-class (merged taxonomy)', transform=ax.get_xaxis_transform(),
            ha='center', fontsize=9, color='gray', style='italic')

    ax.set_xticks(x)
    ax.set_xticklabels(stages, fontsize=9)
    ax.set_ylabel('Score')
    ax.set_ylim(0.3, 1.08)
    ax.legend(loc='center left', fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    fig.savefig(os.path.join(OUT, 'yolo_evolution_timeline.png'))
    plt.close(fig)
    print('Saved yolo_evolution_timeline.png')


# --- Chart 6: Radar/Spider chart for best models ---
def chart_radar_comparison():
    categories = ['Precision', 'Recall', 'mAP@0.5', 'mAP@0.5:0.95', 'Precision']  # close the polygon
    models_data = {
        'YOLOv7 (61-class)': [0.93, 0.78, 0.83, 0.60, 0.93],
        'YOLOv7 (15-class)': [0.97468, 0.93496, 0.95623, 0.72662, 0.97468],
        'YOLOv11 (15-class)': [0.96174, 0.92093, 0.95309, 0.70326, 0.96174],
    }
    colors_r = {'YOLOv7 (61-class)': '#888888', 'YOLOv7 (15-class)': '#d62728', 'YOLOv11 (15-class)': '#ff7f0e'}

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=True)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    for name, vals in models_data.items():
        ax.plot(angles, vals, 'o-', label=name, color=colors_r[name], linewidth=1.5, markersize=5)
        ax.fill(angles, vals, alpha=0.1, color=colors_r[name])

    ax.set_thetagrids(angles[:-1] * 180 / np.pi, categories[:-1], fontsize=10)
    ax.set_ylim(0.4, 1.0)
    ax.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    ax.set_yticklabels(['0.5', '0.6', '0.7', '0.8', '0.9', '1.0'], fontsize=8)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.15), fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.savefig(os.path.join(OUT, 'yolo_radar_comparison.png'))
    plt.close(fig)
    print('Saved yolo_radar_comparison.png')


# --- Chart 7: Class count impact visualization ---
def chart_class_impact():
    fig, ax = plt.subplots(figsize=(7, 5))

    # Show how the same architecture (YOLOv7) improves from 61-class to 15-class
    metrics_labels = ['Precision', 'Recall', 'mAP@0.5', 'mAP@0.5:0.95']
    v7_61 = [0.93, 0.78, 0.83, 0.60]
    v7_15 = [0.97468, 0.93496, 0.95623, 0.72662]
    improvement = [(b - a) / a * 100 for a, b in zip(v7_61, v7_15)]

    x = np.arange(len(metrics_labels))
    width = 0.30

    bars1 = ax.bar(x - width / 2, v7_61, width, label='YOLOv7 (61-class)', color='#888888', edgecolor='black', linewidth=0.4)
    bars2 = ax.bar(x + width / 2, v7_15, width, label='YOLOv7 (15-class, retrained)', color='#d62728', edgecolor='black', linewidth=0.4)

    # Add improvement percentage labels above bars (no arrows to avoid clutter)
    for i, (a, b, imp) in enumerate(zip(v7_61, v7_15, improvement)):
        ax.text(x[i] + width / 2, b + 0.015, f'+{imp:.1f}%',
                fontsize=9, fontweight='bold', color='#006400', ha='center', va='bottom')
        # Also label bar values
        ax.text(x[i] - width / 2, a + 0.01, f'{a:.2f}', fontsize=8, ha='center', va='bottom', color='#444')
        ax.text(x[i] + width / 2, b + 0.001, f'{b:.3f}', fontsize=8, ha='center', va='bottom', color='#444')

    ax.set_xticks(x)
    ax.set_xticklabels(metrics_labels, fontsize=11)
    ax.set_ylabel('Score')
    ax.set_ylim(0, 1.15)
    ax.legend(fontsize=10)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    fig.savefig(os.path.join(OUT, 'yolo_class_impact.png'))
    plt.close(fig)
    print('Saved yolo_class_impact.png')


# ============================================================
# RUN ALL
# ============================================================
if __name__ == '__main__':
    chart_yolo_full_comparison()
    chart_15class_training_curves()
    chart_15class_final_bar()
    chart_ocr_comparison()
    chart_evolution_timeline()
    chart_radar_comparison()
    chart_class_impact()
    print('\n=== All charts generated successfully ===')
