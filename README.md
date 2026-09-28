# Trabajo Práctico Integrador I
## Fundamentos Teóricos de la Informática

**Conversión de AFND a AFD y Minimización de Autómatas Finitos**

| | |
|---|---|
| **Materia** | Fundamentos Teóricos de la Informática |
| **Integrantes** | Agustin Gigliotti Farias · Moises Kutnich |
| **Docentes** | Ing. Leonardo Moreno · Lic. Pablo Toledo |
| **Fecha de Entrega** | 28 de septiembre de 2026 |

---

## ¿Qué hace este programa?

Este proyecto implementa en Python un sistema completo que toma un autómata no determinista (AFND), lo convierte a su versión determinista equivalente (AFD) y luego lo reduce al mínimo posible sin cambiar el lenguaje que reconoce.

El programa hace 3 cosas en orden:

1. **Convierte el AFND a AFD** usando el Algoritmo de Construcción de Subconjuntos con clausura lambda (λ).
2. **Minimiza el AFD** eliminando estados inalcanzables y fusionando estados equivalentes con el Algoritmo de Refinamiento de Particiones.
3. **Valida la equivalencia** probando cadenas de prueba y verificando que el AFND original y el AFD mínimo aceptan exactamente las mismas palabras.

---

## Estructura del proyecto

```
Trabajo_Practico_Integrador_I_FTI/
│
├── modelo.py          # Clase Automata: definición, clausura_lambda y evaluación de cadenas
├── conversor.py       # Algoritmo de Construcción de Subconjuntos (AFND → AFD)
├── minimizador.py     # Algoritmo de Refinamiento de Particiones (AFD → AFD Mínimo)
├── io_handler.py      # Lectura/escritura JSON y TXT, tablas ASCII y gráfico con Matplotlib
├── main.py            # Punto de entrada principal, orquesta el flujo completo
├── ejemplos/
├── requirements.txt   # Dependencias del proyecto
├── entrada.json       # Archivo de entrada por defecto
└── README.md
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone git@github.com:agusgigliottifarias/Trabajo_Pr-ctico_Integrador_I_FTI.git
cd Trabajo_Pr-ctico_Integrador_I_FTI
```

### 2. Activar el entorno virtual

```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```
## Dependencias

| Librería | Uso |
|---|---|
| `matplotlib` | Renderizado gráfico del autómata en ventana emergente (solo Linux) |
| `networkx` | Construcción del grafo de estados y transiciones |

Instalables con:
```bash
pip install -r requirements.txt
```

---

## Visualización de los autómatas

**En Linux:** El programa abre automáticamente una ventana gráfica con el diagrama del autómata al finalizar cada ejecución.

**En Windows (WSL):** La ventana gráfica no funciona en WSL porque no tiene acceso al sistema de ventanas de Windows por defecto (no tiene servidor gráfico X11 configurado). En ese caso, para evitar andar instalando dependencias fuera del proyecto, el programa igual genera el archivo `resultado_minimo.json` al terminar, que puede importarse directamente en **[AutomataLab](https://www.automataaa.com/)** para visualizar el diagrama del autómata.

---

## Cómo ejecutarlo

### Con un ejemplo incluido
```bash
python3 main.py ejemplos/ejemplo1_afnd_con_epsilon.json
python3 main.py ejemplos/ejemplo2_afd_con_redundantes.json
python3 main.py ejemplos/ejemplo3_afnd_multiples_caminos.json
python3 main.py ejemplos/ejemplo4_afd_inalcanzables.json
python3 main.py ejemplos/ejemplo5_afd_paridad.json
```

### Con tu propio archivo
```bash
python3 main.py ruta/tu_automata.json
```

> El archivo debe estar en formato JSON compatible con AutomataLab.

---

## Archivos de salida

Cada ejecución genera automáticamente en la raíz del proyecto:

| Archivo | Descripción |
|---|---|
| `resultado_minimo.json` | AFD Mínimo en formato JSON compatible con AutomataLab |
| `resultado_minimo.txt` | AFD Mínimo en formato de texto plano |

---

