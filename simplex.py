#Programa para solucionar problemas de optimizacion, con el metodo simplex
# o tambien conocido como programacion lineal.

# Importamos las librerías necesarias
import numpy as np
from scipy.optimize import linprog

# Función para solicitar los datos al usuario
def leer_problema():
    print("Método Simplex")
    tipo = input("¿Desea maximizar o minimizar? (max/min): ").strip().lower()
    while tipo not in ["maximizar", "minimizar"]:
        print("Entrada no válida. Intente de nuevo.")
        tipo = input("¿Desea maximizar o minimizar? (max/min): ").strip().lower()
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
        if tipo == "max": #validamos si es maximizar o minimizar
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

    #Ahora implementaremos el meotodo simplex, con varias iteracionmes, con pivoteo de Gauss-Jordan
    #este metodo asume que las filas A_rows rpresentan B_inv * A de la tabla tranformada
    # y b representa B_inv * b la cual indica que variable es basica por fila
    def simplex(A_rows, b, c, basis, var_names, max_iters = MAX_ITERS, titulo_prefix = "Iter"):
        #la solucion seria asi: ejecuta las iteracciones del metodo simplex para una maximizacion Z = c * x, partiendo la tabala dada anteriormente
        #lo cual devuelve: 
        #status: "optimal", "unbounded", "iteration_limit"
        #x: vector solución (longitud = número total variables)
        #Z_val: valor objetivo
        #basis: base final
        #A_rows, b (tabla final)

        m =len(A_rows) #llamamos el numero de restrincciones y las guardamos
        nvars = lent(A_rows[0]) if m>0 else len(c) # le colocamos como condicion si A_rowstiene al menos una fila que tome las columnas como su longitud, si no que tome la longitud del vector de c

        #realizamos un ciclo for donde realiza cada iteracion, como punto clabe podemos utlizar un mas_iters el cual nos ayudara a no tener varias iteraciones infinitas o un ciclo for infinito
        for it in range(1, max_iters+1):
            #imprimimos la tabla actual
            imprimir_tableau(A_rows, b, c, basis, var_names, titulo=f"{titulo_prefix} {it}")

            #calcular costos reducidos de c_j - Zj
            c_B = [c[idx] for idx in basis]
            Zj = []
            for j in range(nvars):
                zj = sum[(c_B[i]*A_rows[i][j] for i in range(m)) for j in range(nvars)]
                Zj.append(zj)
            rc = [c[j] - Zj[j] for j in range(nvars)]

        #Verificamos si la condicion es optima
        entering = None #inicializamos la variable de entrada
        max_rc = 0.0 #con la variable max_rc le pedimos que guarde el valor mayor al costo reducido
        for j in range(nvars): #comenzamos un un ciclo for para que valide cada variable / valor encontrada
            if rc[j] > max_rc + TOL: #en la codicion le pedidmos que si el valor de la variable es mayor al valor guardado en max_rc, gaurde el valor y actualice el indice con entering
                max_rc = rc[j]
                entering = j
        if entering is None: #si no se encontro ningun valor mayor a cero, se concluye que la solucion es optima
            #solucion optima encontrada
            x = [0.0]*nvars
            for i in range(m):
                x[basis[i]] = b[i]
            Z_val = sum(c_B[i]*b[i] for i in range(m))
            return "optimal", x, Z_val, basis, A_rows, b

            #si hay variable de entrada, realizamos un calculo de la variable de salida
            ratios = [] #creamos una lista vacia para guardar los valores de las razones
            for i in range(m):
                a_ij = A_rows[i][entering]
                if a_ij > TOL: #si el valor de la variable es mayor a cero, se calcula la razon, no aplican valores negativos
                    ratio = b[i]/a_ij
                    ratios.append((ratio, i)) #guardamos la razon y el indice de la fila en nuestra lista vacia
            if not ratios: #si no se encontro ninguna razon positiva, el problema es ilimitado
                return "unbounded", None, None, basis, A_rows, b
            
            # nuestro siguiente paso a seguir es escoger la fila pivote para una razon minima
            ratios.sort(key=lambda x: (x[0], x[1])) #ordenamos la lista ratios / razones de menor a mayor
            pivot_radio, pivot_row = ratios[0] #selecionamos la menor razon y su fila correspondiente (el pivot_radio es el valor minimo de la razon y pivot_row  indicara la fila pivote)
            pivot_col = entering #pivot_col asigna la columna, a la variablke que entrara. 

            #mostraremos que es loq ue pivotemos
            prnt(f"Pivote seleccionado: colunba (Entrada) = {var_name[pivot_col]}, fila (Salida) = {var_names[basis[pivot_row]]}")
            #realizamos la operacion Gauss-Jordan: pedimos normalizar la fila pivote y anulamos la columna en otras filas
            pivot_val = A_rows[pivot_row][pivot_col] #guardamos el valor del pivote
            #normalizamos la fila pivote dividiendo todos sus elementos por el valor del pivote
            A_rows[pivot_row] = [val/pivot_val for val in A_rows[pivot_row]] #dividimos cada elemento de la fila pivote por el valor del pivote y pivote_val convierte el elemento pivoteen 1 y ajsuta el resto de las filas
            b[pivot_row] = b[pivot_row] / pivot_val #dividimos el termino independiente RHS, de la fila a la que realizamos el pivote, por el valor pivote

            #reducimos los valors de las otras filas i
            for i in range(m): #realizamos un ciclo for para que itere en cada fila de todas la restrincciones
                if i == pivot_row: #le colocamos una condicion donde si la fila es la pivote que normalizamos, no la tome en cuenta y salte a la otra
                    continue
                factor = A_rows[i][pivot_col] #obtenemos el valor del coeficiente de la variable que entra a la base de la columna pivote y el cual indica que valores hay en la restrinccion
                if abs(factor) > TOL: #si el factor es mayor a cero, realizamos la operacion de reduccion
                    A_rows[i] = [A_rows[i][j] - factor * A_rows[pivot_row][j] for j in range(nvars)] #actualizamo la fila restando el valor del factor por la fila pivote
                    #actualizamos el valor del termino independiente RHS
                    b[i] = b[i] - factor * b[pivot_row]

            #actualizamos la base
            basis[pivot_row] = pivot_col #la variable que entra a la base reemplaza a la que sale

        #si se alcanza el maximo de iteraciones sin encontrar una solucion optima, se detiene el proceso
        return "iteration_limit", None, None, basis, A_rows, b

        #Creamos una funcion principal para integrar todas lo que fuimos pidiendo y crando para la solucion, estas osn_
        # lectura, preporcesamiento, costruccion, simplex y postprocesamiento
        def resolver_simplex_completo():

        #realizamos la resolicoon completa, tomando: lectura, correccion de signos, creamos forma estandar, creamos la funcion objetivo, ejecutamos el metodo simplex, comprobamos variables artificiales. 

        #leemos el problema ingresado por el usuario
        tipo, c_origen, restricciones = leer_problema()

        #solucion para resolver un problema de minimizacion
        # si es minimizacion, convertimos a maximizacion multiplicando por -1
        es_min = (tipo == "min")
        if es_min:
            c_for_algo = [-val for val in c_origen]
        else:
            c_for_algo = list(c_origen)

        #volvemos repetir el procedimiento de la correccion de signos con los valores independientes (RHS)
        restricciones = corregir_signo_restricciones(restricciones)

        #costruimos la forma estandar con los datos obtenidos
        A_rows, b, var_names, basis, art_indices = construir_forma_estandar(c_for_algo, restricciones)

        #costruimso el vector c_big 
        nvars = len(A_rows[0]) if A_rows else len(c_for_algo) #calculamos el numero total de las variables ingresada spor el usuario
        c_big = [0.0] * nvars #creamos una lista de ceros dond evana  ser agregadas las variables ingresadas

        #copiamos los coeficientes originales a las posiciones correctas
        for i in range(len(c_for_algo)): #creamos un ciclo for para que itere en cada uno de los valores ingresados por el usuario
            c_big[i] = c_for_algo[i]  #traemos cada coeficiente original y las colocamos al nuevo vector c_big, gracias esto mantenemos los valores de la holgura y exceso en cero
            #para los valores artificiales los colocamos en un valor muy grande (M)
        for idx in art_indices:
            c_big[idx] = M

        #mostramos los datos iniciales
        