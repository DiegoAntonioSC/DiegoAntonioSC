# ...existing code...
## ERROR DE ORDEN DE EJECUCIÓN: Se elimina el bloque de ejecución automática al inicio. Solo debe estar al final del archivo.
## El bloque correcto estará al final del archivo.
MAX_ITERS = 100
TOL = 1e-8
M = 1e6
#Programa para solucionar problemas de optimizacion, con el metodo simplex
# o tambien conocido como programacion lineal.

# Importamos las librerías necesarias
import numpy as np
from scipy.optimize import linprog

# Función para solicitar los datos al usuario
def leer_problema():
    print("Método Simplex")
    tipo = input("¿Desea maximizar o minimizar? solo coloca: (max/min): ").strip().lower()
    while tipo not in ["max", "min"]:
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

        #Si el usuario desea maximizar, la libreria linprog minimiza, por lo que todo debe multiplicarse por -1
        # ERROR DE INDENTACIÓN: El bloque que sigue al 'if' debe estar indentado Identado (o indentación) es el uso de espacios o tabulaciones al inicio de una línea de código para indicar que pertenece a un bloque, como el cuerpo de una función, un ciclo o una condición. En Python, la indentación es obligatoria y define la estructura del programa. 
        if tipo == "max": #validamos si es maximizar o minimizar
            c = [-ci for ci in c] #si es maximizar, todos los valores de la lista c se multiplican por -1

        #Solicitamos el numero de restricciones
        m = int(input("Ingresa el numero de restricciones:"))
        restricciones = [] #creamos una lista vacia donde vamos a guardar las restricciones
        print("para cda restriccion ingrese su valor, su signo y el valor total a la produccion")
        # ERROR DE SINTAXIS: Falta el nombre de la variable en el ciclo for
        for i in range(m):
            print(f"numero de restriccion {i+1}:")
            coef_restriccion = [] #creamos una lista vacia donde vamos a guardar
            for j in range(n):
                aij = float(input(f"coeficiente de x{j+1}: ")) #ingresamos los coeficientes de cada variable
                coef_restriccion.append(aij) #los vamos agregando a la lista vacia
            signo = input("Signo de restriccion (<=, >=, =): ").strip() #ingresamos el signo de la restriccion
            # ERROR DE NOMBRE: 'sigono' no existe, debe ser 'signo'
            while signo not in ["<=", ">=", "="]:
                print("Signo no valido. Intente de nuevo.")
                signo = input("tipo de restriccion (<=, >=, =): ").strip()
            rhs = float(input("Valor total de la produccion: (valor derecho RHS) ")) #ingresamos el valor total de la produccion
            restricciones.append((coef_restriccion, signo, rhs)) #agregamos los datos a la lista vacia
            return tipo, c, restricciones #recolectamos los datos ingresados y los retornamos para el procimeso del programa

    #Solucion al problema paraoptimizar un resultado
    #Existen  varias condiciones que se deben cumplir para que el metodo simplex funcione.
    #Primer Condicion. Si el valor total de la produccion es negativo, multiplioca toda la restriccion por -1 y se ajusta el signo de la restriccion ya se ha (<=, >=, =), pero si es = esta no cambia
def corregir_signo_restricciones(restricciones):
    # ERROR DE INDENTACIÓN: el ciclo debe estar dentro de la función
    for r in restricciones:
        if r[2] < 0: # ERROR DE ACCESO: 'rhs' es el tercer elemento de la tupla
            #multiplicamos por -1 toda la restriccion
            r[0] = [-a for a in r[0]] # ERROR DE NOMBRE: 'coef_restriccion' es el primer elemento
            r[2] = -r[2]
            #cambiamos el signo si no es igualdad
            if r[1] == "<=":
                r[1] = ">="
            elif r[1] == ">=":
                r[1] = "<="
                #si el signo es = este no va a cambiar
    return restricciones #retornamos las restricciones corregidas

def construir_forma_estandar(c_origen, restricciones):
    # ERROR DE INDENTACIÓN: la función debe estar al nivel superior
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
    slack_count = 0 # ERROR DE NOMBRE: era 'salck_count'
    excess_count = 0
    art_count = 0

    #recorremos cada una de las restricciones ingresadas por el usuario y construimos la fila correspondiente
    for r in restricciones:
        fila = list(r[0]) # ERROR DE SINTAXIS: usar paréntesis en vez de llaves
        # si por ahora hay más columnas (porque otras restricciones añadieron variables),
        # extendemos la fila con ceros para que coincida con var_names
        if len(fila) < len(var_names):
            fila.extend([0.0] * (len(var_names) - len(fila)))

        #manejamos los valores según el signo
        if r[1] == "<=": # ERROR DE ACCESO: 'signo' es el segundo elemento de la tupla
            # agregar variable de holgura (S) con coeficiente +1
            slack_count += 1
            # antes de añadir la columna nueva, añadir ceros a filas previas
            for prev in A_rows:
                prev.append(0.0)
            fila.append(1.0)
            var_names.append(f"S{slack_count}")
            # la holgura queda en la base inicialmente
            basis.append(len(var_names)-1)
        elif r[1] == ">=":
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
        elif r[1] == "=":
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
        b.append(r[2]) # ERROR DE ACCESO: 'rhs' es el tercer elemento de la tupla

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

