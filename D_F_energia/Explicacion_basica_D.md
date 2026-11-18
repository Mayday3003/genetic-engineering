# Explicación básica de la parte D (energía de unión)

Definiciones primero y después las tres gráficas de la parte D, una por una. Datos en `tablas/`, figuras en `figuras/`. Para el análisis completo (componentes, residuos, réplicas), ver `D_F_energia_libre.md`.

---

# 1. Definiciones

### Energía libre de unión (ΔG)
Un número que dice **qué tan favorable es que el nanobody y la RNasa estén unidos**, comparado con estar separados.

**ΔG = energía del complejo − energía de la RNasa sola − energía del nanobody solo**

- Si da **negativo**, estar unidos es más favorable que estar separados.
- Cuanto **más negativo**, más favorable.
- La unidad es la **kcal/mol**.

### ΔΔG (la diferencia entre sistemas)
**ΔΔG = ΔG de 2B − ΔG de 2A**
- Si da **negativo**, 2B se une mejor que 2A.
- El valor experimental, calculado de las KD (23 nM y 0.15 nM), es **ΔΔG = −2.98 kcal/mol**. Es el número que queremos reproducir.

### MM/GBSA (el método)
Método para **estimar ΔG usando las instantáneas de la simulación**:
- **MM** (mecánica molecular): calcula la energía entre los átomos con las reglas del campo de fuerza. Da dos términos: van der Waals y electrostática.
- **GBSA** (Generalized Born + Surface Area): en vez de usar las miles de moléculas de agua, **aproxima el efecto del agua** con una fórmula. Da otros dos términos: solvatación polar (GB) y solvatación no polar (SA).

### Cómo se calcula
1. Se toma una **instantánea** de la simulación (coordenadas de todos los átomos en un instante).
2. Se quita el agua y se calcula la energía del **complejo**.
3. Con esas mismas coordenadas se separan las dos proteínas y se calcula la energía de cada una **sola**.
4. Se resta: complejo − RNasa − nanobody. Eso es el ΔG de esa instantánea.
5. Se repite en **101 instantáneas** (de 500 a 1000 ps, una cada 5 ps) y se promedia.

Consecuencia: cada proteína separada se calcula con la forma que tenía dentro del complejo, sin relajarse. Por eso las energías internas (enlaces, ángulos, diedros) se cancelan y valen 0 en la diferencia.

### Los términos de energía
| Término | Qué es | Signo habitual |
|---|---|---|
| **ΔE vdW** | Atracción y repulsión entre átomos cercanos (qué tan bien encajan) | Negativo |
| **ΔE electrostática** | Fuerzas entre las cargas de las dos proteínas | Negativo |
| **ΔG solvatación polar (GB)** | Cambio en la energía de que los grupos polares y cargados estén rodeados de agua; al unirse se pierde parte de ese contacto | **Positivo** (desfavorable) |
| **ΔG solvatación no polar** | Energía asociada a la superficie en contacto con el agua | Negativo y pequeño |

**ΔG gas = vdW + electrostática. ΔG solvatación = polar + no polar. ΔG de unión = ΔG gas + ΔG solvatación.**

Electrostática y solvatación polar son **grandes y de signo opuesto** y casi se cancelan; por eso nunca se interpretan por separado.

### Lo que MM/GBSA no incluye
- **La entropía** (el cambio de libertad de movimiento al unirse).
- **El agua individual**: solo una fórmula aproximada.

Por eso los ΔG (≈ −50 kcal/mol) son mucho más negativos que los experimentales (≈ −10 a −13). **No se comparan con el experimento**; solo se usa la diferencia ΔΔG entre dos sistemas tratados igual.

### Réplica
Repetir la simulación con las mismas condiciones, cambiando solo el azar de las velocidades iniciales. Si el resultado cambia mucho entre réplicas, el resultado de una sola no es confiable.

---

# 2. Gráfica por gráfica
Colores como en la parte C: **azul = 2A, naranja = 2B.**

## Gráfica 1: `figuras/D_serie_tiempo_dG.png`

**Qué es cada cosa**
- **Eje X:** tiempo de la simulación (500–1000 ps). **Eje Y:** ΔG de unión (kcal/mol) calculado en esa instantánea.
- **Cada punto de la línea:** el ΔG de una instantánea (101 puntos por curva).
- **Leyenda:** el promedio de la curva: 2A = −50.11 y 2B = −52.33.

**Qué se ve:** cada curva sube y baja mucho (entre −40 y −61 kcal/mol) y las dos se cruzan muchas veces.

**Qué significa**
- El ΔG de **una** instantánea varía unas ±4 kcal/mol (desviación ≈ 3.6 en 2A y ≈ 4.1 en 2B).
- La diferencia entre los promedios (2.2 kcal/mol) es **menor** que esa variación; por eso se promedian las 101 instantáneas. El promedio es más preciso que cada punto, pero la gráfica ya sugiere que la diferencia no es grande frente al ruido.

