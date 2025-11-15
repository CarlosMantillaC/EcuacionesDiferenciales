"""
Interfaz gráfica para el solucionador de ecuaciones diferenciales
Usando CustomTkinter para un diseño moderno
"""

import customtkinter as ctk
from tkinter import messagebox
from ode_solver import ODESolver


# Configuración de apariencia
ctk.set_appearance_mode("dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"


class ODESolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de Ecuaciones Diferenciales")
        self.root.geometry("1100x800")
        
        self.solver = ODESolver()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Título
        title_label = ctk.CTkLabel(
            self.root,
            text="🔬 Solucionador de Ecuaciones Diferenciales Ordinarias",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame principal con scrollbar
        main_frame = ctk.CTkScrollableFrame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Selector de método
        method_frame = ctk.CTkFrame(main_frame)
        method_frame.pack(fill='x', pady=(0, 15), padx=10)
        
        method_title = ctk.CTkLabel(
            method_frame,
            text="📐 Seleccionar Método de Resolución",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        method_title.pack(pady=(15, 10))
        
        self.method_var = ctk.StringVar(value='general')
        
        # Separador visual
        separator1 = ctk.CTkLabel(
            method_frame,
            text="━━━ ECUACIONES DE PRIMER ORDEN ━━━",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray50", "gray70")
        )
        separator1.pack(pady=(5, 10))
        
        methods_first_order = [
            ('🤖 Método General (Automático)', 'general'),
            ('📊 Variables Separables', 'separable'),
            ('🔄 Ecuaciones Homogéneas', 'homogeneous'),
            ('✓ Ecuaciones Exactas', 'exact'),
            ('📈 Ecuaciones Lineales', 'linear'),
            ('🎯 Ecuaciones de Bernoulli', 'bernoulli'),
            ('⚙️ Factores Integrantes', 'integrating_factor')
        ]
        
        # Crear grid de radio buttons para primer orden
        radio_container1 = ctk.CTkFrame(method_frame, fg_color="transparent")
        radio_container1.pack(pady=(0, 15), padx=20)
        
        for i, (text, value) in enumerate(methods_first_order):
            rb = ctk.CTkRadioButton(
                radio_container1,
                text=text,
                variable=self.method_var,
                value=value,
                font=ctk.CTkFont(size=13),
                command=self.on_method_change
            )
            rb.grid(row=i//2, column=i%2, sticky='w', padx=15, pady=8)
        
        # Separador para segundo orden
        separator2 = ctk.CTkLabel(
            method_frame,
            text="━━━ ECUACIONES DE SEGUNDO ORDEN ━━━",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray50", "gray70")
        )
        separator2.pack(pady=(10, 10))
        
        methods_second_order = [
            ('🔢 Coeficientes Constantes', 'second_order_const'),
            ('🔄 Reducible a Primer Orden', 'reducible'),
            ('📐 Variación de Parámetros', 'variation_params')
        ]
        
        radio_container2 = ctk.CTkFrame(method_frame, fg_color="transparent")
        radio_container2.pack(pady=(0, 15), padx=20)
        
        for i, (text, value) in enumerate(methods_second_order):
            rb = ctk.CTkRadioButton(
                radio_container2,
                text=text,
                variable=self.method_var,
                value=value,
                font=ctk.CTkFont(size=13),
                command=self.on_method_change
            )
            rb.grid(row=i//2, column=i%2, sticky='w', padx=15, pady=8)
        
        # Frame de entrada
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill='x', pady=(0, 15), padx=10)
        
        input_title = ctk.CTkLabel(
            input_frame,
            text="✏️ Entrada de Ecuación",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        input_title.pack(pady=(15, 10))
        
        # Container para inputs
        input_container = ctk.CTkFrame(input_frame, fg_color="transparent")
        input_container.pack(pady=(0, 15), padx=20, fill='x')
        
        # Entrada principal
        self.equation_label = ctk.CTkLabel(
            input_container,
            text="Ecuación (ej: dy/dx = x*y, y' = x + y):",
            font=ctk.CTkFont(size=13)
        )
        self.equation_label.pack(anchor='w', pady=(5, 2))
        
        self.equation_entry = ctk.CTkEntry(
            input_container,
            font=ctk.CTkFont(size=14),
            height=40,
            placeholder_text="Ingrese su ecuación aquí..."
        )
        self.equation_entry.pack(fill='x', pady=(0, 10))
        
        # Entradas para ecuaciones exactas (M y N) - inicialmente ocultas
        self.m_label = ctk.CTkLabel(
            input_container,
            text="M(x,y) (coeficiente de dx):",
            font=ctk.CTkFont(size=13)
        )
        
        self.m_entry = ctk.CTkEntry(
            input_container,
            font=ctk.CTkFont(size=14),
            height=40,
            placeholder_text="Ej: 2*x*y"
        )
        
        self.n_label = ctk.CTkLabel(
            input_container,
            text="N(x,y) (coeficiente de dy):",
            font=ctk.CTkFont(size=13)
        )
        
        self.n_entry = ctk.CTkEntry(
            input_container,
            font=ctk.CTkFont(size=14),
            height=40,
            placeholder_text="Ej: x**2 + 1"
        )
        
        # Frame de ejemplos
        examples_frame = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray20"))
        examples_frame.pack(fill='x', pady=(0, 15), padx=10)
        
        examples_title = ctk.CTkLabel(
            examples_frame,
            text="💡 Ejemplos de Ecuaciones",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        examples_title.pack(pady=(10, 5))
        
        examples_text = """PRIMER ORDEN:
📊 Variables Separables: dy/dx = x*y  |  y' = x/y
🔄 Homogéneas: dy/dx = (x+y)/x  |  y' = y/x + x/y
✓ Exactas: M(x,y) = 2*x*y, N(x,y) = x**2 + 1
📈 Lineales: dy/dx + y = x  |  y' + 2*x*y = x**2
🎯 Bernoulli: dy/dx + y = x*y**2  |  y' - y = x*y**3
⚙️ Factores Integrantes: M(x,y) = 3*x**2 + y, N(x,y) = x**2*y - x

SEGUNDO ORDEN:
🔢 Coef. Constantes: y'' - 3*y' + 2*y = 0  |  y'' + y = x
🔄 Reducible: y'' = x  |  y'' = y'**2
📐 Variación: y'' + y = sec(x)"""
        
        examples_label = ctk.CTkLabel(
            examples_frame,
            text=examples_text,
            font=ctk.CTkFont(size=12),
            justify='left'
        )
        examples_label.pack(pady=(5, 10), padx=20)
        
        # Botones
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill='x', pady=15, padx=10)
        
        button_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_container.pack()
        
        solve_button = ctk.CTkButton(
            button_container,
            text="🚀 Resolver Ecuación",
            command=self.solve_equation,
            font=ctk.CTkFont(size=15, weight="bold"),
            height=45,
            width=200,
            fg_color="#27ae60",
            hover_color="#229954"
        )
        solve_button.pack(side='left', padx=10)
        
        clear_button = ctk.CTkButton(
            button_container,
            text="🗑️ Limpiar",
            command=self.clear_all,
            font=ctk.CTkFont(size=15, weight="bold"),
            height=45,
            width=150,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        clear_button.pack(side='left', padx=10)
        
        # Área de resultados
        result_frame = ctk.CTkFrame(main_frame)
        result_frame.pack(fill='both', expand=True, pady=(0, 15), padx=10)
        
        result_title = ctk.CTkLabel(
            result_frame,
            text="📋 Solución",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        result_title.pack(pady=(15, 10))
        
        self.result_text = ctk.CTkTextbox(
            result_frame,
            font=ctk.CTkFont(family="Consolas", size=13),
            wrap='word',
            height=300
        )
        self.result_text.pack(fill='both', expand=True, padx=20, pady=(0, 15))
    
    def on_method_change(self):
        """Actualiza la interfaz según el método seleccionado"""
        method = self.method_var.get()
        
        # Ocultar todos los campos adicionales
        self.m_label.pack_forget()
        self.m_entry.pack_forget()
        self.n_label.pack_forget()
        self.n_entry.pack_forget()
        
        if method in ['exact', 'integrating_factor']:
            # Mostrar campos M y N
            self.equation_label.configure(text="Ecuación en forma M(x,y)dx + N(x,y)dy = 0")
            self.equation_entry.pack_forget()
            
            self.m_label.pack(anchor='w', pady=(5, 2))
            self.m_entry.pack(fill='x', pady=(0, 10))
            self.n_label.pack(anchor='w', pady=(5, 2))
            self.n_entry.pack(fill='x', pady=(0, 10))
        else:
            # Mostrar campo de ecuación normal
            if method in ['second_order_const', 'reducible', 'variation_params']:
                self.equation_label.configure(text="Ecuación de Segundo Orden (ej: y'' - 3*y' + 2*y = 0):")
            else:
                self.equation_label.configure(text="Ecuación (ej: dy/dx = x*y, y' = x + y):")
            self.equation_entry.pack(fill='x', pady=(0, 10))
    
    def solve_equation(self):
        """Resuelve la ecuación según el método seleccionado"""
        method = self.method_var.get()
        
        self.result_text.delete("1.0", "end")
        
        try:
            if method in ['exact', 'integrating_factor']:
                M_str = self.m_entry.get().strip()
                N_str = self.n_entry.get().strip()
                
                if not M_str or not N_str:
                    messagebox.showerror("Error", "Por favor ingrese M(x,y) y N(x,y)")
                    return
                
                if method == 'exact':
                    result = self.solver.solve_exact(M_str, N_str)
                else:
                    result = self.solver.find_integrating_factor(M_str, N_str)
            else:
                equation = self.equation_entry.get().strip()
                
                if not equation:
                    messagebox.showerror("Error", "Por favor ingrese una ecuación")
                    return
                
                if method == 'general':
                    result = self.solver.solve_general(equation)
                elif method == 'separable':
                    result = self.solver.solve_separable(equation)
                elif method == 'homogeneous':
                    result = self.solver.solve_homogeneous(equation)
                elif method == 'linear':
                    result = self.solver.solve_linear(equation)
                elif method == 'bernoulli':
                    result = self.solver.solve_bernoulli(equation)
                elif method == 'second_order_const':
                    result = self.solver.solve_second_order_constant_coeff(equation)
                elif method == 'reducible':
                    result = self.solver.solve_reducible_to_first_order(equation)
                elif method == 'variation_params':
                    result = self.solver.solve_variation_of_parameters(equation)
            
            self.display_result(result)
            
        except Exception as e:
            self.result_text.insert("end", "❌ ERROR\n\n")
            self.result_text.insert("end", f"{str(e)}\n")
    
    def display_result(self, result):
        """Muestra el resultado en el área de texto"""
        self.result_text.insert("end", f"📌 MÉTODO: {result['method']}\n")
        self.result_text.insert("end", "="*80 + "\n\n")
        
        if result['success']:
            self.result_text.insert("end", "✅ SOLUCIÓN ENCONTRADA\n\n")
            
            if 'solution' in result:
                # Mostrar solución formateada si está disponible
                if 'solution_formatted' in result:
                    self.result_text.insert("end", "📊 Solución:\n")
                    self.result_text.insert("end", f"   {result['solution_formatted']}\n\n")
                    
                    # Mostrar también en LaTeX
                    if 'solution_latex' in result:
                        self.result_text.insert("end", "📐 LaTeX:\n")
                        self.result_text.insert("end", f"   {result['solution_latex']}\n\n")
                    
                    # Mostrar formato original
                    self.result_text.insert("end", "🔤 Formato SymPy:\n")
                    self.result_text.insert("end", f"   {result['solution']}\n\n")
                else:
                    self.result_text.insert("end", "📊 Solución:\n")
                    self.result_text.insert("end", f"   {result['solution']}\n\n")
            
            if 'factor' in result:
                self.result_text.insert("end", "⚙️ Factor Integrante:\n")
                self.result_text.insert("end", f"   {result['type']} = {result['factor']}\n\n")
            
            if 'steps' in result:
                self.result_text.insert("end", "📝 Pasos:\n")
                self.result_text.insert("end", f"{result['steps']}\n\n")
            
            if 'hints' in result:
                self.result_text.insert("end", "🔍 Clasificación:\n")
                for hint in result['hints'][:5]:  # Mostrar primeros 5 hints
                    self.result_text.insert("end", f"  • {hint}\n")
            
            if 'is_exact' in result and result['is_exact']:
                self.result_text.insert("end", "\n✅ La ecuación es EXACTA\n")
        else:
            self.result_text.insert("end", "❌ NO SE PUDO RESOLVER\n\n")
            self.result_text.insert("end", f"Error: {result['error']}\n\n")
            
            if 'is_exact' in result and not result['is_exact']:
                self.result_text.insert("end", "⚠️ La ecuación NO es exacta.\n")
                self.result_text.insert("end", "💡 Intente usar el método de Factores Integrantes.\n")
            
            if 'dM_dy' in result:
                self.result_text.insert("end", f"\n∂M/∂y = {result['dM_dy']}\n")
                self.result_text.insert("end", f"∂N/∂x = {result['dN_dx']}\n")
    
    def clear_all(self):
        """Limpia todos los campos"""
        self.equation_entry.delete(0, "end")
        self.m_entry.delete(0, "end")
        self.n_entry.delete(0, "end")
        self.system_text.delete("1.0", "end")
        self.vars_entry.delete(0, "end")
        self.result_text.delete("1.0", "end")


def main():
    root = ctk.CTk()
    app = ODESolverGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
