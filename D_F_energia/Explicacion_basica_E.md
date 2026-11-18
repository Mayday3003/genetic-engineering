# Explicación básica de la parte E (componentes de energía)

Requiere haber leído `Explicacion_basica_D.md` (definiciones de ΔG, ΔΔG y MM/GBSA). Datos en `tablas/`, figuras en `figuras/`. Se reproduce con `.venv/bin/python scripts/figuras_componentes.py`.

## 1. Qué pide el enunciado en la parte E
> "Debe determinarse si la mejora proviene principalmente de van der Waals, electrostática, solvatación polar, contribución no polar o compensación entre varios términos. No deben interpretarse componentes aislados: una electrostática más favorable puede estar acompañada por una mayor penalización de desolvatación."

Es decir: **descomponer el ΔΔG en sus términos** y ver cuál (o qué combinación) lo explica, sin interpretar la electrostática y la solvatación polar por separado.

## 2. Los términos y qué significan (repaso)
| Término | Qué representa | Signo habitual |
|---|---|---|
| ΔE vdW | Encaje entre átomos cercanos (atracción y repulsión de corto alcance) | Negativo |
| ΔE electrostática | Fuerzas entre las cargas de las dos proteínas | Negativo |
| ΔG solvatación polar (GB) | Coste de perder, al unirse, parte del contacto de los grupos polares y cargados con el agua | Positivo |
| ΔG solvatación no polar | Energía asociada a la superficie que queda expuesta al agua | Negativo, pequeño |

Cada uno se calcula como **complejo − RNasa sola − nanobody solo** y después se compara 2B − 2A. Los valores de cada término son enormes (decenas de kcal/mol) y la diferencia buscada es de ~3 kcal/mol, por eso pequeños errores en un término tapan el resultado.

---

## 3. Gráfica 1: `figuras/E_compensacion.png`

**Qué es cada cosa**
- **Eje X:** ΔE electrostática de una instantánea (kcal/mol). **Eje Y:** ΔG de solvatación polar (GB) de **la misma** instantánea.
- **Cada punto:** una instantánea de la simulación. Hay 606 (101 por cada una de las 6 corridas: 3 réplicas de 2A y 3 de 2B).
- **Azul = 2A, naranja = 2B.** **Línea punteada:** la recta que mejor ajusta todos los puntos.

**Qué se ve**
- Los puntos forman una **línea descendente**: cuando la electrostática es más negativa (más favorable), la solvatación polar es más positiva (menos favorable).
- La relación es muy fuerte: coeficiente de correlación **r = −0.94** y pendiente **−0.80**.
- Los puntos de 2A y 2B están mezclados sobre la misma recta.

**Qué significa**
- Cuando la electrostática mejora 1 kcal/mol, la solvatación polar empeora ~0.8 kcal/mol. **Los dos términos casi se cancelan.**
- Esto ocurre porque ambos dependen de lo mismo: cómo están colocados los grupos cargados y polares. Si dos grupos cargados se acercan, ganan atracción (electrostática favorable) pero pierden más contacto con el agua (solvatación más costosa).
- Consecuencia práctica: cada término por separado fluctúa mucho entre instantáneas (desviación de 14 a 18 kcal/mol), pero **su suma fluctúa mucho menos** (5 a 6 kcal/mol). Por eso se interpreta la suma y no cada término.
- 2A y 2B siguen **la misma relación**; lo que cambia entre ellos es en qué parte de la recta caen, no la recta.

**Qué no significa:** que la electrostática "sea mala" o la solvatación "buena". Los dos valores individuales no tienen significado independiente en este método.

---

## 4. Gráfica 2: `figuras/E_componentes_replicas.png`

**Qué es cada cosa**
- **Cada barra:** ΔΔ de un término = valor en 2B − valor en 2A, promediado en las 3 réplicas. Hacia la izquierda es favorable para 2B.
- **Barra de error:** error entre réplicas (desviación entre réplicas dividida por √3, combinada para 2A y 2B).
- **Línea negra en 0:** sin diferencia. **Línea punteada:** valor experimental (−2.98).

Datos (`tablas/componentes_replicas.txt`):

