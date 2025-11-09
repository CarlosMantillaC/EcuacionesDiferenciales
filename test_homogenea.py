from ode_solver import ODESolver
import sympy as sp

solver = ODESolver()

# Probar ecuación homogénea
print("Probando: dy/dx = (x+y)/x")
result = solver.solve_homogeneous("dy/dx = (x+y)/x")
print(f"Success: {result['success']}")
if result['success']:
    print(f"Solución: {result['solution']}")
else:
    print(f"Error: {result['error']}")

# Resolver manualmente para verificar
print("\n--- Solución manual ---")
x = sp.Symbol('x')
y = sp.Function('y')
eq = sp.Eq(sp.Derivative(y(x), x), (x + y(x))/x)
sol = sp.dsolve(eq, y(x))
print(f"Solución correcta: {sol}")
