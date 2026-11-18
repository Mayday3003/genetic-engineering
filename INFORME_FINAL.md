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

## Análisis detallado de la interfaz

Mediciones sobre los cristales 2A y 2B. Se reproducen con
`pymol -cq -d "run visualizar/analisis_interfaz.py"` y quedan en
[`A_inspeccion/tablas/analisis_interfaz.txt`](A_inspeccion/tablas/analisis_interfaz.txt).
Criterio de interfaz: residuo con algún átomo a **≤ 4 Å** del otro socio.

### 1. Mutaciones frente a interfaz: son dos listas distintas
Hay 9 mutaciones y 14 residuos del nanobody en la interfaz de 2B. Solo se solapan en parte:

| Grupo | Posiciones | N | Efecto posible |
|---|---|---|---|
| Mutadas **y** en la interfaz | 29, 101, 106, 107, 110 | 5 | Directo |
| Mutadas **fuera** de la interfaz | 28, 102, 104, 105 | 4 | Indirecto (rigidez o forma del lazo) |
| En la interfaz **sin mutar** | 27, 30, 31, 32, 33, 99, 100, 108, 109 | 9 | Solo por su entorno |

Distancia mínima de cada posición a la RNasa (Å): 28 (5.8 → 5.7), 29 (3.3 → 3.5), 101 (3.2 → 3.1), 102 (4.8 → 4.5), 104 (**4.0 → 5.9**, se pierde), 105 (5.9 → 6.0), 106 (2.9 → 2.9), 107 (2.7 → 2.7), 110 (**4.9 → 3.7**, se gana). **Thr30 no mutó** pero pasa de 4.3 a 3.9 Å y entra a la interfaz; en la MD toca el 38 % del tiempo en 2B frente al 1 % en 2A. Es un residuo que cambia de rol por el reacomodo de sus vecinos (Tyr29→Trp), no por su propia mutación. Nota: 4 Å es un corte, no una frontera física (Arg104 está en 4.0 Å, y en la MD su ocupación es de solo 0.26).

### 2. Los dos lados de la interfaz son distintos
| Residuos en la interfaz | Nanobody 2A (13) | Nanobody 2B (14) | RNasa 2A (15) | RNasa 2B (15) |
|---|---|---|---|---|
| Aromáticos (Tyr, Trp) | 6 | 5 | 3 | 3 |
| Apolares (Gly, Ile, Ala, Val, Pro) | 4 | 4 | 4 | 3 |
| Polares neutros (Thr, Asn, Gln, Ser) | 1 | 2 | 6 | 7 |
| Positivos (Arg, Lys) | 2 | 2 | 1 | 1 |
| Negativos (Asp, Glu) | 0 | 1 | 1 | 1 |

- El **nanobody** aporta una superficie rica en aromáticos y glicinas (apilamiento, flexibilidad). La **RNasa** aporta un parche polar (Gln60, Asn62, Gln69, Thr70, Asn71) con un par de cargas opuestas (Lys61, Glu111) que casi se cancelan.
- El lado de la **RNasa casi no cambia** entre 2A y 2B: 14 de sus 15 residuos son los mismos (sale Gly68, entra Ser59). Lo que se reinventa, por diseño, es el nanobody. La RNasa es la cerradura y la maduración talló mejor la llave.

### 3. Cargas en la interfaz
Con el corte de 4 Å:

| | Cargas en la interfaz | Neta |
|---|---|---|
| Nanobody 2A | Arg104 (+), Arg106 (+) | **+2** |
| Nanobody 2B | Arg107 (+), Arg110 (+), Asp101 (−) | **+1** |
| RNasa (2A y 2B) | Lys61 (+), Glu111 (−) | **0** |

Las cargas **negativas** de la interfaz de 2A dependen del corte: con 4 Å la única es Glu111 (RNasa); con 5 Å entra Glu102 del nanobody (a 4.8 Å); con 6 Å, también Asp105 (a 5.9 Å). Glu102 y Asp105 son mutaciones (E102A, D105A), pero **no tocan la RNasa**. Por eso, entre las 9 posiciones mutadas, 2A tiene dos cargas + (Arg104, Arg106) y dos − (Glu102, Asp105), y 2B tiene dos + (Arg107, Arg110) y una − (Asp101): esa lista es otra cuenta, no la de la interfaz.

