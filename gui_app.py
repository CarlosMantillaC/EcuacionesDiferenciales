"""
Interfaz gráfica para el solucionador de ecuaciones diferenciales
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from ode_solver import ODESolver


class ODESolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de Ecuaciones Diferenciales")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        self.solver = ODESolver()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Título
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="Solucionador de Ecuaciones Diferenciales Ordinarias",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Selector de método
        method_frame = tk.LabelFrame(
            main_frame,
            text="Seleccionar Método",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        method_frame.pack(fill='x', pady=(0, 10))
        
        self.method_var = tk.StringVar(value='general')
        
        methods = [
            ('Método General (Automático)', 'general'),
            ('Variables Separables', 'separable'),
            ('Ecuaciones Homogéneas', 'homogeneous'),
            ('Ecuaciones Exactas', 'exact'),
            ('Ecuaciones Lineales', 'linear'),
            ('Ecuaciones de Bernoulli', 'bernoulli'),
            ('Factores Integrantes', 'integrating_factor')
        ]
        
        for i, (text, value) in enumerate(methods):
            rb = tk.Radiobutton(
                method_frame,
                text=text,
                variable=self.method_var,
                value=value,
                font=('Arial', 10),
                bg='#f0f0f0',
                command=self.on_method_change
            )
            rb.grid(row=i//2, column=i%2, sticky='w', padx=10, pady=5)
        
        # Frame de entrada
        input_frame = tk.LabelFrame(
            main_frame,
            text="Entrada de Ecuación",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Entrada principal
        self.equation_label = tk.Label(
            input_frame,
            text="Ecuación (ej: dy/dx = x*y, y' = x + y):",
            font=('Arial', 10),
            bg='#f0f0f0'
        )
        self.equation_label.grid(row=0, column=0, sticky='w', pady=5)
        
        self.equation_entry = tk.Entry(input_frame, font=('Arial', 11), width=60)
        self.equation_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Entradas para ecuaciones exactas (M y N)
        self.m_label = tk.Label(
            input_frame,
            text="M(x,y) (coeficiente de dx):",
            font=('Arial', 10),
            bg='#f0f0f0'
        )
        
        self.m_entry = tk.Entry(input_frame, font=('Arial', 11), width=60)
        
        self.n_label = tk.Label(
            input_frame,
            text="N(x,y) (coeficiente de dy):",
            font=('Arial', 10),
            bg='#f0f0f0'
        )
        
        self.n_entry = tk.Entry(input_frame, font=('Arial', 11), width=60)
        
        # Frame de ejemplos
        examples_frame = tk.LabelFrame(
            main_frame,
            text="Ejemplos",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=5
        )
        examples_frame.pack(fill='x', pady=(0, 10))
        
        examples_text = """
