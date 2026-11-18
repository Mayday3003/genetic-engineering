# Guion de la presentación — Pareja 2 (System_2A → System_2B)

Tiempo total: **~14 min** (12 diapositivas). Versión corta de **~8 min**: diapositivas 1, 3, 4, 6, 7, 9, 11 y 12.
Todos los comandos se ejecutan desde la raíz del proyecto. **Antes de empezar:** abre las figuras y PyMOL (sección 4).

## 0. El mensaje central (memorízalo)
> Un nanobody se mejoró en el laboratorio con 9 mutaciones y une a la RNasa ~153 veces más fuerte, aunque su estructura es casi idéntica. Simulamos las dos variantes en agua y vimos que la interfaz **no crece, se reorganiza**: la mutación Y101D pierde un contacto clave, el puente salino con Glu111 pasa de la Arg106 a la Arg107, y hay ~1 puente de H más en 2B. **El cálculo de energía (MM/GBSA) acertó con una réplica (−2.2 frente a −2.98), pero con tres réplicas no distingue las variantes (+1.4 ± 4.5)**: el método, con 1 ns, no es lo bastante preciso.

---

## 1. Diapositiva 1 — Título y pregunta (0:30)
**Decir:** "Estudiamos cómo 9 mutaciones aumentan 153 veces la afinidad de un nanobody por la RNasa A, si las estructuras son casi iguales. Usamos dinámica molecular y energía libre."
**Pregunta guía:** ¿Qué cambia en la interfaz y puede el cálculo explicar la mejora?

## 2. Diapositiva 2 — El sistema (1:00)
**Mostrar:** `A_inspeccion/figuras/A3_superposicion.png`
**Decir:**
- Complejo nanobody (cadena B) – RNasa A (cadena A). 2A es la variante inicial (PDB 2P49, KD = 23 nM); 2B, la madurada (PDB 2P4A, KD = 0.15 nM).
- Mejora de afinidad: 23 / 0.15 ≈ 153 veces.
- ΔΔG experimental = RT·ln(0.15/23) = **−2.98 kcal/mol**. Es el número a reproducir.
- Una diferencia de afinidad de 153× son solo ~3 kcal/mol: un puente de H o uno salino aporta 1–3 kcal/mol.

## 3. Diapositiva 3 — Parte A: las 9 mutaciones (1:00)
**Mostrar:** `bash visualizar/pymol.sh visualizar/A_mutaciones.pml`
**Decir:**
- 9 mutaciones, todas en los lazos CDR1 y CDR3, ninguna en el esqueleto: A28P, Y29W, Y101D, E102A, R104V, D105A, R106T, T107R, Q110R.
- Gly−1/Ser0 (2A) y Lys1 (2B) no son mutaciones: son extremos de la secuencia.
- Cambios de carga: el CDR3 pasa de neutro a +1.
**Si preguntan:** "¿Por qué solo el nanobody?" Porque la RNasa es idéntica; la maduración modifica solo el anticuerpo.

## 4. Diapositiva 4 — Parte A: la interfaz (1:30)
**Mostrar:** `bash visualizar/pymol.sh visualizar/A_interfaz_contactos.pml`
**Decir:**
- Interfaz = residuos a ≤ 4 Å de la otra proteína.
- **5 mutaciones tocan la RNasa** (Y29W, Y101D, R106T, T107R, Q110R); **R104V** pierde un contacto; **A28P, E102A y D105A** son indirectas.
- **El tamaño de la interfaz no cambia** (1178 → 1165 Å²), pero hay más encaje: pares de átomos a < 4 Å pasan de 100 a 132, y los contactos polares de 10 a 12.
- El nanobody se apoya ~2 Å distinto sobre la RNasa (2.1 Å en el cristal).
- **El puente salino con Glu111 se conserva, pero pasa de Arg106 a Arg107.**
**Cuidado:** el acortamiento de Tyr27–Gln60 en el cristal (3.48 → 2.64 Å) **no se mantiene en la dinámica**; no lo presentes como una ganancia.

