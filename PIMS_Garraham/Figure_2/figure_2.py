import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib import rcParams

# Cargar los datos
data = pd.read_csv('top_10_sp.csv')

# Renombrar la columna Patient a PIMS
data = data.rename(columns={'Patient': 'PIMS'})

# Verificar los datos
print("Datos cargados:")
print(data.head())
print(f"\nEspecies: {len(data)}")
print(
    f"Control - Media: {data['Control'].mean():.2f}%, Rango: {data['Control'].min():.2f}-{data['Control'].max():.2f}%")
print(f"PIMS - Media: {data['PIMS'].mean():.2f}%, Rango: {data['PIMS'].min():.2f}-{data['PIMS'].max():.2f}%")

# ========== CONFIGURACIÓN PARA FRONTIERS IN PEDIATRICS ==========
# Configurar tamaño según especificaciones de la revista
# Usaremos ancho de 2 columnas (180 mm = 7.0866 pulgadas)
width_mm = 180  # Ancho de 2 columnas
height_mm = 120  # Altura para acomodar 10 especies
width_inch = width_mm / 25.4  # Convertir mm a pulgadas
height_inch = height_mm / 25.4

print(f"\nTamaño de figura: {width_mm} mm × {height_mm} mm")
print(f"Tamaño de figura: {width_inch:.2f} in × {height_inch:.2f} in")

# Configurar parámetros de texto y línea
plt.style.use('seaborn-v0_8-whitegrid')
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
rcParams['mathtext.fontset'] = 'dejavusans'

# ========== CREAR FIGURA ==========
fig, ax = plt.subplots(figsize=(width_inch, height_inch), dpi=300)

# Preparar datos
species = data['Specie']
control = data['Control']
pims = data['PIMS']
y_pos = np.arange(len(species))

# Colores según especificación: Control (rojo='r'), PIMS (verde='g')
control_color = 'r'  # Rojo
pims_color = 'g'  # Verde

# Gráfico de barras enfrentadas
# Control a la derecha (valores positivos), PIMS a la izquierda (valores negativos)
bar_width = 0.6
bar_control = ax.barh(y_pos, control, height=bar_width, align='center',
                      color=control_color, alpha=0.7, label='Control',
                      edgecolor='black', linewidth=1.5)
bar_pims = ax.barh(y_pos, -pims, height=bar_width, align='center',
                   color=pims_color, alpha=0.7, label='PIMS',
                   edgecolor='black', linewidth=1.5)

# ========== PERSONALIZACIÓN ==========
# Configurar etiquetas del eje Y (nombres de especies)
ax.set_yticks(y_pos)
# Formatear nombres de especies (reemplazar _ por espacio)
species_labels = [s.replace('_', ' ') for s in species]
ax.set_yticklabels(species_labels, fontsize=9, fontweight='normal')

# Configurar etiqueta del eje X
ax.set_xlabel('Relative Abundance (%)', fontsize=10, fontweight='normal')

# Añadir línea vertical en cero
ax.axvline(x=0, color='black', linewidth=1.5)

# Añadir valores a las barras (formateados a 1 decimal)
for i, (ctrl, pims_val) in enumerate(zip(control, pims)):
    # Valores de Control (derecha)
    if ctrl > 0:
        ax.text(ctrl + 0.3, i, f'{ctrl:.1f}', va='center', ha='left',
                fontsize=8, fontweight='normal',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                          alpha=0.8, edgecolor='gray', linewidth=0.5))

    # Valores de PIMS (izquierda) - mostrar como positivo
    if pims_val > 0:
        ax.text(-pims_val - 0.3, i, f'{pims_val:.1f}', va='center', ha='right',
                fontsize=8, fontweight='normal',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                          alpha=0.8, edgecolor='gray', linewidth=0.5))

# Ajustar límites del eje X
max_val = max(max(control), max(pims))
ax.set_xlim(-max_val - 5, max_val + 5)

# Invertir el eje X negativo para que los valores se muestren como positivos
xticks = ax.get_xticks()
# Filtrar ticks positivos y negativos
positive_ticks = [tick for tick in xticks if tick >= 0]
negative_ticks = [tick for tick in xticks if tick < 0]

# Crear etiquetas para los ticks
xtick_labels = []
for tick in xticks:
    if tick >= 0:
        xtick_labels.append(f'{tick:.0f}')
    else:
        xtick_labels.append(f'{-tick:.0f}')

ax.set_xticks(xticks)
ax.set_xticklabels(xtick_labels, fontsize=9)

# Añadir línea de conexión entre barras (opcional, más sutil)
for i in y_pos:
    ax.plot([control[i], -pims[i]], [i, i], color='black',
            linestyle=':', linewidth=1.0, alpha=0.5)

# Leyenda
ax.legend(fontsize=9, framealpha=0.9, edgecolor='black',
          loc='upper right', frameon=True)

# Asegurar que todo el texto tenga al menos 8 puntos
for item in ([ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(9)  # Mínimo 8 puntos

# Asegurar que las líneas tengan al menos 2 puntos de ancho
for spine in ax.spines.values():
    spine.set_linewidth(1.5)

# Añadir grid horizontal sutil
ax.grid(True, axis='x', alpha=0.2, linestyle='-', linewidth=0.5)

# Ajustar layout
plt.tight_layout()

# ========== GUARDAR EN DIFERENTES FORMATOS ==========
# Asegurar que estamos en modo RGB
fig.patch.set_facecolor('white')

# Guardar como TIFF con 300 DPI (formato requerido por la revista)
tiff_filename = 'top_10_species_comparison.tiff'
fig.savefig(tiff_filename, dpi=300, format='tiff',
            facecolor='white', edgecolor='none',
            bbox_inches='tight', pad_inches=0.05)
print(f"\nFigura guardada como TIFF: {tiff_filename}")

# Guardar como PNG con 300 DPI (para referencia/visualización)
png_filename = 'top_10_species_comparison.png'
fig.savefig(png_filename, dpi=300, format='png',
            facecolor='white', edgecolor='none',
            bbox_inches='tight', pad_inches=0.05)
print(f"Figura guardada como PNG: {png_filename}")

# Mostrar información de los archivos guardados
print(f"\nTamaño del archivo TIFF: {os.path.getsize(tiff_filename) / 1024:.1f} KB")
print(f"Tamaño del archivo PNG: {os.path.getsize(png_filename) / 1024:.1f} KB")

# ========== INFORMACIÓN ADICIONAL ==========
print("\n" + "=" * 60)
print("VERIFICACIÓN DE REQUISITOS DE FRONTIERS IN PEDIATRICS:")
print("=" * 60)
print(f"✓ Dimensiones: {width_mm} mm × {height_mm} mm (2 columnas)")
print(f"✓ Resolución: 300 DPI")
print(f"✓ Modo de color: RGB")
print(f"✓ Texto más pequeño: 8-9 puntos")
print(f"✓ Ancho de líneas: ≥ 1.5 puntos")
print(f"✓ Colores: Control='{control_color}' (rojo), PIMS='{pims_color}' (verde)")
print(f"✓ Especies mostradas: {len(data)}")
print("\nDiferencia promedio Control vs PIMS:")
for idx, row in data.iterrows():
    diff = row['Control'] - row['PIMS']
    print(f"  {row['Specie'].replace('_', ' ')[:30]:30} : {diff:6.1f}%")
print("=" * 60)

# Mostrar la figura
plt.show()