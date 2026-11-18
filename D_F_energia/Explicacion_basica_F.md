# Explicación básica de la parte F (descomposición por residuo)

Requiere `Explicacion_basica_D.md` y `Explicacion_basica_E.md`. Figuras en `figuras/`, tablas en `tablas/` (`descomposicion_por_residuo.csv` para r1 y `descomposicion_replicas.csv` para las 3 réplicas). Se regeneran con `scripts/analisis_energia.py` y `scripts/analisis_replicas.py`.

## 1. Qué pide el enunciado
> "Se realizará la descomposición de ambas trayectorias y se compararán las contribuciones de posiciones equivalentes residuo a residuo: ΔΔG_i = ΔG_i,MUT − ΔG_i,WT. Residuos mutados, residuos vecinos, residuos del antígeno, regiones que no presentan mutación pero cambian su contribución. El objetivo es evaluar si los cambios energéticos se concentran en los residuos modificados o se distribuyen por la interfaz, y discutir si son compatibles con un efecto cooperativo."

## 2. Definiciones
- **Residuo:** cada aminoácido de la cadena (por ejemplo, Tyr101 del nanobody o Gln69 de la RNasa).
- **ΔG_i (contribución del residuo i):** la parte del ΔG de unión que corresponde a ese residuo. Se calcula con los mismos términos de la parte D (vdW, electrostática, solvatación polar y no polar), pero repartidos entre los residuos.
  - ΔG_i **negativo**: ese residuo **favorece** la unión.
  - ΔG_i **positivo**: ese residuo **perjudica** la unión.
  - Un residuo que no está en la interfaz tiene ΔG_i ≈ 0.
- **Suma de todos los ΔG_i ≈ ΔG de unión total.** (2A, 3 réplicas: −51.3 frente a −50.4 del total; la pequeña diferencia es normal en este método.)
- **ΔΔG_i = ΔG_i en 2B − ΔG_i en 2A**, para la misma posición:
  - Negativo: ese residuo contribuye **más** en 2B.
  - Positivo: contribuye **menos** en 2B.
- En las posiciones mutadas el residuo cambia de nombre (Tyr101 → Asp101): se compara la **posición**, no el aminoácido.

Las posiciones se agrupan así:
| Grupo | Qué es |
|---|---|
| **Mutados** | Las 9 posiciones que cambian: 28, 29, 101, 102, 104, 105, 106, 107, 110 |
| **Nanobody no mutado** | El resto de residuos del nanobody (incluye los de la interfaz que no mutaron) |
| **RNasa** | Todos los residuos del antígeno |

---

## 3. Gráfica 1: `figuras/F_top_ddg_residuo.png` (solo réplica r1)
- **Cada barra:** un residuo. Se muestran los 18 con mayor |ΔΔG_i|, ordenados de mayor a menor.
- **Largo de la barra:** ΔΔG_i (kcal/mol). Hacia la derecha: contribuye menos en 2B; hacia la izquierda: contribuye más.
- **Raya horizontal con topes:** error (método de bloques de la trayectoria, como en la parte E).
- **Nombre de la barra:** `NB:TYR101→ASP` = nanobody, posición 101, que pasa de Tyr a Asp.

**Qué se ve en r1**
| Residuo | ΔΔG_i | Lectura |
|---|---|---|
| Tyr101→Asp (NB) | **+6.8** | Pierde un residuo clave |
| Arg106→Thr (NB) | +2.5 | Pierde el puente salino |
| Thr107→Arg (NB) | −2.4 | Gana |
| Gly99 (NB, sin mutar) | −2.3 | Gana |
| Gln69 (RNasa) | −2.0 | Gana |
| Tyr115 (RNasa) | +1.9 | Pierde |
| Gly100 (NB, sin mutar) | −1.8 | Gana |

Con una réplica parece que ganan residuos no mutados (Gly99, Gly100). **Esto se desmonta con las tres réplicas** (ver gráfica 2).

### Un ejemplo de compensación a nivel de residuo (Tyr101→Asp, r1)
| Término | ΔΔG_i |
|---|---|
| vdW | +1.28 |
| Electrostática | **−21.96** |
| Solvatación polar | **+27.39** |
| No polar | +0.08 |
| **Total** | **+6.79** |

La electrostática (−22) y la solvatación polar (+27) son enormes y de signo opuesto, como en la parte E; su suma (+5.4) más el vdW (+1.3) da el +6.8. Es una mutación a un aminoácido cargado: la carga negativa nueva se paga cara por la desolvatación. Además se pierde el contacto aromático (vdW).

