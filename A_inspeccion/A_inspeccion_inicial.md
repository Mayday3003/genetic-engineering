# A. Inspección inicial

**Estado: completa.**

Preguntas que responde: **1** (qué mutaciones hay y dónde están) y **2** (qué tan similares son las estructuras).

Archivos de esta carpeta:
- `alineamientos/`: alineamientos de Clustal (complejo y nanobody)
- `figuras/`: imágenes de PyMOL para el informe
- `sesiones/`: sesiones de PyMOL (`.pse`), para abrir con `pymol sesiones/<archivo>.pse`

Cómo abrir PyMOL para esta parte (desde la raíz del proyecto):
```bash
cd ~/Documents/githubrepos/genetic-engineering && pymol
load 01_estructuras/System_2A.pdb, wt
load 01_estructuras/System_2B.pdb, mut
```


### A1. Identificar cadenas (nanobody vs antígeno)
- Qué: saber qué cadena es cuál, para definir los grupos de todo el proyecto.
- Cómo: leer la secuencia de cada cadena (alineamientos de Clustal y PDB).
- Resultado (igual en 2A y 2B):
  - **Cadena A = antígeno**: ribonucleasa A pancreática bovina (RNasa A, secuencia `KETAAAKFERQHMDSS...`, ~124 aa).
  - **Cadena B = nanobody (VHH)**: secuencia `QVQLVESGGGLVQAGGSLRLSCAAS...WGQGTQVTVSS`.
  - La numeración de residuos es la misma en los dos PDB, así que una posición equivalente tiene el mismo número.

### A1b. Origen de las estructuras
- Cómo: búsqueda por secuencia en RCSB y comparación de coordenadas con los PDB originales.

| | System_2A | System_2B |
|---|---|---|
| Entrada PDB | 2P49 | 2P4A (cadenas A y B; el cristal trae además C y D) |
| Nanobody | cAb-RN05 original | cAb-RN05 madurado |
| Resolución | 1.38 Å | 1.90 Å |
| R / R-free | 0.156 / 0.185 | 0.184 / 0.218 |
| Grupo espacial | P 1 21 1 | C 2 2 21 |
| Ion en el sitio activo (no incluido en nuestros archivos) | fosfato | sulfato |
| Átomos idénticos al PDB | 1840 de 1862 | 1852 de 1852 |

- Proteínas: RNasa A de *Bos taurus* y VHH de *Camelus dromedarius*, expresado en *E. coli*.
- Referencias: Koide et al., *J. Mol. Biol.* 2007, 373:941 (doi:10.1016/j.jmb.2007.08.027), origen de 2P49 y 2P4A. Estructura original del complejo: PDB 1BZQ, *Structure* 1999, 7:361 (doi:10.1016/S0969-2126(99)80049-5).
- Método del artículo: scanning mutagenesis y maduración con bibliotecas combinatorias sintéticas en yeast display.
- Ojo con la KD: fuentes secundarias citan 180 pM para la variante madurada y el enunciado da 0.15 nM. Falta confirmarlo en el texto completo; para el proyecto se usa el valor del enunciado.
- Diferencias de preparación entre los archivos y los cristales:
  - **Residuos 18-21 de la RNasa en 2A:** no están resueltos en 2P49 (REMARK 465), pero sí aparecen en System_2A. Son los 22 átomos que no coinciden, es decir, un bucle modelado y no experimental. Está a ~24 Å del nanobody.
  - **Ion del sitio activo:** está junto a His12, Lys41 e His119, a ~12 Å del nanobody. No se simuló en ninguno de los dos sistemas.
  - **Agua cristalográfica y conformaciones alternativas:** no están en los archivos.
- Disulfuros: 4 en la RNasa (26-84, 40-95, 58-110, 65-72) y 1 en el VHH (22-96). Están presentes en la topología de 2A y 2B.
- Sitio activo: el nanobody no lo ocupa, pero His119 queda a ~9.5 Å del VHH.

