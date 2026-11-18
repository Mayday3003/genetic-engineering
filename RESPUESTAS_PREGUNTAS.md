# Respuestas a las preguntas del enunciado — Pareja 2 (System_2A → System_2B)

Cada respuesta tiene: **respuesta corta**, **evidencia** (con los datos) y **límites**. Todo se basa en los resultados de las partes A–F; los archivos de apoyo están indicados. Convención: **2A** = variante inicial (KD 23 nM); **2B** = variante madurada (KD 0.15 nM); ΔΔG_exp = RT ln(0.15/23) = **−2.98 kcal/mol**; ΔΔG = ΔG(2B) − ΔG(2A).

---

## Pregunta 1. ¿Qué modificaciones diferencian ambas variantes y dónde se localizan respecto a la interfaz?
*Identifique los cambios presentes y determine cuáles tienen contacto directo con el antígeno y cuáles podrían tener efectos indirectos.*

### Respuesta corta
Hay **9 mutaciones**, todas en los lazos **CDR1** (A28P, Y29W) y **CDR3** (Y101D, E102A, R104V, D105A, R106T, T107R, Q110R); ninguna en el esqueleto. **Cinco tienen contacto directo con la RNasa en 2B** (Y29W, Y101D, R106T, T107R, Q110R); **R104V elimina** un contacto que existía en 2A; **tres son indirectas** (A28P, E102A, D105A).

### Evidencia
Distancia mínima de cada posición a la RNasa en los cristales (contacto = ≤ 4 Å):

| Mutación | Tipo de cambio | 2A (Å) | 2B (Å) | Clasificación |
|---|---|---|---|---|
| A28P | apolar → apolar | 5.8 | 5.7 | Indirecta |
| Y29W | aromático → aromático | 3.3 | 3.5 | **Directa** |
| Y101D | aromático → carga (−) | 3.2 | 3.1 | **Directa** |
| E102A | carga (−) → apolar | 4.8 | 4.5 | Indirecta |
| R104V | carga (+) → apolar | **4.0** | 5.9 | Contacto **perdido** |
| D105A | carga (−) → apolar | 5.9 | 6.0 | Indirecta |
| R106T | carga (+) → polar | 2.9 | 2.9 | **Directa** |
| T107R | polar → carga (+) | 2.7 | 2.7 | **Directa** |
| Q110R | polar → carga (+) | 4.9 | 3.7 | **Directa** (contacto nuevo) |

- **Thr30 no está mutado**, pero pasa de 4.3 a 3.9 Å y entra en la interfaz de 2B (en la MD toca el 38 % del tiempo frente al 1 % en 2A): un residuo cambia de papel por el reacomodo de sus vecinos.
- Gly−1/Ser0 (2A) y Lys1 de la RNasa (2B) **no son mutaciones**: son extremos de la secuencia resueltos en una estructura y no en la otra, lejos de la interfaz (> 8 Å).
- **Efectos indirectos posibles:**
  - A28P (Pro) rigidiza la base del CDR1.
  - E102A y D105A eliminan cargas negativas que no tocan la RNasa; D105A además elimina el puente salino interno **Asp105–Arg45** de 2A (presente el 100 % de la MD), que anclaba el CDR3 al esqueleto del nanobody.
  - En 2B aparece un puente salino interno nuevo, **Asp101–Arg107** (2.9 Å; 99 % de la MD).
  - El CDR3 pasa de carga neta 0 a +1 y el nanobody completo de +1 a +2.
- Archivos: `A_inspeccion/A_inspeccion_inicial.md`, `A_inspeccion/tablas/analisis_interfaz.txt`, `visualizar/A_mutaciones.pml`.

### Límites
El criterio de 4 Å es un corte, no una frontera física (Arg104 está justo en 4.0 Å y en la MD su ocupación es solo 0.26). Los cristales son estructuras estáticas.

---

## Pregunta 2. ¿Hasta qué punto son realmente similares las dos estructuras?
*Determine si la similitud estructural global oculta diferencias locales en regiones específicas del nanobody, del antígeno o de la interfaz.*