Cargas netas totales: nanobody **+1 (2A) → +2 (2B)**; RNasa **+4**. La RNasa es básica en conjunto, así que **más carga positiva en el nanobody no atrae por sí sola**; si acaso repele de lejos. Lo que importa es qué carga queda frente a cuál:
- **Puente salino Arg–Glu111:** se conserva, pero cambia de arginina: Arg106–Glu111 (3.34 Å) en 2A y Arg107–Glu111 (3.11 Å) en 2B. Además, Arg104 en 2A estaba a 4.9 Å del Glu111 y se pierde (R104V): en 2A había dos argininas cerca del Glu111 y en 2B una.
- **Las dos cargas nuevas de 2B no tienen pareja opuesta en la RNasa.** Asp101 (−) queda a 7.2 Å del Glu111, que también es negativo; Arg110 (+) queda a 9.5 Å de la Lys61, también positiva. Hacia el antígeno, una carga sin pareja paga la desolvatación sin ganar atracción, lo que encaja con que **Y101D sea la mutación más desfavorable** en la parte energética (ΔΔG_i ≈ +6.5 kcal/mol, reproducible en las 3 réplicas).
- **Pero Asp101 sí tiene pareja dentro del propio nanobody: Arg107.** Forman un puente salino interno (2.9 Å en el cristal; en la MD de 2B la distancia mínima media es 2.9 Å y el contacto está presente el **99 %** del tiempo entre 200 y 1000 ps). Es la carga positiva que "aparece al lado" del Asp101.

### 3b. Puentes salinos internos del CDR3: cambian de lugar
| Sistema | Puente interno (Asp/Glu – Arg) | Cristal | MD (200–1000 ps) |
|---|---|---|---|
| 2A | Asp105 – Arg45 (del esqueleto) | 2.3 Å | 2.8 Å, 100 % |
| 2A | Glu102 – Arg104 | 4.8 Å | 3.9 Å, 53 % |
| 2B | **Asp101 – Arg107** (nuevo) | 2.9 Å | 2.9 Å, 99 % |

En 2A el CDR3 se ancla al esqueleto del nanobody mediante Asp105–Arg45 (y de forma parcial, Glu102–Arg104); en 2B, esas cargas desaparecen (D105A, E102A, R104V) y el CDR3 se estabiliza con un puente nuevo, **dentro del propio lazo** (Asp101–Arg107). **Hipótesis** (no demostrada, una réplica por sistema): esto podría contribuir a que el nanobody de 2B sea internamente más rígido (RMSD 0.88 frente a 1.53 Å) y quede más preorganizado para unirse, lo que reduciría la pérdida de libertad al unirse. Se reproduce con `bash scripts/puentes_salinos_internos.sh`.

### 4. Contactos polares (N/O a ≤ 3.5 Å)
Son 10 en 2A y 12 en 2B:

| Tipo | Contactos |
|---|---|
| **Iguales** (7) | Tyr27–Asn62, Tyr27–Gln60*, Ile32–Asn62, Gly99–Tyr73, Gly99–Tyr115, Gly100–Thr70 (×2) |
| **Se transfieren a otro residuo** (3) | puente salino Arg106→Arg107 con Glu111; Arg106 O→Thr106 O con Gly112 N; Thr107 O→Arg107 O con Tyr115 OH |
| **Nuevos en 2B** (2) | Asp101 OD1–Thr70 N (3.07 Å); Thr106 OG1–Gly112 N (3.10 Å) |

\* Tyr27 no mutó, pero en los cristales su contacto con Gln60 O se acorta de 3.48 a 2.64 Å (0.84 Å): pasa de casi tocar a formar un puente de H. **En la dinámica ese acortamiento no persiste** (500–1000 ps: 3.89 Å con 9 % de ocupación en 2A y 4.17 Å con 2 % en 2B; ver parte C), así que es un indicio del cristal y no una ganancia confirmada en solución.

