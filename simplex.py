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
        c.append(coef) # los datos ingresados los vamos colocando en la lista vacia (c) con el metodo append que sirve para agregar elementos a una lista, estos valores ya estan convertidos a float, con la linea anterior.

        #Si el usario desea maximizar, la libreria linprog entra en juego ya que va a minimizar, por lo que todo sera multiplicado por -1
        if tipo == "maximizar": #validamos si es maximizar o minimizar
        c = [-ci for ci in c] #si es maximizar, todos los valores de la lista c se multiplican por -1

        #Solicitamos el numero de restricciones
        m = int(input("Ingresa el numero de restricciones:"))
        restricciones = [] #creamos una lista vacia donde vamos a guardar las restricciones
        print("para cda restriccion ingrese su valor, su signo y el valor total a la produccion")
        for in range(m):
            print(f"numero de restriccion {i+1}:")
            coef_restriccion = [] #creamos una lista vacia donde vamos a guardar
            for j in range(n):
                aij = float(input(f"coeficiente de x{j+1}: ")) #ingresamos los coeficientes de cada variable
                coef_restriccion.append(aij) #los vamos agregando a la lista vacia
            signo = input("Signo de restriccion (<=, >=, =): ").strip() #ingresamos el signo de la restriccion
            while sigono not in ["<=", ">=", "="]: #validamos que el signo sea correcto
                print("Signo no valido. Intente de nuevo.")
                signo = input("tipo de restriccion (<=, >=, =): ").strip()
            rhs = float(input("Valor total de la produccion: (valor derecho RHS) ")) #ingresamos el valor total de la produccion
            restricciones.append((coef_restriccion, signo, rhs)) #agregamos los datos a la lista vacia
            return tipo, c, restricciones #recolectamos los datos ingresados y los retornamos para el procimeso del programa

    #Solucion al problema paraoptimizar un resultado
    #Existen  varias condiciones que se deben cumplir para que el metodo simplex funcione.
    #Primer Condicion. Si el valor total de la produccion es negativo, multiplioca toda la restriccion por -1 y se ajusta el signo de la restriccion ya se ha (<=, >=, =), pero si es = esta no cambia
    def corregir_signo_restricciones(restricciones):
        for r in restricciones: #comenzamos un ciclo for para validar cada uno de los signos de cada restrinccion y asi correfirlos con la condicion a cumplir.
        if r["rhs"] < 0: #inciamos las condiciones
            #multiplicamos por -1 toda la restriccion
            r["coef_restrincion"] = [-a for a in r["coef_restriccion"]]
            r["rhs"] = -r["rhs"] #ajistamos el signo de la produccion total
            #cambiamos el signo si no es igualdad
            if r[signo] == "<=":
                r["signo"] = ">="
            elif r["signo"] == ">=":
                r["signo"] = "<="
                #esi el signo es = este no va a cambiar
        return restricciones #retornamos las restricciones corregidas

        #Segunda condicion. Convertir a la forma estandae (añadiendo holguras, excesos, valores artificales), manteniendo el orden entre variables.
        def construir_forma_estandar(c_origen, restricciones):
            #c_origen: coeficientes originales de la funcion objetivo
            #restricciones: lista de restricciones con coeficientes de restrincciones, signos y coeficientes totales

            #Construimos la matriz A, vector b
            n = len(c_origen) #numero de variables originales
            var_names = [f"x{i+1}" for i in range(n)] #nombres de las variables originales
            A_rows  = [] #lista para las filas de la matriz A
            b = [] #lista para el vector b
            basis = [] #lista para las variables basicas por fila
            art_indices = [] #indices de variables artificiales

            #inicializamos contadores que serviran para llevar la cuenta de cuántas variables de cada tipo se agregan mientras el usuario ingresa restricciones.
            #contador de varianle holgura
            #si el signo de la restriccion es (<=) se invrementara en 1
            salck_count = 0
            #contador de variable de exceso
            #si el signo de la restriccion es (>=) se incrementara en 1
            excess_count = 0
            #contador de variable artificial
            #si el signo de la restriccion es (>=) o (=) y el metodo de dos faseses no seria factible.
            art_count = 0

            #recorremos cada una de las restricciones ingresadas por el usuario y construimos la fila correspondiente
            for r in restricciones:
                fila = list{r["coef_restriccion"]} #comenzamos con los coeficientes originales de la restriccion
                # si por ahora hay más columnas (porque otras restricciones añadieron variables),
            # extendemos la fila con ceros para que coincida con var_names
            if len(fila) < len(var_names):
            fila.extend([0.0] * (len(var_names) - len(fila)))

            #manejamos los valores según el signo
        if r["signo"] == "<=":
            # agregar variable de holgura (S) con coeficiente +1
            slack_count += 1
            # antes de añadir la columna nueva, añadir ceros a filas previas
            for prev in A_rows:
                prev.append(0.0)
            fila.append(1.0)
            var_names.append(f"S{slack_count}")
            # la holgura queda en la base inicialmente
            basis.append(len(var_names)-1)
        elif r["signo"] == ">=":
            #agregar variable de exceso (E) con coef -1 y variable artificial (A) con +1
            excess_count += 1
            art_count += 1
            #añadir ceros a filas previas por 2 nuevas columnas (E y A)
            for prev in A_rows:
                prev.extend([0.0, 0.0])
            fila.append(-1.0)              # coef de exceso
            fila.append(1.0)               # coef de artificial
            var_names.append(f"E{excess_count}")
            var_names.append(f"A{art_count}")
            # la artificial va a la base inicialmente
            basis.append(len(var_names)-1)
            art_indices.append(len(var_names)-1)
        elif r["signo"] == "=":
            #agregar variable artificial (A) con coef +1
            art_count += 1
            for prev in A_rows:
                prev.append(0.0)
            fila.append(1.0)
            var_names.append(f"A{art_count}")
            basis.append(len(var_names)-1)
            art_indices.append(len(var_names)-1)
        else:
            raise ValueError("Signo de restricción no reconocido")

        A_rows.append(fila)
        b.append(r["rhs"])

    #si algunas filas quedaron cortas (teóricamente no debería),
    #igualamos tamaño agregando ceros (por seguridad)
    max_cols = max(len(row) for row in A_rows) if A_rows else len(var_names)
    for row in A_rows:
        if len(row) < max_cols:
            row.extend([0.0] * (max_cols - len(row)))
    #sincronizamos var_names al tamaño final
    if len(var_names) < max_cols:
        #si no añadimos variables en el bucle final
        for i in range(len(var_names), max_cols):
            var_names.append(f"aux{i}")

    return A_rows, b, var_names, basis, art_indices

    #imprimimos la matriz de forma legible. 
    def imprimir_tableau(A_rows, b, c, basis, var_names, titulo="Tabla")
    #imprimimos la tabla actual: columnas (variables), filas (restricciones y RHS), muestra la base actual y el vector de costos reduciendolo en cada calculo 

    m = len(A_rows)
    nvars = len(var_names[0]) if m>0 else 0

    # creamos el encabezado
    print("\n" + "="*60)
    print(f"{titulo:^60}")
    print("="*60)

    #creamos la fila de los nombre de las variables
    encabezado = ["Base", "Cb", "R"] + var_names
    print("{:>6} {:>8} {:>12}".format(encabezado[0], encabezado[1], encabezado[2]), end="")
    for name in encabezado[3:]:
        print(f"{name:>10}", end="")
    print()

    #calcularcalcular c_B
    c_B = [c[idx]for  idx in basis]

    #imprimimos cada fila de restricciones
    for i, row in enumerate(A_rows):
        base_var = var_names[basis[i]]
        cb = c_B
        Ri = b[i]
        print(f"{base_var:>6} {cb:8.2f} {Ri:12.6g}", end="")
        for val in row:
            print(f"{val:10.4g}", end="")
        print()

        #realizamos el calculo dw Zj = c_B *(B^-1 * A) => usando filas creadas anteriormente (tabla) Zj_j = sum_i c_B[i]*A_rows[i][j]
        Zj = [] #creamos una lista vacia
        for j in range(nvars):
            zj = sum(c_B[i]*A_rows[i][j] for i in range(m))
            Zj.append(zj)
        #calculamos los costos reducidos C_j - Zj
        rc = [c[j] - Zj[j] for j in range(nvars)]
        #imprimimos Zj y rc en dos filas separadas
        print("-"*60)
        print(f"{'Zj':>6} {'':>8} {'':>12}", end="")
        for zj in Zj:
            print(f"{zj:10.4g}", end="")
        print()
        print(f"{'cj-zj':>6} {'':8} {'':12}", end="")
    for v in rc:
        print(f"{v:10.4g}", end="")
    print()
    # imprimir valor actual de Z = sum(c_B * b)
    Z_val = sum(c_B[i] * b[i] for i in range(m))
    print("-"*60)
    print(f"Valor actual de Z (según base actual) = {Z_val:10.6g}")
    print("="*60 + "\n")
    #aqui ya imprimos nuestro resultados, la creacion de la tabla y los resultados necesarios para el metodo simplex

    