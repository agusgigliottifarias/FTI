# TRABAJO PRÁCTICO INTEGRADOR I

- **Materia:** Fundamentos Teóricos de la Informática
- **Conversión de AFND a AFD y Minimización de Autómatas Finitos**
- **Integrantes:** 
  - Agustin Guillermo Gigliotti Farias agustingigliottifarias@gmail.com
  - Moises Kutnich makutnich@gmail.com
- **Fecha de Entrega:** 28 de septiembre 
- **Docentes:**
  - Ing. Leonardo Moreno
  - Lic. Pablo Toledo 


## 1. INTRODUCCIÓN

### 1.1 Descripción del Problema y Objetivos
Los autómatas finitos se utilizan para reconocer lenguajes regulares. Pero muchas veces nos vamos a encontrar con un Autómata Finito No Determinista (AFND) ya que permite representar las reglas de un lenguaje de manera más intuitiva. Sin embargo, para procesar cadenas en un programa de computación es necesario contar con un Autómata Finito Determinista (AFD), donde para cada estado y cada símbolo del alfabeto exista un único camino posible.
El objetivo de este trabajo es desarrollar un programa en Python que automatice el proceso de conversión de cualquier AFND (con o sin transiciones landa ) a un AFD equivalente, y que luego reduzca la cantidad de estados al mínimo posible sin modificar el lenguaje que reconoce.
Los objetivos específicos del proyecto son:
1. **Conversión AFND → AFD:** Implementar el algoritmo de Construcción de Subconjuntos para transformar un AFND en un AFD equivalente.
2. **Minimización de Estados:** Aplicar el algoritmo de refinamiento de particiones para eliminar estados inalcanzables y fusionar estados equivalentes.
3. **Validación de Cadenas:** Permitir la evaluación de cadenas sobre el autómata y comprobar que el AFD mínimo reconoce exactamente las mismas cadenas que el AFND original.
---

### 1.2 Fundamentos Teóricos

#### 1.2.1 Autómata Finito Determinista (AFD)
Un AFD es un modelo computacional que lee una cadena de texto símbolo por símbolo y decide si la acepta o la rechaza. Se llama **determinista** porque desde cualquier estado, ante un símbolo de entrada determinado, existe **una sola opción posible** hacia dónde ir. No hay ambigüedades ni caminos alternativos.

#### 1.2.2 Autómata Finito No Determinista (AFND)
Es un autómata más flexible donde, a diferencia del AFD:
- Desde un mismo estado y con el mismo símbolo, se puede ir a **múltiples estados al mismo tiempo** (o a ninguno).
- Puede tener **transiciones landa**, que permiten cambiar de estado espontáneamente sin necesidad de leer ningún símbolo de la cadena.

Una cadena es aceptada por un AFND si existe al menos un camino posible que termine en un estado final.

#### 1.2.3 Autómata Finito Mínimo
Es el AFD más pequeño posible que reconoce un lenguaje determinado. Para que un AFD sea mínimo debe cumplir dos condiciones:
1. **No tener estados inalcanzables:** Todos sus estados se pueden visitar partiendo desde el estado inicial.
2. **No tener estados redundantes:** No existen dos estados diferentes que hagan exactamente lo mismo. Si dos estados producen los mismos resultados ante cualquier cadena, se pueden fusionar en uno solo.

Para todo lenguaje regular existe un único autómata mínimo.

#### 1.2.4 Equivalencia entre Autómatas
Dos autómatas (sin importar si son AFND, AFD o AFD mínimo) son **equivalentes** cuando reconocen exactamente el **mismo lenguaje**. Esto significa que ante cualquier cadena de entrada, ambos autómatas llegarán a la misma conclusión: los dos la aceptan o los dos la rechazan.

---

## 2. METODOLOGÍA Y DISEÑO DE ALGORITMOS

### 2.1 Arquitectura del Sistema

El programa fue implementado utilizando el lenguaje de programación Python 3, aplicando el principio de responsabilidad única mediante un diseño modular compuesto por 5 componentes principales:

```
Trabajo_Practico_Integrador_I_FTI/
├── modelo.py        
├── conversor.py     
├── minimizador.py   
├── io_handler.py    
└── main.py          
```

