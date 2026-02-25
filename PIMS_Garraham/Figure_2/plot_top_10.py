import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar los datos
data = pd.read_csv('top_10_sp.csv')

# Verificar estilos disponibles
print("Estilos disponibles:", plt.style.available)

# Configuración del estilo (usando un estilo válido)
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'

# Crear figura
fig, ax = plt.subplots(figsize=(12, 8))

# Preparar datos
species = data['Specie']
control = data['Control']
patient = data['Patient']
y_pos = np.arange(len(species))

# Gráfico de barras enfrentadas
bar_control = ax.barh(y_pos, control, align='center', color='#3498db', label='Control')
bar_patient = ax.barh(y_pos, -patient, align='center', color='#e74c3c', label='Paciente')

# Personalización
# ax.set_title('Comparación de Abundancia Bacteriana: Control vs. Paciente', fontsize=16, pad=20)
ax.set_yticks(y_pos)
ax.set_yticklabels(species, fontsize=10)
ax.set_xlabel('Abundancia Relativa (%)', fontsize=12)
ax.legend(fontsize=12)

# Añadir línea vertical en cero
ax.axvline(x=0, color='black', linewidth=0.8)

# Añadir valores a las barras
for i, (ctrl, pat) in enumerate(zip(control, patient)):
    ax.text(ctrl + 0.5, i, f'{ctrl:.1f}', va='center', ha='left', fontsize=9)
    ax.text(-pat - 0.5, i, f'{pat:.1f}', va='center', ha='right', fontsize=9)

# Ajustar límites del eje X
max_val = max(max(control), max(patient))
ax.set_xlim(-max_val - 5, max_val + 5)

# Invertir el eje X negativo para que los valores sean positivos
xticks = ax.get_xticks()
ax.set_xticklabels([f'{abs(x):.0f}' for x in xticks])

# Añadir línea de diferencia entre barras
for i in y_pos:
    ax.plot([control[i], -patient[i]], [i, i], color='black', linestyle=':', linewidth=0.8)

plt.tight_layout()
plt.show()