## 5. Diapositiva 5 — Parte B: la simulación (1:00)
**Mostrar:** `C_analisis/figuras/B8_temperatura_2A_vs_2B.png`
**Decir:**
- Mismo protocolo para ambos: AMBER99SB-ILDN, agua TIP3P, caja cúbica con margen de 1 nm (~29 000 aguas), iones para neutralizar (4 Cl⁻ en 2A y 6 en 2B).
- Minimización → NVT (100 ps) → NPT (500 ps) → producción de **1 ns**.
- Verificaciones: temperatura 298 K, densidad ~994 kg/m³, presión con promedio de pocos bar (la presión instantánea fluctúa ±80 bar), las cadenas nunca se separan.
**Si preguntan:** "¿Es suficiente 1 ns?" No para convergencia termodinámica; permite un flujo comparativo (lo dice el enunciado).

## 6. Diapositiva 6 — Parte C: RMSD (1:30)
**Mostrar:** `C_analisis/figuras/C2_rmsd_complejo_2A_vs_2B.png` y `C2_rmsd_nanobody_2A_vs_2B.png`
**Decir:**
- RMSD de Cα (500–1000 ps): **complejo 1.57 frente a 1.55 Å**, los dos estables y sin deriva.
- **Nanobody por sí solo: 1.53 (2A) frente a 0.88 Å (2B)**: el de 2B es internamente más rígido.
- Nanobody sobre la RNasa: 2.48 frente a 3.12 Å, pero las curvas se cruzan (dentro del ruido).
- Por qué el complejo es igual y el nanobody distinto: el RMSD del complejo mezcla cambio de forma y desplazamiento relativo, y se compensan.
**Cuidado:** di "equilibrado", no "convergido". Los .xvg están en nm (0.15 nm = 1.5 Å).

## 7. Diapositiva 7 — Parte C: contactos y puentes de H (1:30)
**Mostrar:** `C_analisis/figuras/C3_puentes_H_2A_vs_2B.png` y `C_analisis/figuras/explicativas/Puentes_H_analisis.png`
**Decir:**
- Pares de átomos a < 4 Å: 551 frente a 562 (+11 ± 8): **sin diferencia**.
- **Puentes de H: 6.19 frente a 7.22 (+1.03 ± 0.28)**; 2B tiene 8 o más puentes en el 42 % de los cuadros frente al 6 % de 2A. La diferencia aparece tras ~200 ps.
- El puente salino con Glu111 es **menos estable** en 2B (78 % frente a 96 % del tiempo); los contactos nuevos Asp101–Thr70 (67 %) y Thr106–Gly112 (34 %) son parciales.
- Hipótesis (no demostrada): en 2B el Asp101 forma un puente salino con Arg107 dentro del CDR3 (99 % del tiempo), reemplazando al Asp105–Arg45 de 2A; podría relacionarse con la rigidez.
**Cuidado:** es una réplica. El +1 puente de H es un indicio compatible con la mejora, no una prueba.

## 8. Diapositiva 8 — Parte D: el método de energía (1:00)
**Decir:**
- MM/GBSA estima ΔG de unión = energía(complejo) − energía(nanobody) − energía(RNasa) en 101 instantáneas (500–1000 ps).
- Cuatro términos: vdW, electrostática, solvatación polar (GB) y no polar. No incluye entropía.
- Los valores absolutos (≈ −50) no se comparan con el experimento (−10 a −13); solo se usa **ΔΔG = ΔG(2B) − ΔG(2A)**.

## 9. Diapositiva 9 — Parte D: el resultado (1:30) — **la más importante**
**Mostrar:** `D_F_energia/figuras/D_componentes_ddg.png` (réplica 1) y luego `D_F_energia/figuras/D_replicas_dG.png`
**Decir:**
- **Con una réplica:** ΔΔG = −2.22 ± 0.99: signo y magnitud cercanos al experimental (−2.98).
- **Con tres réplicas:** ΔG de 2A = −50.4, −57.1, −44.0; de 2B = −52.3, −50.3, −44.5. **ΔΔG = +1.36 ± 4.46.**
- La dispersión entre réplicas (4–7 kcal/mol) supera la diferencia buscada (3 kcal/mol): **el método con este muestreo no distingue 2A de 2B**. El −2.2 de la primera réplica fue en parte azar.
- Esto no significa que 2B no una mejor (el experimento lo prueba); significa que nuestro cálculo no lo detecta.

