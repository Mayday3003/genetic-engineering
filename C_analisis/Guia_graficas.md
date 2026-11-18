# Cómo leer las gráficas de la parte C (RMSD, puentes de H y contactos)

Guía para **interpretar, explicar y defender** las gráficas de 2A y 2B. Todas las cifras salen de `datos/` y de `datos/estadistica_C3.txt`.

Figuras para estudiar (se regeneran con `.venv/bin/python scripts/figuras_explicativas.py`):
- `figuras/explicativas/RMSD_4_paneles.png`
- `figuras/explicativas/Puentes_H_analisis.png`
- `figuras/explicativas/Contactos_analisis.png`

Para verlas en xmgrace (negro = primer archivo, rojo = segundo; **los `.xvg` están en nm**, 1 nm = 10 Å):
```bash
xmgrace C_analisis/datos/2A/C2_rmsd_complejo.xvg C_analisis/datos/2B/C2_rmsd_complejo.xvg
```

---

## 1. Antes de interpretar cualquier gráfica: cinco preguntas

1. **¿Qué hay en el eje X?** Tiempo (ps). La producción dura 1000 ps (1 ns).
2. **¿Qué hay en el eje Y y en qué unidades?** Si dice nm, multiplica por 10 para tener Å.
3. **¿Qué es cada curva?** Dos sistemas: 2A (inicial) y 2B (madurada).
4. **¿Qué parte del tiempo se interpreta?** Los primeros ~200 ps son de relajación: la proteína sale de la forma del cristal y se acomoda en agua. Se analiza **500–1000 ps**, cuando ya se ha estabilizado.
5. **¿Cuánto vale el ruido?** Una curva molecular siempre oscila. Lo importante no es cada punto sino la **tendencia y la media**.

---

## 2. RMSD

### 2.1 Qué mide
El **RMSD** (desviación cuadrática media) es una **distancia promedio** entre la proteína en el instante *t* y la proteína en el instante inicial, calculada sobre los átomos de Cα (uno por aminoácido), **después de superponer las dos estructuras** para quitar traslaciones y giros.

- **0 Å** = idéntica a la inicial. Al principio de la curva siempre es ~0.
- **Valor alto** = se ha movido o deformado mucho.
- **No dice "mejor" ni "peor"**: dice cuánto se ha alejado de su punto de partida.

### 2.2 Escala
| RMSD de Cα | Lectura |
|---|---|
| < 1 Å | Casi idéntica a la inicial |
| 1 a 3 Å | **Movimiento térmico normal** de una proteína globular estable |
| > 4–5 Å y creciendo | Algo va mal (despliegue o error de preparación) |

### 2.3 Las cuatro curvas son cuatro preguntas distintas
| Archivo | Cómo se superpone | Qué responde |
|---|---|---|
| `C2_rmsd_complejo` | Todo el complejo sobre sí mismo | ¿Se mantiene el complejo entero? |
| `C2_rmsd_nanobody` | Solo el nanobody sobre sí mismo | ¿Cambia la **forma interna** del nanobody? |
| `C2_rmsd_antigeno` | Solo la RNasa sobre sí misma | ¿Cambia la **forma interna** de la RNasa? |
| `C2_rmsd_nanobody_sobre_antigeno` | Se superpone la RNasa y se mide el nanobody | ¿Cómo se **desplaza** el nanobody respecto a la RNasa? |

Analogía: un ladrillo rígido que se desliza sobre una mesa. Su forma no cambia (RMSD interno bajo) pero su posición sí (RMSD sobre la mesa, alto).

### 2.4 Las fases de una curva de RMSD
1. **Subida inicial (0–~150 ps):** la proteína se relaja desde la forma del cristal. Es esperada.
2. **Meseta con oscilaciones:** el sistema fluctúa alrededor de una forma estable. Eso es "equilibrado".
3. **Deriva:** si sigue subiendo o bajando de forma sostenida, todavía no se ha equilibrado.

"Equilibrado" no es "convergido": que el RMSD se aplane no demuestra que se haya muestreado todo lo importante. Con 1 ns y una réplica, la convergencia termodinámica no se demuestra (lo dice el enunciado).

### 2.5 Nuestros resultados (500–1000 ps, en Å)
| Curva | 2A | 2B | Qué se ve |
|---|---|---|---|
| Complejo | 1.57 ± 0.13 | 1.55 ± 0.22 | Iguales: ambos estables |
| Nanobody (forma interna) | 1.53 ± 0.12 | **0.88 ± 0.11** | 2B es claramente más rígido por dentro |
| RNasa (forma interna) | 1.21 ± 0.16 | 0.89 ± 0.11 | 2B algo menor; la de 2A baja de 1.3 a 1.0 al final |
| Nanobody sobre RNasa | 2.48 ± 0.49 | 3.12 ± 0.65 | 2B se desplaza algo más, pero las curvas se cruzan |

