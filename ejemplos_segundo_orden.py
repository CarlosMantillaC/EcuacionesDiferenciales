"""
Ejemplos de uso del solucionador para ecuaciones de segundo orden y sistemas
"""

from ode_solver import ODESolver


def main():
    solver = ODESolver()
    
    print("=" * 80)
    print("EJEMPLOS DE ECUACIONES DE SEGUNDO ORDEN Y SISTEMAS")
    print("=" * 80)
    
    # Ejemplo 1: Coeficientes Constantes Homogénea
    print("\n1. COEFICIENTES CONSTANTES HOMOGÉNEA")
    print("-" * 80)
    print("Ecuación: y'' - 3*y' + 2*y = 0")
    result = solver.solve_second_order_constant_coeff("y'' - 3*y' + 2*y = 0")
    if result['success']:
        print(f"✓ Solución: {result['solution_formatted']}")
        print(f"Tipo: {'Homogénea' if result.get('is_homogeneous') else 'No Homogénea'}")
        print(f"\nPasos:\n{result['steps']}")
    else:
        print(f"✗ Error: {result['error']}")
    
    # Ejemplo 2: Coeficientes Constantes No Homogénea
    print("\n2. COEFICIENTES CONSTANTES NO HOMOGÉNEA")
    print("-" * 80)
    print("Ecuación: y'' + y = x")
    result = solver.solve_second_order_constant_coeff("y'' + y = x")
    if result['success']:
        print(f"✓ Solución: {result['solution_formatted']}")
        print(f"LaTeX: {result['solution_latex']}")
    else:
        print(f"✗ Error: {result['error']}")
    
    # Ejemplo 3: Ecuación de Cauchy-Euler
    print("\n3. ECUACIÓN DE CAUCHY-EULER")
    print("-" * 80)
    print("Ecuación: x**2*y'' + x*y' - y = 0")
    result = solver.solve_cauchy_euler("x**2*y'' + x*y' - y = 0")
    if result['success']:
        print(f"✓ Solución: {result['solution_formatted']}")
        print(f"\nPasos:\n{result['steps']}")
    else:
        print(f"✗ Error: {result['error']}")
    
    # Ejemplo 4: Reducible a Primer Orden - Caso y'' = f(x)
    print("\n4. REDUCIBLE A PRIMER ORDEN - Caso y'' = f(x)")
    print("-" * 80)
    print("Ecuación: y'' = x")
    result = solver.solve_reducible_to_first_order("y'' = x", case_type='f_x')
    if result['success']:
        print(f"✓ Solución: {result['solution_formatted']}")
        print(f"\nPasos:\n{result['steps']}")
    else:
        print(f"✗ Error: {result['error']}")
    
    # Ejemplo 5: Reducible a Primer Orden - Caso y'' = f(y')
    print("\n5. REDUCIBLE A PRIMER ORDEN - Caso y'' = f(y')")
    print("-" * 80)
    print("Ecuación: y'' = y'**2")
    result = solver.solve_reducible_to_first_order("y'' = y'**2", case_type='f_yp')
    if result['success']:
        print(f"✓ Solución: {result['solution_formatted']}")
    else:
        print(f"✗ Error: {result['error']}")
    
    # Ejemplo 6: Variación de Parámetros
    print("\n6. VARIACIÓN DE PARÁMETROS")
    print("-" * 80)
    print("Ecuación: y'' + y = tan(x)")
    result = solver.solve_variation_of_parameters("y'' + y = tan(x)")
    if result['success']:
        print(f"✓ Solución: {result['solution']}")
        print(f"\nPasos:\n{result['steps']}")
    else:
        print(f"✗ Error: {result['error']}")
    
    # Ejemplo 7: Sistema de Ecuaciones Lineales
    print("\n7. SISTEMA DE ECUACIONES DIFERENCIALES LINEALES")
    print("-" * 80)
    print("Sistema:")
    print("  x' = x + 2*y")
    print("  y' = 3*x + 2*y")
    print("Variables: x, y")
    
    equations = ["x' = x + 2*y", "y' = 3*x + 2*y"]
    result = solver.solve_linear_system(equations, "x,y")
    if result['success']:
        print(f"✓ Solución del sistema:")
        print(result['solution_formatted'])
        print(f"\nPasos:\n{result['steps']}")
    else:
        print(f"✗ Error: {result['error']}")
    
    # Ejemplo 8: Sistema 2 - Otro ejemplo
    print("\n8. SISTEMA DE ECUACIONES - Ejemplo 2")
    print("-" * 80)
    print("Sistema:")
    print("  f' = -f + g")
    print("  g' = 2*f - 2*g")
    print("Variables: f, g")
    
    equations = ["f' = -f + g", "g' = 2*f - 2*g"]
    result = solver.solve_linear_system(equations, "f,g")
    if result['success']:
        print(f"✓ Solución del sistema:")
        print(result['solution_formatted'])
    else:
        print(f"✗ Error: {result['error']}")
    
    # Ejemplo 9: Ecuación con raíces complejas
    print("\n9. COEFICIENTES CONSTANTES - Raíces Complejas")
    print("-" * 80)
    print("Ecuación: y'' + 4*y = 0")
    result = solver.solve_second_order_constant_coeff("y'' + 4*y = 0")
    if result['success']:
        print(f"✓ Solución: {result['solution_formatted']}")
        print(f"(Raíces complejas: ±2i)")
    else:
        print(f"✗ Error: {result['error']}")
    
    # Ejemplo 10: Raíz doble
    print("\n10. COEFICIENTES CONSTANTES - Raíz Doble")
    print("-" * 80)
    print("Ecuación: y'' - 2*y' + y = 0")
    result = solver.solve_second_order_constant_coeff("y'' - 2*y' + y = 0")
    if result['success']:
        print(f"✓ Solución: {result['solution_formatted']}")
        print(f"(Raíz doble: r = 1)")
    else:
        print(f"✗ Error: {result['error']}")
    
    print("\n" + "=" * 80)
    print("FIN DE LOS EJEMPLOS")
    print("=" * 80)


if __name__ == "__main__":
    main()
