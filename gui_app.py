"""
Interfaz gráfica para el solucionador de ecuaciones diferenciales
Usando CustomTkinter para un diseño moderno
"""

import io

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
        self.latex_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Título
        title_label = ctk.CTkLabel(
            self.root,
            text="🔬 Solucionador de Ecuaciones Diferenciales",
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
            ('🔄 Reducible a Primer Orden', 'reducible')
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
        
        # Condiciones iniciales (opcional)
        self.ic_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        self.ic_frame.pack(fill='x', pady=(5, 5))
        ic_title = ctk.CTkLabel(
            self.ic_frame,
            text="Condiciones iniciales (opcional)",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        ic_title.grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 5))
        
        self.x0_entry = ctk.CTkEntry(
            self.ic_frame,
            width=120,
            placeholder_text="x0"
        )
        self.x0_entry.grid(row=1, column=0, padx=5, pady=5, sticky='we')
        self.y0_entry = ctk.CTkEntry(
            self.ic_frame,
            width=120,
            placeholder_text="y(x0)"
        )
        self.y0_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        self.yp0_entry = ctk.CTkEntry(
            self.ic_frame,
            width=120,
            placeholder_text="y'(x0)"
        )
        self.yp0_entry.grid(row=1, column=2, padx=5, pady=5, sticky='we')
        
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
🔄 Reducible: y'' = x  |  y'' = y'**2"""
        
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
        
        # Título y contenedor para solución en LaTeX
        self.solution_title = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.solution_title.pack(pady=(10, 0))
        
        self.latex_image_label = ctk.CTkLabel(main_frame, text="")
        self.latex_image_label.pack(pady=(5, 15))
        self.latex_image_label.pack_forget()
    
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
            self.ic_frame.pack_forget()
            
            self.m_label.pack(anchor='w', pady=(5, 2))
            self.m_entry.pack(fill='x', pady=(0, 10))
            self.n_label.pack(anchor='w', pady=(5, 2))
            self.n_entry.pack(fill='x', pady=(0, 10))
        else:
            # Mostrar campo de ecuación normal
            if method in ['second_order_const', 'reducible']:
                self.equation_label.configure(text="Ecuación de Segundo Orden (ej: y'' - 3*y' + 2*y = 0):")
            else:
                self.equation_label.configure(text="Ecuación (ej: dy/dx = x*y, y' = x + y):")
            self.equation_entry.pack(fill='x', pady=(0, 10))
            if not self.ic_frame.winfo_ismapped():
                self.ic_frame.pack(fill='x', pady=(5, 5))
    
    def solve_equation(self):
        """Resuelve la ecuación según el método seleccionado"""
        method = self.method_var.get()
        
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
                
                try:
                    initial_conditions = self._get_initial_conditions()
                except ValueError as ic_error:
                    messagebox.showerror("Error", str(ic_error))
                    return
                
                if method == 'general':
                    result = self.solver.solve_general(equation, initial_conditions=initial_conditions)
                elif method == 'separable':
                    result = self.solver.solve_separable(equation, initial_conditions=initial_conditions)
                elif method == 'homogeneous':
                    result = self.solver.solve_homogeneous(equation, initial_conditions=initial_conditions)
                elif method == 'linear':
                    result = self.solver.solve_linear(equation, initial_conditions=initial_conditions)
                elif method == 'bernoulli':
                    result = self.solver.solve_bernoulli(equation, initial_conditions=initial_conditions)
                elif method == 'second_order_const':
                    result = self.solver.solve_second_order_constant_coeff(equation, initial_conditions=initial_conditions)
                elif method == 'reducible':
                    result = self.solver.solve_reducible_to_first_order(equation, initial_conditions=initial_conditions)
            
            self._show_latex_solution(result)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _show_latex_solution(self, result):
        if not result.get('success'):
            messagebox.showerror("Error", result.get('error', 'No se pudo resolver la ecuación'))
            self.solution_title.configure(text="")
            self._clear_latex_image()
            return
        latex_text = result.get('solution_latex') or result.get('solution')
        if not latex_text:
            latex_text = 'No se encontró una solución.'
        self.solution_title.configure(text="📐 Solución en LaTeX")
        self._display_latex_image(latex_text)

    def _display_latex_image(self, latex_str):
        image = self._render_latex_image(latex_str)
        if image:
            self.latex_image_label.configure(image=image, text="")
            self.latex_image_label.image = image  # Evitar recolección de basura
            self.latex_image = image
            self.latex_image_label.pack(pady=(5, 15))
        else:
            self._clear_latex_image()

    def _clear_latex_image(self):
        self.latex_image_label.configure(image=None, text="")
        self.latex_image_label.image = None
        self.latex_image = None
        self.latex_image_label.pack_forget()

    def _render_latex_image(self, latex_str):
        try:
            buffer = io.BytesIO()
            text_len = max(len(latex_str), 1)
            width = min(max(text_len * 0.12, 3), 8)
            fig = plt.figure(figsize=(width, 1.3), dpi=200)
            fig.patch.set_facecolor('none')
            ax = fig.add_subplot(111)
            ax.axis('off')
            ax.text(
                0.5,
                0.5,
                f"${latex_str}$",
                fontsize=18,
                ha='center',
                va='center',
                color='white'
            )
            fig.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.15, transparent=True)
            plt.close(fig)
            buffer.seek(0)
            image = Image.open(buffer).convert('RGBA')
            return ImageTk.PhotoImage(image)
        except Exception:
            return None

    def clear_all(self):
        """Limpia todos los campos"""
        self.equation_entry.delete(0, "end")
        self.m_entry.delete(0, "end")
        self.n_entry.delete(0, "end")
        self.x0_entry.delete(0, "end")
        self.y0_entry.delete(0, "end")
        self.yp0_entry.delete(0, "end")
        self.solution_title.configure(text="")
        self._clear_latex_image()

    def _get_initial_conditions(self):
        x0 = self.x0_entry.get().strip()
        y0 = self.y0_entry.get().strip()
        yp0 = self.yp0_entry.get().strip()
        if not any([x0, y0, yp0]):
            return None
        if not x0:
            raise ValueError("Ingrese x0 para aplicar condiciones iniciales")
        ic_dict = {'x0': x0}
        if y0:
            ic_dict['y0'] = y0
        if yp0:
            ic_dict['yp0'] = yp0
        return ic_dict


def main():
    root = ctk.CTk()
    app = ODESolverGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
