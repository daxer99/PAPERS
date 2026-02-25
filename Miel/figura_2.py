import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict
import numpy as np

# --- Load data ---
df = pd.read_csv('figura_2.csv')

# Rename 'other' to avoid collisions across Taxa groups
df['Organism_key'] = df.apply(
    lambda r: f"other ({r['Taxa']})" if r['Organism'] == 'other' else r['Organism'], axis=1
)

# --- Color palettes by Taxa ---
taxa_palettes = {
    'Plant':    ['#2d7d46', '#4CAF50', '#88C969', '#C5E8A0'],
    'Bacteria': ['#1a4f7a', '#2573A8', '#4A9BC8', '#72B5D8', '#96CCE8', '#B8DFF0', '#D0EDFA', '#E4F5FF'],
    'Virus':    ['#9C2A1E', '#C0614A'],
}
gray = '#BDBDBD'

# Build color map in order of mean abundance within each taxa group
taxa_order = ['Plant', 'Bacteria', 'Virus']
org_order  = []
org_meta   = {}

for taxa in taxa_order:
    sub = df[df['Taxa'] == taxa].copy()
    mean_ab = sub.groupby('Organism_key')['Relative Abundance'].mean().sort_values(ascending=False)
    keys = mean_ab.index.tolist()
    non_other = [k for k in keys if not k.startswith('other')]
    other_keys = [k for k in keys if k.startswith('other')]
    keys = non_other + other_keys

    palette = taxa_palettes.get(taxa, ['#999999'])
    color_idx = 0
    for key in keys:
        label = df[df['Organism_key'] == key]['Organism'].iloc[0]
        color = gray if key.startswith('other') else palette[color_idx % len(palette)]
        if not key.startswith('other'):
            color_idx += 1
        org_meta[key] = {'taxa': taxa, 'label': label, 'color': color}
        org_order.append(key)

# --- Pivot using Organism_key ---
df_pivot = df.pivot_table(
    index='Sample', columns='Organism_key',
    values='Relative Abundance', aggfunc='sum'
).fillna(0)

sample_order  = ['control', 'honeyA', 'honeyB']
sample_labels = {
    'control': 'Control\n(Rosa chinensis)',
    'honeyA':  'Honey A',
    'honeyB':  'Honey B'
}

df_sorted = df_pivot.reindex(sample_order)
org_order = [o for o in org_order if o in df_sorted.columns]

# --- Plot ---
fig, ax = plt.subplots(figsize=(8, 5.5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

n = len(sample_order)
x = np.arange(n)
bottom = np.zeros(n)

for key in org_order:
    vals = df_sorted[key].values.astype(float)
    ax.bar(x, vals, bottom=bottom,
           color=org_meta[key]['color'],
           edgecolor='white', linewidth=0.5, width=0.55)
    bottom += vals

# --- Axes styling ---
ax.set_xlim(-0.45, n - 0.55)
ax.set_ylim(0, 108)
ax.set_xticks(x)
ax.set_xticklabels([sample_labels[s] for s in sample_order], fontsize=12)
ax.set_ylabel('Relative Abundance (%)', fontsize=12, labelpad=8)
ax.tick_params(axis='y', labelsize=11)
ax.tick_params(axis='x', length=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#dddddd', zorder=0)
ax.set_axisbelow(True)

# --- Legend ---
legend_elements = []
seen_keys = set()

for taxa in taxa_order:
    legend_elements.append(mpatches.Patch(color='none', label=taxa))
    for key in org_order:
        if org_meta[key]['taxa'] != taxa or key in seen_keys:
            continue
        seen_keys.add(key)
        legend_elements.append(
            mpatches.Patch(
                facecolor=org_meta[key]['color'],
                edgecolor='white', linewidth=0.5,
                label=f"  {org_meta[key]['label']}"
            )
        )

legend = ax.legend(
    handles=legend_elements,
    bbox_to_anchor=(1.02, 1),
    loc='upper left',
    frameon=False,
    fontsize=9.5,
    handlelength=1.2,
    handleheight=1.1,
    borderpad=0,
    labelspacing=0.35,
)

for text, handle in zip(legend.get_texts(), legend.legend_handles):
    if text.get_text().strip() in ['Plant', 'Bacteria', 'Virus']:
        text.set_fontweight('bold')
        text.set_fontsize(10.5)
        handle.set_visible(False)

plt.tight_layout()
plt.savefig('Figure_2.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('Figure_2.tiff', bbox_inches='tight', facecolor='white')