| Término | 2A | 2B | ΔΔ (2B − 2A) |
|---|---|---|---|
| ΔE vdW | −69.09 ± 3.82 | −71.75 ± 3.22 | **−2.66 ± 2.88** |
| ΔE electrostática | −61.68 ± 6.07 | −52.07 ± 11.29 | +9.61 ± 7.40 |
| ΔG solvatación polar (GB) | +88.93 ± 8.64 | +83.41 ± 7.51 | −5.52 ± 6.61 |
| ΔG solvatación no polar | −8.56 ± 0.16 | −8.63 ± 0.18 | −0.06 ± 0.14 |
| **Electrostática + solv. polar** | 27.25 ± 2.67 | 31.34 ± 4.01 | **+4.09 ± 2.78** |
| **ΔG de unión** | −50.40 ± 6.55 | −49.04 ± 4.09 | **+1.36 ± 4.46** |

(± en 2A y 2B es la desviación entre réplicas.)

**Qué se ve**
- **vdW:** −2.7, favorable para 2B; el error (±2.9) es casi del tamaño del valor.
- **Electrostática:** +9.6 (desfavorable) y **solvatación polar:** −5.5 (favorable), con errores enormes (±7). Van en sentidos opuestos, como muestra la gráfica 1.
- **Su suma:** +4.1 ± 2.8, **desfavorable** para 2B.
- **No polar:** prácticamente 0 y con error muy pequeño.
- **Total:** +1.4 ± 4.5: el error cruza el cero y también el valor experimental.

**Qué significa**
- **No polar sin cambio:** la superficie enterrada es la misma, lo que coincide con el área enterrada de los cristales (1178 frente a 1165 Å²).
- **vdW:** es el único término que apunta en el sentido de la mejora de afinidad. Es coherente con el mejor encaje visto en los cristales (pares de átomos a < 4 Å: 100 → 132), pero su diferencia no es significativa.
- **Electrostática + solvatación polar:** si algo indican, es que **la parte polar no ayuda a 2B** (+4.1). Esto es lo contrario de lo que daba la réplica 1 sola (−1.3).
- **Total:** con tres réplicas no se distingue 2A de 2B.

---

## 5. Gráfica 3 (repaso): `figuras/D_componentes_ddg.png` (solo réplica r1)
Con una sola réplica: vdW −0.9, electrostática +0.7, solvatación polar −2.0, suma de los dos polares **−1.3**, total −2.2. Al comparar con la gráfica 2 se ve que **el signo de la parte polar cambia de una réplica sola (−1.3) a tres réplicas (+4.1)**: ese término no es fiable.

| | Réplica 1 sola | 3 réplicas |
|---|---|---|
| vdW | −0.9 | −2.7 |
| Electrostática + solv. polar | −1.3 | +4.1 |
| Total | −2.2 | +1.4 |

---

## 6. Qué responde la parte E
Pregunta del enunciado: ¿de dónde viene la mejora, de vdW, de electrostática, de solvatación polar, de la no polar o de una compensación?

1. **No es la contribución no polar:** no cambia (−0.06 ± 0.14).
2. **Electrostática y solvatación polar se compensan** (r = −0.94, pendiente −0.80). No se pueden interpretar por separado; su suma es +4.1 ± 2.8, sin evidencia a favor de 2B.
3. **El único término que apunta en el sentido de la mejora es vdW** (−2.7 ± 2.9), coherente con un mejor encaje, pero no es significativo.
4. **No se puede afirmar un origen:** el ΔΔG total con tres réplicas (+1.4 ± 4.5) no distingue las variantes, y el signo de la parte polar cambia entre una réplica y tres.

Frase para presentar: *"La contribución no polar no cambia; la electrostática y la solvatación polar se compensan casi uno a uno, y su suma no favorece a 2B. El único término que va en el sentido de la mejora es vdW, pero con tres réplicas no es significativo, así que con este muestreo no podemos asignar el origen de la mejora."*

## 7. Preguntas de comprobación
1. En la gráfica 1, ¿qué significa que los puntos formen una línea descendente?
2. ¿Por qué se interpreta la suma de electrostática y solvatación polar y no cada término por separado?
3. ¿Qué cambia entre la réplica r1 sola y las tres réplicas en la parte polar, y qué enseña eso?

