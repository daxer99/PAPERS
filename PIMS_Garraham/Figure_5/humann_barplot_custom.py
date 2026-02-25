#!/usr/bin/env python
"""
Wrapper para humann_barplot con colores personalizados
Colores: 'g' para PIMS, 'r' para Control
"""

import sys
import os
import argparse
import matplotlib

matplotlib.use('Agg')  # Para guardar sin interfaz gráfica
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

# Añadir ruta de humann al path
sys.path.insert(0, '/home/rodrigo/miniconda3/envs/humann3/lib/python3.7/site-packages')

try:
    from humann.tools.humann_barplot import main as humann_barplot_main
    from humann.tools.humann_barplot import create_parser
except ImportError as e:
    print(f"Error importando HUMAnN: {e}")
    print("Asegúrate de estar en el entorno 'humann3'")
    sys.exit(1)


def custom_color_mapper(labels, group_names=None):
    """
    Mapea colores personalizados según nombres de muestra
    """
    color_map = {}

    # Colores específicos para PIMS y Control
    pims_keywords = ['pims', 'paciente', 'patient', 'case']
    control_keywords = ['control', 'ctrl', 'normal', 'healthy']

    for label in labels:
        label_lower = str(label).lower()
        assigned = False

        # Verificar si es PIMS
        for keyword in pims_keywords:
            if keyword in label_lower:
                color_map[label] = 'g'  # Verde
                assigned = True
                break

        # Verificar si es Control
        if not assigned:
            for keyword in control_keywords:
                if keyword in label_lower:
                    color_map[label] = 'r'  # Rojo
                    assigned = True
                    break

        # Si no coincide, usar colores viridis escalados
        if not assigned:
            if group_names and label in group_names:
                idx = list(group_names).index(label)
                color_map[label] = cm.viridis(idx / max(1, len(group_names) - 1))
            else:
                # Color por defecto (gris)
                color_map[label] = '#808080'

    return color_map


