import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Load data
df = pd.read_csv('figura_1.csv')

# --- Publication color palette (colorblind-friendly, muted scientific tones) ---
colors = {
    'Plants':   '#4C9A6B',   # muted green
    'Bacteria': '#5B8DB8',   # muted blue
    'Virus':    '#C0614A',   # muted red
}

taxa_columns = df.columns[1:].tolist()
sample_labels = {
    'control': 'Control\n(Rosa chinensis)',
    'honeyA':  'Honey A',
    'honeyB':  'Honey B',
}

n_samples = len(df)

# --- Figure setup ---
fig, axes = plt.subplots(1, n_samples, figsize=(12, 4.5))
fig.patch.set_facecolor('white')

for i, (_, row) in enumerate(df.iterrows()):
    ax = axes[i]

    values  = [row[t] for t in taxa_columns]
    labels  = taxa_columns
    c_list  = [colors[t] for t in taxa_columns]

    # Filter zeros
    mask     = [v > 0 for v in values]
    fvalues  = [v for v, m in zip(values, mask) if m]
    flabels  = [l for l, m in zip(labels, mask) if m]
    fcolors  = [c for c, m in zip(c_list, mask) if m]

    # Explode slices slightly for polish
    explode  = [0.03] * len(fvalues)

    wedges, texts, autotexts = ax.pie(
        fvalues,
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
        explode=explode,
        colors=fcolors,
        wedgeprops=dict(linewidth=1.2, edgecolor='white'),
        pctdistance=0.72,
        textprops={'fontsize': 11},
    )

    # Style percentage text
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight('bold')
        at.set_color('white')

    # Title styling
    sample_key = row['Sample']
    ax.set_title(
        sample_labels.get(sample_key, sample_key),
        fontsize=13,
        fontweight='bold',
        pad=14,
        color='#222222',
    )

    # Draw a thin circle in the center for donut effect
    centre_circle = plt.Circle((0, 0), 0.40, fc='white', linewidth=1.2, edgecolor='#dddddd')
    ax.add_patch(centre_circle)
    ax.set_aspect('equal')

# --- Shared legend at bottom ---
legend_handles = [
    mpatches.Patch(facecolor=colors[t], edgecolor='white', label=t)
    for t in taxa_columns
]

fig.legend(
    handles=legend_handles,
    loc='lower center',
    ncol=3,
    fontsize=12,
    frameon=False,
    bbox_to_anchor=(0.5, -0.04),
    handlelength=1.5,
    handleheight=1.0,
)

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig(
    'Figure_1.png',
    dpi=300,
    bbox_inches='tight',
    facecolor='white'
)
plt.savefig(
    'Figure_1.tiff',
    bbox_inches='tight',
    facecolor='white'
)
print("Saved Figure_1.png and Figure_1.tiff")