El **núcleo de la interfaz**, sobre todo los contactos de esqueleto (Gly, Ile y los O/N de la cadena principal), es el mismo en las dos variantes. Cambia la periferia.

### 5. ¿Por qué cambios tan pequeños pueden dar 153× de afinidad?
| Medida (cristal) | 2A | 2B |
|---|---|---|
| Área enterrada | 1178 Å² | 1165 Å² |
| Pares de átomos a < 4 Å | 100 | 132 |
| Contactos polares N/O | 10 | 12 |

1. **La escala es logarítmica.** 153× en KD son solo **2.98 kcal/mol**; cada factor de 10 equivale a 1.36 kcal/mol (RT ln 10). Un puente de H o salino bien formado aporta del orden de 1–3 kcal/mol, así que dos contactos nuevos ya están en ese rango. No hay proporción lineal entre cuánto cambia la estructura y cuánto cambia la KD.
2. **La energía depende mucho de la distancia.** En el cristal, Tyr27–Gln60 pasa de 3.48 a 2.64 Å: de contacto dudoso a puente de H. Es un ejemplo de *por qué* décimas de Å importan, pero ese caso concreto **no se sostiene en la MD** (ocupación de 9 % y 2 %), así que no debe presentarse como una ganancia real de 2B.
3. **Mejor encaje, no más área:** los pares de átomos a < 4 Å suben un 32 % con la misma superficie enterrada, lo que suma vdW.
4. **Lo que el cristal no ve (hipótesis):** en la MD el nanobody de 2B es internamente más rígido (RMSD 0.88 frente a 1.53 Å); si está más preorganizado, pierde menos libertad al unirse. Con una réplica de 1 ns no se puede afirmar.

### 6. Qué se puede y qué no se puede afirmar
- **Sí (en el cristal):** hay contactos nuevos (Asp101–Thr70, Thr106–Gly112; en la MD el de Asp101–Thr70 persiste el 67 % del tiempo y el de Thr106–Gly112 el 34 %), el puente salino con Glu111 pasa a Arg107, y Y101D pierde un residuo importante (reproducible).
- **No:** que la suma de estos cambios dé −2.98 kcal/mol. En las 3 réplicas de MM/GBSA el ΔΔG fue **+1.4 ± 4.5**: el método no distingue las variantes. La explicación estructural es plausible, no una prueba.
- Esto sale de **cristales estáticos**: en la dinámica el puente salino de 2B es menos estable (78 % del tiempo frente a 96 % en 2A), y el análisis electrostático no puede interpretarse sin la desolvatación, porque ambos términos se compensan.

### 7. Puentes de H y contactos en la dinámica (¿es real la diferencia?)
Con la serie temporal de 500–1000 ps (detalle en `C_analisis/C_analisis_estructural.md`, sección C3b):
- **Pares de átomos < 4 Å:** 551 ± 6 frente a 562 ± 5, diferencia +11 ± 8 (cociente 1.4, d = 0.30): **sin evidencia de diferencia.**
- **Puentes de H:** 6.19 ± 0.07 frente a 7.22 ± 0.27, diferencia **+1.03 ± 0.28** (cociente 3.6, d = 0.93). Aunque las curvas se solapan cuadro a cuadro (SD ≈ 1), las distribuciones están desplazadas: 2B tiene 8 o más puentes de H en el 42 % de los cuadros y 2A en el 6 %.
- **Cautela:** una réplica por sistema; el error de 2B está subestimado (crece con el tamaño del bloque). El +1 puente de H es el resultado neto de ganancias (Asp101–Thr70, Thr106–Gly112) y pérdidas (puente salino con Glu111, contacto con Tyr115). Es una hipótesis compatible con la mejora de afinidad (un puente de H ≈ 1–3 kcal/mol), pero con el ΔΔG de MM/GBSA no concluyente no se puede afirmar que sea la causa. Reproducir con `python3 scripts/estadistica_c3.py`.

## Limitaciones y mejoras
Más réplicas con estructuras de partida distintas, trayectorias más largas (≥10 ns), comparación con PB o `igb=5`, y estimación de entropía.
