import pandas as pd
from scipy.stats import kruskal, mannwhitneyu
import itertools
import os
import glob


def analyze_alpha_diversity(file_path):
    """Analiza un archivo CSV de diversidad alfa"""
    # Cargar datos
    data = pd.read_csv(file_path)

    # Obtener nombre del archivo
    file_name = os.path.basename(file_path)

    print(f"\n{'=' * 50}")
    print(f"Análisis para archivo: {file_name}")
    print(f"{'=' * 50}\n")

    # Definir métricas y factores de agrupación
    metrics = ['Richness', 'Berger_Parker', 'Simpson']
    grouping_factors = ['Subsampling', 'Metodo', 'DB']

    # Función para realizar pruebas y mostrar resultados
    def perform_tests(data, group_var, group_name):
        print(f"\nResultados para agrupación por {group_name}:")

        for metric in metrics:
            # Obtener grupos únicos
            unique_groups = data[group_var].unique()

            # Si solo hay un grupo, no se puede hacer prueba
            if len(unique_groups) < 2:
                print(f"- {metric}: Solo hay 1 grupo ({unique_groups[0]}). No se puede realizar prueba.")
                continue

            # Preparar datos para Kruskal-Wallis
            groups = [data[data[group_var] == g][metric] for g in unique_groups]

            # Kruskal-Wallis test
            try:
                h, p = kruskal(*groups)
                print(f"- {metric}: H = {h:.3f}, p = {p:.4f}", end='')

                # Interpretación valor p
                if p < 0.001:
                    print(" ***")  # Muy significativo
                elif p < 0.01:
                    print(" **")  # Muy significativo
                elif p < 0.05:
                    print(" *")  # Significativo
                else:
                    print(" (ns)")  # No significativo

                # Post-hoc si es significativo y hay más de 2 grupos
                if p < 0.05 and len(unique_groups) > 2:
                    print("\tComparaciones post-hoc (Mann-Whitney):")
                    # Todas las comparaciones por pares
                    for g1, g2 in itertools.combinations(unique_groups, 2):
                        u, p_val = mannwhitneyu(data[data[group_var] == g1][metric],
                                                data[data[group_var] == g2][metric],
                                                alternative='two-sided')
                        # Solo mostrar comparaciones significativas
                        if p_val < 0.05:
                            print(f"\t{g1} vs {g2}: U = {u:.0f}, p = {p_val:.4f}")

            except ValueError as e:
                print(f"- {metric}: Error en prueba - {str(e)}")

    # Realizar análisis para cada factor de agrupación
    for factor in grouping_factors:
        perform_tests(data, factor, factor)

    print("\n" + "=" * 50 + "\n")


# Procesar todos los archivos CSV en la carpeta
folder_path = 'C:/Users/Lenovo/Documents/PAPERS/Compare_methods_alpha/16s'  # Reemplazar con la ruta real
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

if not csv_files:
    print("No se encontraron archivos CSV en la carpeta especificada.")
else:
    print(f"Analizando {len(csv_files)} archivos en la carpeta...")
    for file in csv_files:
        analyze_alpha_diversity(file)
    print("Análisis completado para todos los archivos.")