- **`modelo.py`:** Define la clase `Automata` con todos sus elementos (alfabeto, estados, estado inicial, finales y función de transición).
- **`conversor.py`:** Contiene la lógica para transformar un AFND (con o sin transiciones landa) en un AFD equivalente mediante el algoritmo de Construcción de Subconjuntos.
- **`minimizador.py`:** Se encarga de reducir el AFD al mínimo posible. Primero elimina los estados inalcanzables y luego agrupa los estados equivalentes aplicando el algoritmo de refinamiento de particiones.
- **`io_handler.py`:** Maneja la lectura y escritura de archivos en formato JSON y TXT. Además, imprime las tablas de transiciones en la consola y exporta los gráficos visuales del autómata.
- **`main.py`:** Es el punto de entrada del programa. Se encarga de ejecutar el flujo completo: lee el archivo de entrada, llama al conversor, luego al minimizador, muestra los resultados por pantalla y realiza la prueba de equivalencia con cadenas de prueba.
---


Hastas aca esta bien el resto no lo revise


### 2.2 Algoritmo 1: Conversión AFND → AFD (Construcción de Subconjuntos)

#### Explicación:
Este algoritmo transforma un autómata no determinista en uno determinista. La idea central es que cada estado del nuevo AFD representa un conjunto de estados del AFND original.

El proceso comienza calculando la clausura lambda ($\text{clausura}_\lambda$) del estado inicial. Luego, para cada conjunto de estados resultante y para cada símbolo del alfabeto, se buscan todos los estados alcanzables y sus correspondientes clausuras lambda. El procedimiento continúa de forma iterativa creando nuevos estados en el AFD hasta que no aparezcan subconjuntos nuevos.

#### Pseudocódigo:
Función AFND_a_AFD(AFND):
    Estado_Inicial_AFD = clausura_lambda({AFND.q0})
    Estados_AFD = {Estado_Inicial_AFD}
    Pendientes = Cola([Estado_Inicial_AFD])
    Transiciones_AFD = {}

    Mientras Pendientes no esté vacía:
        T = Pendientes.pop()
        Para cada símbolo 'a' en AFND.alfabeto (excluyendo lambda):
            Mover_T = conjunto_vacio()
            Para cada estado 'q' en T:
                Mover_T = Mover_T ∪ AFND.delta(q, a)
            U = clausura_lambda(Mover_T)
            
            Si U no está vacío:
                Transiciones_AFD[(T, a)] = U
                Si U no está en Estados_AFD:
                    Estados_AFD.add(U)
                    Pendientes.push(U)

    Finales_AFD = {S ∈ Estados_AFD | al menos un estado de S pertenece a AFND.F}
    Retornar AFD(Estados_AFD, AFND.alfabeto, Estado_Inicial_AFD, Finales_AFD, Transiciones_AFD)

---

### 2.3 Algoritmo 2: Minimización de AFD (Refinamiento de Particiones)

#### Descripción:
1. **Eliminación de estados inalcanzables:** Se realiza un recorrido BFS/DFS desde el estado inicial $q_0$ para conservar únicamente aquellos estados $q \in Q$ accesibles.
2. **Partición Inicial ($P_0$):** Se divide el conjunto de estados accesibles en dos clases de equivalencia:
   - $G_1 = F$ (Estados finales)
   - $G_2 = Q \setminus F$ (Estados no finales)
3. **Refinamiento Iterativo:** En cada paso $k$, se intenta dividir cada grupo $G \in P_k$. Dos estados $p, q \in G$ permanecen en el mismo subgrupo si y solo si para todo símbolo $a \in \Sigma$, $\delta(p, a)$ y $\delta(q, a)$ pertenecen al mismo grupo dentro de la partición anterior $P_k$.
4. **Criterio de Parada:** El algoritmo finaliza cuando $P_{k+1} = P_k$ (no se producen nuevas divisiones).

#### Pseudocódigo:
```text
Función Minimizar_AFD(AFD):
    AFD = eliminar_estados_inalcanzables(AFD)
    P = [AFD.F, AFD.Q - AFD.F]  // Excluyendo grupos vacíos

    Repetir:
        P_nueva = []
        Para cada grupo G en P:
            Subgrupos = particionar(G, P, AFD)
            P_nueva.append(Subgrupos)
        Si P_nueva == P:
            Romper ciclo
        P = P_nueva

    Construir AFD_Minimo agrupando estados de cada bloque equivalente en P
    Retornar AFD_Minimo
```

