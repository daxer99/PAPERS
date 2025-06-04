import os
import pandas as pd
import numpy as np
from scipy.stats import entropy


def calculate_alpha_diversity(df):
    """Calcula métricas de alfa diversidad para un DataFrame"""
    results = {
        'ID': [],
        'Richness': [],
        'Berger_Parker': [],
        'Simpson': [],
        'Shannon': []
    }

    for _, row in df.iterrows():
        # Extraer ID y abundancias
        sample_id = row.iloc[0]
        abundances = row.iloc[1:].astype(float).values  # Asegurar tipo float

        # Filtrar ceros y valores negativos
        abundances = abundances[abundances > 0]

        # Calcular métricas
        richness = len(abundances)

        if richness == 0:  # En caso de muestra vacía
            results['ID'].append(sample_id)
            results['Richness'].append(0)
            results['Berger_Parker'].append(np.nan)
            results['Simpson'].append(np.nan)
            results['Shannon'].append(np.nan)
            continue

        relative_abundances = abundances / abundances.sum()

        # Richness (ya calculado)
        # Berger-Parker: abundancia relativa máxima
        berger_parker = np.max(relative_abundances)

        # Simpson: 1 - sum(p_i^2)
        simpson = 1 - np.sum(relative_abundances ** 2)

        # Shannon: -sum(p_i * ln(p_i))
        # Versión más robusta del cálculo de Shannon
        shannon = -np.sum(relative_abundances * np.log(relative_abundances))

        # Guardar resultados
        results['ID'].append(sample_id)
        results['Richness'].append(richness)
        results['Berger_Parker'].append(berger_parker)
        results['Simpson'].append(simpson)
        results['Shannon'].append(shannon)

    return pd.DataFrame(results)


def process_folder(input_folder, output_folder):
    """Procesa todos los archivos CSV en una carpeta"""
    # Crear carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Procesar cada archivo CSV en la carpeta de entrada
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f'alpha_div_{filename}')

            print(f"Procesando {filename}...")

            try:
                # Leer archivo con manejo de datos problemáticos
                df = pd.read_csv(input_path, engine='python')

                # Verificar que todas las columnas (excepto ID) sean numéricas
                for col in df.columns[1:]:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

                # Calcular métricas
                alpha_div_df = calculate_alpha_diversity(df)

                # Guardar resultados
                alpha_div_df.to_csv(output_path, index=False)
                print(f"Resultados guardados en {output_path}")

            except Exception as e:
                print(f"Error procesando {filename}: {str(e)}")
                # Guardar archivo problemático para diagnóstico
                problem_path = os.path.join(output_folder, f'PROBLEM_{filename}')
                df.to_csv(problem_path, index=False)
                print(f"Se guardó copia del archivo problemático en {problem_path}")


# Configuración
input_folder = '/media/rodrigo/Data1/TESIS/Comparacion_metodos/wgs_alpha/samples_abundancia'  # Cambiar por tu ruta real
output_folder = '/media/rodrigo/Data1/TESIS/Comparacion_metodos/wgs_alpha/samples_alfa'  # Cambiar por tu ruta real

# Ejecutar procesamiento
process_folder(input_folder, output_folder)

print("\nProcesamiento completado!")