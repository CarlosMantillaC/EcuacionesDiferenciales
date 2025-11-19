# 🔬 Solucionador de Ecuaciones Diferenciales Ordinarias

Aplicación completa en Python para resolver ecuaciones diferenciales ordinarias (EDOs) de primer y segundo orden.

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
- **Reducibles a Primer Orden**: 
  - `y'' = f(x)`
  - `y'' = f(y')`
  - `y'' = f(y, y')`
- **Variación de Parámetros**: Para ecuaciones no homogéneas

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
- 📋 Resultado formato LaTeX
- 📝 Pasos de resolución detallados
- 🎯 Condiciones iniciales opcionales para obtener soluciones particulares

### Cómo ingresar condiciones iniciales en la GUI

1. Selecciona cualquier método diferente de **Exactas** o **Factor integrante**.
2. Escribe la ecuación usando `x` como variable y `y` como función (por ejemplo `4*y'' + 4*y' + 17*y = 0`).
3. Completa, si quieres una solución particular, los campos `x0`, `y(x0)` y `y'(x0)`.
   - Puedes dejar en blanco `y(x0)` o `y'(x0)` si solo conoces uno de los dos.
4. Pulsa **Resolver** para ver la solución simbólica y su representación en LaTeX.

### Ejemplos desde Terminal

**Ejemplos de primer orden:**
```bash
python ejemplos.py
```

**Ejemplos de segundo orden:**
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

# Ejemplo 3: Solución particular con condiciones iniciales
ics = {"x0": 0, "y0": -1, "yp0": 2}
result = solver.solve_second_order_constant_coeff("4*y'' + 4*y' + 17*y = 0", initial_conditions=ics)
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

# Reducible a primer orden
"y'' = x"

# Raíces complejas
"y'' + 4*y = 0"

# Raíz doble
"y'' - 2*y' + y = 0"
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
- 📐 **10 métodos de resolución** organizados en 2 categorías
- ✏️ **Entrada dinámica** según el método seleccionado
- 💡 **Ejemplos contextuales** para cada tipo de ecuación
- 🎯 **Condiciones iniciales opcionales** (campos para \(x_0, y(x_0), y'(x_0)\)) para obtener soluciones particulares sin salir de la GUI
- 📋 **Formato de salida** (LaTeX renderizado como imagen con tamaño adaptativo)
- 📝 **Pasos de resolución** detallados
- 🔍 **Clasificación automática** de ecuaciones y manejo de casos especiales (p. ej. \(y\,y'' + (y')^2 = 0\))

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