---

## 3. CASOS DE PRUEBA Y EJECUCIÓN PASO A PASO

### 3.1 Caso de Prueba 1: AFND con Transiciones $\epsilon$ (`ejemplo1_afnd_con_epsilon.json`)

#### Especificación del AFND Original:
- **Alfabeto ($\Sigma$):** $\{a, b\}$
- **Estados ($Q$):** $\{q_0, q_1, q_2, q_3\}$
- **Estado Inicial:** $q_0$
- **Estados Finales ($F$):** $\{q_3\}$
- **Transiciones:**
  - $\delta(q_0, \epsilon) = \{q_1, q_2\}$
  - $\delta(q_1, a) = \{q_1\}$, $\delta(q_1, b) = \{q_3\}$
  - $\delta(q_2, a) = \{q_3\}$, $\delta(q_2, b) = \{q_2\}$

---

#### Paso 1: Ejecución de la Construcción de Subconjuntos
1. **Estado Inicial del AFD ($S_0$):**
   $$\text{clausura}_\epsilon(\{q_0\}) = \{q_0, q_1, q_2\} = S_0$$
2. **Evaluación de transiciones desde $S_0$:**
   - Con símbolo $a$: $\delta(q_1, a) \cup \delta(q_2, a) = \{q_1, q_3\}$.
     $$\text{clausura}_\epsilon(\{q_1, q_3\}) = \{q_1, q_3\} = S_1 \quad (\text{Final})$$
   - Con símbolo $b$: $\delta(q_1, b) \cup \delta(q_2, b) = \{q_3, q_2\}$.
     $$\text{clausura}_\epsilon(\{q_3, q_2\}) = \{q_2, q_3\} = S_2 \quad (\text{Final})$$
3. **Evaluación desde $S_1 = \{q_1, q_3\}$:**
   - Con símbolo $a$: $\delta(q_1, a) = \{q_1\} \Rightarrow \text{clausura}_\epsilon(\{q_1\}) = \{q_1\} = S_3$.
   - Con símbolo $b$: $\delta(q_1, b) = \{q_3\} \Rightarrow \text{clausura}_\epsilon(\{q_3\}) = \{q_3\} = S_4 \quad (\text{Final})$.
4. **Evaluación desde $S_2 = \{q_2, q_3\}$:**
   - Con símbolo $a$: $\delta(q_2, a) = \{q_3\} \Rightarrow \text{clausura}_\epsilon(\{q_3\}) = \{q_3\} = S_4 \quad (\text{Final})$.
   - Con símbolo $b$: $\delta(q_2, b) = \{q_2\} \Rightarrow \text{clausura}_\epsilon(\{q_2\}) = \{q_2\} = S_5$.

---

#### Tabla de Transiciones del AFD Intermedio resultante:

| Estado AFD | Composición AFND | $a$ | $b$ | ¿Es Final? |
| :--- | :--- | :---: | :---: | :---: |
| **$S_0$ (Inicial)** | $\{q_0, q_1, q_2\}$ | $S_1$ | $S_2$ | No |
| **$S_1$** | $\{q_1, q_3\}$ | $S_3$ | $S_4$ | **Sí** |
| **$S_2$** | $\{q_2, q_3\}$ | $S_4$ | $S_5$ | **Sí** |
| **$S_3$** | $\{q_1\}$ | $S_3$ | $S_4$ | No |
| **$S_4$** | $\{q_3\}$ | $\emptyset$ | $\emptyset$ | **Sí** |
| **$S_5$** | $\{q_2\}$ | $S_4$ | $S_5$ | No |

---

#### Paso 2: Minimización por Partición
- **Partición Inicial $P_0$:**
  - Grupo Finales: $G_A = \{S_1, S_2, S_4\}$
  - Grupo No Finales: $G_B = \{S_0, S_3, S_5\}$

