# 🔬 Solucionador de Ecuaciones Diferenciales Ordinarias

Aplicación completa en Python para resolver ecuaciones diferenciales ordinarias (EDOs) de primer y segundo orden, así como sistemas de ecuaciones lineales.

## ✨ Características

### 📊 Ecuaciones de Primer Orden

- **Variables Separables**: `dy/dx = f(x)g(y)`
- **Ecuaciones Homogéneas**: `dy/dx = f(y/x)`
- **Ecuaciones Exactas**: `M(x,y)dx + N(x,y)dy = 0`
- **Ecuaciones Lineales**: `dy/dx + P(x)y = Q(x)`
- **Ecuaciones de Bernoulli**: `dy/dx + P(x)y = Q(x)y^n`
- **Factores Integrantes**: Para ecuaciones no exactas
- **Método General**: Detección automática del tipo de ecuación

### 🔢 Ecuaciones de Segundo Orden

- **Coeficientes Constantes**: `ay'' + by' + cy = 0` y `ay'' + by' + cy = g(x)`
  - Raíces reales distintas
  - Raíz doble
  - Raíces complejas conjugadas
- **Ecuación de Cauchy-Euler**: `ax²y'' + bxy' + cy = 0`
- **Reducibles a Primer Orden**: 
  - `y'' = f(x)`
  - `y'' = f(y')`
  - `y'' = f(y, y')`
- **Variación de Parámetros**: Para ecuaciones no homogéneas

### 🔗 Sistemas de Ecuaciones

- **Método Matricial**: Solución de sistemas lineales `X' = AX`
  - Valores propios reales distintos
  - Valores propios repetidos
  - Valores propios complejos

## 🚀 Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/CarlosMantillaC/EcuacionesDiferenciales.git
cd EcuacionesDiferenciales
```

2. **Crear entorno virtual** (recomendado):
```bash
python -m venv .venv
```

3. **Activar entorno virtual**:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

## 📖 Uso

### Interfaz Gráfica (Recomendado)

```bash
python gui_app.py
```

La interfaz incluye:
- 🎨 Diseño moderno con CustomTkinter (tema oscuro/claro)
- 📐 Selector de métodos organizado por categorías
- ✏️ Entrada intuitiva de ecuaciones
- 💡 Ejemplos integrados
- 📋 Resultados con múltiples formatos (legible, LaTeX, SymPy)
- 📝 Pasos de resolución detallados

### Ejemplos desde Terminal

**Ejemplos de primer orden:**
```bash
python ejemplos.py
```

**Ejemplos de segundo orden y sistemas:**
```bash
python ejemplos_segundo_orden.py
```

### Uso Programático

```python
from ode_solver import ODESolver

solver = ODESolver()

# Ejemplo 1: Ecuación de primer orden
result = solver.solve_general("dy/dx = x*y")
print(result['solution_formatted'])

# Ejemplo 2: Ecuación de segundo orden
result = solver.solve_second_order_constant_coeff("y'' - 3*y' + 2*y = 0")
print(result['solution_formatted'])

# Ejemplo 3: Sistema de ecuaciones
equations = ["x' = x + 2*y", "y' = 3*x + 2*y"]
result = solver.solve_linear_system(equations, "x,y")
print(result['solution_formatted'])
```

## 📝 Ejemplos de Ecuaciones

### Primer Orden

```python
# Variables Separables
"dy/dx = x*y"

# Ecuación Homogénea
"dy/dx = (x+y)/x"

# Ecuación Exacta
M = "2*x*y"
N = "x**2 + 1"

# Ecuación Lineal
"dy/dx + y = x"

# Ecuación de Bernoulli
"dy/dx + y = x*y**2"
```

### Segundo Orden

```python
# Coeficientes constantes homogénea
"y'' - 3*y' + 2*y = 0"

# Coeficientes constantes no homogénea
"y'' + y = x"

# Cauchy-Euler
"x**2*y'' + x*y' - y = 0"

# Reducible a primer orden
"y'' = x"

# Raíces complejas
"y'' + 4*y = 0"

# Raíz doble
"y'' - 2*y' + y = 0"
```

### Sistemas

```python
# Sistema 2x2
equations = [
    "x' = x + 2*y",
    "y' = 3*x + 2*y"
]
variables = "x,y"

# Sistema con otras variables
equations = [
    "f' = -f + g",
    "g' = 2*f - 2*g"
]
variables = "f,g"
```

## 🔧 Tecnologías Utilizadas

- **Python 3.13+**
- **SymPy 1.12**: Álgebra simbólica y resolución de EDOs
- **CustomTkinter 5.2.2**: Interfaz gráfica moderna

## 📂 Estructura del Proyecto

```
EcuacionesDiferenciales/
├── ode_solver.py                 # Módulo principal con todos los métodos
├── gui_app.py                    # Interfaz gráfica con CustomTkinter
├── ejemplos.py                   # Ejemplos de primer orden
├── ejemplos_segundo_orden.py     # Ejemplos de segundo orden y sistemas
├── requirements.txt              # Dependencias del proyecto
├── test_formato.py               # Tests de formato
├── test_homogenea.py            # Tests de ecuaciones homogéneas
├── main.py                       # Punto de entrada (placeholder)
└── README.md                     # Este archivo
```

## 🎯 Características de la GUI

### Diseño Moderno
- ✅ Tema oscuro/claro configurable
- ✅ Scroll automático para contenido largo
- ✅ Botones con efectos hover
- ✅ Iconos emoji para navegación visual
- ✅ Ventana responsive (1100x800px)

### Funcionalidades
- 📐 **14 métodos de resolución** organizados en 3 categorías
- ✏️ **Entrada dinámica** según el método seleccionado
- 💡 **Ejemplos contextuales** para cada tipo de ecuación
- 📋 **Múltiples formatos de salida**:
  - Formato legible con símbolos matemáticos
  - Formato LaTeX para documentos
  - Formato SymPy original
- 📝 **Pasos de resolución** detallados
- 🔍 **Clasificación automática** de ecuaciones

## 🧪 Tests

El proyecto incluye archivos de prueba para validar la funcionalidad:

```bash
# Test de formatos de salida
python test_formato.py

# Test de ecuaciones homogéneas
python test_homogenea.py
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 👨‍💻 Autor

**CarlosMantillaC**

## 🙏 Agradecimientos

- **SymPy**: Por la increíble biblioteca de álgebra simbólica
- **CustomTkinter**: Por la hermosa interfaz gráfica moderna
- Comunidad de Python por las herramientas y soporte

## 📚 Referencias

- [SymPy Documentation](https://docs.sympy.org/)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- Ecuaciones Diferenciales Ordinarias - Teoría y aplicaciones

---

⭐ Si te ha sido útil este proyecto, ¡considera darle una estrella en GitHub!
