# Explicación básica de las figuras (carpeta `figuras/`)

Lectura figura por figura, en el orden de `C_analisis/figuras/`. Para cada una: qué es cada eje, qué se ve y qué se concluye. Para el análisis estadístico y las frases de presentación, ver `Guia_graficas.md`.

## Antes de empezar
- La simulación guardó **1001 instantáneas**, una por picosegundo (ps). Cada gráfica toma **un número por instantánea** y lo pone en el eje Y. El eje X es siempre el tiempo, de 0 a 1000 ps.
- **En estas figuras, azul = 2A y naranja = 2B.** En xmgrace es distinto (negro = 2A, rojo = 2B). Mira siempre la leyenda.
- `prom.` en la leyenda es el promedio de **los 1000 ps enteros**. Las tablas del informe usan solo **500–1000 ps** para quitar la relajación inicial, por eso los números cambian un poco (puentes de H: 6.03 y 6.92 aquí, 6.19 y 7.22 en la tabla).
- Las distancias están en **nm**: 0.15 nm = 1.5 Å.

---

## Verificaciones de que la simulación está bien hecha

### `B5_potencial_2A_vs_2B.png` (minimización)
- **Eje X:** paso de minimización (0 a ~1400). **Eje Y:** energía potencial del sistema (kJ/mol).
- **Se ve:** la energía baja muy rápido al principio y luego casi se aplana. 2A termina en −1.416 millones y 2B en −1.435 millones.
- **Significa:** la minimización funcionó: se movieron los átomos hasta que las fuerzas fueron pequeñas y la curva se aplanó.
- **No significa:** que 2B tenga "menos energía" que 2A. Los dos sistemas tienen distinto número de átomos y esas energías no se comparan.

### `B8_temperatura_2A_vs_2B.png`
- **Eje Y:** temperatura (K).
- **Se ve:** los dos oscilan entre ~295 y ~301 K; el promedio de ambos es **298 K**.
- **Significa:** se mantuvo la temperatura pedida durante toda la producción. Las oscilaciones de ±2 K son normales en ~90 000 átomos.

### `B8_densidad_2A_vs_2B.png`
- **Se ve:** la densidad se queda en ~994 kg/m³ en los dos.
- **Significa:** el agua tiene la densidad esperada para el modelo TIP3P. Que 2A y 2B difieran en menos de 1 kg/m³ no tiene importancia.

---

## RMSD: cuánto se mueve la proteína
El **RMSD** es la distancia promedio entre cada átomo Cα en ese instante y su posición en la primera instantánea, después de superponer las estructuras para quitar traslaciones y giros. Empieza en 0 porque la primera instantánea se compara consigo misma.

### `C2_rmsd_complejo_2A_vs_2B.png`
- **Eje Y:** RMSD del complejo completo (nm).
- **Se ve:** suben rápido durante ~100 ps hasta ~0.13 nm y luego oscilan entre 0.10 y 0.21 nm. Promedios: 0.150 nm (2A) y 0.145 nm (2B), es decir **~1.5 Å** en los dos.
- **Significa:** los dos complejos se mantienen estables. 1.5 Å es un movimiento pequeño y normal, y las curvas no suben sin parar.
- **No significa:** convergencia termodinámica; solo que se estabilizaron en 1 ns.

### `C2_rmsd_nanobody_2A_vs_2B.png`
- **Qué mide:** solo el nanobody, superpuesto sobre sí mismo: cuánto cambia **su forma**.
- **Se ve:** 2A en ~1.5 Å y 2B en ~0.9 Å.
- **Significa:** en esta simulación el nanobody de 2B cambia menos de forma. La diferencia (0.65 Å) es mucho mayor que la oscilación de cada curva.

### `C2_rmsd_antigeno_2A_vs_2B.png`
- **Qué mide:** lo mismo para la RNasa.
- **Se ve:** 2B en ~0.9 Å y 2A en ~1.2 Å, con 2A bajando de 1.3 a 1.0 Å al final.
- **Significa:** la RNasa también es estable en ambos; la diferencia es menos clara que en el nanobody.

### `C2_rmsd_nanobody_sobre_antigeno_2A_vs_2B.png`
- **Qué mide:** se superpone la RNasa en cada instantánea y se mide cuánto se mueve el nanobody **respecto a ella**. No mide su forma, mide su posición relativa.
- **Se ve:** valores más altos que las otras curvas, entre 0.13 y 0.45 nm. Promedios del ejercicio completo: 0.251 nm (2A) y 0.288 nm (2B). Las curvas se cruzan varias veces.
- **Significa:** el nanobody cambia de posición sobre la RNasa más de lo que cambia su propia forma; algo más en 2B, pero la diferencia es del tamaño de las oscilaciones.
- **No significa:** que 2B se mueva claramente más.

