# C. Análisis estructural

**Estado: completa.** Una réplica de 1 ns por sistema, así que todo es comparativo y no demuestra convergencia.

- Datos: `datos/2A/`, `datos/2B/` · Figuras 2A vs 2B: `figuras/`
- Cálculos: `../B_dinamica/colab/analizar_sistema.sh` y `../scripts/persistencia_interfaz.sh`
- Grupos: antígeno = `Protein_chain1` (cadena A); nanobody = `Protein_chain2` (cadena B). Las selecciones son iguales en los dos sistemas.

- **Cómo leer las gráficas de esta parte (RMSD, puentes de H y contactos), con figuras explicativas y frases modelo:** [`Guia_graficas.md`](Guia_graficas.md). Explicación básica, figura por figura de la carpeta `figuras/`: [`Explicacion_basica_figuras.md`](Explicacion_basica_figuras.md).

### C1. Corrección de PBC
`gmx trjconv -pbc nojump -center` sobre el grupo Protein. Resultado: `proteina.xtc` y `proteina.tpr` en cada carpeta `*_colab/`.

### C2. RMSD de Cα (referencia: inicio de la producción de cada sistema)
Promedio ± desviación entre 500 y 1000 ps, en Å.

| Región | 2A | 2B |
|---|---|---|
| Complejo | 1.57 ± 0.13 | 1.55 ± 0.22 |
| Nanobody (ajustado sobre sí mismo) | 1.53 ± 0.12 | 0.88 ± 0.11 |
| Antígeno (ajustado sobre sí mismo) | 1.21 ± 0.16 | 0.89 ± 0.11 |
| Nanobody ajustando sobre el antígeno | 2.48 ± 0.49 | 3.12 ± 0.65 |

- Los dos complejos son estables y las curvas se aplanan tras ~200 ps.
- En 2B el nanobody es internamente más rígido (0.88 frente a 1.53 Å), lo que sería compatible con una preorganización. Una sola réplica no basta para afirmarlo.
- La posición del nanobody sobre el antígeno oscila más que cada proteína por separado, y algo más en 2B: la unión se mueve como un cuerpo rígido.

**Diferencia entre sistemas.** Ajustando sobre el antígeno:

| Comparación 2A vs 2B | Nanobody | CDR1 | CDR3 |
|---|---|---|---|
| Cristales | 2.08 Å | 1.33 Å | 1.26 Å |
| Estructuras promedio de MD (200–1000 ps) | 2.58 Å | 1.38 Å | 1.67 Å |

El desplazamiento del nanobody visto en los cristales se mantiene en solución. Ojo: su tamaño (~2.6 Å) es parecido a la oscilación propia de cada sistema (2.5–3.1 Å), así que no se puede tratar como una diferencia exacta.

- Por qué el RMSD del complejo coincide aunque el del nanobody difiera (compensación entre cambio de forma y desplazamiento relativo): sección 8 de `../INFORME_FINAL.md`.

### C3. Contactos de la interfaz y persistencia
Promedios entre 500 y 1000 ps.

| Medida | 2A | 2B |
|---|---|---|
| Pares de átomos a < 4 Å | 551 ± 37 | 562 ± 37 |
| Puentes de H nanobody–RNasa | 6.2 ± 1.0 | 7.2 ± 1.2 |
| Distancia mínima entre cadenas | 1.74 Å | 1.70 Å |

Persistencia por residuo: fracción de frames entre 200 y 1000 ps con algún átomo pesado a < 4 Å de la RNasa.

| Residuo | 2A | 2B |
|---|---|---|
| 27, 32, 33, 99, 100 | 1.00 | 1.00 |
| 29 | Tyr 0.93 | Trp 0.96 |
| 30 | Thr 0.01 | Thr **0.38** |
| 31 | Tyr 0.80 | Tyr 0.80 |
| 101 | Tyr 1.00 | Asp 1.00 |
| 104 | Arg **0.26** | Val 0.02 |
| 106 | Arg 1.00 | Thr 1.00 |
| 107 | Thr 1.00 | Arg 1.00 |
| 108 | Tyr 0.91 | Tyr 0.99 |
| 109 | Gly 1.00 | Gly 1.00 |
| 110 | Gln 0.18 | Arg **0.85** |
| 1 | Gln 0.34 | Gln 0.00 |

- El tamaño de la interfaz casi no cambia; cambia su composición.
- Los cambios de huella de A4 se confirman: Arg110 se vuelve un contacto persistente, Arg104 pierde el suyo y Thr30, sin estar mutado, entra de forma parcial.
- 2B tiene ~1 puente de H más en promedio, una diferencia cercana a la fluctuación (±1).

### C3b. ¿Es real la diferencia de contactos y puentes de H? (análisis estadístico)
Script: `scripts/estadistica_c3.py` → `datos/estadistica_C3.txt`. Ventana 500–1000 ps; el error es el SEM por bloques (5 bloques de 100 ps), el mismo criterio de la parte D. Los puentes de H son un conteo geométrico automático de GROMACS entre nanobody y RNasa.