## 10. Diapositiva 10 — Parte E: componentes (1:00)
**Mostrar:** `D_F_energia/figuras/E_compensacion.png` y `D_F_energia/figuras/E_componentes_replicas.png`
**Decir:**
- **Electrostática y solvatación polar se compensan** casi uno a uno (r = −0.94, pendiente −0.80): la electrostática calculada sin agua exagera la atracción y la solvatación lo corrige. Solo su suma tiene sentido físico.
- Con tres réplicas: vdW −2.66 ± 2.88 (apunta a favorable, sin ser significativo), electrostática + solvatación polar +4.09 ± 2.78, **no polar −0.06 ± 0.14 (no cambia)**.
- Lo único afirmable: la contribución no polar no cambia, coherente con que el área enterrada sea igual.

## 11. Diapositiva 11 — Parte F: por residuo (1:30)
**Mostrar:** `D_F_energia/figuras/F_mutaciones_ddG_r1.png` y `D_F_energia/figuras/F_top_ddg_replicas.png`
Opcional en 3D: `bash visualizar/pymol.sh visualizar/F_energia_bfactor.pml`
**Decir:**
- ΔΔG_i = contribución del residuo en 2B − en 2A.
- **Tyr101→Asp pierde un residuo clave** (+6.5 con tres réplicas; −5.2 → +1.3): cambia un aromático grande por una carga que paga desolvatación.
- **Thr107→Arg gana** (−2.7): la arginina nueva forma el puente salino con Glu111. **Arg106→Thr pierde** (+1.3). Juntas, R106T y T107R se compensan (la arginina "se corre" una posición).
- **Gln69 de la RNasa gana** (−2.0).
- **La suma de las 9 mutaciones es desfavorable** (+5.95 en r1; +3.76 con tres réplicas): la mejora no puede venir de la suma de los residuos mutados.
- Con una réplica parecía que ganaban residuos no mutados (Gly99, Gly100); **no se repite en las otras réplicas**.

## 12. Diapositiva 12 — Conclusiones y limitaciones (1:30)
**Conclusiones (lo que sí se sostiene):**
1. Las 9 mutaciones están en CDR1/CDR3; 5 tocan la RNasa. La interfaz **no crece**, se reorganiza.
2. En la dinámica: complejos estables, nanobody de 2B internamente más rígido, ~1 puente de H más y mismo número de contactos.
3. La energía no se distingue entre variantes con tres réplicas (+1.4 ± 4.5). La contribución no polar no cambia, y electrostática y solvatación polar se compensan.
4. A nivel de residuo, Tyr101→Asp pierde, Thr107→Arg y Gln69 ganan; las mutaciones, sumadas, empeoran la unión.

**Limitaciones:** 1 ns y 3 réplicas que parten de la misma estructura; GB sin entropía; 2A conserva Gly−1/Ser0 y le falta Lys1 a la RNasa (lejos de la interfaz).
**Mejoras:** más réplicas con estructuras de partida distintas, ≥10 ns, comparar con PB o `igb=5`, estimar la entropía.

---

## 13. Preparación antes de presentar
```bash
# Figuras (ábrelas antes)
xdg-open A_inspeccion/figuras/A3_superposicion.png
xdg-open C_analisis/figuras/C2_rmsd_complejo_2A_vs_2B.png
xdg-open C_analisis/figuras/C2_rmsd_nanobody_2A_vs_2B.png
xdg-open C_analisis/figuras/C3_puentes_H_2A_vs_2B.png
xdg-open D_F_energia/figuras/D_componentes_ddg.png
xdg-open D_F_energia/figuras/D_replicas_dG.png
xdg-open D_F_energia/figuras/E_compensacion.png
xdg-open D_F_energia/figuras/E_componentes_replicas.png
xdg-open D_F_energia/figuras/F_mutaciones_ddG_r1.png
xdg-open D_F_energia/figuras/F_top_ddg_replicas.png
# Estructuras
bash visualizar/pymol.sh visualizar/A_mutaciones.pml
bash visualizar/pymol.sh visualizar/A_interfaz_contactos.pml
bash visualizar/pymol.sh visualizar/F_energia_bfactor.pml
# Película (primero: bash visualizar/preparar_trayectoria.sh)
vmd -e visualizar/C_trayectoria.tcl
# Informe
less INFORME_FINAL.md
```