(± es la desviación de la curva, no un error de la media.)

### 2.6 Qué podemos decir
- **Complejo:** "los dos complejos son estables durante 1 ns, con un RMSD de ~1.5 Å y sin deriva". Verdadero y seguro: las curvas se solapan y no suben sin parar.
- **Nanobody:** "el nanobody de 2B conserva mejor su forma interna (0.88 frente a 1.53 Å)". La diferencia (0.65 Å) es mucho mayor que la oscilación (±0.12), por lo que es un resultado claro **en esta trayectoria**.
- **Nanobody sobre RNasa:** "el nanobody se desliza sobre la RNasa más que cada proteína sobre sí misma, y algo más en 2B". Hay que decirlo con cautela: la diferencia (0.64 Å) es del tamaño de la oscilación (±0.5 y ±0.65) y las curvas se cruzan varias veces.
- **Aparente contradicción:** 2B es más rígido por dentro pero se mueve más como bloque. No hay contradicción: son dos RMSD distintos (forma interna frente a posición).

### 2.7 Qué NO podemos decir
- Que "converge": se ha equilibrado, no convergido.
- Que "la rigidez explica la afinidad": es una hipótesis (conectada con el puente salino interno Asp101–Arg107). Una réplica por sistema no basta.
- Que "2B se desplaza más": la diferencia está dentro del ruido.

---

## 3. Puentes de H

### 3.1 Qué cuenta
`gmx hbond` cuenta en cada cuadro los puentes de H entre nanobody y RNasa con un criterio **geométrico**: distancia donante–aceptor ≤ 0.35 nm (3.5 Å) y un ángulo adecuado (≤ 30°). Es un **conteo entero** (4, 5, 6...), por eso la curva es muy ruidosa: un puente puede aparecer y desaparecer en un cuadro.

### 3.2 Cómo leerla
- **El ruido fino (±1) es normal.** No significa nada por sí solo.
- Lo que informa es la **tendencia** (media móvil), la **media** de la ventana, la **distribución** (qué porcentaje de cuadros tiene 6, 7, 8...) y la **evolución por bloques de 100 ps**.

### 3.3 Resultados (500–1000 ps)
| | 2A | 2B |
|---|---|---|
| Media ± SEM | 6.19 ± 0.07 | 7.22 ± 0.27 |
| Diferencia 2B − 2A | **+1.03 ± 0.28** (3.6× su error; d de Cohen = 0.93) |  |
| Cuadros con ≥ 8 puentes | 6 % | **42 %** |

| N.º de puentes en un cuadro | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|
| 2A | 5 % | 18 % | 35 % | 36 % | 6 % | 0 | 0 |
| 2B | 1 % | 7 % | 22 % | 29 % | 27 % | 13 % | 2 % |

### 3.4 Lo que enseña la evolución en el tiempo
En `Puentes_H_analisis.png` (panel de bloques de 100 ps):
- **Los primeros 200 ps son iguales** en 2A y 2B (~5.5).
- Hacia ~200 ps, **2B salta a ~7.4** y se queda más alto, con vaivenes entre 6.5 y 7.9.
- **2A sube despacio** y se queda en torno a 6.

La diferencia no está presente desde el principio: aparece **después de una reorganización** en 2B alrededor de los 200 ps. Eso explica que a simple vista las curvas se vean solapadas en la primera parte y se separen después. También explica por qué el error de 2B es mayor: su serie tiene una deriva lenta.

### 3.5 Qué podemos decir
- "En 2B hay en promedio **~1 puente de H más** en esta trayectoria (7.2 frente a 6.2), y la distribución está desplazada hacia 8–9."
- "La diferencia aparece tras unos 200 ps."
- "Es compatible con la mejora de afinidad (un puente de H aporta del orden de 1–3 kcal/mol)."

### 3.6 Qué NO podemos decir
- **Que ese puente de H sea la causa de la afinidad.** Una réplica; y el ΔΔG de MM/GBSA con 3 réplicas fue +1.4 ± 4.5 (no concluyente).
- **Que sean "+1 puente sin pérdidas".** Se ganan Asp101–Thr70 (67 %) y Thr106–Gly112 (34 %), y se pierden parcialmente el puente salino con Glu111 (78 % frente a 96 %) y esqueleto 107–Tyr115 (32 % frente a 100 %).
- **Que la diferencia es "grande".** Es de ~1 puente sobre ~7, y el error real de 2B es mayor que 0.27 (crece con el tamaño del bloque).