### A2. Alineamiento de secuencia y residuos distintos
- Archivos: `alineamientos/alineamiento_complejo.aln` (complejo completo, cadenas concatenadas) y `alineamientos/alineamiento_nanobody.aln` (solo el nanobody).
- Por qué basta con el nanobody: el antígeno es idéntico en los dos sistemas. La única diferencia es que en 2A falta Lys1, un extremo no resuelto. La maduración de afinidad modifica **solo el anticuerpo**. Alinear el complejo concatenado además mezcla los extremos de las dos cadenas: el "GS" inicial del nanobody de 2A aparece pegado al final del antígeno.
- Ojo: en estos archivos la línea de símbolos (`*`, `.`, `:`) está desplazada y marca como distintos residuos que son iguales. La tabla de abajo se armó comparando posición por posición desde los PDB.

| Pos. (PDB, cadena B) | 2A (inicial) | 2B (madurada) | Región | Comentario |
|---|---|---|---|---|
| −1, 0 | Gly, Ser | — | N-terminal | restos del tag de expresión; no es una mutación |
| 28 | Ala | Pro | CDR1 | |
| 29 | Tyr | Trp | CDR1 | aromático más grande |
| 101 | Tyr | Asp | CDR3 | |
| 102 | Glu | Ala | CDR3 | se pierde una carga (−) |
| 104 | Arg | Val | CDR3 | se pierde una carga (+) |
| 105 | Asp | Ala | CDR3 | se pierde una carga (−) |
| 106 | Arg | Thr | CDR3 | se pierde una carga (+) |
| 107 | Thr | Arg | CDR3 | aparece una carga (+) |
| 110 | Gln | Arg | CDR3 | aparece una carga (+) |
| Antígeno 1 | — | Lys | N-terminal de la RNasa | no resuelto en 2A; no es una mutación |

- Interpretación: hay **9 mutaciones reales**, todas en los CDR (2 en el CDR1 y 7 en el CDR3), y ninguna en el framework. El CDR3 cambia mucho su patrón de cargas. Queda pendiente comprobar en A4–A5 si estas posiciones tocan directamente a la RNasa.

### A3. Superposición estructural (RMSD global / por cadena / por CDR)
- Herramienta: PyMOL, `align <mut sel> and name CA, <wt sel> and name CA, cycles=0`. Con `cycles=0` no se descarta ningún outlier.
- Por qué `cycles=0`: con los valores por defecto, que equivalen al botón Align, PyMOL descarta los átomos que más se mueven. Para el complejo da 0.439 Å, pero calculado solo con 203 de 244 Cα; descarta 41 residuos (~17%). Ese número **oculta** las diferencias locales.

| Región (Cα) | Átomos | RMSD (Å) |
|---|---|---|
| Complejo completo | 244 | 0.990 |
| Nanobody (cadena B) | 121 | 1.100 |
| Antígeno RNasa (cadena A) | 123 | 0.637 |
| CDR1 (B 26-33), ajustado sobre sí mismo | 8 | 0.292 |
| CDR3 (B 99-112), ajustado sobre sí mismo | 14 | 0.246 |

- Interpretación:
  - Todos los valores están por debajo de ~1 Å, así que las estructuras son globalmente muy similares, como dice el enunciado.
  - El nanobody (1.10 Å) varía casi el doble que el antígeno (0.64 Å). Tiene sentido, porque las mutaciones están en el nanobody.
  - Los CDR mutados conservan su **forma interna** (<0.3 Å). Ojo: al alinear un CDR sobre sí mismo solo se compara su forma, no su **posición** respecto al resto del complejo. Eso se mide en A3b.

### A3b. Desplazamiento de las regiones (sin re-ajustar)
- Método: se superpone una sola vez sobre el antígeno (`align ... chain A ..., cycles=0`, 0.637 Å). Después `rms_cur` mide cada región sin volver a mover nada.
- Ojo: `rms_cur` empareja los átomos por nombre de residuo, así que **excluye las posiciones mutadas**. Por eso aparecen 112 en lugar de 121 átomos, 6 de 8 en el CDR1 y 7 de 14 en el CDR3.

| Región (Cα, referencia = antígeno) | Átomos | RMSD (Å) |
|---|---|---|
| Nanobody completo | 112 | **2.126** |
| CDR1 (26-33) | 6 | 1.233 |
| CDR3 (99-112) | 7 | 1.287 |

