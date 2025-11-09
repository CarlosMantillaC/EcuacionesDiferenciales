from ode_solver import ODESolver

solver = ODESolver()

# Probar diferentes ecuaciones
ecuaciones = [
    ("dy/dx = x*y", "Variables Separables"),
    ("dy/dx = (x+y)/x", "Homogénea"),
    ("dy/dx + y = x", "Lineal"),
]

print("="*80)
print("PRUEBA DE FORMATO DE SOLUCIONES")
print("="*80)

for ecuacion, tipo in ecuaciones:
    print(f"\n{tipo}: {ecuacion}")
    print("-"*80)
    
    result = solver.solve_general(ecuacion)
    
    if result['success']:
        print(f"✓ Formato Original:")
        print(f"  {result['solution']}")
        
        print(f"\n✓ Formato Legible:")
        print(f"  {result['solution_formatted']}")
        
        print(f"\n✓ Formato LaTeX:")
        print(f"  {result['solution_latex']}")
    else:
        print(f"✗ Error: {result['error']}")
    
    print()