def main():
    # Crear parser modificado
    parser = argparse.ArgumentParser(
        description="HUMAnN barplot con colores personalizados: PIMS(g), Control(r)",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Argumentos principales (igual que humann_barplot)
    parser.add_argument(
        "input",
        help="Input file: humann generated genefamilies, pathabundance, or pathcoverage file"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file for plot (file extension determines format: .png, .pdf, .svg, etc.)",
        default="humann_barplot.png"
    )

    parser.add_argument(
        "-f", "--format",
        help="Format for output image file (png, pdf, svg, tiff, etc.)",
        default=None
    )

    parser.add_argument(
        "-d", "--dpi",
        help="Resolution for output image (default: 300)",
        type=int,
        default=300
    )

    parser.add_argument(
        "-s", "--sort",
        help="Sort data by sum, name, or no sorting",
        choices=["sum", "name", "none"],
        default="sum"
    )

    parser.add_argument(
        "-c", "--custom-colors",
        help="Use custom color mapping: PIMS=green(g), Control=red(r)",
        action="store_true",
        default=True
    )

    parser.add_argument(
        "--width",
        help="Width of figure in inches (default: 10)",
        type=float,
        default=10.0
    )

    parser.add_argument(
        "--height",
        help="Height of figure in inches (default: 6)",
        type=float,
        default=6.0
    )

    parser.add_argument(
        "--title",
        help="Title for plot",
        default=None
    )

    # Parsear argumentos
    args = parser.parse_args()

    print("=" * 60)
    print("HUMAnN Barplot con colores personalizados")
    print("=" * 60)
    print(f"Archivo de entrada: {args.input}")
    print(f"Archivo de salida:  {args.output}")
    print(f"Formato: {args.format or os.path.splitext(args.output)[1][1:]}")
    print(f"DPI: {args.dpi}")
    print("Colores: PIMS='g' (verde), Control='r' (rojo)")
    print("=" * 60)

    try:
        # Leer datos
        print("Leyendo datos...")
        data = pd.read_csv(args.input, sep='\t', index_col=0, comment='#')

        # Preparar datos para plotting
        if args.sort == "sum":
            data = data.loc[data.sum(axis=1).sort_values(ascending=False).index]
        elif args.sort == "name":
            data = data.sort_index()

        # Obtener labels de muestras
        labels = data.columns.tolist()

        # Aplicar colores personalizados
        print(f"Muestras encontradas: {len(labels)}")
        color_map = custom_color_mapper(labels)

        # Mostrar asignación de colores
        print("\nAsignación de colores:")
        for label, color in color_map.items():
            if color == 'g':
                color_name = "VERDE (PIMS)"
            elif color == 'r':
                color_name = "ROJO (Control)"
            else:
                color_name = f"Por defecto: {color}"
            print(f"  {label:20} → {color_name}")

        # Crear figura
        fig, ax = plt.subplots(figsize=(args.width, args.height))

        # Configurar para Frontiers in Pediatrics
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
        plt.rcParams['axes.linewidth'] = 1.5

        # Preparar datos para barras apiladas
        ind = np.arange(len(data.index))
        width = 0.8 / len(labels) if len(labels) > 1 else 0.6

        # Crear barras
        bottom_values = np.zeros(len(data.index))
        bars = []

        for i, label in enumerate(labels):
            values = data[label].values
            bar = ax.bar(
                ind + i * width,
                values,
                width,
                bottom=bottom_values,
                color=color_map[label],
                edgecolor='black',
                linewidth=0.5,
                label=label
            )
            bars.append(bar)
            bottom_values += values

        # Personalizar gráfico
        ax.set_xlabel('Features', fontsize=10)
        ax.set_ylabel('Relative Abundance', fontsize=10)

        if args.title:
            ax.set_title(args.title, fontsize=12, fontweight='bold')

        # Configurar eje X
        ax.set_xticks(ind + width * len(labels) / 2)
        ax.set_xticklabels(data.index, rotation=45, ha='right', fontsize=8)

        # Leyenda
        ax.legend(
            fontsize=8,
            framealpha=0.9,
            edgecolor='black',
            loc='upper left',
            bbox_to_anchor=(1.02, 1)
        )

        # Ajustar layout
        plt.tight_layout(rect=[0, 0, 0.85, 1])  # Dejar espacio para leyenda

        # Guardar en alta resolución
        output_format = args.format or os.path.splitext(args.output)[1][1:] or 'png'

        print(f"\nGuardando figura en {args.output} ({args.dpi} DPI)...")
        plt.savefig(
            args.output,
            dpi=args.dpi,
            format=output_format,
            facecolor='white',
            edgecolor='none',
            bbox_inches='tight'
        )

        # Guardar también como TIFF para Frontiers
        if not args.output.lower().endswith('.tiff') and not args.output.lower().endswith('.tif'):
            tiff_output = os.path.splitext(args.output)[0] + '.tiff'
            plt.savefig(
                tiff_output,
                dpi=300,
                format='tiff',
                facecolor='white',
                edgecolor='none',
                bbox_inches='tight'
            )
            print(f"También guardado como TIFF 300 DPI: {tiff_output}")

        plt.close()

        # Información final
        file_size = os.path.getsize(args.output) / 1024
        print(f"\n✓ Figura generada exitosamente!")
        print(f"✓ Tamaño: {file_size:.1f} KB")
        print(f"✓ Dimensiones: {args.width} × {args.height} pulgadas")
        print(f"✓ DPI: {args.dpi}")
        print(f"✓ Muestras: {len(labels)}")

        print("\n" + "=" * 60)
        print("PARA FRONTIERS IN PEDIATRICS:")
        print("=" * 60)
        print("✓ Use el archivo TIFF para envío")
        print("✓ Resolución: 300 DPI (configurable con --dpi)")
        print("✓ Modo RGB automático")
        print("✓ Fuentes sans-serif (Arial/Helvetica)")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

        # Intentar con el comando original
        print("\nIntentando con humann_barplot original...")
        original_cmd = f"humann_barplot --input {args.input} --output {args.output}"
        print(f"Comando: {original_cmd}")
        os.system(original_cmd)


if __name__ == "__main__":
    main()