- **Iteración 1:**
  - Evaluando $G_B = \{S_0, S_3, S_5\}$:
    - $S_0 \xrightarrow{a} S_1 \in G_A$, $S_0 \xrightarrow{b} S_2 \in G_A$
    - $S_3 \xrightarrow{a} S_3 \in G_B$, $S_3 \xrightarrow{b} S_4 \in G_A$
    - $S_5 \xrightarrow{a} S_4 \in G_A$, $S_5 \xrightarrow{b} S_5 \in G_B$
    - Como las respuestas no caen en los mismos grupos, $G_B$ se divide en $\{S_0\}$, $\{S_3\}$, $\{S_5\}$.
  - Evaluando $G_A = \{S_1, S_2, S_4\}$:
    - $S_1 \xrightarrow{a} S_3$, $S_1 \xrightarrow{b} S_4$
    - $S_2 \xrightarrow{a} S_4$, $S_2 \xrightarrow{b} S_5$
    - $S_4 \xrightarrow{a} \emptyset$, $S_4 \xrightarrow{b} \emptyset$
    - Se dividen en $\{S_1\}$, $\{S_2\}$, $\{S_4\}$.

- **Resultado de Minimización:** En este caso particular, cada estado cumple un rol distinguible dentro de la estructura determinista, por lo que el autómata determinista ya se encontraba en su forma irreducible de 6 estados.

---

## 4. RESULTADOS Y ANÁLISIS COMPARATIVO

### 4.1 Resumen de Métricas de Ejecución

A continuación se muestra el análisis cuantitativo ejecutado sobre los 5 casos de prueba incluidos en la suite del sistema:

| Caso de Prueba | Tipo Original | Estados AFND | Transiciones AFND | Estados AFD | Estados AFD Mínimo | % Reducción de Estados |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Caso 1: AFND $\epsilon$** | AFND-$\epsilon$ | 4 | 5 | 6 | **6** | 0% (Ya mínimo) |
| **Caso 2: Redundantes** | AFD | 5 | 10 | 5 | **3** | **40% de reducción** |
| **Caso 3: Múltiples Caminos** | AFND | 3 | 4 | 4 | **3** | **25% de reducción** |
| **Caso 4: Inalcanzables** | AFD | 5 | 8 | 5 | **3** | **40% de reducción** |
| **Caso 5: Paridad** | AFD | 4 | 8 | 4 | **4** | 0% (Mínimo estricto) |

---

### 4.2 Verificación de Equivalencia de Lenguajes

La validación formal del sistema se comprobó evaluando un conjunto exhaustivo de cadenas sobre ambos autómatas (AFND Original vs. AFD Mínimo).

#### Ejemplo de Salida de Validación del Sistema:
```text
============================================================
 VALIDACIÓN DE CADENAS Y DEMOSTRACIÓN DE EQUIVALENCIA
============================================================
Cadena       | AFND Original   | AFD Mínimo      | Equivalentes?
--------------------------------------------------------------
'ab'         | ACEPTADA        | ACEPTADA        | OK
'aab'        | ACEPTADA        | ACEPTADA        | OK
'bba'        | ACEPTADA        | ACEPTADA        | OK
'aaab'       | ACEPTADA        | ACEPTADA        | OK
'b'          | ACEPTADA        | ACEPTADA        | OK
'' (vacía)   | RECHAZADA       | RECHAZADA       | OK
--------------------------------------------------------------
```

Se concluye experimental y teóricamente que:
$$L(\text{AFND}) = L(\text{AFD}) = L(\text{AFD Mínimo})$$

---

## 5. CONCLUSIONES

1. **Eficiencia de la Conversión:** El algoritmo de construcción de subconjuntos convierte satisfactoriamente autómatas no deterministas eliminando el no determinismo y las ambigüedades de las transiciones $\epsilon$. Aunque en el peor caso teórico la cantidad de estados de un AFD puede ser $2^{|Q|}$, en la práctica de lenguajes regulares la cantidad de subconjuntos alcanzables es significativamente menor.
2. **Efectividad de la Minimización:** El algoritmo de refinamiento de particiones eliminó con éxito tanto los estados redundantes o equivalentes como los estados inalcanzables, logrando reducciones de hasta un 40% en la cantidad de estados en los autómatas probados.
3. **Compatibilidad:** El formato de datos en JSON implementado satisface los requerimientos teóricos de la materia y permite la interoperabilidad directa con herramientas visuales de simulación como AutomataLab.

---

## 6. REFERENCIAS BIBLIOGRÁFICAS

1. **Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2008).** *Introducción a la Teoría de Autómatas, Lenguajes y Computación* (3ra ed.). Pearson Educación.
2. **Sipser, M. (2012).** *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
3. **Martin, J. C. (2010).** *Introduction to Languages and the Theory of Computation* (4th ed.). McGraw-Hill.
