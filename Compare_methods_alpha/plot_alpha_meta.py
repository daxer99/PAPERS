import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


def extract_number(filename):
    match = re.search(r'Mock-(\d+)', filename)
    return int(match.group(1)) if match else float('inf')


# Configuración
input_folder = '/media/rodrigo/Data1/pythonProject/PAPERS/Compare_methods_alpha/meta'
output_file = '/media/rodrigo/Data1/pythonProject/PAPERS/Compare_methods_alpha/meta/comparacion_6_graficos_ordenados.png'

# Crear figura con 6 subgráficos (2 filas x 3 columnas)
fig, axs = plt.subplots(2, 3, figsize=(20, 12))

# Obtener lista de archivos CSV, ordenarlos y tomar los primeros 6
csv_files = sorted(
    [f for f in os.listdir(input_folder) if f.endswith('.csv')],
    key=extract_number
)[:6]

# Crear leyenda personalizada para todos los gráficos
legend_elements = [
    plt.Line2D([0], [0], color='blue', marker='o', linestyle='--', label='Berger-Parker', markersize=8),
    plt.Line2D([0], [0], color='green', marker='o', linestyle='--', label='Simpson', markersize=8),
    plt.Line2D([0], [0], color='red', marker='o', linestyle='--', label='Shannon', markersize=8)
]

for i, filename in enumerate(csv_files):
    try:
        # Leer datos
        filepath = os.path.join(input_folder, filename)
        df = pd.read_csv(filepath)

        methods = df['ID'].values
        berger_parker = df['Berger_Parker'].values
        simpson = df['Simpson'].values
        shannon = df['Shannon'].values
        base_name = os.path.splitext(filename)[0]

        # Determinar posición del subgráfico
        row = i // 3
        col = i % 3
        ax = axs[row, col]

        x = np.arange(len(methods))
        width = 0.25

        # Barras
        ax.bar(x - width, berger_parker, width, color='skyblue')
        ax.bar(x, simpson, width, color='lightgreen')
        ax.bar(x + width, shannon, width, color='salmon')

        # Puntos en los valores máximos
        ax.scatter(x - width, berger_parker, color='blue', zorder=5, s=50)
        ax.scatter(x, simpson, color='green', zorder=5, s=50)
        ax.scatter(x + width, shannon, color='red', zorder=5, s=50)

        # Líneas conectivas
        ax.plot(x - width, berger_parker, color='blue', linestyle='--', alpha=0.5)
        ax.plot(x, simpson, color='green', linestyle='--', alpha=0.5)
        ax.plot(x + width, shannon, color='red', linestyle='--', alpha=0.5)

        # Configuración del subgráfico
        letra = chr(65 + i)  # 65 es 'A' en ASCII
        ax.set_title(f'{base_name}', fontsize=12, pad=10, loc='left')
        ax.set_xlabel('Methods', fontsize=10)
        ax.set_ylabel('Index Value', fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels(methods, rotation=45, ha='right', fontsize=9)

        # Agregar letra de identificación en la esquina superior izquierda
        ax.text(-0.05, 1.05, letra, transform=ax.transAxes, fontsize=18,
                fontweight='bold', va='top', ha='right')

        # Añadir leyenda dentro de cada gráfico
        ax.legend(handles=legend_elements, loc='upper right', fontsize=9,
                  framealpha=0.9, edgecolor='black')

    except Exception as e:
        print(f"Error procesando {filename}: {str(e)}")
        axs[row, col].text(0.5, 0.5, f'Error\n{filename}', ha='center', va='center')
        axs[row, col].axis('off')

# Ajustar layout y guardar
plt.tight_layout()
plt.savefig(output_file, bbox_inches='tight', dpi=300)
plt.close()

print(f"Figura con 6 gráficos ordenados y etiquetados guardada en: {output_file}")