### Respuesta corta
Son muy similares en forma (RMSD global 0.99 Å), pero **esa similitud oculta una reorganización local**: el nanobody se apoya ~2 Å distinto sobre la RNasa, y la interfaz cambia de composición y de contactos aunque su tamaño sea el mismo.

### Evidencia
- **Forma (superposición de cristales, Cα):** complejo 0.99 Å; nanobody 1.10 Å; RNasa 0.64 Å; CDR1 0.29 Å y CDR3 0.25 Å cuando cada lazo se alinea sobre sí mismo (conservan su forma interna).
- **Posición relativa (alineando sobre la RNasa, sin reajustar):** el nanobody se desplaza **2.13 Å**; CDR1 1.2–1.3 Å y CDR3 1.3 Å. En la MD el desplazamiento es 2.6 Å, del orden de la oscilación propia de cada sistema.
- **Interfaz:**

| Medida (cristal) | 2A | 2B |
|---|---|---|
| Área enterrada | 1178 Å² | 1165 Å² |
| Pares de átomos pesados a < 4 Å | 100 | 132 |
| Contactos polares N/O ≤ 3.5 Å | 10 | 12 |
| Residuos de la interfaz del nanobody | 13 | 14 (sale Arg104; entran Arg110 y Thr30) |
| Residuos de la interfaz de la RNasa | 15 | 15 (14 iguales; sale Gly68, entra Ser59) |

  El **tamaño no cambia** (1178 → 1165 Å²); cambia **qué residuos y qué contactos**: el núcleo (contactos de esqueleto Gly, Ile32) es el mismo y cambia la periferia.
- **Cargas de la interfaz:** nanobody 2A: Arg104(+), Arg106(+); 2B: Arg107(+), Arg110(+), Asp101(−). La RNasa (Lys61(+), Glu111(−)) no cambia.
- **Dinámica (1 ns):** el RMSD del complejo es igual (1.57 frente a 1.55 Å), pero el del nanobody por sí solo es **1.53 (2A) frente a 0.88 Å (2B)**: 2B es internamente más rígido. El RMSD del complejo coincide porque mezcla cambio de forma y desplazamiento relativo y ambos se compensan (el desplazamiento del nanobody sobre la RNasa es 2.48 frente a 3.12 Å, dentro del ruido).
- **Contactos en la MD:** pares de átomos < 4 Å: 551 frente a 562 (sin diferencia); **puentes de H: 6.19 frente a 7.22** (+1.03 ± 0.28), con 8 o más puentes en el 42 % de los cuadros de 2B frente al 6 % de 2A.
- Archivos: `A_inspeccion/A_inspeccion_inicial.md`, `C_analisis/C_analisis_estructural.md`, `C_analisis/Guia_graficas.md`.

### Límites
La diferencia de rigidez y de puentes de H sale de **una sola réplica por sistema** y el error de 2B está subestimado (crece con el tamaño del bloque). El desplazamiento nanobody–RNasa en la MD está dentro del ruido.

---

## Pregunta 3. Si ambas estructuras son tan parecidas, ¿cómo explicar una mejora de más de dos órdenes de magnitud?
*Determine si existen diferencias energéticas entre ambos complejos compatibles con el comportamiento experimental.*

### Respuesta corta
Con **una réplica** el cálculo da una diferencia compatible (ΔΔG = −2.22 ± 0.99). Con **tres réplicas** el resultado es **+1.36 ± 4.46**: **no se puede afirmar** que el método reproduzca la mejora. Estructuralmente hay indicios plausibles (más contactos polares, mejor encaje, ~1 puente de H más), pero no están demostrados energéticamente.

### Evidencia
- **Escala:** 153× en KD son solo **2.98 kcal/mol**; cada factor de 10 equivale a 1.36 kcal/mol. Un puente de H o salino aporta 1–3 kcal/mol, así que el cambio estructural observado (contactos polares 10 → 12) es del orden necesario; no hace falta un cambio grande de geometría.
- **ΔG de unión por réplica (kcal/mol):**