- Interpretación:
  - El nanobody tiene casi la misma forma interna (1.10 Å), pero **respecto al antígeno se desplaza ~2.1 Å**. Las dos variantes **se apoyan distinto sobre la RNasa**: hay un cambio de orientación o de posición de cuerpo rígido.
  - Incluso los residuos **no mutados** de los CDR cambian de posición más de 1 Å.
  - Esto responde la pregunta 2: la similitud global (~1 Å) oculta un reacomodo de la interfaz.

- CDR incluyendo las posiciones mutadas (`rms_cur ..., matchmaker=-1`, empareja por orden): CDR1 = **1.326 Å** (8 Cα), CDR3 = **1.263 Å** (14 Cα). Son valores muy parecidos a los que excluyen las mutaciones, así que todo el lazo se desplaza, no solo los residuos que mutaron.

- Figura: `figuras/A3_superposicion.png`: superposición alineada sobre el antígeno (gris = 2A, cian = 2B, rojo = mutaciones).

### A4. Localización de mutaciones respecto a la interfaz
- Criterio: residuos del nanobody con algún átomo a ≤ 4 Å del antígeno (`byres (chain B) within 4 of (chain A)`).
- Interfaz del nanobody en 2B (14 residuos): 27 Tyr, 29 Trp, 30 Thr, 31 Tyr, 32 Ile, 33 Tyr (CDR1); 99 Gly, 100 Gly, 101 Asp, 106 Thr, 107 Arg, 108 Tyr, 109 Gly, 110 Arg (CDR3).
- Interfaz en 2A (13 residuos): 27 Tyr, 29 Tyr, 31 Tyr, 32 Ile, 33 Tyr (CDR1); 99 Gly, 100 Gly, 101 Tyr, 104 Arg, 106 Arg, 107 Thr, 108 Tyr, 109 Gly (CDR3).
- Cambios en la huella de contacto (2A → 2B):
  - **Se pierde:** 104 (Arg en 2A, Val en 2B, que ya no toca la RNasa).
  - **Se gana:** 110 (Gln en 2A no contactaba; Arg en 2B sí) y **30 Thr, que no está mutado**.
  - La interfaz cambia de composición aunque el número de residuos sea casi igual (13 → 14).

| Mutación | ¿En la interfaz de 2B? | Tipo |
|---|---|---|
| A28P (CDR1) | no | indirecta: Pro rigidiza la base del lazo |
| Y29W (CDR1) | sí | contacto directo |
| Y101D (CDR3) | sí | contacto directo |
| E102A (CDR3) | no | indirecta |
| R104V (CDR3) | no (en 2A **sí**) | contacto **perdido**: Arg104 tocaba la RNasa en 2A |
| D105A (CDR3) | no | indirecta |
| R106T (CDR3) | sí | contacto directo |
| T107R (CDR3) | sí | contacto directo |
| Q110R (CDR3) | sí (en 2A no) | contacto **nuevo** |

- Interpretación: en 2B, **5 mutaciones están en contacto directo** (Y29W, Y101D, R106T, T107R, Q110R; Q110R es un contacto nuevo). R104V **elimina** un contacto que existía en 2A. A28P, E102A y D105A son indirectas. Además, Thr30, que **no está mutado**, entra en la interfaz: es evidencia de un reacomodo cooperativo. Las indirectas probablemente modulan la conformación y la electrostática del CDR3. En la imagen de la superposición, el CDR3 mutado (en rojo) forma la hélice corta que se mete en la interfaz con la RNasa.

### A5. Contactos de los residuos mutados
- Método: `cmd.find_pairs` en PyMOL entre átomos N/O de los residuos B 29, 30, 101, 104, 106, 107 y 110 y la RNasa (cadena A), con cutoff de 3.5 Å y `mode=0` (sin filtro de geometría). Se usó el mismo criterio en los dos sistemas.
- Sesión guardada: `A_inspeccion/sesiones/A_inspeccion_2A_vs_2B.pse`

