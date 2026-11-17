# Informe final — Pareja 2 (System_2A → System_2B)

Nanobody cAb-RN05 contra RNasa A. KD 23 nM → 0.15 nM; ΔΔGexp = −2.98 kcal/mol.
Detalle y datos: [A](A_inspeccion/A_inspeccion_inicial.md) · [B](B_dinamica/B_dinamica_molecular.md) · [C](C_analisis/C_analisis_estructural.md) · [D–F](D_F_energia/D_F_energia_libre.md).

## Resumen
Las dos estructuras son casi iguales (0.99 Å global), pero 9 mutaciones en CDR1 y CDR3 reorganizan la interfaz. MM/GBSA reproduce el signo y el orden de magnitud del cambio de afinidad (ΔΔGcalc = −2.22 ± 0.99 kcal/mol). La ganancia no viene de las mutaciones sumadas (+6 kcal/mol, desfavorables) sino de residuos vecinos no mutados: la mejora es cooperativa.

## Respuestas
1. **Modificaciones.** 9 mutaciones, todas en CDR1 (A28P, Y29W) y CDR3 (Y101D, E102A, R104V, D105A, R106T, T107R, Q110R). En contacto directo con el antígeno en 2B: Y29W, Y101D, R106T, T107R, Q110R. R104V elimina un contacto de 2A. A28P, E102A y D105A no tocan el antígeno (efecto indirecto).
2. **Similitud real.** Cada cadena conserva su forma, pero el nanobody se desplaza 2.1 Å respecto a la RNasa en el cristal y 2.6 Å en MD, del orden de su oscilación propia. La interfaz conserva su tamaño y cambia de composición (entran Arg110 y Thr30, sale Arg104).
3. **Origen de la mejora.** Hay diferencia energética: ΔΔG = −2.22 kcal/mol, con ~−1.3 de balance electrostático/solvatación (menor penalización de desolvatación polar) y ~−0.9 de vdW; el no polar no cambia. La electrostática directa por sí sola empeora un poco.
4. **¿Individual o cooperativo?** Cooperativo. Las 9 posiciones mutadas suman +5.95 kcal/mol (Tyr101→Asp +6.8, Arg106→Thr +2.5; Thr107→Arg −2.4). La ganancia está en residuos no mutados del nanobody (Gly99, Gly100, Tyr27, Tyr33: −5.4) y de la RNasa (Gln69, Lys61, Tyr73: −2.5 neto).
5. **Mapa energético.** Cambió. Hotspots en 2A: Tyr101, Tyr115, Ile32, Glu111, Arg106. En 2B: Arg107, Ile32, Thr70, Gln69, Tyr115. Tyr115 y Glu111 de la RNasa pierden peso, lo que coincide con su debilitamiento en la MD (parte C).
6. **Acuerdo con el experimento.** Signo correcto y magnitud cercana (−2.2 vs −3.0), con origen coherente. Cautela: una réplica de 1 ns, el SEM subestima el error real, MM/GBSA sin entropía (los ΔG absolutos ≈ −50 no son comparables) y 2A conserva 2 residuos de etiqueta que 2B no tiene.

## Limitaciones y mejoras
Réplicas independientes, trayectorias más largas, comparación con PB o `igb=5`, y estimación de entropía.
