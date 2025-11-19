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
    
    def solve_separable(self, equation_str):
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
            
            solution = dsolve(eq, y)
            
            # Simplificar la solución
            if isinstance(solution, list):
                solution = solution[0]
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Variables Separables',
                'steps': self._get_separable_steps(eq)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Variables Separables'
            }
    
    def solve_homogeneous(self, equation_str):
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
            
            # Intentar sin hint específico para mejor resultado
            solution = dsolve(eq, y)
            
            # Simplificar la solución
            if isinstance(solution, list):
                solution = solution[0]
            
            solution_simplified = simplify(solution)
            
            return {
                'success': True,
                'solution': str(solution_simplified),
                'solution_formatted': self.format_solution(solution_simplified),
                'solution_latex': self.get_latex_solution(solution_simplified),
                'method': 'Ecuación Homogénea',
                'steps': 'Sustitución: v = y/x, entonces y = vx y dy/dx = v + x(dv/dx)'
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
                    'is_exact': True,
                    'steps': f'∂M/∂y = {dM_dy}\n∂N/∂x = {dN_dx}\nLa ecuación es exacta.'
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
    
    def solve_linear(self, equation_str):
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
            
            solution = dsolve(eq, y)
            
            # Simplificar la solución
            if isinstance(solution, list):
                solution = solution[0]
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Ecuación Lineal',
                'steps': 'Forma estándar: dy/dx + P(x)y = Q(x)\nFactor integrante: μ(x) = e^(∫P(x)dx)'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Ecuación Lineal'
            }
    
    def solve_bernoulli(self, equation_str, n=None):
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
            
            solution = dsolve(eq, y)
            
            # Simplificar la solución
            if isinstance(solution, list):
                solution = solution[0]
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Ecuación de Bernoulli',
                'steps': f'Forma: dy/dx + P(x)y = Q(x)y^n\nSustitución: v = y^(1-n), transforma en ecuación lineal'
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
                    return {
                        'success': True,
                        'factor': str(mu),
                        'type': 'μ(x)',
                        'method': 'Factor Integrante'
                    }
            except:
                pass
            
            # Intentar factor integrante que depende solo de y
            try:
                factor_y = (dN_dx - dM_dy) / M
                factor_y_simplified = simplify(factor_y)
                
                if not factor_y_simplified.has(x):
                    mu = exp(integrate(factor_y_simplified, y))
                    return {
                        'success': True,
                        'factor': str(mu),
                        'type': 'μ(y)',
                        'method': 'Factor Integrante'
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
    
    def solve_general(self, equation_str):
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
            
            solution = dsolve(eq, y)
            
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
    
    def solve_second_order_constant_coeff(self, equation_str):
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
            
            steps = self._get_second_order_steps(eq, is_homogeneous)
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Ecuación de Segundo Orden con Coeficientes Constantes',
                'steps': steps,
                'is_homogeneous': is_homogeneous
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Ecuación de Segundo Orden con Coeficientes Constantes'
            }
    
    def solve_reducible_to_first_order(self, equation_str, case_type='general'):
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
            
            steps_dict = {
                'f_x': 'Caso: y\'\' = f(x)\nSolución: Integrar dos veces\ny\' = ∫f(x)dx + C₁\ny = ∫(∫f(x)dx)dx + C₁x + C₂',
                'f_yp': 'Caso: y\'\' = f(y\')\nSustitución: p = y\', entonces y\'\' = dp/dx\nSe reduce a: dp/dx = f(p)',
                'f_y_yp': 'Caso: y\'\' = f(y, y\')\nSustitución: p = y\', entonces y\'\' = p(dp/dy)\nSe reduce a ecuación de primer orden en p',
                'general': 'Ecuación reducible a primer orden mediante sustitución apropiada'
            }
            
            steps = steps_dict.get(case_type, steps_dict['general'])
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Ecuación Reducible a Primer Orden',
                'steps': steps
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Ecuación Reducible a Primer Orden'
            }
    
    def solve_variation_of_parameters(self, equation_str):
        """
        Resuelve ecuaciones no homogéneas usando variación de parámetros
        ay'' + by' + cy = g(x)
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
            
            steps = """Método de Variación de Parámetros:
1. Resolver ecuación homogénea: ay'' + by' + cy = 0 → y_h
2. Encontrar soluciones fundamentales y₁, y₂
3. Calcular Wronskiano: W = y₁y₂' - y₁'y₂
4. Solución particular: y_p = -y₁∫(y₂g/W)dx + y₂∫(y₁g/W)dx
5. Solución general: y = y_h + y_p"""
            
            return {
                'success': True,
                'solution': str(solution),
                'solution_formatted': self.format_solution(solution),
                'solution_latex': self.get_latex_solution(solution),
                'method': 'Variación de Parámetros',
                'steps': steps
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Variación de Parámetros'
            }
    
    
    def _get_second_order_steps(self, eq, is_homogeneous):
        """Genera pasos para ecuaciones de segundo orden con coeficientes constantes"""
        if is_homogeneous:
            return """Ecuación homogénea: ay'' + by' + cy = 0
1. Ecuación característica: ar² + br + c = 0
2. Resolver para r (raíces r₁, r₂)
3. Casos:
   • Raíces reales distintas: y = C₁e^(r₁x) + C₂e^(r₂x)
   • Raíz doble r: y = (C₁ + C₂x)e^(rx)
   • Raíces complejas α±βi: y = e^(αx)(C₁cos(βx) + C₂sin(βx))"""
        else:
            return """Ecuación no homogénea: ay'' + by' + cy = g(x)
1. Solución homogénea: y_h (resolver ay'' + by' + cy = 0)
2. Solución particular: y_p (usando coeficientes indeterminados o variación de parámetros)
3. Solución general: y = y_h + y_p"""
    
    def _get_separable_steps(self, eq):
        """Genera pasos para ecuaciones separables"""
        return "1. Separar variables: g(y)dy = f(x)dx\n2. Integrar ambos lados\n3. Resolver para y"

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
            steps = (
                "1. Observa que d/dx[y·y'] = y·y'' + (y')^2\n"
                "2. Integra una vez: y·y' = C₁\n"
                "3. Integra nuevamente: y^2 = C₁x + C₂"
            )
            return {
                'success': True,
                'solution': str(solution_eq),
                'solution_formatted': self.format_solution(solution_eq),
                'solution_latex': self.get_latex_solution(solution_eq),
                'method': "Caso especial: y·y'' + (y')² = 0",
                'steps': steps
            }
        return None