---

## Contactos de la interfaz

### `C3_contactos_4A_2A_vs_2B.png` (pares de átomos a < 0.4 nm)
- **Eje Y:** cuántos pares (átomo del nanobody, átomo de la RNasa) están a menos de 0.4 nm en cada instantánea (incluye hidrógenos).
- **Se ve:** las curvas se solapan casi por completo, entre 450 y 690. Promedios: 555 (2A) y 564 (2B).
- **Significa:** el número de contactos es prácticamente el mismo. La diferencia (~9) es pequeña frente a la oscilación (±37).

### `C3_puentes_H_2A_vs_2B.png`
- **Eje Y:** número de puentes de hidrógeno entre nanobody y RNasa en cada instantánea. Es un entero (4, 5, 6...), por eso la curva tiene forma de escalones.
- **Se ve:** en los primeros ~200 ps las dos están entre 5 y 7. Después 2B sube y pasa mucho tiempo en 8 o más; 2A se queda entre 5 y 7. Promedios: 6.03 y 6.92.
- **Significa:** en esta simulación 2B tiene en promedio ~1 puente de H más, y la diferencia aparece tras ~200 ps.
- **No significa:** que sea la causa de la mejora de afinidad (una sola réplica).

### `C3_distancia_minima_2A_vs_2B.png`
- **Eje Y:** distancia entre el par de átomos más cercano del nanobody y de la RNasa en cada instantánea.
- **Se ve:** las dos oscilan alrededor de 0.17 nm. Promedios: 0.1745 y 0.1699 nm (1.75 y 1.70 Å).
- **Significa:** en todo momento hay dos átomos de las cadenas a menos de 2 Å: **las proteínas nunca se separan**. La diferencia entre sistemas no importa; esta figura solo comprueba que el complejo se mantiene unido, y no sirve para decir cuál une mejor.

---

## Contactos concretos

### `C4_salino_Arg_Glu111_2A_vs_2B.png`
- **Qué mide:** distancia entre el átomo central de la arginina (Arg106 en 2A, Arg107 en 2B) y el átomo central del Glu111 de la RNasa (nm). Es el puente salino.
- **Se ve:** 2A se mantiene en ~0.40–0.45 nm casi todo el tiempo (promedio 0.436). 2B está en ~0.45–0.55 y de vez en cuando sube a 0.7–0.8 (promedio 0.514).
- **Significa:** el puente salino se conserva en los dos, pero **en 2B se separa con más frecuencia**: es menos estable (78 % frente a 96 % del tiempo).
- **Aclaración:** estos valores son mayores que los 2.9–3.3 Å de los cristales porque aquí se mide entre los átomos centrales de cada grupo, no entre el N y el O más cercanos.

### `C4_Tyr27_Gln60_2A_vs_2B.png`
- **Qué mide:** distancia entre el O de la Tyr27 del nanobody y el O de la Gln60 de la RNasa (nm).
- **Se ve:** las dos están en ~0.40 nm (2A: 0.391; 2B: 0.402), con oscilaciones entre 0.30 y 0.54.
- **Significa:** en el cristal de 2B esa distancia era 2.64 Å (puente de H); en la simulación está en ~4.0 Å en los dos sistemas, más allá de un puente de H (~3.5 Å). **El acortamiento del cristal no se mantiene en solución.**

---

## Resumen

| Figura | Resultado |
|---|---|
| B5, B8 temperatura, B8 densidad | La simulación está bien hecha |
| RMSD complejo | Los dos complejos son estables y casi iguales |
| RMSD nanobody | 2B conserva mejor su forma interna |
| RMSD antígeno | Estable en ambos |
| RMSD nanobody sobre antígeno | Se desplaza algo más en 2B, dentro del ruido |
| Contactos | Igual cantidad en 2A y 2B |
| Puentes de H | ~1 más en 2B desde ~200 ps (una réplica) |
| Distancia mínima | Las cadenas nunca se separan |
| Puente salino | Se conserva, pero es menos estable en 2B |
| Tyr27–Gln60 | El acortamiento del cristal no persiste |

## Preguntas de comprobación
1. Si el RMSD del complejo es igual en 2A y 2B pero el del nanobody es distinto, ¿qué parte del complejo explica esa diferencia?
2. En `C3_distancia_minima` los dos sistemas dan ~0.17 nm. ¿Por qué esa figura no sirve para decir qué sistema une mejor?
