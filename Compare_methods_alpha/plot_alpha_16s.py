import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
from scipy.stats import kruskal
import numpy as np

# Configuración estética
# plt.style.use('seaborn')
# sns.set_palette("Set2")
plt.rcParams['font.size'] = 9
plt.rcParams['axes.titlesize'] = 11


# Función para cargar archivos
def load_files(file_pattern):
    return sorted(glob.glob(file_pattern))


# Función para análisis estadístico
def add_stat_annot(ax, data, x, y, hue):
    hue_groups = data[hue].unique()
    x_groups = data[x].unique()

    for x_group in x_groups:
        subset = data[data[x] == x_group]
        groups = [subset[subset[hue] == h][y] for h in hue_groups]
        try:
            h, p = kruskal(*groups)
            if p < 0.05:
                x_pos = np.where(x_groups == x_group)[0][0]
                y_pos = subset[y].max() * 1.05
                ax.text(x_pos, y_pos, f'p={p:.2e}*', ha='center', color='red', fontsize=8)
        except:
            pass


# Cargar archivos
files = load_files('/media/rodrigo/Data1/pythonProject/PAPERS/Compare_methods_alpha/16s/Alpha - Mock-*.csv')

# ==============================================
# FIGURA 1: COMPARACIÓN POR MÉTODO (6 subplots)
# ==============================================
fig1, axes1 = plt.subplots(2, 3, figsize=(18, 12))

for ax, file in zip(axes1.flat, files):
    df = pd.read_csv(file)
    dataset_name = os.path.basename(file).replace('Alpha - ', '').replace('.csv', '')

    # Gráfico de violín con boxplot interno
    sns.violinplot(x='Metodo', y='Richness', data=df, ax=ax, inner='box', cut=0)
    ax.set_title(dataset_name, fontweight='bold')
    ax.set_xlabel('Methods')
    ax.set_ylabel('Richness')

    # Anotaciones estadísticas entre métodos
    groups = [df[df['Metodo'] == m]['Richness'] for m in df['Metodo'].unique()]
    h, p = kruskal(*groups)
    if p < 0.05:
        ax.text(0.5, 1.05, f'Diff between methods: p={p:.2e}*',
                transform=ax.transAxes, ha='center', color='blue')

plt.tight_layout()
plt.savefig('Figura1_Comparacion_por_Metodo.png', dpi=300, bbox_inches='tight')

# ==================================================
# FIGURA 2: COMPARACIÓN POR BASE DE DATOS (6 subplots)
# ==================================================
fig2, axes2 = plt.subplots(2, 3, figsize=(18, 12))

for ax, file in zip(axes2.flat, files):
    df = pd.read_csv(file)
    dataset_name = os.path.basename(file).replace('Alpha - ', '').replace('.csv', '')

    # Boxplot con puntos swarm
    sns.boxplot(x='DB', y='Simpson', data=df, ax=ax, width=0.6)
    sns.swarmplot(x='DB', y='Simpson', data=df, ax=ax, color='black', size=3, alpha=0.6)
    ax.set_title(dataset_name, fontweight='bold')
    ax.set_xlabel('Databases')
    ax.set_ylabel('Simpson')

    # Anotaciones estadísticas entre DBs
    groups = [df[df['DB'] == db]['Simpson'] for db in df['DB'].unique()]
    h, p = kruskal(*groups)
    if p < 0.05:
        ax.text(0.5, 1.05, f'Diff. between DBs: p={p:.2e}*',
                transform=ax.transAxes, ha='center', color='blue')

plt.tight_layout()
plt.savefig('Figura2_Comparacion_por_DB.png', dpi=300, bbox_inches='tight')

# ==================================================
# FIGURA 3: COMPARACIÓN DE BERGER-PARKER (6 subplots)
# ==================================================
fig3, axes3 = plt.subplots(2, 3, figsize=(18, 12))
fig3.suptitle('Comparación de Índice Berger-Parker por Método y DB', fontsize=14, y=1.02)

for ax, file in zip(axes3.flat, files):
    df = pd.read_csv(file)
    dataset_name = os.path.basename(file).replace('Alpha - ', '').replace('.csv', '')

    # Gráfico de barras con error
    sns.barplot(x='Metodo', y='Berger_Parker', hue='DB',
                data=df, ax=ax, ci='sd', errwidth=1, capsize=0.1)
    ax.set_title(dataset_name, fontweight='bold')
    ax.set_xlabel('Método')
    ax.set_ylabel('Berger-Parker')
    ax.legend(title='Base de Datos', bbox_to_anchor=(1, 1))

    # Anotar diferencias método-DB
    if len(df['Metodo'].unique()) > 1 and len(df['DB'].unique()) > 1:
        interaction_groups = df.groupby(['Metodo', 'DB'])['Berger_Parker'].mean()
        max_val = interaction_groups.max() * 1.1
        for i, (group, val) in enumerate(interaction_groups.items()):
            if val == max_val / 1.1:  # Solo anotar el valor máximo para evitar saturación
                ax.text(i, max_val, f'{val:.2f}', ha='center', fontsize=8)

plt.tight_layout()
plt.savefig('Figura3_Berger_Parker.png', dpi=300, bbox_inches='tight')

print("Figuras guardadas correctamente:")
print("- Figura1_Comparacion_por_Metodo.png")
print("- Figura2_Comparacion_por_DB.png")
print("- Figura3_Berger_Parker.png")