| | Réplica 1 | Réplica 2 | Réplica 3 | Media ± SD |
|---|---|---|---|---|
| 2A | −50.11 | −57.10 | −44.01 | −50.40 ± 6.55 |
| 2B | −52.33 | −50.32 | −44.46 | −49.04 ± 4.09 |

  ΔΔG = **−2.22 ± 0.99** (r1, error dentro de la trayectoria) y **+1.36 ± 4.46** (3 réplicas, error entre réplicas). La dispersión entre réplicas (4–7) supera la diferencia buscada (3). Solo 5 de las 9 combinaciones de réplicas 2B−2A dan signo negativo.
- **Indicios estructurales compatibles con una mejor unión:** pares de átomos a < 4 Å 100 → 132 con la misma área enterrada (mejor encaje); contactos polares 10 → 12 (nuevos: Asp101–Thr70 y Thr106–Gly112); ~1 puente de H más en la MD; nanobody internamente más rígido (hipótesis).
- Archivos: `D_F_energia/D_F_energia_libre.md`, `D_F_energia/figuras/D_replicas_dG.png`, `D_F_energia/tablas/resumen_replicas.txt`.

### Límites
1 ns y tres réplicas que parten de la misma estructura minimizada (solo cambia la semilla de las velocidades); GB sin entropía. El −2.22 de la réplica 1 fue en parte azar y no debe presentarse como resultado.

---

## Pregunta 4. ¿La mejora puede atribuirse individualmente a los residuos modificados o emerge de cambios cooperativos en la interfaz?
*Analice cómo cambian las contribuciones de los residuos del nanobody y del antígeno y determine si aparecen nuevas interacciones, se fortalecen interacciones preexistentes o se produce una redistribución más amplia.*

### Respuesta corta
**No puede atribuirse a los residuos modificados individualmente**: sumados, empeoran la unión (+3.8 kcal/mol con tres réplicas; +5.95 en r1). Hay **nuevas interacciones, interacciones que cambian de residuo y una redistribución del mapa**, pero con los datos disponibles **no se puede afirmar un efecto cooperativo**.

### Evidencia (ΔΔG_i = ΔG_i(2B) − ΔG_i(2A))
| Posición | ΔG_i 2A → 2B (3 réplicas) | ΔΔG_i | Lectura |
|---|---|---|---|
| **Tyr101→Asp** | −5.21 → +1.27 | **+6.48 ± 0.14** | Pierde el mayor hotspot de 2A (un aromático pasa a una carga con alto coste de desolvatación) |
| **Thr107→Arg** | −2.51 → −5.22 | **−2.71 ± 1.29** | Gana: la arginina nueva forma el puente salino con Glu111 |
| **Arg106→Thr** | −2.85 → −1.53 | +1.33 ± 0.49 | Pierde el puente salino de 2A |
| **Gln69 (RNasa)** | −1.73 → −3.77 | **−2.04 ± 0.08** | Gana contribución sin estar mutado |
| Tyr29→Trp | −2.55 → −3.27 | −0.72 ± 0.36 | Cambio pequeño |
| Resto de mutadas | ≈ 0 | |

- **Suma por región:**

| Región | r1 | 3 réplicas |
|---|---|---|
| 9 posiciones mutadas | +5.95 | **+3.76** |
| Nanobody no mutado | −5.38 | **−0.22** |
| RNasa | −2.45 | **−1.89** |

- **Nuevas interacciones:** Asp101–Thr70 N (3.07 Å; 67 % de la MD) y Thr106–Gly112 N (3.10 Å; 34 %). **Interacción que cambia de residuo:** el puente salino con Glu111 pasa de Arg106 (3.34 Å) a Arg107 (3.11 Å); R106T (+2.54) y T107R (−2.42) suman ≈ **+0.12** en r1 (la arginina "se corre" una posición). **Interacciones debilitadas en la MD:** puente salino 96 % → 78 %; contacto 107–Tyr115 100 % → 32 %.
- **Casi todo el +5.95 viene de Y101D (+6.79);** las otras ocho mutaciones suman −0.84. Las mutaciones E102A, R104V y D105A tienen electrostática y solvatación polar de ±10 que se cancelan (totales −0.10, +0.02, −0.59), coherente con que no tocan la RNasa.
- **No reproducible:** la ganancia que r1 mostraba en residuos no mutados del nanobody (Gly99, Gly100, Tyr27, Tyr33: −5.4) **desaparece con tres réplicas** (Gly99 cambia de signo: −2.28, +1.45, +1.31).
- Archivos: `D_F_energia/Explicacion_basica_F.md`, `D_F_energia/figuras/F_top_ddg_replicas.png`, `F_mutaciones_ddG_r1.png`, `F_mutaciones_componentes_r1.png`, `D_F_energia/tablas/descomposicion_replicas.csv`.

