# C. Análisis estructural

**Estado: completa.** Una réplica de 1 ns por sistema, así que todo es comparativo y no demuestra convergencia.

- Datos: `datos/2A/`, `datos/2B/` · Figuras 2A vs 2B: `figuras/`
- Cálculos: `../B_dinamica/colab/analizar_sistema.sh` y `../scripts/persistencia_interfaz.sh`
- Grupos: antígeno = `Protein_chain1` (cadena A); nanobody = `Protein_chain2` (cadena B). Las selecciones son iguales en los dos sistemas.

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
