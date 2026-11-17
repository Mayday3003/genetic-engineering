# Informe final — Pareja 2 (System_2A → System_2B)

Nanobody cAb-RN05 contra RNasa A. KD 23 nM → 0.15 nM; ΔΔGexp = −2.98 kcal/mol.
Detalle y datos: [A](A_inspeccion/A_inspeccion_inicial.md) · [B](B_dinamica/B_dinamica_molecular.md) · [C](C_analisis/C_analisis_estructural.md) · [D–F](D_F_energia/D_F_energia_libre.md).

## Resumen
Las dos estructuras son casi iguales (0.99 Å global), pero 9 mutaciones en CDR1 y CDR3 reorganizan la interfaz. Con una sola trayectoria MM/GBSA daba ΔΔG = −2.22 kcal/mol, cercano al experimental (−2.98). Con 3 réplicas por sistema el resultado es **ΔΔG = +1.4 ± 4.5**: la variabilidad entre réplicas supera la diferencia, así que **el método (GB, 1 ns, sin entropía) no reproduce de forma fiable la mejora de afinidad**. Sí son reproducibles cambios locales: se pierde el hotspot Tyr101 (+6.5), gana Arg107 (−2.7) y gana Gln69 de la RNasa (−2.0).

## Respuestas
1. **Modificaciones.** 9 mutaciones, todas en CDR1 (A28P, Y29W) y CDR3 (Y101D, E102A, R104V, D105A, R106T, T107R, Q110R). En contacto directo en 2B: Y29W, Y101D, R106T, T107R, Q110R. R104V elimina un contacto de 2A. A28P, E102A y D105A no tocan el antígeno (efecto indirecto).
2. **Similitud real.** Cada cadena conserva su forma, pero el nanobody se desplaza 2.1 Å respecto a la RNasa en el cristal y 2.6 Å en MD, del orden de su oscilación propia. La interfaz conserva su tamaño y cambia de composición (entran Arg110 y Thr30, sale Arg104).
3. **Origen de la mejora.** No queda demostrado con este modelo: ΔΔG(3 réplicas) = +1.4 ± 4.5 (r1 sola: −2.2). Lo reproducible es un cambio local de la interfaz, no del tamaño (el término no polar no cambia) ni de la geometría global.
4. **¿Individual o cooperativo?** Las 9 posiciones mutadas suman +3.8 kcal/mol (desfavorables), con Tyr101→Asp (+6.5) y Arg106→Thr (+1.3) perdidos y Thr107→Arg (−2.7) ganado; la RNasa suma −1.9 (Gln69 −2.0). El efecto cooperativo en residuos no mutados del nanobody que mostraba r1 no se reproduce, por lo que no se puede afirmar con estos datos.
5. **Mapa energético.** Cambia en lo local: 2A se apoya en Tyr101, 2B en Arg107 y en Gln69 de la RNasa. Los cambios de Tyr115 y Glu111 (vistos en r1 y en la parte C) quedan dentro del ruido entre réplicas.
6. **Acuerdo con el experimento.** Con una réplica parecía bueno (−2.2 vs −3.0); con tres no hay acuerdo concluyente (+1.4 ± 4.5; 5 de 9 combinaciones con signo correcto). Falta entropía, muestreo (réplicas con estructuras distintas, más de 1 ns) y quizá otro modelo de solvatación (PB). La variabilidad en EEL y GB (±10 kcal/mol, compensados entre sí) es la principal fuente de ruido.

## Limitaciones y mejoras
Más réplicas con estructuras de partida distintas, trayectorias más largas (≥10 ns), comparación con PB o `igb=5`, y estimación de entropía.