def imprimir_tableau(A_rows, b, c, basis, var_names, titulo="Tabla"):
    # ERROR DE INDENTACIÓN: la función debe estar al nivel superior
    #imprimimos la tabla actual: columnas (variables), filas (restricciones y RHS), muestra la base actual y el vector de costos reduciendolo en cada calculo 

    m = len(A_rows)
    nvars = len(var_names) if m > 0 else 0 # ERROR DE ACCESO: debe ser len(var_names)

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
    c_B = [c[idx] for idx in basis]

    #imprimimos cada fila de restricciones
    for i, row in enumerate(A_rows):
        base_var = var_names[basis[i]]
        cb = c_B[i] # ERROR DE ACCESO: debe ser el valor correspondiente
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
    # ERROR DE INDENTACIÓN: la función debe estar al nivel superior
        #la solucion seria asi: ejecuta las iteracciones del metodo simplex para una maximizacion Z = c * x, partiendo la tabala dada anteriormente
        #lo cual devuelve: 
        #status: "optimal", "unbounded", "iteration_limit"
        #x: vector solución (longitud = número total variables)
        #Z_val: valor objetivo
        #basis: base final
        #A_rows, b (tabla final)

    m = len(A_rows)
    nvars = len(A_rows[0]) if m > 0 else len(c)

    #realizamos un ciclo for donde realiza cada iteracion, como punto clave podemos utilizar un max_iters para evitar bucles infinitos
    for it in range(1, max_iters+1):
        #imprimimos la tabla actual
        imprimir_tableau(A_rows, b, c, basis, var_names, titulo=f"{titulo_prefix} {it}")

        #calcular costos reducidos de c_j - Zj
        c_B = [c[idx] for idx in basis]
        Zj = []
        for j in range(nvars):
            zj = sum(c_B[i]*A_rows[i][j] for i in range(m))
            Zj.append(zj)
        rc = [c[j] - Zj[j] for j in range(nvars)]

        #Verificamos si la condicion es optima
        entering = None #inicializamos la variable de entrada
        max_rc = 0.0 #con la variable max_rc le pedimos que guarde el valor mayor al costo reducido
        for j in range(nvars):
            if rc[j] > max_rc + TOL:
                max_rc = rc[j]
                entering = j
        if entering is None:
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
            if a_ij > TOL:
                ratio = b[i]/a_ij
                ratios.append((ratio, i))
        if not ratios:
            return "unbounded", None, None, basis, A_rows, b
        # nuestro siguiente paso a seguir es escoger la fila pivote para una razon minima
        ratios.sort(key=lambda x: (x[0], x[1]))
        pivot_radio, pivot_row = ratios[0]
        pivot_col = entering

        print(f"Pivote seleccionado: columna (Entrada) = {var_names[pivot_col]}, fila (Salida) = {var_names[basis[pivot_row]]}")
        pivot_val = A_rows[pivot_row][pivot_col]
        A_rows[pivot_row] = [val/pivot_val for val in A_rows[pivot_row]]
        b[pivot_row] = b[pivot_row] / pivot_val

        for i in range(m):
            if i == pivot_row:
                continue
            factor = A_rows[i][pivot_col]
            if abs(factor) > TOL:
                A_rows[i] = [A_rows[i][j] - factor * A_rows[pivot_row][j] for j in range(nvars)]
                b[i] = b[i] - factor * b[pivot_row]

        basis[pivot_row] = pivot_col

    return "iteration_limit", None, None, basis, A_rows, b

    #Creamos una funcion principal para integrar todo lo que fuimos pidiendo y creando para la solución, estas son:
    # lectura, preprocesamiento, construcción, simplex y postprocesamiento

