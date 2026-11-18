# Proyecto final: MD y energía libre en ingeniería de proteínas (Pareja 2)

Complejo **nanobody (cadena B) – RNasa A (cadena A)**.
System_2A = inicial (KD 23 nM) · System_2B = madurada (KD 0.15 nM) · ΔΔGexp ≈ −2.98 kcal/mol

**Origen de las estructuras:** VHH cAb-RN05 de dromedario unido a RNasa A bovina. System_2A viene de PDB [2P49](https://www.rcsb.org/structure/2P49) (1.38 Å) y System_2B de [2P4A](https://www.rcsb.org/structure/2P4A) (1.90 Å). Artículo: Koide et al., *J. Mol. Biol.* 2007, 373:941 ([DOI](https://doi.org/10.1016/j.jmb.2007.08.027)). Detalles en [A_inspeccion](A_inspeccion/A_inspeccion_inicial.md#a1b-origen-de-las-estructuras).

**Para estudiar y presentar:** empieza por [GUIA_COMPLETA.md](GUIA_COMPLETA.md) (biología desde cero, comandos para ver cada resultado) y [INFORME_FINAL.md](INFORME_FINAL.md).

| Carpeta | Contenido | Entrega |
|---|---|---|
| [00_enunciado/](00_enunciado/) | Instrucciones del proyecto (.docx) | — |
| [01_estructuras/](01_estructuras/) | PDB de partida (System_2A, System_2B) | — |
| [A_inspeccion/](A_inspeccion/A_inspeccion_inicial.md) | Alineamiento, superposición, interfaz, contactos | 1 |
| [B_dinamica/](B_dinamica/B_dinamica_molecular.md) | MD en GROMACS (2A y 2B) | 1 |
| [C_analisis/](C_analisis/C_analisis_estructural.md) | RMSD, contactos en el tiempo, entorno de las mutaciones | 1 |
| [D_F_energia/](D_F_energia/D_F_energia_libre.md) | gmx_MMPBSA, componentes, descomposición | 2 |
| [scripts/](scripts/) | `graficar_xvg.py`: grafica .xvg · `analisis_energia.py`: componentes y descomposición de gmx_MMPBSA | — |
| [referencia_clase_gromacs/](referencia_clase_gromacs/) | Ejercicio guiado de clase (plantilla del protocolo) | — |

Cada parte tiene un documento `.md` con su letra y tema (por ejemplo `A_inspeccion_inicial.md`), con lo que se hizo, los comandos usados, los resultados y su interpretación.

## Estado actual
| Parte | Estado |
|---|---|
| A. Inspección | Completa |
| B. MD de 2A y 2B | Completa (Colab, A100); resultados en `B_dinamica/2A_colab/` y `2B_colab/` |
| C. Análisis estructural | Completa |
| D–F. Energía | Completa (gmx_MMPBSA en Colab; análisis con `scripts/analisis_energia.py`) |

## Hallazgos hasta ahora
- 9 mutaciones, todas en CDR1 y CDR3; el antígeno es igual en los dos sistemas.
- El nanobody está desplazado respecto a la RNasa entre variantes: 2.1 Å en cristales y 2.6 Å en MD, en el orden de su oscilación propia.
- La interfaz conserva su tamaño pero cambia de composición: Arg110 y Thr30 entran, Arg104 sale.
- En MD 2B tiene ~1 puente de H más (6.2 → 7.2), pero con pérdidas parciales: el puente salino con Glu111 y el enlace con Tyr115 son menos estables.
- MM/GBSA, 3 réplicas por sistema: ΔΔGcalc = +1.4 ± 4.5 kcal/mol (exp. −2.98). La réplica original daba −2.22, pero la variabilidad entre réplicas supera la diferencia: el método no resuelve 2A vs 2B con 1 ns.
- Reproducible entre réplicas: pérdida de Tyr101→Asp (+6.5), ganancia de Arg107 (−2.7) y de Gln69 de la RNasa (−2.0).
