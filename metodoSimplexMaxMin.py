MAX_ITERS = 100
TOL = 1e-8
M = 1e6

import numpy as np
from scipy.optimize import linprog

def leer_problema():
    print("Método Simplex")
    tipo = input("¿Desea maximizar o minimizar? solo coloca: (max/min): ").strip().lower()
    while tipo not in ["max", "min"]:
        print("Entrada no válida. Intente de nuevo.")
        tipo = input("¿Desea maximizar o minimizar? (max/min): ").strip().lower()
    n = int(input("Ingresa el numero de variables:"))
    print("Ingresa los valores a validar:")
    c = []
    for i in range(n):
        coef = float(input(f"coeficiente de x{i+1}: "))
        c.append(coef)
        if tipo == "max":
            c = [-ci for ci in c]
        m = int(input("Ingresa el numero de restricciones:"))
        restricciones = []
        print("para cda restriccion ingrese su valor, su signo y el valor total a la produccion")
        for i in range(m):
            print(f"numero de restriccion {i+1}:")
            coef_restriccion = []
            for j in range(n):
                aij = float(input(f"coeficiente de x{j+1}: "))
                coef_restriccion.append(aij)
            signo = input("Signo de restriccion (<=, >=, =): ").strip()
            while signo not in ["<=", ">=", "="]:
                print("Signo no valido. Intente de nuevo.")
                signo = input("tipo de restriccion (<=, >=, =): ").strip()
            rhs = float(input("Valor total de la produccion: (valor derecho RHS) "))
            restricciones.append((coef_restriccion, signo, rhs))
            return tipo, c, restricciones

def corregir_signo_restricciones(restricciones):
    for r in restricciones:
        if r[2] < 0:
            r[0] = [-a for a in r[0]]
            r[2] = -r[2]
            if r[1] == "<=":
                r[1] = ">="
            elif r[1] == ">=":
                r[1] = "<="
    return restricciones

def construir_forma_estandar(c_origen, restricciones):
    n = len(c_origen)
    var_names = [f"x{i+1}" for i in range(n)]
    A_rows  = []
    b = []
    basis = []
    art_indices = []
    slack_count = 0
    excess_count = 0
    art_count = 0
    for r in restricciones:
        fila = list(r[0])
        if len(fila) < len(var_names):
            fila.extend([0.0] * (len(var_names) - len(fila)))
        if r[1] == "<=":
            slack_count += 1
            for prev in A_rows:
                prev.append(0.0)
            fila.append(1.0)
            var_names.append(f"S{slack_count}")
            basis.append(len(var_names)-1)
        elif r[1] == ">=":
            excess_count += 1
            art_count += 1
            for prev in A_rows:
                prev.extend([0.0, 0.0])
            fila.append(-1.0)
            fila.append(1.0)
            var_names.append(f"E{excess_count}")
            var_names.append(f"A{art_count}")
            basis.append(len(var_names)-1)
            art_indices.append(len(var_names)-1)
        elif r[1] == "=":
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
        b.append(r[2])
    max_cols = max(len(row) for row in A_rows) if A_rows else len(var_names)
    for row in A_rows:
        if len(row) < max_cols:
            row.extend([0.0] * (max_cols - len(row)))
    if len(var_names) < max_cols:
        for i in range(len(var_names), max_cols):
            var_names.append(f"aux{i}")
    return A_rows, b, var_names, basis, art_indices

def imprimir_tableau(A_rows, b, c, basis, var_names, titulo="Tabla"):
    m = len(A_rows)
    nvars = len(var_names) if m > 0 else 0
    print("\n" + "="*60)
    print(f"{titulo:^60}")
    print("="*60)
    encabezado = ["Base", "Cb", "R"] + var_names
    print("{:>6} {:>8} {:>12}".format(encabezado[0], encabezado[1], encabezado[2]), end="")
    for name in encabezado[3:]:
        print(f"{name:>10}", end="")
    print()
    c_B = [c[idx] for idx in basis]
    for i, row in enumerate(A_rows):
        base_var = var_names[basis[i]]
        cb = c_B[i]
        Ri = b[i]
        print(f"{base_var:>6} {cb:8.2f} {Ri:12.6g}", end="")
        for val in row:
            print(f"{val:10.4g}", end="")
        print()
    Zj = []
    for j in range(nvars):
        zj = sum(c_B[i]*A_rows[i][j] for i in range(m))
        Zj.append(zj)
    rc = [c[j] - Zj[j] for j in range(nvars)]
    print("-"*60)
    print(f"{'Zj':>6} {'':>8} {'':>12}", end="")
    for zj in Zj:
        print(f"{zj:10.4g}", end="")
    print()
    print(f"{'cj-zj':>6} {'':8} {'':12}", end="")
    for v in rc:
        print(f"{v:10.4g}", end="")
    print()
    Z_val = sum(c_B[i] * b[i] for i in range(m))
    print("-"*60)
    print(f"Valor actual de Z (según base actual) = {Z_val:10.6g}")
    print("="*60 + "\n")