### Límites
La mejora, si existe en el cálculo, no está en los residuos mutados; solo Gln69 (RNasa) es un cambio claro fuera de ellos. Como el ΔΔG total con tres réplicas no se distingue de cero, un efecto cooperativo es **compatible pero no demostrable**. El criterio "|ΔΔG_i| > 2 errores" con n = 3 es permisivo; el criterio más robusto es que el signo se repita en las tres réplicas (cumplen Tyr101, Thr107, Gln69, Arg106; no cumplen Gly99 ni Tyr115).

---

## Pregunta 5. ¿Cambió el mapa energético de la interfaz durante la maduración de la afinidad?
*Identifique qué regiones o residuos ganan o pierden importancia energética y determine si la variante madura presenta una interfaz energéticamente diferente a pesar de conservar una geometría global similar.*

### Respuesta corta
**Sí, localmente:** el hotspot de **Tyr101 se pierde** y aparece uno en **Arg107**, y gana peso **Gln69** de la RNasa. El resto del mapa (Ile32, Thr70, Glu111, Tyr115) se mantiene. La interfaz es energéticamente distinta en las posiciones mutadas pese a la geometría global similar.

### Evidencia (ΔG_i, media de 3 réplicas, kcal/mol)
| Residuo | 2A | 2B | Cambio |
|---|---|---|---|
| Tyr101 → Asp101 | −5.21 | **+1.27** | Pierde importancia (deja de ser hotspot) |
| Thr107 → Arg107 | −2.51 | **−5.22** | Gana importancia (pasa a ser el mayor hotspot del nanobody junto con Ile32) |
| Arg106 → Thr106 | −2.85 | −1.53 | Pierde |
| Gln69 (RNasa) | −1.73 | **−3.77** | Gana |
| Ile32 | −5.06 | −4.74 | Se mantiene |
| Thr70 (RNasa) | −3.65 | −4.11 | Se mantiene |
| Tyr115 (RNasa) | −3.28 | −3.12 | Se mantiene |
| Glu111 (RNasa) | −3.32 | −3.07 | Se mantiene |

- Con r1 sola parecía que **Tyr115 y Glu111 de la RNasa perdían importancia** (+1.9 y +1.2); **con tres réplicas no se sostiene** (+0.16 y +0.25, dentro del ruido).
- El **mapa de cargas** también cambia: la interfaz del nanobody pasa de dos cargas + (Arg104, Arg106) a dos + (Arg107, Arg110) y una − (Asp101); en 2A el CDR3 se ancla al esqueleto con Asp105–Arg45 y en 2B con Asp101–Arg107.
- Archivos: `D_F_energia/figuras/F_mapa_interfaz.png` (r1), `F_top_ddg_replicas.png` (3 réplicas), `visualizar/F_energia_bfactor.pml` (3D).

### Límites
`F_mapa_interfaz` es de una réplica; los valores finos pueden variar entre réplicas. El "mapa" cambia en los residuos con cambio robusto (Tyr101, Arg107, Gln69); los demás son estables o dentro del ruido.

---

## Pregunta 6. ¿Qué tan bien puede el modelo energético explicar el comportamiento experimental durante la maduración de la afinidad?
*Compare la dirección y magnitud del cambio calculado con los valores experimentales y analice qué aspectos parecen correctamente representados y cuáles no.*

### Respuesta corta
**Mal en lo cuantitativo y no concluyente en la dirección**: con una réplica acierta (−2.2 frente a −2.98), con tres no (+1.4 ± 4.5, compatible con cero y con el valor experimental). Representa razonablemente **qué residuos cambian** y que **la contribución no polar no cambia**; no representa la **magnitud neta**.

### Evidencia
**Dirección y magnitud**
| | ΔΔG (kcal/mol) |
|---|---|
| Experimental | −2.98 |
| Calculado, réplica 1 | −2.22 ± 0.99 |
| Calculado, 3 réplicas | **+1.36 ± 4.46** |