| Interacción con la RNasa | 2A (inicial) | 2B (madurada) |
|---|---|---|
| Puente salino con Glu111 | **Arg106** NE–OE2, 3.34 Å | **Arg107** NE–OE1, 3.11 Å |
| Esqueleto 106 O – Gly112 N | 2.90 Å | 2.90 Å |
| Esqueleto 107 O – Tyr115 OH | 2.71 Å | 2.66 Å |
| Cadena lateral 106 OG1 – Gly112 N | — | **Thr106**, 3.10 Å (nuevo) |
| Asp101 OD1 – Thr70 N | — (era Tyr101) | **3.07 Å (nuevo)** |
| **Subtotal (solo los 7 residuos analizados)** | **3** | **5** |
| **Total en toda la interfaz** (cualquier N/O de la cadena B a ≤ 3.5 Å de la cadena A) | **10** | **12** |

- Interpretación:
  1. **El puente salino con Glu111 se conserva, pero cambia de residuo.** En 2A lo forma Arg106 y en 2B lo forma Arg107, una posición más adelante y algo más corto (3.34 → 3.11 Å). El "intercambio" R106T/T107R mantiene esa carga positiva frente a Glu111, como si se hubiera corrido un lugar.
  2. Los dos puentes de H del esqueleto (106 O y 107 O) son idénticos en los dos sistemas. Son el anclaje común del CDR3.
  3. **2B gana 2 puentes de H nuevos**: Asp101 con Thr70 de la RNasa (gracias a Y101D) y Thr106 con Gly112 (gracias a R106T).
  4. Arg104 (2A), Trp29, Thr30 y Arg110 (2B) no forman contactos polares con la RNasa. Su contribución, si existe, sería de van der Waals o hidrofóbica (Trp29) o electrostática de largo alcance (Arg110). Eso se evaluará con la descomposición energética (parte F).
- Contactos polares del resto de la interfaz, presentes en los dos sistemas (residuos no mutados):

| Par nanobody – RNasa | 2A (Å) | 2B (Å) |
|---|---|---|
| Tyr27 OH – Gln60 O | 3.48 | 2.64 |
| Tyr27 OH – Asn62 N | 2.81 | 2.84 |
| Ile32 N – Asn62 OD1 | 2.95 | 2.94 |
| Gly99 O – Tyr73 OH | 2.65 | 2.99 |
| Gly99 O – Tyr115 OH | 3.34 | 3.30 |
| Gly100 O – Thr70 O | 3.38 | 3.15 |
| Gly100 O – Thr70 OG1 | 2.73 | 2.69 |

- Lectura: el balance de toda la interfaz es 10 → 12, con la misma ganancia de 2 contactos. Tyr27 OH – Gln60 O se acorta 0.84 Å sin que Tyr27 haya mutado. El par Gly100 O – Thr70 O es oxígeno con oxígeno de esqueleto, así que es cercanía y no un puente de H real: el criterio solo mide distancia.
- Limitación: son estructuras estáticas. La persistencia de estos contactos se evalúa en la parte C.
- Hipótesis para la parte energética: la mejora de afinidad combina **más puentes de H** con un **reacomodo del CDR3** que conserva el puente salino. Probablemente no se debe a un único residuo.

### A6. Análisis ampliado de la interfaz (cargas, composición y contactos)
- Script: `visualizar/analisis_interfaz.py` (PyMOL) → resultados completos en `tablas/analisis_interfaz.txt`. El desarrollo, las tablas y la interpretación están en la sección *Análisis detallado de la interfaz* de `../INFORME_FINAL.md`.
- Resumen: área enterrada igual (1178 → 1165 Å²) pero más pares de átomos a < 4 Å (100 → 132); interfaz del nanobody rica en aromáticos y glicinas frente a una interfaz de la RNasa polar y casi idéntica entre 2A y 2B; el puente salino con Glu111 se conserva pero pasa de Arg106 a Arg107; las dos cargas nuevas de 2B (Asp101, Arg110) no tienen pareja opuesta cerca.
- Visualización paso a paso en PyMOL: `../GUIA_COMPLETA.md`, sección 14.

### Respuestas parciales
- **Pregunta 1:** 9 mutaciones, todas en CDR. En 2B, cinco están en la interfaz (Y29W, Y101D, R106T, T107R, Q110R), R104V elimina un contacto de 2A y A28P, E102A y D105A no tocan el antígeno.
- **Pregunta 2:** la similitud global (0.99 Å) oculta un desplazamiento del nanobody de 2.13 Å respecto a la RNasa, aunque cada parte conserva casi su forma.
