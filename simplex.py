#Programa para solucionar problemas de optimizacion, con el metodo simplex
# o tambien conocido como programacion lineal.

# Importamos las librerías necesarias
import numpy as np
from scipy.optimize import linprog

# Función para solicitar los datos al usuario
def leer_datos():
    print("Método Simplex")
    tipo = input("¿Desea maximizar o minimizar").strip().lower()

    #Solicitamos el numero de variables // ejemplo dos productos, dos precios, dos costos, etc, 
    #en pocas palabras cuantos datos vamos a validar
    n = int(input("Ingresa el numero de variables:"))

    #Solicitamos los coeficientes de la funcion objetivo, recordar que los coeficientes van ha ser los que multiplcar a x1, x2, x3 depedniendo de cuantos datos tenems a validar
    print("Ingresa los valores a validar:")
    c = [] #creamos una lista vacia donde vamos a guardar los valores / coeficientes que ingresemos
    for i in range(n): #realizaremos un cliclo for donde i comienza en cero (i=0) hasta que i se igual a -1 (i = n-1)
        coef = float(input(f"coeficiente de x{i+1}: ")) #una vez ingresados los datos, convertimos esos valores de string a float, ya que no pueden ser valores enteros y se lo mostramos con i+1 dependieno de cuantos datos haya ingresado
        c.append(coef)