**Componentes (3 réplicas, ΔΔ = 2B − 2A)**
| Término | ΔΔ | Lectura |
|---|---|---|
| vdW | −2.66 ± 2.88 | Apunta a favorable (compatible con el mejor encaje), sin significación |
| Electrostática | +9.61 ± 7.40 | Sin significación |
| Solvatación polar (GB) | −5.52 ± 6.61 | Sin significación |
| Electrostática + solvatación polar | +4.09 ± 2.78 | Signo desfavorable; **en r1 era −1.28**: el signo no es fiable |
| Solvatación no polar | −0.06 ± 0.14 | **No cambia** (precisión suficiente) |

- **Compensación:** por instantánea, electrostática y solvatación polar se correlacionan de forma inversa (r = −0.94, pendiente −0.80); cada una fluctúa 14–18 kcal/mol y su suma 5–6. Por eso solo se interpreta la suma, y por eso los términos aislados tienen errores tan grandes.

**Lo que parece bien representado**
- Que la contribución no polar no cambia (consistente con el área enterrada igual: 1178 frente a 1165 Å²).
- Que la ganancia de vdW (mejor encaje) apunta en el sentido de la mejora (consistente con 100 → 132 pares de átomos).
- La pérdida de Tyr101→Asp como residuo clave, el puente salino con Glu111 que pasa a Arg107, y la ganancia de Gln69 (coherentes con la estructura y la MD).
- La compensación electrostática–solvatación esperada en MM/GBSA.

**Lo que no está representado**
- La **magnitud y el signo neto** del ΔΔG con muestreo suficiente (el error entre réplicas, 4.5, supera el efecto, 3).
- El signo de la parte polar (cambia de r1 a tres réplicas).
- Los valores absolutos (≈ −50 frente a ≈ −10 y −13): el método no incluye entropía y trata el agua de forma implícita.

### Limitaciones del modelo y del muestreo
- **Muestreo:** 1 ns por réplica; las tres réplicas parten de la misma estructura minimizada y solo cambian las velocidades iniciales. El error de una réplica (±1) solo mide la fluctuación dentro de ella y subestima la incertidumbre real unas 4 veces.
- **Modelo:** GB (GB-Neck2) sin entropía configuracional ni aguas de interfaz; campo de fuerza fijo; el término polar fluctúa ±10 y se compensa.
- **Sistemas:** 2A conserva dos residuos de la etiqueta de expresión (Gly−1, Ser0) y a la RNasa le falta la Lys1 (lejos de la interfaz; efecto ≈ 0.1 kcal/mol).
- **Descomposición por residuo:** no suma exactamente el ΔΔG global (−1.88 frente a −2.22 en r1).

### Mejoras propuestas
Más réplicas con estructuras de partida distintas; producciones de ≥ 10 ns; comparar con PB o `igb=5` para ver si el signo se mantiene; estimar la entropía (interaction entropy o C2); recalcular con ambas cadenas con la misma composición de residuos.

---

## Resumen de una tabla
| Pregunta | Respuesta breve | Robustez |
|---|---|---|
| 1. Modificaciones | 9 mutaciones en CDR1/CDR3; 5 directas, 1 con contacto perdido, 3 indirectas | Alta |
| 2. Similitud | Forma casi igual (0.99 Å), pero reorganización local (desplazamiento ~2 Å, composición e interacciones de la interfaz) | Alta (estructura); media (MD, una réplica) |
| 3. Mejora de 153× | Indicios estructurales plausibles; el cálculo no la reproduce con 3 réplicas (+1.4 ± 4.5) | Baja (energía) |
| 4. Individual o cooperativo | Las mutaciones suman +3.8 (desfavorable); nuevas interacciones y redistribución; cooperatividad compatible pero no demostrable | Media |
| 5. Mapa energético | Cambia localmente (Tyr101 pierde; Arg107 y Gln69 ganan); el resto es estable | Media-alta (Tyr101); media (resto) |
| 6. Modelo vs experimento | Acierta con 1 réplica, no con 3; no cambia lo no polar; compensación EEL/GB; falta muestreo y entropía | Alta (conclusión), baja (cifra) |
