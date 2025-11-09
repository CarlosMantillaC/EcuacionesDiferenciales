"""
Módulo para resolver ecuaciones diferenciales ordinarias de primer orden
Soporta: Variables separables, Homogéneas, Exactas, Lineales, Bernoulli, Factores integrantes
"""

import sympy as sp
from sympy import symbols, Function, Eq, dsolve, diff, integrate, simplify, exp, log, sqrt
from sympy.parsing.sympy_parser import parse_expr
import re


class ODESolver:
    def __init__(self):
        self.x = symbols('x')
        self.y = Function('y')
        self.C1, self.C2 = symbols('C1 C2')
    
    def parse_equation(self, equation_str):
        """
        Parsea una ecuación diferencial en formato string
        Formatos aceptados:
        - dy/dx = f(x,y)
        - y' = f(x,y)
        - M(x,y) + N(x,y)*dy/dx = 0
        """
        equation_str = equation_str.replace(' ', '')
        # Primero reemplazar dy/dx y y' antes de reemplazar y
        equation_str = equation_str.replace('dy/dx', "Derivative(y(x), x)")
        equation_str = equation_str.replace("y'", "Derivative(y(x), x)")
        # Reemplazar y solo cuando no es parte de Derivative
        import re
        # Reemplazar y que no esté seguido de (x) y no esté dentro de Derivative
        equation_str = re.sub(r'\by\b(?!\()', 'y(x)', equation_str)
        
        return equation_str
    
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
                lhs = parse_expr(parts[0], local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
                rhs = parse_expr(parts[1], local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
                eq = Eq(lhs, rhs)
            else:
                eq = parse_expr(eq_str, local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
            
            solution = dsolve(eq, y, hint='separable')
            return {
                'success': True,
                'solution': str(solution),
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
                lhs = parse_expr(parts[0], local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
                rhs = parse_expr(parts[1], local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
                eq = Eq(lhs, rhs)
            else:
                eq = parse_expr(eq_str, local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
            
            solution = dsolve(eq, y, hint='1st_homogeneous_coeff_best')
            return {
                'success': True,
                'solution': str(solution),
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
            
            M = parse_expr(M_str, local_dict={'x': x, 'y': y})
            N = parse_expr(N_str, local_dict={'x': x, 'y': y})
            
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
                lhs = parse_expr(parts[0], local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
                rhs = parse_expr(parts[1], local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
                eq = Eq(lhs, rhs)
            else:
                eq = parse_expr(eq_str, local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
            
            solution = dsolve(eq, y, hint='1st_linear')
            return {
                'success': True,
                'solution': str(solution),
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
                lhs = parse_expr(parts[0], local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
                rhs = parse_expr(parts[1], local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
                eq = Eq(lhs, rhs)
            else:
                eq = parse_expr(eq_str, local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
            
            solution = dsolve(eq, y, hint='Bernoulli')
            return {
                'success': True,
                'solution': str(solution),
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
            
            M = parse_expr(M_str, local_dict={'x': x, 'y': y})
            N = parse_expr(N_str, local_dict={'x': x, 'y': y})
            
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
                lhs = parse_expr(parts[0], local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
                rhs = parse_expr(parts[1], local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
                eq = Eq(lhs, rhs)
            else:
                eq = parse_expr(eq_str, local_dict={'x': self.x, 'y': self.y, 'Derivative': sp.Derivative})
            
            solution = dsolve(eq, y)
            
            # Obtener el tipo de ecuación
            hints = sp.classify_ode(eq, y)
            
            return {
                'success': True,
                'solution': str(solution),
                'method': 'Método General',
                'hints': hints
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Método General'
            }
    
    def _get_separable_steps(self, eq):
        """Genera pasos para ecuaciones separables"""
        return "1. Separar variables: g(y)dy = f(x)dx\n2. Integrar ambos lados\n3. Resolver para y"