---

## 4. Gráfica 2: `figuras/F_top_ddg_replicas.png` (las 3 réplicas, la que sirve)
- **Cada barra:** un residuo, con ΔΔG_i **promediado en las tres réplicas**. El error es la variación **entre réplicas**.
- **Barra azul fuerte:** el cambio es mayor que 2 veces su error. **Barra azul clara:** está dentro del ruido.

| Residuo | ΔΔG_i | Significativo |
|---|---|---|
| Tyr101→Asp | **+6.48 ± 0.14** | Sí |
| Thr107→Arg | **−2.71 ± 1.29** | Sí |
| Gln69 (RNasa) | **−2.04 ± 0.08** | Sí |
| Arg106→Thr | +1.33 ± 0.49 | Sí |
| Gly100 (NB) | −1.06 ± 0.55 | No |
| Tyr29→Trp | −0.72 ± 0.36 | Sí |
| Gly99 (NB) | +0.16 ± 0.91 | No |
| Tyr115 (RNasa) | +0.16 ± 1.01 | No |

**Qué significa**
- Se mantiene en las tres réplicas: **Tyr101→Asp pierde, Thr107→Arg gana, Gln69 gana, Arg106→Thr pierde**.
- **Gly99 y Tyr115 desaparecen:** lo que parecía un cambio en r1 era ruido.
- "Significativo" no es lo mismo que "importante": Ala28→Pro es significativo (−0.16 ± 0.02) pero el efecto es de 0.16 kcal/mol, despreciable.

**Suma por región**
| Región | Réplica r1 | 3 réplicas |
|---|---|---|
| 9 posiciones mutadas | +5.95 | **+3.76** |
| Nanobody no mutado | −5.38 | **−0.22** |
| RNasa | −2.45 | **−1.89** |

La ganancia de −5.4 en residuos no mutados del nanobody que mostraba r1 casi desaparece (−0.2) al promediar tres réplicas.

---

## 5. Gráfica 3: `figuras/F_mapa_interfaz.png` (réplica r1)
- **Dos paneles:** nanobody (izquierda) y RNasa (derecha).
- **Cada par de barras:** un residuo de la interfaz; azul = su ΔG_i en 2A y naranja = su ΔG_i en 2B. No es la diferencia: son los dos valores.
- Se muestran los residuos con |ΔG_i| > 0.5 en algún sistema. Los nombres con barra (`TYR101/ASP`) son posiciones mutadas.

**Qué se ve y qué significa**
- Es el "mapa energético de la interfaz": qué residuos sostienen la unión en cada variante.
- **Hotspots de 2A:** Tyr101 (−5.4), Tyr115, Ile32, Glu111, Arg106. **Hotspots de 2B:** Arg107 (−5.6), Ile32, Thr70, Gln69, Tyr115.
- El mapa cambia en las posiciones mutadas: Tyr101 deja de ser hotspot (pasa de −5.2 a +1.3 con 3 réplicas) y Arg107 pasa a serlo (de −2.5 a −5.2). Se mantienen casi iguales Ile32 (−5.1 → −4.7), Tyr115 (−3.3 → −3.1) y Glu111 (−3.3 → −3.1).
- Es r1 sola: los valores finos pueden variar entre réplicas.

---

## 6. Qué responde la parte F
**¿Los cambios se concentran en los residuos modificados o se distribuyen?**
- Los residuos modificados concentran los cambios más grandes: Tyr101→Asp (+6.5), Thr107→Arg (−2.7) y Arg106→Thr (+1.3).
- Fuera de ellos, solo Gln69 de la RNasa (−2.0) es un cambio claro y reproducible.
- La suma de las mutaciones es **desfavorable** (+3.8): **la mejora no puede explicarse por la suma de los residuos modificados**. Lo que compensa, si algo lo hace, está en la RNasa (−1.9), sobre todo en Gln69.

**¿Cooperativo?** Es compatible con una reorganización en la que Thr107→Arg y el entorno de Gln69 compensan la pérdida de Tyr101, pero los datos no permiten afirmarlo: el ΔΔG total no se distingue de cero con tres réplicas y los cambios fuera de las mutaciones son pocos y pequeños.

**¿Cambió el mapa energético?** Sí, en las posiciones mutadas: el hotspot de Tyr101 se pierde y aparece uno en Arg107. El resto de la interfaz (Ile32, Glu111, Tyr115) se mantiene.