• Variables Separables: dy/dx = x*y  |  y' = x/y
• Homogéneas: dy/dx = (x+y)/x  |  y' = y/x + x/y
• Exactas: M(x,y) = 2*x*y, N(x,y) = x**2 + 1
• Lineales: dy/dx + y = x  |  y' + 2*x*y = x**2
• Bernoulli: dy/dx + y = x*y**2  |  y' - y = x*y**3
• Factores Integrantes: M(x,y) = 3*x**2 + y, N(x,y) = x**2*y - x
        """
        
        examples_label = tk.Label(
            examples_frame,
            text=examples_text,
            font=('Arial', 9),
            bg='#f0f0f0',
            justify='left'
        )
        examples_label.pack()
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=10)
        
        solve_button = tk.Button(
            button_frame,
            text="Resolver",
            command=self.solve_equation,
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2'
        )
        solve_button.pack(side='left', padx=5)
        
        clear_button = tk.Button(
            button_frame,
            text="Limpiar",
            command=self.clear_all,
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2'
        )
        clear_button.pack(side='left', padx=5)
        
        # Área de resultados
        result_frame = tk.LabelFrame(
            main_frame,
            text="Solución",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        result_frame.pack(fill='both', expand=True)
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            font=('Courier', 11),
            wrap=tk.WORD,
            height=15,
            bg='#ffffff'
        )
        self.result_text.pack(fill='both', expand=True)
        
        # Configurar tags para formato
        self.result_text.tag_config('title', font=('Arial', 12, 'bold'), foreground='#2c3e50')
        self.result_text.tag_config('success', foreground='#27ae60', font=('Arial', 11, 'bold'))
        self.result_text.tag_config('error', foreground='#e74c3c', font=('Arial', 11, 'bold'))
        self.result_text.tag_config('info', foreground='#3498db')
    
    def on_method_change(self):
        """Actualiza la interfaz según el método seleccionado"""
        method = self.method_var.get()
        
        # Ocultar todos los campos adicionales
        self.m_label.grid_forget()
        self.m_entry.grid_forget()
        self.n_label.grid_forget()
        self.n_entry.grid_forget()
        
        if method in ['exact', 'integrating_factor']:
            # Mostrar campos M y N
            self.equation_label.config(text="Ecuación en forma M(x,y)dx + N(x,y)dy = 0")
            self.equation_entry.grid_forget()
            
            self.m_label.grid(row=0, column=0, sticky='w', pady=5)
            self.m_entry.grid(row=0, column=1, padx=10, pady=5)
            self.n_label.grid(row=1, column=0, sticky='w', pady=5)
            self.n_entry.grid(row=1, column=1, padx=10, pady=5)
        else:
            # Mostrar campo de ecuación normal
            self.equation_label.config(text="Ecuación (ej: dy/dx = x*y, y' = x + y):")
            self.equation_entry.grid(row=0, column=1, padx=10, pady=5)
    
    def solve_equation(self):
        """Resuelve la ecuación según el método seleccionado"""
        method = self.method_var.get()
        
        self.result_text.delete(1.0, tk.END)
        
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
            
            self.display_result(result)
            
        except Exception as e:
            self.result_text.insert(tk.END, "ERROR\n", 'error')
            self.result_text.insert(tk.END, f"\n{str(e)}\n")
    
    def display_result(self, result):
        """Muestra el resultado en el área de texto"""
        self.result_text.insert(tk.END, f"MÉTODO: {result['method']}\n", 'title')
        self.result_text.insert(tk.END, "="*80 + "\n\n")
        
        if result['success']:
            self.result_text.insert(tk.END, "✓ SOLUCIÓN ENCONTRADA\n\n", 'success')
            
            if 'solution' in result:
                # Mostrar solución formateada si está disponible
                if 'solution_formatted' in result:
                    self.result_text.insert(tk.END, "Solución:\n", 'info')
                    self.result_text.insert(tk.END, f"{result['solution_formatted']}\n\n", 'title')
                    
                    # Mostrar también en LaTeX
                    if 'solution_latex' in result:
                        self.result_text.insert(tk.END, "LaTeX:\n", 'info')
                        self.result_text.insert(tk.END, f"{result['solution_latex']}\n\n")
                    
                    # Mostrar formato original (colapsado)
                    self.result_text.insert(tk.END, "Formato SymPy:\n", 'info')
                    self.result_text.insert(tk.END, f"{result['solution']}\n\n")
                else:
                    self.result_text.insert(tk.END, "Solución:\n", 'info')
                    self.result_text.insert(tk.END, f"{result['solution']}\n\n")
            
            if 'factor' in result:
                self.result_text.insert(tk.END, "Factor Integrante:\n", 'info')
                self.result_text.insert(tk.END, f"{result['type']} = {result['factor']}\n\n")
            
            if 'steps' in result:
                self.result_text.insert(tk.END, "Pasos:\n", 'info')
                self.result_text.insert(tk.END, f"{result['steps']}\n\n")
            
            if 'hints' in result:
                self.result_text.insert(tk.END, "Clasificación:\n", 'info')
                for hint in result['hints'][:5]:  # Mostrar primeros 5 hints
                    self.result_text.insert(tk.END, f"  • {hint}\n")
            
            if 'is_exact' in result and result['is_exact']:
                self.result_text.insert(tk.END, "\n✓ La ecuación es EXACTA\n", 'success')
        else:
            self.result_text.insert(tk.END, "✗ NO SE PUDO RESOLVER\n\n", 'error')
            self.result_text.insert(tk.END, f"Error: {result['error']}\n\n")
            
            if 'is_exact' in result and not result['is_exact']:
                self.result_text.insert(tk.END, "La ecuación NO es exacta.\n", 'error')
                self.result_text.insert(tk.END, "Intente usar el método de Factores Integrantes.\n")
            
            if 'dM_dy' in result:
                self.result_text.insert(tk.END, f"\n∂M/∂y = {result['dM_dy']}\n")
                self.result_text.insert(tk.END, f"∂N/∂x = {result['dN_dx']}\n")
    
    def clear_all(self):
        """Limpia todos los campos"""
        self.equation_entry.delete(0, tk.END)
        self.m_entry.delete(0, tk.END)
        self.n_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)


def main():
    root = tk.Tk()
    app = ODESolverGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
