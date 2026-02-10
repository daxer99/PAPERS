import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import os

# Cargar los datos
df = pd.read_csv('/home/rodrigo/Documents/Microbiome/PIMS/alpha.csv')

# Configurar estilo y parámetros para Frontiers in Pediatrics
plt.style.use('seaborn-v0_8-whitegrid')
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
rcParams['mathtext.fontset'] = 'dejavusans'

# Configurar tamaño según especificaciones de la revista
# Usaremos ancho de 2 columnas (180 mm = 7.0866 pulgadas)
width_mm = 180  # Ancho de 2 columnas
height_mm = 90  # Altura más compacta para boxplots
width_inch = width_mm / 25.4  # Convertir mm a pulgadas
height_inch = height_mm / 25.4

# Crear figura con 2 subplots
fig, axes = plt.subplots(1, 2, figsize=(width_inch, height_inch),
                         constrained_layout=True, dpi=300)

# Colores según especificación: PIMS (verde), Control (rojo)
colors = ['g', 'r']  # PIMS, Control


# ========== FUNCIÓN PARA CREAR BOXPLOT SIMPLIFICADO ==========
def create_simple_boxplot(ax, data_pims, data_control, ylabel, letter):
    """Crea un boxplot simplificado sin títulos ni leyendas"""

    # Preparar datos para boxplot
    box_data = [data_pims, data_control]

    # Crear boxplot
    boxplot = ax.boxplot(box_data, patch_artist=True, widths=0.6,
                         medianprops=dict(color='black', linewidth=2),
                         whiskerprops=dict(linewidth=2),
                         capprops=dict(linewidth=2),
                         boxprops=dict(linewidth=2),
                         flierprops=dict(marker='o', markersize=6,
                                         markerfacecolor='black',
                                         markeredgecolor='black', alpha=0.5))

    # Colorear las cajas
    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
        patch.set_linewidth(2)
        patch.set_edgecolor('black')

    # Configurar ejes - SIN TÍTULO
    ax.set_xticklabels(['PIMS', 'Control'], fontsize=10, fontweight='normal')
    ax.set_ylabel(ylabel, fontsize=10, fontweight='normal')

    # Añadir puntos individuales (jitter plot)
    np.random.seed(42)  # Para reproducibilidad
    for i, data in enumerate(box_data, 1):
        x = np.random.normal(i, 0.05, size=len(data))
        ax.scatter(x, data, color=colors[i - 1], alpha=0.7, s=40,
                   edgecolor='black', linewidth=0.8, zorder=10)

    # Ajustar límites y grid
    y_min = min(min(data_pims), min(data_control))
    y_max = max(max(data_pims), max(data_control))
    y_range = y_max - y_min
    ax.set_ylim(bottom=y_min - 0.05 * y_range, top=y_max + 0.1 * y_range)

    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=9)

    # Asegurar que las líneas del marco tengan al menos 1.5 puntos
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)

    # Añadir letra identificadora (A o B)
    ax.text(0.02, 0.98, letter, transform=ax.transAxes,
            fontsize=14, fontweight='bold',
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      alpha=0.9, edgecolor='black', linewidth=1))


# ========== PRIMER SUBPLOT (A): Boxplot de Ace ==========
ax1 = axes[0]
pims_ace = df[df['group'] == 'PIMS']['Ace']
control_ace = df[df['group'] == 'Control']['Ace']

create_simple_boxplot(ax1, pims_ace, control_ace, 'Ace Index', 'A')

# ========== SEGUNDO SUBPLOT (B): Boxplot de Shannon ==========
ax2 = axes[1]
pims_shannon = df[df['group'] == 'PIMS']['Shannon']
control_shannon = df[df['group'] == 'Control']['Shannon']

create_simple_boxplot(ax2, pims_shannon, control_shannon, 'Shannon Index', 'B')

# ========== AJUSTES FINALES DE LA FIGURA ==========
# Asegurar que todo el texto tenga al menos 8 puntos
for ax in axes:
    for item in ([ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(9)

# Ajustar espacio entre subplots
plt.subplots_adjust(wspace=0.25)

# ========== GUARDAR EN DIFERENTES FORMATOS ==========
fig.patch.set_facecolor('white')

# Guardar como TIFF con 300 DPI
tiff_filename = 'alpha_diversity_boxplots_simple.tiff'
fig.savefig(tiff_filename, dpi=300, format='tiff',
            facecolor='white', edgecolor='none',
            bbox_inches='tight', pad_inches=0.05)
print(f"Figura guardada como TIFF: {tiff_filename}")

# Guardar como PNG con 300 DPI
png_filename = 'alpha_diversity_boxplots_simple.png'
fig.savefig(png_filename, dpi=300, format='png',
            facecolor='white', edgecolor='none',
            bbox_inches='tight', pad_inches=0.05)
print(f"Figura guardada como PNG: {png_filename}")

# Mostrar información
print(f"\nTamaño del archivo TIFF: {os.path.getsize(tiff_filename) / 1024:.1f} KB")
print(f"Tamaño del archivo PNG: {os.path.getsize(png_filename) / 1024:.1f} KB")

# Mostrar la figura
plt.show()

print("\n" + "=" * 60)
print("RESUMEN DE LA FIGURA GENERADA:")
print("=" * 60)
print("✓ Figura A: Boxplot de Ace Index (sin título)")
print("✓ Figura B: Boxplot de Shannon Index (sin título)")
print("✓ Sin leyendas adicionales")
print("✓ Letras A y B mantienen identificación")
print("✓ Colores: PIMS(verde='g'), Control(rojo='r')")
print("✓ Cumple requisitos Frontiers in Pediatrics")
print("=" * 60)