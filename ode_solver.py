"""
Módulo para resolver ecuaciones diferenciales ordinarias de primer orden
Soporta: Variables separables, Homogéneas, Exactas, Lineales, Bernoulli, Factores integrantes
"""

import sympy as sp
from sympy import symbols, Function, Eq, dsolve, diff, integrate, simplify, exp, log, sqrt, latex
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re


class ODESolver:
    def __init__(self):
        self.x = symbols('x')
        self.y = Function('y')
        self.C1, self.C2 = symbols('C1 C2')
        self.parse_locals = {
            'x': self.x,
            'y': self.y,
            'Derivative': sp.Derivative,
            'E': sp.E,
            'e': sp.E,
            'pi': sp.pi,
            'PI': sp.pi,
            'exp': sp.exp
        }
        self.transformations = standard_transformations + (implicit_multiplication_application,)
    
    def format_solution(self, solution):
        """
        Convierte la solución de SymPy a formato más legible
        """
        # Convertir a string
        sol_str = str(solution)
        
        # Si es una ecuación Eq(y(x), ...), extraer solo el lado derecho
        if sol_str.startswith('Eq(y(x), '):
            # Extraer la parte después de 'Eq(y(x), ' y antes del último ')'
            rhs = sol_str[9:-1]
            sol_str = f"y(x) = {rhs}"
        
        # Reemplazos para hacer más legible
        sol_str = sol_str.replace('**', '^')
        sol_str = sol_str.replace('*', '·')
        sol_str = sol_str.replace('exp(', 'e^(')
        sol_str = sol_str.replace('log(', 'ln(')
        sol_str = sol_str.replace('sqrt(', '√(')
        
        return sol_str
    
    def get_latex_solution(self, solution):
        """Convierte la solución a formato LaTeX legible"""
        try:
            if isinstance(solution, sp.Eq):
                lhs = latex(solution.lhs)
                rhs = latex(solution.rhs)
                return f"{lhs} = {rhs}"
            return latex(solution)
        except Exception:
            return str(solution)
    
    def parse_equation(self, equation_str):
        """
        Parsea una ecuación diferencial en formato string
        Formatos aceptados:
        - dy/dx = f(x,y)
        - y' = f(x,y)
        - y'' = f(x,y,y')
        - M(x,y) + N(x,y)*dy/dx = 0
        """
        equation_str = equation_str.replace(' ', '')
        # Reemplazar derivadas de segundo orden primero
        equation_str = equation_str.replace("y''", "Derivative(y(x), x, 2)")
        equation_str = equation_str.replace("d2y/dx2", "Derivative(y(x), x, 2)")
        # Luego primeras derivadas
        equation_str = equation_str.replace('dy/dx', "Derivative(y(x), x)")
        equation_str = equation_str.replace("y'", "Derivative(y(x), x)")
        # Reemplazar y -> y(x) incluso cuando está pegado a coeficientes, evitando dobles reemplazos
        import re
        placeholder = "__YFUNC__"
        equation_str = equation_str.replace('y(x)', placeholder)
        equation_str = re.sub(r'y(?!\()', 'y(x)', equation_str)
        equation_str = equation_str.replace(placeholder, 'y(x)')
        
        return equation_str

    def _parse(self, expr, local_dict=None):
        """Helper para parsear expresiones habilitando multiplicación implícita"""
        loc = local_dict or self.parse_locals
        return parse_expr(expr, local_dict=loc, transformations=self.transformations)
    
    def _dsolve(self, eq, y, initial_conditions=None):
        ics = self._prepare_ics(initial_conditions)
        if ics:
            return dsolve(eq, y, ics=ics)
        return dsolve(eq, y)
    
    def _prepare_ics(self, initial_conditions):
        if not initial_conditions:
            return None
        x0 = initial_conditions.get('x0') if isinstance(initial_conditions, dict) else None
        y0 = initial_conditions.get('y0') if isinstance(initial_conditions, dict) else None
        yp0 = initial_conditions.get('yp0') if isinstance(initial_conditions, dict) else None
        if not any([y0, yp0]):
            return None
        if x0 is None:
            raise ValueError("Debe especificar x0 para aplicar condiciones iniciales")
        try:
            x0 = sp.sympify(x0)
            ics = {}
            if y0 is not None:
                ics[self.y(self.x).subs(self.x, x0)] = sp.sympify(y0)
            if yp0 is not None:
                ics[diff(self.y(self.x), self.x).subs(self.x, x0)] = sp.sympify(yp0)
            return ics or None
        except (sp.SympifyError, ValueError) as exc:
            raise ValueError(f"Condiciones iniciales inválidas: {exc}")
    
    def solve_separable(self, equation_str, initial_conditions=None):
        """
        Resuelve ecuaciones de variables separables: dy/dx = f(x)g(y)
        """
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            
            # Intentar resolver con dsolve
            if '=' in eq_str:
                parts = eq_str.split('=')
                lhs = self._parse(parts[0])
                rhs = self._parse(parts[1])
                eq = Eq(lhs, rhs)
            else:
                eq = self._parse(eq_str)
            
            special_solution = self._solve_special_cases(eq)
            if special_solution:
                return special_solution
            
            solution = self._dsolve(eq, y, initial_conditions)
            
            # Simplificar la solución
            if isinstance(solution, list):
                solution = solution[0]
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Variables Separables'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Variables Separables'
            }
    
    def solve_homogeneous(self, equation_str, initial_conditions=None):
        """
        Resuelve ecuaciones homogéneas: dy/dx = f(y/x)
        """
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            
            if '=' in eq_str:
                parts = eq_str.split('=')
                lhs = self._parse(parts[0])
                rhs = self._parse(parts[1])
                eq = Eq(lhs, rhs)
            else:
                eq = self._parse(eq_str)
            
            special_solution = self._solve_special_cases(eq)
            if special_solution:
                return special_solution
            
            solution = self._dsolve(eq, y, initial_conditions)
            
            # Simplificar la solución
            if isinstance(solution, list):
                solution = solution[0]
            
            solution_simplified = simplify(solution)
            
            return {
                'success': True,
                'solution': str(solution_simplified),
                'solution_formatted': self.format_solution(solution_simplified),
                'solution_latex': self.get_latex_solution(solution_simplified),
                'method': 'Ecuación Homogénea'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Ecuación Homogénea'
            }
    
    def solve_exact(self, M_str, N_str):
        """
        Resuelve ecuaciones exactas: M(x,y)dx + N(x,y)dy = 0
        Verifica si ∂M/∂y = ∂N/∂x
        """
        try:
            x, y = self.x, symbols('y')
            
            M_str = M_str.replace('y', 'y').replace('x', 'x')
            N_str = N_str.replace('y', 'y').replace('x', 'x')
            
            local_symbols = {'x': x, 'y': y, 'E': sp.E, 'e': sp.E, 'pi': sp.pi, 'PI': sp.pi, 'exp': sp.exp}
            M = self._parse(M_str, local_dict=local_symbols)
            N = self._parse(N_str, local_dict=local_symbols)
            
            # Verificar si es exacta
            dM_dy = diff(M, y)
            dN_dx = diff(N, x)
            
            is_exact = simplify(dM_dy - dN_dx) == 0
            
            if is_exact:
                # Encontrar la función potencial F(x,y)
                F = integrate(M, x)
                # Agregar términos que dependen solo de y
                g_y = integrate(N - diff(F, y), y)
                F = F + g_y
                
                solution = f"F(x,y) = {F} = C"
                
                return {
                    'success': True,
                    'solution': solution,
                    'method': 'Ecuación Exacta',
                    'is_exact': True
                }
            else:
                return {
                    'success': False,
                    'error': f'La ecuación no es exacta. ∂M/∂y = {dM_dy}, ∂N/∂x = {dN_dx}',
                    'method': 'Ecuación Exacta',
                    'is_exact': False,
                    'dM_dy': str(dM_dy),
                    'dN_dx': str(dN_dx)
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Ecuación Exacta'
            }
    
    def solve_linear(self, equation_str, initial_conditions=None):
        """
        Resuelve ecuaciones lineales: dy/dx + P(x)y = Q(x)
        """
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            
            if '=' in eq_str:
                parts = eq_str.split('=')
                lhs = self._parse(parts[0])
                rhs = self._parse(parts[1])
                eq = Eq(lhs, rhs)
            else:
                eq = self._parse(eq_str)
            
            solution = self._dsolve(eq, y, initial_conditions)
            
            # Simplificar la solución
            if isinstance(solution, list):
                solution = solution[0]
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Ecuación Lineal'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Ecuación Lineal'
            }
    
    def solve_bernoulli(self, equation_str, n=None, initial_conditions=None):
        """
        Resuelve ecuaciones de Bernoulli: dy/dx + P(x)y = Q(x)y^n
        """
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            
            if '=' in eq_str:
                parts = eq_str.split('=')
                lhs = self._parse(parts[0])
                rhs = self._parse(parts[1])
                eq = Eq(lhs, rhs)
            else:
                eq = self._parse(eq_str)
            
            solution = self._dsolve(eq, y, initial_conditions)
            
            # Simplificar la solución
            if isinstance(solution, list):
                solution = solution[0]
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Ecuación de Bernoulli'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Ecuación de Bernoulli'
            }
    
    def find_integrating_factor(self, M_str, N_str):
        """
        Encuentra factor integrante para ecuaciones no exactas
        """
        try:
            x, y = self.x, symbols('y')
            
            local_dict = {'x': x, 'y': y, 'E': sp.E, 'e': sp.E, 'pi': sp.pi, 'PI': sp.pi, 'exp': sp.exp}
            M = self._parse(M_str, local_dict=local_dict)
            N = self._parse(N_str, local_dict=local_dict)
            
            dM_dy = diff(M, y)
            dN_dx = diff(N, x)
            
            # Intentar factor integrante que depende solo de x
            try:
                factor_x = (dM_dy - dN_dx) / N
                factor_x_simplified = simplify(factor_x)
                
                if not factor_x_simplified.has(y):
                    mu = exp(integrate(factor_x_simplified, x))
                    mu_str = str(mu)
                    return {
                        'success': True,
                        'factor': mu_str,
                        'type': 'μ(x)',
                        'method': 'Factor Integrante',
                        'solution': f"μ(x) = {mu_str}",
                        'solution_formatted': f"μ(x) = {mu_str}",
                        'solution_latex': f"\\mu(x) = {latex(mu)}"
                    }
            except:
                pass
            
            # Intentar factor integrante que depende solo de y
            try:
                factor_y = (dN_dx - dM_dy) / M
                factor_y_simplified = simplify(factor_y)
                
                if not factor_y_simplified.has(x):
                    mu = exp(integrate(factor_y_simplified, y))
                    mu_str = str(mu)
                    return {
                        'success': True,
                        'factor': mu_str,
                        'type': 'μ(y)',
                        'method': 'Factor Integrante',
                        'solution': f"μ(y) = {mu_str}",
                        'solution_formatted': f"μ(y) = {mu_str}",
                        'solution_latex': f"\\mu(y) = {latex(mu)}"
                    }
            except:
                pass
            
            return {
                'success': False,
                'error': 'No se encontró un factor integrante simple',
                'method': 'Factor Integrante'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Factor Integrante'
            }
    
    def solve_general(self, equation_str, initial_conditions=None):
        """
        Intenta resolver la ecuación con el método general de SymPy
        """
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            
            if '=' in eq_str:
                parts = eq_str.split('=')
                lhs = self._parse(parts[0])
                rhs = self._parse(parts[1])
                eq = Eq(lhs, rhs)
            else:
                eq = self._parse(eq_str)
            
            special_solution = self._solve_special_cases(eq)
            if special_solution:
                return special_solution
            
            solution = self._dsolve(eq, y, initial_conditions)
            
            # Obtener el tipo de ecuación
            hints = sp.classify_ode(eq, y)
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Método General',
                'hints': hints
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Método General'
            }
    
    def solve_second_order_constant_coeff(self, equation_str, initial_conditions=None):
        """
        Resuelve ecuaciones lineales de segundo orden con coeficientes constantes
        ay'' + by' + cy = 0 o ay'' + by' + cy = g(x)
        """
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            
            if '=' in eq_str:
                parts = eq_str.split('=')
                lhs = self._parse(parts[0])
                rhs = self._parse(parts[1])
                eq = Eq(lhs, rhs)
            else:
                eq = self._parse(eq_str)
            
            solution = dsolve(eq, y)
            
            # Obtener coeficientes para ecuación característica
            hints = sp.classify_ode(eq, y)
            is_homogeneous = 'nth_linear_constant_coeff_homogeneous' in hints
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Ecuación de Segundo Orden con Coeficientes Constantes',
                'is_homogeneous': is_homogeneous
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Ecuación de Segundo Orden con Coeficientes Constantes'
            }
    
    def solve_reducible_to_first_order(self, equation_str, case_type='general', initial_conditions=None):
        """
        Resuelve ecuaciones reducibles a primer orden
        Casos: y'' = f(x), y'' = f(y'), y'' = f(y, y')
        """
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            
            if '=' in eq_str:
                parts = eq_str.split('=')
                lhs = self._parse(parts[0])
                rhs = self._parse(parts[1])
                eq = Eq(lhs, rhs)
            else:
                eq = self._parse(eq_str)
            
            solution = dsolve(eq, y)
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Ecuación Reducible a Primer Orden'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Ecuación Reducible a Primer Orden'
            }
    
    def _solve_special_cases(self, eq):
        """Intenta resolver casos especiales no cubiertos por SymPy"""
        handlers = (
            self._solve_case_y_times_ypp_plus_yp_sq,
        )
        for handler in handlers:
            result = handler(eq)
            if result:
                return result
        return None

    def _solve_case_y_times_ypp_plus_yp_sq(self, eq):
        y = self.y(self.x)
        if isinstance(eq, sp.Equality):
            expr = sp.simplify(eq.lhs - eq.rhs)
        else:
            expr = sp.simplify(eq)
        target = sp.simplify(sp.diff(y * diff(y, self.x), self.x))
        if sp.simplify(expr - target) == 0:
            solution_eq = Eq(y**2, self.C1 * self.x + self.C2)
            return {
                'success': True,
                'solution': str(solution_eq),
                'solution_formatted': self.format_solution(solution_eq),
                'solution_latex': self.get_latex_solution(solution_eq),
                'method': "Caso especial: y·y'' + (y')² = 0"
            }
        return None
