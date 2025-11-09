from ode_solver import ODESolver

solver = ODESolver()

# Probar una ecuación simple
print("Probando: dy/dx = x*y")
result = solver.solve_general("dy/dx = x*y")
print(f"Success: {result['success']}")
if result['success']:
    print(f"Solución: {result['solution']}")
else:
    print(f"Error: {result['error']}")