def simplex(A_rows, b, c, basis, var_names, max_iters = MAX_ITERS, titulo_prefix = "Iter"):
    m = len(A_rows)
    nvars = len(A_rows[0]) if m > 0 else len(c)
    for it in range(1, max_iters+1):
        imprimir_tableau(A_rows, b, c, basis, var_names, titulo=f"{titulo_prefix} {it}")
        c_B = [c[idx] for idx in basis]
        Zj = []
        for j in range(nvars):
            zj = sum(c_B[i]*A_rows[i][j] for i in range(m))
            Zj.append(zj)
        rc = [c[j] - Zj[j] for j in range(nvars)]
        entering = None
        max_rc = 0.0
        for j in range(nvars):
            if rc[j] > max_rc + TOL:
                max_rc = rc[j]
                entering = j
        if entering is None:
            x = [0.0]*nvars
            for i in range(m):
                x[basis[i]] = b[i]
            Z_val = sum(c_B[i]*b[i] for i in range(m))
            return "optimal", x, Z_val, basis, A_rows, b
        ratios = []
        for i in range(m):
            a_ij = A_rows[i][entering]
            if a_ij > TOL:
                ratio = b[i]/a_ij
                ratios.append((ratio, i))
        if not ratios:
            return "unbounded", None, None, basis, A_rows, b
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

def resolver_simplex_completo():
    tipo, c_origen, restricciones = leer_problema()
    es_min = (tipo == "min")
    if es_min:
        c_for_algo = [-val for val in c_origen]
    else:
        c_for_algo = list(c_origen)
    restricciones = corregir_signo_restricciones(restricciones)
    A_rows, b, var_names, basis, art_indices = construir_forma_estandar(c_for_algo, restricciones)
    nvars = len(A_rows[0]) if A_rows else len(c_for_algo)
    c_big = [0.0] * nvars
    for i in range(len(c_for_algo)):
        c_big[i] = c_for_algo[i]
    for idx in art_indices:
        c_big[idx] = M
    print("Problema ingresado:")
    print("variables originales:", [f"x{i+1}" for i in range(len(c_origen))])
    print("Nombre de variables:", var_names)
    print("Base inicial:", [var_names[i] for i in basis])
    print("Indices artificiales:", [var_names[i] for i in art_indices])
    imprimir_tableau(A_rows, b, c_big, basis, var_names, titulo="Tabla Inicial")
    status, x_big, Z_big, basis_final, A_final, b_final = simplex(A_rows = A_rows, b = b, basis = basis, var_names = var_names, titulo_prefix = "Big-M")
    if status == "unbounded":
        print("El problema no tiene solución óptima (no acotado).")
        return
    elif status == "iteration_limit":
        print("Se alcanzó el límite máximo de iteraciones sin encontrar solución óptima.")
        return
    sum_art = sum(x_big[idx] for idx in art_indices) if x_big is not None else None
    print(f"Suma de variables artificiales en solución: {sum_art}")
    if sum_art is None or sum_art > TOL:
        print("El problema no es factible (variables artificiales en solución).")
        return
    c_phase2 = [0.0] * len(c_big)
    for i in range(len(c_for_algo)):
        c_phase2[i] = c_for_algo[i]
    print("iniciando fase final")
    status2, x_final, Z_final, basis_final2, b_final2, = simplex(A_rows = A_final, b = b_final, c = c_phase2, basis = basis_final, var_names = var_names, titulo_prefix = "Fase 2")
    if status2 == "optimal":
        if es_min:
            Z_report = -Z_final
        else:
            Z_report = Z_final
        print("/Solucion Final")
        print(f"Estado: {status2}")
        print(f"Valor óptimo de Z: {Z_report:.6g}")
        print("Valores de las variables")
        for i, name in enumerate(var_names):
            val = x_final[i] if x_final is not None else 0.0
            print(f" {name:>6}: {val:.6g}")
        print("Variables en la base final:")
        for i in range(len(basis_final2)):
            print(f"  Fila {i+1}: base = {var_names[basis_final2[i]]}, valor = {b_final2[i]:.6g}")
    elif status2 == "unbounded":
        print ("La fase final no tiene solución óptima (no acotada).")
    else:
        print("No se alcanzó la solución de la fase final")