## 7. Para verlo en 3D
```bash
bash visualizar/pymol.sh visualizar/F_energia_bfactor.pml
```
Colorea 2B por ΔΔG_i (3 réplicas): azul = contribuye más en 2B, rojo = contribuye menos.

## 8. Preguntas de comprobación
1. ¿Qué significa que el ΔG_i de un residuo sea negativo? ¿Y su ΔΔG_i?
2. ¿Por qué las barras de Gly99 y Gly100 de r1 se descartan al mirar las 3 réplicas?
3. Si las 9 mutaciones suman +3.8 (desfavorable), ¿puede la mejora de afinidad venir de ellas?

---

## 9. Anexo: solo las 9 posiciones mutadas, solo la réplica r1
Script: `scripts/figuras_mutaciones.py`. Figuras: `figuras/F_mutaciones_dG_r1.png`, `F_mutaciones_ddG_r1.png`, `F_mutaciones_componentes_r1.png`. Tabla: `tablas/mutaciones_r1.txt`. Las posiciones no se escogen por su efecto: son las 9 que difieren en la secuencia (parte A), así que no hay sesgo de selección.

| Mutación | Antes → después | Tipo | ¿Toca la RNasa en 2B? | ΔG_i 2A | ΔG_i 2B | ΔΔG_i | vdW | Electrost. | Solv. polar | No polar |
|---|---|---|---|---|---|---|---|---|---|---|
| A28P | Ala → Pro | apolar → apolar | No | −0.03 | −0.14 | −0.11 | −0.03 | −0.32 | +0.22 | +0.01 |
| Y29W | Tyr → Trp | arom. → arom. | Sí | −2.49 | −2.69 | −0.20 | −0.83 | +3.54 | −2.70 | −0.21 |
| **Y101D** | Tyr → Asp | arom. → (−) | Sí | −5.36 | +1.43 | **+6.79** | +1.27 | −21.96 | +27.39 | +0.08 |
| E102A | Glu → Ala | (−) → apolar | No | +0.12 | +0.01 | −0.10 | +0.02 | +10.92 | −11.05 | 0.00 |
| R104V | Arg → Val | (+) → apolar | No (en 2A sí) | −0.10 | −0.08 | +0.02 | +0.27 | −10.71 | +10.42 | +0.04 |
| D105A | Asp → Ala | (−) → apolar | No | +0.66 | +0.08 | −0.59 | +0.05 | +9.65 | −10.28 | 0.00 |
| **R106T** | Arg → Thr | (+) → polar | Sí | −3.66 | −1.12 | **+2.54** | +0.54 | +4.04 | −2.29 | +0.25 |
| **T107R** | Thr → Arg | polar → (+) | Sí | −3.23 | −5.64 | **−2.42** | −1.53 | +4.89 | −5.63 | −0.15 |
| Q110R | Gln → Arg | polar → (+) | Sí (en 2A no) | −0.21 | −0.19 | +0.02 | −0.94 | +0.04 | +1.23 | −0.32 |
| **Suma** | | | | −14.29 | −8.34 | **+5.95** | | | | |

(arom. = aromático; (+) y (−) = aminoácido con carga.)

**Por qué unas cambian mucho y otras no**
- **Cambian mucho:** Y101D, R106T y T107R. Las tres **tocan la RNasa** y **cambian de carácter químico**: Y101D pasa de un aromático grande a una carga negativa; R106T pierde una carga positiva; T107R gana una carga positiva.
- **R106T y T107R se compensan:** +2.54 y −2.42 suman **+0.12**. La arginina que formaba el puente salino con Glu111 "se corre una posición". Neto: ≈ 0.
- **Casi todo el +5.95 viene de Y101D (+6.79).** El resto de las mutaciones suma −0.84.
- **No cambian:** A28P, E102A, R104V y D105A no tocan la RNasa en 2B (en R104V, Arg104 contribuía solo −0.10 en 2A). Y29W cambia un aromático por otro (−0.20) y Q110R gana una carga sin pareja cercana (+0.02).

Lectura:
- Tres mutaciones concentran el cambio: Y101D (+6.8), R106T (+2.5) y T107R (−2.4). La suma de las nueve es +5.95 (desfavorable).
- **E102A, R104V y D105A** son mutaciones de cargas que no tocan la RNasa: su electrostática cambia ±10 y su solvatación polar cambia ∓10, y el total del residuo queda en ≈ 0 (−0.10, +0.02, −0.59). Es la compensación de la parte E vista residuo a residuo.
- Los errores de las barras son del trayecto r1 (bloques de 100 ps) y subestiman la incertidumbre real.