---

## 4. Contactos (pares de átomos a < 4 Å)

### 4.1 Qué cuenta
`gmx mindist -d 0.4` cuenta los **pares de átomos (nanobody, RNasa) a menos de 0.4 nm**. Incluye **todos los átomos, también los hidrógenos**. Por eso da ~550, mientras que en los cristales (sin H, solo átomos pesados) eran ~100–130: **no son comparables entre sí**. Se comparan solo 2A con 2B dentro de la dinámica.

### 4.2 Resultados
| | 2A | 2B |
|---|---|---|
| Media (500–1000 ps) | 551 ± 6 | 562 ± 5 |
| Diferencia 2B − 2A | **+11 ± 8** (1.4× su error; d de Cohen = 0.30) |  |

### 4.3 Qué podemos decir
- "El **número de contactos es prácticamente el mismo**: las curvas se solapan y la diferencia (+11) es menor que 1.5 veces su error."
- "Coincide con el área enterrada de los cristales (1178 frente a 1165 Å²): la interfaz no crece."

### 4.4 Qué NO podemos decir
- Que 2B tenga "más contactos": no hay evidencia.
- Que la interfaz sea igual en composición: el número es igual, pero los residuos que contactan cambian (sale Arg104, entran Arg110 y Thr30). Eso se ve en la persistencia por residuo (C3), no en esta curva.

---

## 5. Cómo comparar dos curvas que se solapan

| Herramienta | Para qué sirve |
|---|---|
| **Media ± error** (SEM por bloques) | Cuánto se conoce el valor medio. Mucho más preciso que el ruido de cada cuadro |
| **Diferencia / error** | Si es > 3 se considera una señal; si es < 2 es indistinguible del ruido |
| **Distribución (histograma)** | Muestra si el desplazamiento es de toda la distribución o de unos pocos cuadros |
| **Evolución por bloques de 100 ps** | Detecta deriva, saltos y si la diferencia es estable |
| **d de Cohen** | Tamaño del efecto: 0.2 pequeño, 0.5 medio, 0.8 o más grande |

Reglas prácticas:
1. **Solapamiento visual ≠ sin diferencia.** El ruido es de un cuadro; la media es de 500.
2. **Pero un error dentro de una trayectoria no es el error real.** Entre réplicas la variación puede ser varias veces mayor (en la parte D fue 4–7 veces).
3. **Mide siempre en la misma ventana** para los dos sistemas (500–1000 ps).

---

## 6. Resumen: qué dice cada gráfica

| Gráfica | Qué se ve | Qué podemos afirmar | Qué no |
|---|---|---|---|
| RMSD complejo | Iguales, ~1.5 Å, sin deriva | Ambos estables | "Convergido" |
| RMSD nanobody | 2B ≈ 0.9 Å frente a 2A ≈ 1.5 Å | 2B más rígido por dentro (en esta réplica) | Que la rigidez explique la afinidad |
| RMSD RNasa | 2B algo menor; 2A baja con el tiempo | Ambas estables | Diferencia concluyente |
| RMSD nanobody sobre RNasa | 2.5 frente a 3.1 Å, curvas cruzadas | El nanobody se desliza como bloque | Diferencia entre sistemas |
| Puentes de H | 6.2 frente a 7.2, 2B salta a ~200 ps | ~1 puente más en 2B (en esta réplica) | Que sea la causa de la afinidad |
| Contactos < 4 Å | 551 frente a 562 | Misma cantidad de contactos | Que 2B tenga más |

---

## 7. Frases modelo para presentar

- "Las dos simulaciones se equilibran en unos 200 ps. Medimos entre 500 y 1000 ps para evitar la relajación inicial."
- "El RMSD del complejo es igual en las dos (≈1.5 Å): los complejos son estables. Lo que las diferencia es la forma interna del nanobody: 0.9 Å en 2B y 1.5 Å en 2A."
- "El número de contactos no cambia (551 frente a 562): la interfaz no crece. Lo que cambia es qué residuos la forman y cuántos puentes de H hay: ~1 más en 2B (7.2 frente a 6.2)."
- "Esa diferencia es un indicio, no una prueba: hay una sola réplica por sistema y el cálculo de energía con tres réplicas no distinguió las dos variantes."

---

## 8. Reproducir
```bash
bash scripts/preparar_entorno.sh                         # una sola vez
python3 scripts/estadistica_c3.py                        # tablas de C3 → datos/estadistica_C3.txt
.venv/bin/python scripts/figuras_explicativas.py         # figuras de esta guía
```
