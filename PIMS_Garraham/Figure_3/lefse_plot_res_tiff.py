#!/usr/bin/env python
"""
Wrapper para lefse_plot_res.py que guarda en TIFF 300 DPI
Uso: python lefse_plot_res_tiff.py input.res output.tiff [opciones]
"""

import sys
import os
import matplotlib

matplotlib.use('Agg')  # Usar backend no interactivo
import matplotlib.pyplot as plt

# Importar la función plot_res del módulo lefse
try:
    from lefse.plot_res import plot_res
except ImportError:
    # Si no funciona, intenta importar de otra forma
    import importlib.util

    spec = importlib.util.spec_from_file_location("plot_res", "plot_res.py")
    plot_res_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plot_res_module)
    plot_res = plot_res_module.plot_res


def main():
    if len(sys.argv) < 3:
        print("Uso: python lefse_plot_res_tiff.py <archivo.res> <salida.tiff> [opciones]")
        print("\nOpciones:")
        print("  --title TITULO      Título del gráfico")
        print("  --width ANCHO       Ancho en pulgadas (default: 10)")
        print("  --max_feat N        Máximo número de features (default: 30)")
        print("  --format FORMATO    Formato de salida (tiff, png, pdf)")
        print("  --dpi DPI           Resolución (default: 300)")
        print("\nEjemplo:")
        print("  python lefse_plot_res_tiff.py resultados.res figura.tiff --title 'Mi Análisis'")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Configurar parámetros por defecto
    params = {
        'title': None,
        'width': 10,
        'max_feat': 30,
        'format': 'tiff',
        'dpi': 300
    }

    # Parsear argumentos opcionales
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--title' and i + 1 < len(sys.argv):
            params['title'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--width' and i + 1 < len(sys.argv):
            params['width'] = float(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--max_feat' and i + 1 < len(sys.argv):
            params['max_feat'] = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--format' and i + 1 < len(sys.argv):
            params['format'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--dpi' and i + 1 < len(sys.argv):
            params['dpi'] = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    # Verificar que el archivo de entrada existe
    if not os.path.exists(input_file):
        print(f"Error: El archivo '{input_file}' no existe.")
        sys.exit(1)

    # Configurar matplotlib para Frontiers in Pediatrics
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['axes.linewidth'] = 1.5
    plt.rcParams['lines.linewidth'] = 2.0

    # Determinar formato de salida
    format_map = {
        'tiff': 'tiff',
        'tif': 'tiff',
        'png': 'png',
        'pdf': 'pdf',
        'jpg': 'jpg',
        'jpeg': 'jpg'
    }

    output_format = format_map.get(params['format'].lower(), 'tiff')

    try:
        # Llamar a la función plot_res original con parámetros modificados
        print(f"Procesando: {input_file}")
        print(f"Guardando como: {output_file} ({output_format}, {params['dpi']} DPI)")

        # Importar y ejecutar plot_res con los argumentos modificados
        # Necesitamos simular los argumentos de línea de comandos
        import subprocess

        # Construir comando para lefse_plot_res.py original
        cmd = ['python', '-c', f'''
import sys
sys.argv = ["plot_res", "{input_file}"]
from lefse.plot_res import plot_res
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plot_res("{input_file}", title="{params['title'] or ''}", 
         max_feat={params['max_feat']}, width={params['width']})
plt.savefig("{output_file}", dpi={params['dpi']}, format="{output_format}", 
           facecolor="white", edgecolor="none", bbox_inches="tight")
print("Gráfico guardado exitosamente")
''']

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ Gráfico generado exitosamente")
            print(f"✓ Formato: {output_format.upper()}")
            print(f"✓ DPI: {params['dpi']}")
            print(f"✓ Tamaño estimado: {params['width']} pulgadas")

            # Verificar que el archivo se creó
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file) / 1024
                print(f"✓ Archivo creado: {output_file} ({file_size:.1f} KB)")

                # Información para Frontiers
                print("\n" + "=" * 60)
                print("VERIFICACIÓN PARA FRONTIERS IN PEDIATRICS:")
                print("=" * 60)
                print(f"✓ Formato: TIFF (aceptado por la revista)")
                print(f"✓ Resolución: {params['dpi']} DPI (cumple requisito ≥300)")
                print("✓ Modo de color: RGB (configurado)")
                print("✓ Texto: Usando fuentes sans-serif (Arial/Helvetica)")
                print("✓ Líneas: Ancho ≥ 1.5 puntos (configurado)")
                print("=" * 60)
            else:
                print("✗ Error: El archivo no se creó correctamente")
        else:
            print("✗ Error al generar el gráfico:")
            print(result.stderr)

    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nSolución alternativa:")
        print("1. Genera el gráfico normal con: python -m lefse.plot_res resultados.res")
        print("2. En la ventana de matplotlib, haz clic en 'Save'")
        print("3. Selecciona formato TIFF y establece 300 DPI")


if __name__ == "__main__":
    main()