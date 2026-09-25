# Trabajo Práctico Integrador I - Fundamentos de Teoría de la Computación / Informática

Este proyecto implementa en Python un sistema completo para el procesamiento, conversión y minimización de Autómatas Finitos.

## 📌 Funcionalidades Principales

1. **Eliminación de No Determinismo (AFND $\rightarrow$ AFD):** Convierte cualquier Autómata Finito No Determinista (con o sin transiciones $\epsilon$ / nulas) a su Autómata Finito Determinista equivalente utilizando el **Algoritmo de Construcción de Subconjuntos**.
2. **Minimización de Autómatas (AFD $\rightarrow$ AFD Mínimo):** Elimina estados inalcanzables y aplica el **Algoritmo de Refinamiento de Particiones** (equivalencia de Moore/Hopcroft) para obtener el autómata mínimo equivalente.
3. **Soporte I/O Multiformato:** Carga y exporta autómatas en archivos **JSON** y **Texto Plano**.
4. **Visualización y Reportes:** 
   * Muestra tablas de transiciones formateadas en la terminal.
   * Genera gráficos vectoriales en formato **Graphviz (`.dot`)**.
   * Abre ventanas emergentes interactivas con los autómatas dibujados en pantalla.
5. **Validación de Cadenas:** Prueba y demuestra formalmente que $L(AFND) = L(AFD_{min})$.

---

## 🛠️ Instalación y Configuración del Entorno (`.venv`)

### 1. Clonar o Descargar el Proyecto
Navega hasta la carpeta del proyecto en tu terminal:

```bash
git clone git@github.com:agusgigliottifarias/Trabajo_Pr-ctico_Integrador_I_FTI.git
```

### 2. Activar el Entorno Virtual (`.venv`)

* **En Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```
* **En Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

### 3. Instalar las Dependencias
Con el entorno virtual activado, instala todos los paquetes necesarios:

```bash
.venv/bin/pip install -r requirements.txt`
```


---

## 🚀 Uso y Ejecución

### 1. Ejecución con el archivo por defecto (`entrada.json`)

```bash
.venv/bin/python main.py
```

### 2. Ejecución pasando un archivo de la carpeta `ejemplos/`

Puedes probar cualquiera de los 5 casos de prueba incluidos en la carpeta `ejemplos/`:

```bash
# Ejemplo 1: AFND con transiciones Épsilon (#)
.venv/bin/python main.py ejemplos/ejemplo1_afnd_con_epsilon.json

# Ejemplo 2: AFD con estados equivalentes redundantes
.venv/bin/python main.py ejemplos/ejemplo2_afd_con_redundantes.json

# Ejemplo 3: AFND con múltiples caminos de transición
.venv/bin/python main.py ejemplos/ejemplo3_afnd_multiples_caminos.json

# Ejemplo 4: AFD con estados inalcanzables desde el inicio
.venv/bin/python main.py ejemplos/ejemplo4_afd_inalcanzables.json

# Ejemplo 5: AFD de paridad de ceros
.venv/bin/python main.py ejemplos/ejemplo5_afd_paridad.json
```

---

## 🧪 Ejecución de Pruebas Unitarias Automated

Para verificar el correcto funcionamiento de los algoritmos mediante la suite de tests automáticos (`unittest`):

```bash
.venv/bin/python -m unittest test_automata.py
```

---

## 📁 Estructura del Código

* 📄 `modelo.py`: Clase base `Automata` (transiciones, clausura $\epsilon$, función `mover`, evaluación de cadenas).
* 📄 `conversor.py`: Lógica de conversión AFND $\rightarrow$ AFD (`afnd_a_afd`).
* 📄 `minimizador.py`: Algoritmo de minimización de estados (`minimizar_afd`).
* 📄 `io_handler.py`: Módulo de E/S para cargar y guardar en JSON/Texto, generar tablas ASCII y gráficos DOT/ventanas.
* 📄 `main.py`: Punto de entrada y orquestador principal.
* 📄 `test_automata.py`: Suite de pruebas unitarias automáticas.
* 📂 `ejemplos/`: Carpeta con 5 archivos JSON de prueba.
* 📄 `requirements.txt`: Lista de dependencias del proyecto.

---

## 📤 Resultados de Salida

Cada ejecución genera automáticamente los siguientes archivos de salida en la raíz:
* `resultado_minimo.json`: El autómata determinista mínimo resultante en formato JSON.
* `resultado_minimo.txt`: El autómata mínimo en formato de texto plano.
* `grafico_afnd.dot`, `grafico_afd.dot`, `grafico_minimo.dot`: Código fuente Graphviz para incluir gráficos en el informe técnico.