## 14. Frases que NO debes decir (y qué decir)
| No decir | Decir |
|---|---|
| "El RMSD converge" | "Se equilibra en ~200 ps; 1 ns no demuestra convergencia" |
| "La rigidez explica la afinidad" | "Es una hipótesis compatible; hay una sola réplica" |
| "Los puentes de H causan la mejora" | "Hay ~1 más en 2B; es un indicio, no una prueba" |
| "Tyr27–Gln60 se acorta en 2B" | "Se acorta en el cristal, pero no persiste en la dinámica" |
| "El CDR3 estaba fijado a la RNasa" | "En 2A el CDR3 se ancla al esqueleto del nanobody (Asp105–Arg45); en 2B se estabiliza con Asp101–Arg107" |
| "La mejora viene de la desolvatación" | "Con una réplica lo parecía; con tres, la parte polar cambia de signo" |
| "El método acierta (−2.2)" | "Con una réplica sí; con tres no distingue las variantes" |
| "La RNasa es negativa" | "La RNasa es básica en conjunto (carga neta +4)" |
| "Interpretamos EEL y GB por separado" | "Solo su suma tiene sentido físico (se compensan)" |

## 15. Preguntas probables
- **¿Por qué 1 ns?** El enunciado lo pide para un flujo comparativo; no demuestra convergencia. Por eso hicimos réplicas.
- **¿Por qué los ΔG son −50 y el experimental −10?** MM/GBSA sin entropía y con agua implícita infla los absolutos; solo se usa la diferencia.
- **¿Por qué se usan los últimos 500 ps?** El sistema se equilibra en ~200 ps; 101 instantáneas dan promedios estables dentro de una trayectoria.
- **¿Qué es GB?** Generalized Born: aproxima el agua como un medio continuo.
- **¿Por qué se compensan EEL y GB?** Ambos dependen de cómo están colocados los grupos cargados: si se acercan, ganan atracción y pierden contacto con el agua.
- **¿Qué falló en el análisis inicial?** El parser de la descomposición por residuo mezclaba el residuo N del nanobody con el de la RNasa; se corrigió.
- **¿Por qué las réplicas parten de la misma estructura?** Solo cambia la semilla de las velocidades; miden el muestreo dinámico, no la incertidumbre estructural. Mejoraría con estructuras de partida distintas.
- **¿Por qué el error de una réplica no basta?** Solo mide la fluctuación dentro de esa simulación, no la variación entre simulaciones.
- **¿Qué haría falta para explicar los 153×?** Más muestreo (réplicas y ≥10 ns), entropía y quizá PB o PBSA.

## 16. Tabla de datos de respaldo
| Dato | 2A | 2B |
|---|---|---|
| KD | 23 nM | 0.15 nM |
| ΔΔG experimental | | −2.98 kcal/mol |
| Área enterrada (cristal) | 1178 Å² | 1165 Å² |
| Pares de átomos < 4 Å (cristal) | 100 | 132 |
| Contactos polares (cristal) | 10 | 12 |
| RMSD complejo (500–1000 ps) | 1.57 Å | 1.55 Å |
| RMSD nanobody | 1.53 Å | 0.88 Å |
| Pares de átomos < 4 Å (MD) | 551 ± 6 | 562 ± 5 |
| Puentes de H (MD) | 6.19 ± 0.07 | 7.22 ± 0.27 |
| Puente salino Arg–Glu111 (ocupación) | 96 % | 78 % |
| ΔG de unión (r1) | −50.11 | −52.33 |
| ΔG de unión (3 réplicas) | −50.4 ± 6.6 | −49.0 ± 4.1 |
| **ΔΔG (r1)** | | **−2.22 ± 0.99** |
| **ΔΔG (3 réplicas)** | | **+1.36 ± 4.46** |
| Suma ΔΔG_i de las 9 mutaciones (r1 / 3 réplicas) | | +5.95 / +3.76 |
