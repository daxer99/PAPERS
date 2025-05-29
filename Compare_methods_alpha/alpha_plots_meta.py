import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# Configuración
input_folder = 'C:/Users/Lenovo/Documents/PAPERS/Compare_methods_alpha/meta'  # Carpeta con los archivos CSV de entrada
output_folder = 'C:/Users/Lenovo/Documents/PAPERS/Compare_methods_alpha/meta'  # Carpeta donde se guardarán los gráficos

# Crear carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)


# Función para generar los gráficos
def generar_graficos(df, filename):
    methods = df['ID'].values
    berger_parker = df['Berger_Parker'].values
    simpson = df['Simpson'].values
    shannon = df['Shannon'].values

    base_name = os.path.splitext(filename)[0]

    # 1. Gráficos individuales de barras
    plt.figure(figsize=(15, 10))

    # Berger-Parker
    plt.subplot(3, 1, 1)
    plt.bar(methods, berger_parker, color='skyblue')
    plt.title(f'{base_name} - Índice de Berger-Parker\n(Mayor valor = mayor dominancia)')
    plt.ylabel('Valor del índice')
    plt.ylim(0, 0.3)

    # Simpson
    plt.subplot(3, 1, 2)
    plt.bar(methods, simpson, color='lightgreen')
    plt.title(f'{base_name} - Índice de Simpson\n(Mayor valor = mayor diversidad)')
    plt.ylabel('Valor del índice')
    plt.ylim(0.8, 0.9)

    # Shannon
    plt.subplot(3, 1, 3)
    plt.bar(methods, shannon, color='salmon')
    plt.title(f'{base_name} - Índice de Shannon\n(Mayor valor = mayor diversidad)')
    plt.ylabel('Valor del índice')
    plt.ylim(1.8, 2.4)

    plt.tight_layout()
    plt.savefig(f'{output_folder}/{base_name}_indices_individuales.png')
    plt.close()

    # 2. Gráfico combinado de barras
    plt.figure(figsize=(12, 6))
    x = np.arange(len(methods))
    width = 0.25

    plt.bar(x - width, berger_parker, width, label='Berger-Parker', color='skyblue')
    plt.bar(x, simpson, width, label='Simpson', color='lightgreen')
    plt.bar(x + width, shannon, width, label='Shannon', color='salmon')

    plt.title(f'{base_name} - Comparación de Índices de Diversidad')
    plt.xlabel('Métodos')
    plt.ylabel('Valor del índice')
    plt.xticks(x, methods)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{output_folder}/{base_name}_indices_combinados.png')
    plt.close()

    # 3. Gráfico de radar
    categories = ['Berger-Parker', 'Simpson', 'Shannon']
    N = len(categories)

    # Normalización para el radar
    df_radar = df[['Berger_Parker', 'Simpson', 'Shannon']].copy()
    df_radar['Berger_Parker'] = df_radar['Berger_Parker'] / df_radar['Berger_Parker'].max()
    df_radar['Simpson'] = df_radar['Simpson'] / df_radar['Simpson'].max()
    df_radar['Shannon'] = df_radar['Shannon'] / df_radar['Shannon'].max()

    values = df_radar.values.tolist()

    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)

    plt.xticks(angles[:-1], categories, color='grey', size=10)
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ["0.2", "0.4", "0.6", "0.8", "1.0"], color="grey", size=7)
    plt.ylim(0, 1.1)

    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    for i in range(len(methods)):
        values_i = values[i]
        values_i += values_i[:1]
        ax.plot(angles, values_i, linewidth=1, linestyle='solid',
                label=methods[i], color=colors[i])
        ax.fill(angles, values_i, colors[i], alpha=0.1)

    plt.title(f'{base_name} - Comparación de Índices (Normalizado)', size=15, y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.savefig(f'{output_folder}/{base_name}_radar_diversidad.png')
    plt.close()


# Procesar todos los archivos CSV en la carpeta de entrada
print(f"Procesando archivos en {input_folder}...")
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        print(f"\nProcesando archivo: {filename}")
        try:
            filepath = os.path.join(input_folder, filename)
            df = pd.read_csv(filepath)
            print(f"Datos leídos:\n{df.head()}")

            generar_graficos(df, filename)
            print(f"Gráficos generados para {filename}")

        except Exception as e:
            print(f"Error procesando {filename}: {str(e)}")

print("\nProceso completado. Gráficos guardados en:", output_folder)