**Qué no significa:** que 2B "siempre une mejor": en muchos instantes la curva naranja queda por encima (menos negativa) de la azul.

## Gráfica 2: `figuras/D_componentes_ddg.png`

**Qué es cada cosa**
- **Cada barra:** el ΔΔG (2B − 2A) de un término. Hacia la izquierda es favorable para 2B.
- **Línea negra en 0:** sin diferencia. **Línea punteada:** el valor experimental (−2.98).
- **Barra de error:** incertidumbre calculada dividiendo la trayectoria en 5 bloques.

Datos (`tablas/componentes.csv`):

| Término | 2A | 2B | ΔΔG (2B − 2A) |
|---|---|---|---|
| ΔE vdW | −69.48 | −70.40 | −0.92 ± 0.94 |
| ΔE electrostática | −65.55 | −64.81 | +0.74 ± 5.01 |
| ΔG solvatación polar (GB) | +93.54 | +91.52 | −2.01 ± 4.82 |
| ΔG solvatación no polar | −8.62 | −8.64 | −0.02 ± 0.12 |
| **ΔG de unión** | **−50.11** | **−52.33** | **−2.22 ± 0.99** |

**Qué se ve**
- La barra de ΔG de unión (abajo) llega a −2.2, cerca de la línea punteada, con error de ±1.
- Las barras de electrostática y solvatación polar tienen un error **enorme** (±5) que **cruza el cero**.

**Qué significa**
- En esta réplica, el ΔΔG total acierta el signo y la magnitud aproximada.
- **No se puede decir qué término lo causa**: los errores de la electrostática y la solvatación son mayores que sus valores y esos términos se compensan.

**Qué no significa:** que la mejora venga "de la solvatación" o "de la electrostática" por separado.

**Límite:** es **una sola réplica** (r1); su barra de error es la de una sola trayectoria.

## Gráfica 3: `figuras/D_replicas_dG.png` (la más importante)

**Qué es cada cosa**
- **Cada punto:** el ΔG promedio de una réplica completa (101 instantáneas promediadas). Tres puntos por sistema.
- **Raya negra:** la media de las tres réplicas de cada sistema.
- **El título:** el ΔΔG con las tres réplicas: **+1.36 ± 4.46**.

Datos (`tablas/resumen_replicas.txt`):

| ΔG de unión (kcal/mol) | Réplica 1 | Réplica 2 | Réplica 3 | Media |
|---|---|---|---|---|
| 2A | −50.11 | −57.10 | −44.01 | −50.40 |
| 2B | −52.33 | −50.32 | −44.46 | −49.04 |

**Qué se ve**
- Los puntos de 2A van de −44 a −57 (≈ 13 kcal/mol de rango) y los de 2B de −44 a −52.
- Las dos nubes de puntos **se solapan casi por completo**.
- Las medias están separadas por solo 1.4 kcal/mol y **en sentido contrario al experimental** (2B sale menos favorable).

**Qué significa**
- Cada réplica da un resultado muy distinto de otra del mismo sistema (hasta 13 kcal/mol). Esa variación es **mucho mayor** que la diferencia buscada (3 kcal/mol): **no se puede distinguir 2A de 2B**.
- ΔΔG = +1.36 ± 4.46 es compatible tanto con "2B une mejor" como con "2B une peor"; no sirve como evidencia en ningún sentido.
- El −2.22 de la gráfica 2 (réplica 1) fue en parte **azar**: una de las tres réplicas dio un valor favorable por casualidad.

**Qué no significa:** que 2B no una mejor en la realidad (el experimento dice que sí), sino que **este método, con 1 ns y estas condiciones, no logra detectarlo**.

---

# 3. Resumen
| Gráfica | Qué muestra | Conclusión |
|---|---|---|
| 1. Serie en el tiempo | El ΔG cambia mucho de una instantánea a otra | Hay que promediar; el ruido es del tamaño de la diferencia |
| 2. Componentes (r1) | Cuánto aporta cada término al ΔΔG | El total acierta en esta réplica, pero los términos tienen error mayor que su valor |
| 3. Réplicas | El ΔG de 3 réplicas por sistema | La dispersión entre réplicas supera la diferencia: el método no distingue 2A de 2B |

# 4. Preguntas de comprobación
1. ¿Qué significa que ΔG sea negativo? ¿Y que ΔΔG sea negativo?
2. En la gráfica 3, ¿por qué es un problema que los puntos de 2A abarquen más rango que la diferencia entre las medias?
3. ¿Por qué el −2.22 de la gráfica 2 parecía bueno pero no se puede presentar como resultado?