| Medida | 2A | 2B | Diferencia 2B − 2A | dif./error | d de Cohen |
|---|---|---|---|---|---|
| Puentes de H (media ± SEM) | 6.19 ± 0.07 | 7.22 ± 0.27 | **+1.03 ± 0.28** | 3.6 | 0.93 |
| Pares de átomos < 4 Å | 551 ± 6 | 562 ± 5 | +11 ± 8 | 1.4 | 0.30 |

Distribución de puentes de H por cuadro (500–1000 ps):

| N.º de puentes de H | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|
| 2A | 5 % | 18 % | 35 % | 36 % | 6 % | 0 % | 0 % |
| 2B | 1 % | 7 % | 22 % | 29 % | 27 % | 13 % | 2 % |

- **Contactos < 4 Å:** las dos curvas se superponen casi por completo. La diferencia (+11 ± 8) es menor que 1.5 veces su error y el tamaño del efecto es pequeño (d = 0.30): **no hay evidencia de más contactos en 2B** en la dinámica. Es coherente con que el área enterrada de los cristales sea igual.
- **Puentes de H:** en la gráfica las curvas también se solapan (las dos oscilan entre ~4 y ~9 en cada cuadro, SD ≈ 1), pero las **distribuciones** sí están desplazadas: 2B pasa más tiempo en 8 o más puentes (42 % de los cuadros frente al 6 % de 2A) y en 2A domina 6–7. La diferencia media (+1.0) es unas 3.6 veces su error dentro de esta trayectoria y el efecto es grande (d = 0.93). Probabilidad de que un cuadro al azar de 2B tenga más puentes que uno de 2A: 73 %.
- **Por qué el solapamiento visual engaña:** cada cuadro tiene una oscilación de ±1 (es un conteo de enteros que cambia con cada vibración), pero la media de 500 cuadros se conoce mucho mejor. Para ver la diferencia hay que comparar medias y distribuciones, no curvas.
- **Error de 2B subestimado:** el SEM de 2B crece con el tamaño del bloque (0.11 → 0.27) y no se estabiliza, es decir, la serie de 2B tiene deriva lenta y los cuadros están correlacionados; su incertidumbre real es mayor que 0.27. El de 2A es plano (0.07).
- **Límite principal:** es **una sola réplica por sistema**. En la parte D vimos que la variación entre réplicas de MM/GBSA es 4–7 veces mayor que el error dentro de una trayectoria; lo mismo puede ocurrir aquí. El +1 puente de H es un indicio, no una prueba.
- **Qué lo compone:** no son 1.0 puentes ganados sin pérdidas. En C4 se ve que ganan Asp101–Thr70 (67 % del tiempo) y Thr106–Gly112 (34 %), y se debilitan Arg–Glu111 (78 % frente a 96 %) y esqueleto 107–Tyr115 (32 % frente a 100 %). El saldo neto es +1.
- **¿Explica la afinidad?** Un puente de H bien formado aporta del orden de 1–3 kcal/mol, que es compatible con los −2.98 kcal/mol, pero MM/GBSA con 3 réplicas no resolvió la diferencia (ΔΔG = +1.4 ± 4.5), así que **no se puede afirmar** que sea la causa.

### C4. Entorno de los residuos mutados
Distancias entre 200 y 1000 ps. "Ocupación" = fracción de frames a < 3.5 Å.

| Interacción | 2A | 2B | Comparación con el cristal (A5) |
|---|---|---|---|
| Puente salino Arg–Glu111 (mín. N–O) | Arg106: 2.86 ± 0.29 Å, 96% | Arg107: 3.20 ± 0.70 Å, 78% | **No se confirma** que sea más corto en 2B: en MD es menos estable |
| Asp101 – Thr70 N (mín. O–N) | no existe | 3.38 ± 0.32 Å, 67% | Se mantiene, con ocupación media |
| Thr106 OG1 – Gly112 N | no existe | 3.89 ± 0.66 Å, 34% | Débil y parcial |
| Esqueleto 106 O – Gly112 N (500–1000 ps) | 2.92 Å, 100% | 2.95 Å, 99% | Se mantiene, es el anclaje común |
| Esqueleto 107 O – Tyr115 OH (500–1000 ps) | 2.81 Å, 100% | 3.65 Å, 32% | **Se debilita en 2B** |
| Tyr27 OH – Gln60 O (500–1000 ps) | 3.89 Å, 9% | 4.17 Å, 2% | El acortamiento del cristal **no persiste** |

### Conclusiones para la entrega 1
1. Los dos complejos son estables durante 1 ns.
2. La maduración no agranda la interfaz: reorganiza qué residuos la forman.
3. Los contactos ganados en 2B son reales pero parciales (Asp101–Thr70, Arg110, Thr30), y hay pérdidas compensatorias: el puente salino y el enlace con Tyr115 son menos estables que en 2A.
4. La lectura estática del cristal (10 → 12 contactos polares) exagera la ganancia: en solución son ~6.2 → 7.2 puentes de H.
5. Con esto no se puede explicar aún una mejora de 2.98 kcal/mol. Eso corresponde a las partes D–F.

Limitaciones: una réplica por sistema, 1 ns, y criterios de distancia sin filtro de geometría en los pares de C4.