---

## 8. Profundización: de dónde salen los números y por qué se compensan

### 8.1 Las tres restas
Los números se obtienen con tres restas sucesivas, y en cada una el valor se hace mucho más pequeño, pero el ruido no se reduce en la misma proporción:

| Nivel | Qué se resta | Orden de magnitud |
|---|---|---|
| 1. Energía de cada parte | Se calcula la energía del complejo, del nanobody solo y de la RNasa sola | Miles de kcal/mol (por ejemplo, EEL del complejo = −17 223) |
| 2. Δ de un sistema | Complejo − nanobody − RNasa | Decenas (ΔEEL = −65.6) |
| 3. ΔΔ entre sistemas | Δ(2B) − Δ(2A) | Unidades (ΔΔG ≈ 1 a 3) |

### 8.2 Ejemplo con números reales (2A, réplica 1; `resultados_mmgbsa/2A/FINAL_RESULTS_MMPBSA.dat`)
| Término | Complejo | Nanobody (receptor) | RNasa (ligando) | Δ = complejo − receptor − ligando |
|---|---|---|---|---|
| EEL | −17 223.10 | −8 444.93 | −8 712.62 | **−65.55** |
| EGB | −3 034.19 | −1 427.65 | −1 700.08 | **+93.54** |

Comprobación: −17 223.10 + 8 444.93 + 8 712.62 = −65.55; −3 034.19 + 1 427.65 + 1 700.08 = +93.54.

### 8.3 Qué mide cada uno
- **EEL (−65.55):** las fuerzas entre las cargas de las dos proteínas calculadas **como si no hubiera agua**. Sin agua, las cargas opuestas se atraen con mucha fuerza.
- **EGB (+93.54):** la corrección por la presencia del agua. El agua debilita las fuerzas entre cargas (su constante dieléctrica es ≈ 80, es decir, las fuerzas se reducen unas 80 veces), así que EEL **exagera** la atracción. EGB resta esa exageración.
- **La suma EEL + EGB = +27.99:** la interacción electrostática **en agua**. Es la cifra con sentido físico. Resulta positiva: en conjunto, enterrar los grupos polares y cargados en la interfaz cuesta más de lo que se gana.

### 8.4 Por qué fluctúan de forma opuesta
La recta de la gráfica 1 es **GB ≈ −0.80 × EEL + 40.7**, así que la suma es **EEL + GB ≈ 0.20 × EEL + 40.7**: la suma cambia solo 0.2 por cada unidad que cambia EEL. Dos instantáneas reales (2A, r1):

| Instantánea | EEL | GB | Suma |
|---|---|---|---|
| 20 | −94.7 | +117.7 | **23.0** |
| 78 | −31.3 | +68.3 | **37.0** |

EEL cambia 63 kcal/mol y GB cambia 49 en sentido opuesto, pero la suma cambia solo 14.

### 8.5 Ejercicio con las 6 corridas (kcal/mol)
| Corrida | EEL | GB | EEL + GB |
|---|---|---|---|
| 2A r1 | −65.55 | 93.54 | 27.99 |
| 2A r2 | −54.68 | 78.97 | 24.29 |
| 2A r3 | −64.82 | 94.29 | 29.47 |
| 2B r1 | −64.81 | 91.52 | 26.71 |
| 2B r2 | −48.10 | 82.00 | 33.90 |
| 2B r3 | −43.31 | 76.71 | 33.40 |

Medias de la suma: 2A = 27.25, 2B = 31.34, diferencia **+4.09**. Observa que EEL varía entre −43 y −66 y GB entre 77 y 94 de una corrida a otra, pero la suma solo entre 24 y 34.

### 8.6 Cómo leer una barra de error
- Si la barra de error **cruza el cero**, los datos son compatibles con que no haya diferencia.
- La suma EEL + GB es +4.1 ± 2.8: a ±1 error no cruza el cero (1.3 a 6.9), pero a ±2 errores sí (−1.5 a 9.6). **No es una diferencia significativa.** Y el signo es el contrario del que daba la réplica 1.
