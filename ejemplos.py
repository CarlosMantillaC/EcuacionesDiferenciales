"""
Ejemplos de uso del solucionador de ecuaciones diferenciales
"""

from ode_solver import ODESolver


def main():
    solver = ODESolver()
    
    print("=" * 80)
    print("EJEMPLOS DE RESOLUCIÓN DE ECUACIONES DIFERENCIALES")
    print("=" * 80)
    
    # Ejemplo 1: Variables Separables
    print("\n1. VARIABLES SEPARABLES")
    print("-" * 80)
    print("Ecuación: dy/dx = x*y")
    result = solver.solve_separable("dy/dx = x*y")
    if result['success']:
        print(f"Solución: {result['solution']}")
        print(f"Pasos: {result['steps']}")
    else:
        print(f"Error: {result['error']}")
    
    # Ejemplo 2: Ecuación Homogénea
    print("\n2. ECUACIÓN HOMOGÉNEA")
    print("-" * 80)
    print("Ecuación: dy/dx = (x + y)/x")
    result = solver.solve_homogeneous("dy/dx = (x + y)/x")
    if result['success']:
        print(f"Solución: {result['solution']}")
    else:
        print(f"Error: {result['error']}")
    
    # Ejemplo 3: Ecuación Exacta
    print("\n3. ECUACIÓN EXACTA")
    print("-" * 80)
    print("Ecuación: (2*x*y)dx + (x**2 + 1)dy = 0")
    result = solver.solve_exact("2*x*y", "x**2 + 1")
    if result['success']:
        print(f"Es exacta: {result['is_exact']}")
        print(f"Solución: {result['solution']}")
        print(f"Verificación: {result['steps']}")
    else:
        print(f"Error: {result['error']}")
    
    # Ejemplo 4: Ecuación Lineal
    print("\n4. ECUACIÓN LINEAL")
    print("-" * 80)
    print("Ecuación: dy/dx + y = x")
    result = solver.solve_linear("dy/dx + y = x")
    if result['success']:
        print(f"Solución: {result['solution']}")
        print(f"Método: {result['steps']}")
    else:
        print(f"Error: {result['error']}")
    
    # Ejemplo 5: Ecuación de Bernoulli
    print("\n5. ECUACIÓN DE BERNOULLI")
    print("-" * 80)
    print("Ecuación: dy/dx + y = x*y**2")
    result = solver.solve_bernoulli("dy/dx + y = x*y**2")
    if result['success']:
        print(f"Solución: {result['solution']}")
        print(f"Método: {result['steps']}")
    else:
        print(f"Error: {result['error']}")
    
    # Ejemplo 6: Factor Integrante
    print("\n6. FACTOR INTEGRANTE")
    print("-" * 80)
    print("Ecuación: (3*x**2 + y)dx + (x**2*y - x)dy = 0")
    result = solver.find_integrating_factor("3*x**2 + y", "x**2*y - x")
    if result['success']:
        print(f"Factor integrante: {result['type']} = {result['factor']}")
    else:
        print(f"Error: {result['error']}")
    
    # Ejemplo 7: Método General
    print("\n7. MÉTODO GENERAL (Detección Automática)")
    print("-" * 80)
    print("Ecuación: dy/dx = x/y")
    result = solver.solve_general("dy/dx = x/y")
    if result['success']:
        print(f"Solución: {result['solution']}")
        print(f"Clasificación detectada:")
        for hint in result['hints'][:5]:
            print(f"  • {hint}")
    else:
        print(f"Error: {result['error']}")
    
    print("\n" + "=" * 80)
    print("FIN DE LOS EJEMPLOS")
    print("=" * 80)


if __name__ == "__main__":
    main()
