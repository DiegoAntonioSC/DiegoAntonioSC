# Importamos las librerías necesarias
import numpy as np
from scipy.optimize import linprog

# Función para solicitar los datos al usuario
def leer_datos():
    print("=== Método Simplex ===")
    tipo = input("¿El problema es de 'maximización' o 'minimización'? ").strip().lower()

    # Número de variables
    n_vars = int(input("¿Cuántas variables tiene la función objetivo? "))