# ERROR DE INDENTACIÓN: la función estaba indentada incorrectamente, debe estar al nivel superior
def resolver_simplex_completo():
    #realizamos la resolución completa, tomando: lectura, corrección de signos, creamos forma estándar, creamos la función objetivo, ejecutamos el método simplex, comprobamos variables artificiales. 

    #leemos el problema ingresado por el usuario
    tipo, c_origen, restricciones = leer_problema()

    #solución para resolver un problema de minimización
    # si es minimización, convertimos a maximización multiplicando por -1
    es_min = (tipo == "min")
    if es_min:
        c_for_algo = [-val for val in c_origen]
    else:
        c_for_algo = list(c_origen)

    #volvemos a repetir el procedimiento de la corrección de signos con los valores independientes (RHS)
    restricciones = corregir_signo_restricciones(restricciones)

    #construimos la forma estándar con los datos obtenidos
    A_rows, b, var_names, basis, art_indices = construir_forma_estandar(c_for_algo, restricciones)

    #construimos el vector c_big 
    nvars = len(A_rows[0]) if A_rows else len(c_for_algo) #calculamos el número total de las variables ingresadas por el usuario
    c_big = [0.0] * nvars #creamos una lista de ceros donde van a ser agregadas las variables ingresadas

    #copiamos los coeficientes originales a las posiciones correctas
    for i in range(len(c_for_algo)): #creamos un ciclo for para que itere en cada uno de los valores ingresados por el usuario
        c_big[i] = c_for_algo[i]  #traemos cada coeficiente original y los colocamos al nuevo vector c_big, así mantenemos los valores de la holgura y exceso en cero
    #para los valores artificiales los colocamos en un valor muy grande (M)
    for idx in art_indices:
        c_big[idx] = M

    #mostramos los datos iniciales
    print("Problema ingresado:")
    print("variables originales:", [f"x{i+1}" for i in range(len(c_origen))])
    print("Nombre de variables:", var_names)
    print("Base inicial:", [var_names[i] for i in basis])
    print("Indices artificiales:", [var_names[i] for i in art_indices])
    imprimir_tableau(A_rows, b, c_big, basis, var_names, titulo="Tabla Inicial")

    #Ejecutamos el método simplex con c_big, para empujar los valores artificiales a 0
    status, x_big, Z_big, basis_final, A_final, b_final = simplex(A_rows = A_rows, b = b, basis = basis, var_names = var_names, titulo_prefix = "Big-M")

    #condicionamos el método simplex y le decimos que si: 
    #el problema no tiene una solución óptima, o no está acotado, nos menciona que el problema no tiene una solución óptima
    if status == "unbounded": # ERROR DE SINTAXIS: la línea estaba correcta, pero se marca aquí para referencia
        print("El problema no tiene solución óptima (no acotado).")
        return
    #como el problema no tiene una solución óptima, le decimos que se llegó a un límite de iteraciones y que no hubo una solución óptima
    elif status == "iteration_limit":
        print("Se alcanzó el límite máximo de iteraciones sin encontrar solución óptima.")
        return

    #Otra condición importante, es validar que las variables artificiales sean 0
    sum_art = sum(x_big[idx] for idx in art_indices) if x_big is not None else None #Si existe una solución (x_big no es None), suma los valores de todas las variables artificiales. Si no hay solución (x_big es None), asigna None.
    print(f"Suma de variables artificiales en solución: {sum_art}")

    #si existen variables artificiales diferentes a cero el problema no es factible
    # ERROR DE NOMBRE: 'suma_art' debe ser 'sum_art'
    if sum_art is None or sum_art > TOL:
        print("El problema no es factible (variables artificiales en solución).")
        return

    #Si el problema es factible, realizamos la solución
    c_phase2 = [0.0] * len(c_big) #creamos una lista en ceros para los coeficientes de la fase 2, donde solo nos interesa los coeficientes originales
    for i in range(len(c_for_algo)):
        c_phase2[i] = c_for_algo[i]
        #dejamos los coeficientes artificiales en 0 (ya son 0 si sum_art==0)

    print("iniciando fase final")
    #llamamos al método simplex, usando la tabla final de la fase anterior, pero con los coeficientes originales
    status2, x_final, Z_final, basis_final2, b_final2, = simplex(A_rows = A_final, b = b_final, c = c_phase2, basis = basis_final, var_names = var_names, titulo_prefix = "Fase 2")

    #condicionamos el método simplex y le decimos que si: es óptimo que convierta Z final si el usuario seleccionó minimizar (min)
    if status2 == "optimal":
        if es_min:
            Z_report = -Z_final
        else:
            Z_report = Z_final

        #imprimimos la solución
        print("/Solucion Final")
        print(f"Estado: {status2}")
        print(f"Valor óptimo de Z: {Z_report:.6g}")

        #imprimimos cada variable y su valor
        print("Valores de las variables")
        for i, name in enumerate(var_names):
            val = x_final[i] if x_final is not None else 0.0
            print(f" {name:>6}: {val:.6g}")
        print("Variables en la base final:")
        for i in range(len(basis_final2)):
            print(f"  Fila {i+1}: base = {var_names[basis_final2[i]]}, valor = {b_final2[i]:.6g}")
    elif status2 == "unbounded": # ERROR DE INDENTACIÓN: elif debe estar alineado con if
        print ("La fase final no tiene solución óptima (no acotada).")
    else:
        print("No se alcanzó la solución de la fase final")