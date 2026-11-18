# Guía completa del proyecto (para estudiar y presentar)

Esta guía asume que **no sabes biología**. Está pensada para leerla en orden y correr los comandos mientras estudias. Todos los comandos se ejecutan **desde la raíz del proyecto**:

```bash
cd ~/Documents/githubrepos/genetic-engineering
```

**Índice**
0. [Preparar el computador](#0-preparar-el-computador)
1. [La idea en 2 minutos](#1-la-idea-en-2-minutos)
2. [Biología desde cero](#2-biología-desde-cero)
3. [Cómputo desde cero](#3-cómputo-desde-cero)
4. [Mapa del proyecto](#4-mapa-del-proyecto)
5. [Parte A: Inspección inicial](#5-parte-a-inspección-inicial)
6. [Parte B: Dinámica molecular](#6-parte-b-dinámica-molecular)
7. [Parte C: Análisis estructural](#7-parte-c-análisis-estructural)
8. [Partes D, E y F: Energía](#8-partes-d-e-y-f-energía)
9. [Las réplicas (el resultado que más importa)](#9-las-réplicas-el-resultado-que-más-importa)
10. [Respuestas a las 6 preguntas, en simple](#10-respuestas-a-las-6-preguntas-en-simple)
11. [Preguntas que puede hacer el profe](#11-preguntas-que-puede-hacer-el-profe)
12. [Guion y checklist para presentar](#12-guion-y-checklist-para-presentar)
13. [Problemas frecuentes](#13-problemas-frecuentes)
14. [Visualización manual en la consola de PyMOL](#14-visualización-manual-en-la-consola-de-pymol)

---

## 0. Preparar el computador

Ya tienes `gmx` (GROMACS) y `pymol`. Falta Python con sus librerías, una sola vez:

```bash
bash scripts/preparar_entorno.sh
```

Después, los scripts de Python se corren con `.venv/bin/python` en vez de `python3`.

Para abrir imágenes desde la terminal: `xdg-open ruta/imagen.png` (o `display ruta/imagen.png`).

**Herramientas de visualización instaladas** y para qué se usa cada una:

| Herramienta | Para qué | Cómo se abre |
|---|---|---|
| **PyMOL** | Ver estructuras 3D, mutaciones, contactos, películas | `bash visualizar/pymol.sh visualizar/<script>.pml` |
| **VMD** | Ver la trayectoria (película) de la MD | `vmd -e visualizar/<script>.tcl` |
| **xmgrace** | Ver las curvas `.xvg` (RMSD, temperatura, etc.) | `xmgrace archivo.xvg` |
| **xdg-open** | Ver las figuras `.png` | `xdg-open figura.png` |

Los scripts de `visualizar/` ya dejan todo coloreado y listo. **Siempre desde la raíz del proyecto.** Dentro de PyMOL puedes pegar comandos en la línea de abajo; el panel de la derecha activa/desactiva objetos (clic en el nombre).

**Si instalaste PyMOL con Flatpak:** PyMOL corre en un sandbox que **no ve tus carpetas**, por eso los scripts fallaban con `Invalid selection name "wt"` (nunca cargó las estructuras). Por eso se abre siempre con `bash visualizar/pymol.sh ...`, que le da permiso solo a la carpeta del proyecto y funciona se instale como se instale. Para abrir PyMOL a mano con permiso: `flatpak run --filesystem=$PWD org.pymol.PyMOL`.

Antes de ver las películas (partes B y C) corre **una sola vez**:
```bash
bash visualizar/preparar_trayectoria.sh
```

---

## 1. La idea en 2 minutos

- Un **nanobody** es una proteína pequeña (un anticuerpo "mini") que se pega a otra proteína, la **RNasa A**, como una llave en una cerradura.
- Los científicos tomaron un nanobody inicial (**System_2A**, se pega con fuerza media) y lo **mejoraron en laboratorio** cambiando 9 aminoácidos (**System_2B**). Ahora se pega **~153 veces más fuerte**.
- **Misterio:** las dos estructuras 3D se ven casi idénticas. ¿Por qué 2B se pega mucho mejor?
- **Qué hicimos:** simulamos en computador cómo se mueven ambas proteínas en agua (dinámica molecular), medimos cómo cambian las zonas de contacto y calculamos con un método de energía si el computador "predice" que 2B se pega mejor.
- **Resultado final (honesto):** con una simulación el método acertaba (−2.2 vs −2.98 experimental). Con **3 réplicas** vimos que era casualidad: el ΔΔG sale **+1.4 ± 4.5**, no resuelve la diferencia. Sí encontramos cambios locales reproducibles (se pierde Tyr101, se gana Arg107 y Gln69).

---

## 2. Biología desde cero

### 2.1 Proteínas y aminoácidos
Una **proteína** es una cadena de bloques llamados **aminoácidos** (hay 20 tipos). Cada uno tiene nombre, código de 3 letras y de 1 letra (ej. Tirosina = Tyr = Y). Los nombramos con su número de posición: **Tyr101** = la tirosina en la posición 101.

Tipos que aparecen en el proyecto:

| Tipo | Ejemplos | Qué hacen |
|---|---|---|
| Cargados **positivos** | Arg (R), Lys (K) | Atraen cargas negativas |
| Cargados **negativos** | Asp (D), Glu (E) | Atraen cargas positivas |
| Polares sin carga | Thr (T), Gln (Q), Asn (N), Ser (S) | Forman puentes de hidrógeno con agua u otros |
| Aromáticos grandes | Tyr (Y), Trp (W) | Se "apilan" y dan contactos fuertes (vdW) |
| Apolares | Ile (I), Val (V), Ala (A), Pro (P), Gly (G) | Evitan el agua; Gly es la más pequeña y flexible; Pro es rígida |

Una **mutación** como **Y101D** se lee "la Tyr de la posición 101 se cambió por Asp".

### 2.2 Anticuerpo, nanobody, antígeno, CDR
- **Antígeno:** la proteína que se quiere reconocer. Aquí, la **RNasa A** (cadena A en los archivos).
- **Nanobody:** fragmento de anticuerpo de camélido (aquí dromedario) que reconoce al antígeno. Es la **cadena B**. Su nombre es cAb-RN05.
- **CDR (regiones determinantes de complementariedad):** los 3 "lazos" del nanobody que tocan al antígeno. Aquí importan **CDR1** (posiciones ~26–33) y **CDR3** (~99–112). El resto (el "framework") es el esqueleto.
- **Interfaz:** la superficie donde las dos proteínas se tocan.

### 2.3 Afinidad y KD
- **KD** mide qué tan fuerte se pega: **menor KD = más afinidad**. 2A: KD = 23 nM. 2B: KD = 0.15 nM. 23/0.15 ≈ **153 veces** mejor.
- **Maduración de afinidad:** proceso (natural o en laboratorio) que introduce mutaciones y selecciona las que mejoran la unión. 2B salió de ese proceso.

### 2.4 Energía libre: ΔG y ΔΔG
- **ΔG de unión** = energía de pegarse. Más **negativo** = se pega mejor.
- **ΔΔG** = diferencia entre variantes. Aquí: **ΔΔG = ΔG(2B) − ΔG(2A)**. Negativo = la variante mejora.
- Experimental: **ΔΔG_exp = RT·ln(KD,2B / KD,2A) = 0.592 × ln(0.15/23) ≈ −2.98 kcal/mol** (RT = 0.592 kcal/mol a 25 °C). Se puede comprobar:
  ```bash
  python3 -c "import math; print(0.592*math.log(0.15/23))"
  ```
- 1 kcal/mol es una unidad de energía. Un cambio de 3 kcal/mol ≈ 150 veces en KD. Por eso errores de ±4 kcal/mol son enormes.

### 2.5 Las fuerzas que mantienen unidas dos proteínas
- **Puente de hidrógeno (puente de H):** atracción entre un H unido a O/N y otro O/N. Muy direccional.
- **Puente salino:** atracción entre una carga + y una − (Arg/Lys con Asp/Glu). Ej.: Arg106 (o Arg107) con **Glu111** de la RNasa.
- **van der Waals (vdW):** atracción débil por cercanía y buen "encaje" de formas.
- **Electrostática:** fuerza entre cargas.
- **Desolvatación:** para que dos proteínas se toquen deben soltar el agua que tenían pegada. Eso **cuesta energía**. Un residuo cargado puede atraer mucho a su pareja (electrostática favorable) pero costar mucho al soltar agua (desolvatación desfavorable). Por eso **nunca se interpreta electrostática sola**.

---

## 3. Cómputo desde cero

- **Dinámica molecular (MD):** una película en computador. Se calculan fuerzas entre todos los átomos y se avanza en pasos de 2 femtosegundos (2 fs). Aquí: **1 ns (nanosegundo) = 500 000 pasos**. Es muy poco tiempo biológico, por eso hay que ser cautos.
- **Campo de fuerza (AMBER99SB-ILDN):** las "reglas de física" de los átomos. Se usa AMBER porque es el que entiende la herramienta de energía (gmx_MMPBSA).
- **Agua TIP3P y iones (Cl⁻):** la proteína se simula dentro de una caja de ~29 000 moléculas de agua. Los iones neutralizan la carga.
- **Etapas del protocolo (B1–B8):**

  | Etapa | Qué hace | Por qué |
  |---|---|---|
  | B1 topología | Pone hidrógenos y reglas físicas | Los PDB no traen H |
  | B2–B3 caja y agua | Rodea la proteína de agua | La proteína vive en agua |
  | B4 iones | Neutraliza la carga | Una caja cargada da errores |
  | B5 minimización | Quita choques entre átomos | Evita que la simulación "explote" |
  | B6 NVT (100 ps) | Calienta a 298 K | Lleva el sistema a temperatura ambiente |
  | B7 NPT (100 ps) | Ajusta presión y densidad | Que el agua tenga densidad real |
  | B8 producción (1 ns) | La película que se analiza | Es el dato real |

- **RMSD:** cuánto se aleja una estructura de su punto de partida (en Å o nm). Curva que se aplana = sistema estable.
- **Corrección PBC:** la caja se repite en todas direcciones; a veces la proteína "sale" por un lado y entra por el otro. Se corrige antes de medir.
- **gmx_MMPBSA / MM/GBSA:** método **aproximado** para estimar la energía de unión a partir de la simulación. Calcula energía de la proteína sola y en complejo, y trata el agua como un medio continuo (GB). Da **valores absolutos inflados (≈ −50 kcal/mol)** que no se comparan con el experimento; solo sirve para **diferencias (ΔΔG)**, y no incluye entropía.
- **Réplica:** repetir la simulación cambiando la aleatoriedad inicial. Si los resultados cambian mucho entre réplicas, el resultado de una sola no es confiable.
- **SD vs SEM:** SD = qué tanto varían los datos. SEM = SD/√n, el error de la media. Con 3 réplicas se usa el error entre réplicas.

---

## 4. Mapa del proyecto

| Carpeta / archivo | Qué hay | Para qué |
|---|---|---|
| `00_enunciado/` | El enunciado (.docx) | Qué piden |
| `01_estructuras/` | `System_2A.pdb`, `System_2B.pdb` y FASTA | Las dos estructuras de partida |
| `A_inspeccion/` | Alineamientos, figura, sesión PyMOL, informe | Parte A |
| `B_dinamica/` | MDP, scripts, notebook Colab, simulaciones (`2A_colab/`, `2B_colab/`), informe | Parte B |
| `C_analisis/` | Datos `.xvg`, figuras 2A vs 2B, informe | Parte C |
| `D_F_energia/` | Notebooks, resultados, tablas, figuras, informe, `replicas/` | Partes D–F y réplicas |
| `scripts/` | Scripts de Python/bash para gráficas y análisis | Reproducir |
| `visualizar/` | Scripts de PyMOL (`.pml`) y VMD (`.tcl`) listos para abrir | Ver estructuras y películas |
| `INFORME_FINAL.md` | Resumen y respuestas a las 6 preguntas | Entregable principal |
| `GUIA_COMPLETA.md` | Esta guía | Estudiar |

Orígenes: 2A = PDB **2P49**, 2B = PDB **2P4A** (artículo Koide et al., *J Mol Biol* 2007).

---

## 5. Parte A: Inspección inicial

**Qué es:** comparar las dos estructuras **antes** de simular: qué cambió y dónde.
**Por qué:** para saber qué esperar y a qué residuos mirar después.

### Ver los resultados
```bash
# Las secuencias de cada sistema (cadena A = RNasa, cadena B = nanobody)
cat 01_estructuras/System_2A.fasta 01_estructuras/System_2B.fasta

# Alineamiento del nanobody (las diferencias son las mutaciones)
cat A_inspeccion/alineamientos/nanobody_2A_vs_2B.fasta

# Figura de la superposición (gris = 2A, cian = 2B, rojo = mutaciones)
xdg-open A_inspeccion/figuras/A3_superposicion.png

# Informe completo de la parte A
less A_inspeccion/A_inspeccion_inicial.md
```

### Visualizar en 3D
```bash
# 1) Las 9 mutaciones sobre las estructuras superpuestas (gris = 2A, cian = 2B, naranja/rojo = mutaciones)
bash visualizar/pymol.sh visualizar/A_mutaciones.pml

# 2) La interfaz y los contactos polares (rojo = contactos en 2B, amarillo = en 2A)
bash visualizar/pymol.sh visualizar/A_interfaz_contactos.pml

# 3) Lo mismo en VMD (imprime el RMSD de la superposición: 0.64 Å)
vmd -e visualizar/A_mutaciones.tcl

# 4) La sesión de PyMOL que ya hicieron antes
bash visualizar/pymol.sh A_inspeccion/sesiones/A_inspeccion_2A_vs_2B.pse
```
**Qué mirar:** en (1) las mutaciones están todas en los lazos que apuntan a la RNasa (verde). En (2) activa y desactiva `contactos_2A` / `interfaz_2A` en el panel derecho para ver qué contactos aparecen o desaparecen en 2B.

**Comandos útiles dentro de PyMOL** (los escribes en la línea de comandos de abajo):
```
select CDR3, mut and chain B and resi 99-112     # selecciona el lazo CDR3 de 2B
show sticks, CDR3                                # lo muestra con bastones
zoom CDR3                                        # acerca la cámara
label mut and chain B and resi 101 and name CA, "Asp101"
distance d1, mut and chain B and resi 107 and name NH1, mut and chain A and resi 111 and name OE1
```
(la última mide la distancia del puente salino Arg107–Glu111).

### Qué significan los resultados
- **9 mutaciones**, todas en CDR (2 en CDR1: A28P, Y29W; 7 en CDR3: Y101D, E102A, R104V, D105A, R106T, T107R, Q110R). Ninguna en el esqueleto.
- Las diferencias Gly−1/Ser0 (2A) y Lys1 de la RNasa (2B) **no son mutaciones**: son extremos que quedaron resueltos o no.
- **Contacto directo con la RNasa en 2B:** Y29W, Y101D, R106T, T107R, Q110R. R104V **quita** un contacto de 2A. A28P, E102A y D105A son **indirectas** (no tocan el antígeno).
- **RMSD** entre las dos estructuras: 0.99 Å global (muy parecidas), pero el nanobody como un todo se **desplaza ~2.1 Å** respecto a la RNasa: se apoyan distinto.
- Responde las preguntas **1 y 2**.

---

## 6. Parte B: Dinámica molecular

**Qué es:** simular 1 ns de cada sistema con **exactamente el mismo protocolo**.
**Por qué en Colab:** la CPU local tardaría ~11 h; una GPU A100 de Colab tarda minutos (~220 ns/día).

### Ver los resultados
```bash
# Parámetros usados (los mismos para los dos sistemas)
cat B_dinamica/mdp/md.mdp

# Verificaciones: temperatura, densidad, presión, aguas e iones
cat C_analisis/datos/2A/resumen_verificaciones.txt
cat C_analisis/datos/2B/resumen_verificaciones.txt

# Confirmar que la simulación terminó (1001 cuadros = 1 ns)
gmx check -f B_dinamica/2A_colab/proteina.xtc 2>&1 | grep -E "Last frame|Coords"
gmx check -f B_dinamica/2B_colab/proteina.xtc 2>&1 | grep -E "Last frame|Coords"

# Figuras de verificación
xdg-open C_analisis/figuras/B5_potencial_2A_vs_2B.png
xdg-open C_analisis/figuras/B8_temperatura_2A_vs_2B.png
xdg-open C_analisis/figuras/B8_densidad_2A_vs_2B.png

# Informe completo con la tabla de verificaciones
less B_dinamica/B_dinamica_molecular.md
```

### Ver las curvas de verificación (xmgrace)
```bash
# Temperatura y densidad de la producción de 2A y 2B en la misma ventana (cada archivo es una curva)
xmgrace C_analisis/datos/2A/B8_temperatura.xvg C_analisis/datos/2B/B8_temperatura.xvg
xmgrace C_analisis/datos/2A/B8_densidad.xvg C_analisis/datos/2B/B8_densidad.xvg
xmgrace C_analisis/datos/2A/B5_potencial.xvg C_analisis/datos/2B/B5_potencial.xvg   # minimización
```
Esperado: la temperatura oscila alrededor de 298 K y la densidad alrededor de 994 kg/m³, sin tendencias. En xmgrace: clic derecho en la gráfica → *Autoscale* si no ves la curva.

### Ver la película (la simulación)
```bash
bash visualizar/preparar_trayectoria.sh     # solo la primera vez
bash visualizar/pymol.sh visualizar/C_trayectoria.pml          # 2A a la izquierda (gris), 2B a la derecha (cian); botón ▶ abajo a la derecha
vmd -e visualizar/C_trayectoria.tcl         # lo mismo en VMD (ventana principal: barra de animación)
```
**Qué mirar:** que las proteínas se muevan un poco pero no se separen, y las mutaciones (rojo) en la interfaz. En PyMOL, `frame 1`, `frame 500` y `frame 1001` saltan al inicio, medio y final. Cada cuadro = 1 ps.

### Qué significan los resultados (lo que el profe pide verificar)
| Verificación | Resultado | Lectura |
|---|---|---|
| Minimización | Fmax < 1000 en ambos | Convergió bien |
| Temperatura | ~298 K | Bien (objetivo 298) |
| Densidad | ~993.8 kg/m³, estable | Normal para TIP3P |
| Presión | pocos bar, fluctúa ±80 | Normal, la presión instantánea fluctúa mucho |
| Producción | 1 ns completo, complejo sin separarse | Sin problemas |

Diferencias esperadas: 2B tiene más carga (+6 vs +4), por eso 6 Cl⁻ en vez de 4.

### Cómo se reproduciría
Notebook `B_dinamica/colab/Colab_MD_2A_2B.ipynb` con instrucciones en `B_dinamica/colab/Como_usar_Colab.md`. Los scripts `correr_sistema.sh` (etapas B1–B8) y `analizar_sistema.sh` (partes B y C) hacen el trabajo.

---

## 7. Parte C: Análisis estructural

**Qué es:** medir cómo se comportó cada sistema durante el 1 ns.
**Por qué:** ver si hay diferencias locales que el cristal estático oculta.

### Ver los resultados
```bash
less C_analisis/C_analisis_estructural.md

xdg-open C_analisis/figuras/C2_rmsd_complejo_2A_vs_2B.png
xdg-open C_analisis/figuras/C2_rmsd_nanobody_2A_vs_2B.png
xdg-open C_analisis/figuras/C2_rmsd_antigeno_2A_vs_2B.png
xdg-open C_analisis/figuras/C2_rmsd_nanobody_sobre_antigeno_2A_vs_2B.png
xdg-open C_analisis/figuras/C3_contactos_4A_2A_vs_2B.png
xdg-open C_analisis/figuras/C3_puentes_H_2A_vs_2B.png
xdg-open C_analisis/figuras/C4_salino_Arg_Glu111_2A_vs_2B.png
xdg-open C_analisis/figuras/C4_Tyr27_Gln60_2A_vs_2B.png
```

### Ver las curvas con xmgrace (comparar 2A y 2B en la misma ventana)
```bash
xmgrace C_analisis/datos/2A/C2_rmsd_complejo.xvg C_analisis/datos/2B/C2_rmsd_complejo.xvg
xmgrace C_analisis/datos/2A/C2_rmsd_nanobody.xvg C_analisis/datos/2B/C2_rmsd_nanobody.xvg
xmgrace C_analisis/datos/2A/C3_puentes_H.xvg C_analisis/datos/2B/C3_puentes_H.xvg
xmgrace C_analisis/datos/2A/C4_salino_Arg_Glu111.xvg C_analisis/datos/2B/C4_salino_Arg_Glu111.xvg
```
Las figuras en `.png` (`C_analisis/figuras/`) son estas mismas curvas ya con títulos en español.

### Ver los contactos en la película
```bash
bash visualizar/pymol.sh visualizar/C_trayectoria.pml      # 3D: las mutaciones en rojo se mueven con la interfaz
```
Dentro de PyMOL, para ver el puente salino en un cuadro cualquiera (2B):
```
frame 500
distance salino, sim2B and chain B and resi 107 and name NH1+NH2, sim2B and chain A and resi 111 and name OE1+OE2
```
Mide a lo largo del tiempo moviendo el cuadro (`frame 1`, `frame 300`, `frame 800`): verás que la distancia varía más en 2B (ocupación 78 % vs 96 % en 2A).

### Recalcular un número a mano (para entender de dónde sale)
```bash
# RMSD medio del complejo 2A entre 500 y 1000 ps, en Å (el .xvg está en nm)
grep -v '^[#@]' C_analisis/datos/2A/C2_rmsd_complejo.xvg | awk '$1>=500{s+=$2;n++}END{print s/n*10}'
```
Debe dar ≈ 1.57 (tabla de la parte C).

### Regenerar figuras y hacer una gráfica propia
```bash
PATH=$PWD/.venv/bin:$PATH bash scripts/figuras_2A_vs_2B.sh   # todas las figuras 2A vs 2B (usa .venv)
.venv/bin/python scripts/graficar_xvg.py C_analisis/datos/2A/C2_rmsd_complejo.xvg C_analisis/datos/2B/C2_rmsd_complejo.xvg --etiquetas 2A 2B -o /tmp/prueba.png
```
(`graficar_xvg.py` usa matplotlib; necesita el entorno de la sección 0.)

### Qué significan los resultados
| Medida | 2A | 2B | Lectura |
|---|---|---|---|
| RMSD complejo (Å) | 1.57 | 1.55 | Ambos estables, igual de móviles |
| RMSD nanobody sobre sí mismo | 1.53 | 0.88 | 2B es más rígido (pero 1 réplica no basta para afirmarlo) |
| Pares de átomos a < 4 Å | 551 | 562 | **El tamaño de la interfaz es igual** |
| Puentes de H | 6.2 ± 1.0 | 7.2 ± 1.2 | ~1 más en 2B, dentro del ruido |
| Puente salino Arg–Glu111 | 96% del tiempo | 78% | Menos estable en 2B |
| Enlace con Tyr115 (esqueleto 107–Tyr115) | 100% | 32% | Se debilita en 2B |
| Thr30 (no mutado) | casi no toca | toca 38% | Entra a la interfaz |
| Arg110 | 0.18 | 0.85 | Se vuelve contacto persistente |

**Conclusión de C:** la maduración **no agranda** la interfaz, la **reorganiza**. La imagen estática del cristal (10 → 12 contactos polares) exagera la ganancia. Responde las preguntas 2 y parte de la 4.

---

## 8. Partes D, E y F: Energía

**Qué es:** estimar con MM/GBSA la energía de unión de cada sistema (D), qué componentes la forman (E) y qué aminoácido aporta cuánto (F).
**Cómo:** `gmx_MMPBSA` tomó 101 cuadros (los últimos 500 ps) de cada simulación, con los mismos parámetros en ambos.

### Ver los resultados
```bash
less D_F_energia/D_F_energia_libre.md

# Tabla de componentes (D y E) y todo el resumen impreso
cat D_F_energia/tablas/resumen_energia.txt | head -40

xdg-open D_F_energia/figuras/D_componentes_ddg.png
xdg-open D_F_energia/figuras/D_serie_tiempo_dG.png
xdg-open D_F_energia/figuras/F_top_ddg_residuo.png
xdg-open D_F_energia/figuras/F_mapa_interfaz.png
```

### Ver la energía sobre la estructura 3D (PyMOL)
```bash
python3 visualizar/generar_F_energia.py       # solo si cambiaron los datos; ya está generado
bash visualizar/pymol.sh visualizar/F_energia_bfactor.pml
```
Colorea **2B** según ΔΔG_i (promedio de 3 réplicas): **azul = el residuo contribuye más a la unión en 2B, rojo = contribuye menos**, blanco = sin cambio. Etiqueta los residuos con cambio significativo (Tyr101→Asp en rojo, Arg107 en azul, Gln69 de la RNasa en azul). Es la forma más clara de mostrar al profe "dónde cambió la energía".

Para solo ver la interfaz dentro de PyMOL: `hide cartoon, not (byres chain B within 8 of chain A)`.

### Recalcular todo desde los datos crudos
```bash
.venv/bin/python scripts/analisis_energia.py
```
Lee `D_F_energia/resultados_mmgbsa/{2A,2B}/` y regenera tablas y figuras.

### Datos crudos (por si el profe pregunta de dónde salen)
```bash
# Resultado final de gmx_MMPBSA para 2A (tabla "Delta (Complex - Receptor - Ligand)")
grep -A 18 "^Delta" D_F_energia/resultados_mmgbsa/2A/FINAL_RESULTS_MMPBSA.dat
# Parámetros exactos usados
cat D_F_energia/resultados_mmgbsa/2A/mmgbsa.in
```

### Qué significan los resultados (réplica r1; ver sección 9 para lo robusto)
**D. ΔΔG:** r1 dio ΔG(2A) = −50.1 y ΔG(2B) = −52.3, es decir **ΔΔG = −2.22** (experimental −2.98). Los valores absolutos (−50) no son comparables con el experimento (−10 a −13): esperado en MM/GBSA.

**E. Componentes (ΔΔ, 2B − 2A):**
| Componente | Valor | Significa |
|---|---|---|
| vdW | −0.9 | Algo mejor empaquetamiento |
| Electrostática | +0.7 | Algo peor |
| Solvatación polar (GB) | −2.0 | Se paga menos por soltar agua |
| No polar | −0.02 | Sin cambio (misma superficie enterrada) |
| EEL + GB juntos | −1.3 | Neto favorable |

Electrostática y solvatación se **compensan** (son grandes y de signo opuesto): solo su suma tiene sentido.

**F. Por residuo (ΔΔG_i = ΔG_i(2B) − ΔG_i(2A)):** cuánto aporta cada aminoácido.
| Posición | 2A | 2B | ΔΔG_i | Lectura |
|---|---|---|---|---|
| Tyr101→Asp | −5.4 | +1.4 | **+6.8** | Se pierde un residuo clave |
| Arg106→Thr | −3.7 | −1.1 | +2.5 | Se pierde el puente salino |
| Thr107→Arg | −3.2 | −5.6 | **−2.4** | Nuevo residuo clave de 2B |
| RNasa Gln69 | −1.8 | −3.8 | −2.0 | La RNasa se acomoda |

---

## 9. Las réplicas (el resultado que más importa)

**Problema:** una sola simulación puede salir bien o mal por azar.
**Solución:** repetir 2 veces más cada sistema (r2, r3), cambiando solo la semilla de las velocidades iniciales. Todo lo demás idéntico.

### Ver los resultados
```bash
cat D_F_energia/tablas/resumen_replicas.txt
xdg-open D_F_energia/figuras/D_replicas_dG.png
less D_F_energia/replicas/LEEME.md          # cómo se hicieron
bash visualizar/pymol.sh visualizar/F_energia_bfactor.pml      # mapa de ΔΔG_i por residuo (media de las 3 réplicas)
```

### Recalcular
```bash
.venv/bin/python scripts/analisis_replicas.py
```

### Los números
| ΔG unión (kcal/mol) | r1 | r2 | r3 | Media ± SD |
|---|---|---|---|---|
| 2A | −50.1 | −57.1 | −44.0 | −50.4 ± 6.6 |
| 2B | −52.3 | −50.3 | −44.5 | −49.0 ± 4.1 |

**ΔΔG = +1.4 ± 4.5** (experimental −2.98). 5 de 9 combinaciones dan signo negativo.

### Cómo interpretarlo
- La variación **entre réplicas (4–7 kcal/mol) es mayor que la diferencia buscada (3 kcal/mol)**. Con este método y 1 ns **no se puede distinguir** 2A de 2B.
- El −2.2 de r1 fue **casualidad favorable**.
- **Reproducible en las 3 réplicas:** Tyr101→Asp pierde (+6.5), Thr107→Arg gana (−2.7), Arg106→Thr pierde (+1.3), Gln69 de la RNasa gana (−2.0). Las 9 mutaciones juntas suman **+3.8** (desfavorable).
- **No reproducible:** la ganancia en Gly99/Gly100/Tyr27/Tyr33 y el cambio de Tyr115/Glu111. No afirmar "efecto cooperativo" con estos datos.
- Mensaje para el profe: mostramos que una réplica engaña y que hacen falta varias. Es exactamente la advertencia de la nota del enunciado (1 ns no demuestra convergencia).

---

## 10. Respuestas a las 6 preguntas, en simple

1. **¿Qué diferencia las variantes y dónde?** 9 mutaciones en los lazos CDR1 y CDR3. Cinco tocan directamente al antígeno en 2B (Y29W, Y101D, R106T, T107R, Q110R), una quita un contacto (R104V) y tres actúan indirectamente (A28P, E102A, D105A).
2. **¿Qué tan similares son?** Muy parecidas en conjunto (~1 Å) y cada cadena conserva su forma, pero el nanobody se apoya ~2 Å distinto sobre la RNasa, y la interfaz cambia de composición (entra Arg110/Thr30, sale Arg104).
3. **¿Cómo mejora 153× si se ven iguales?** Con una réplica el modelo da −2.2 kcal/mol, pero con tres da +1.4 ± 4.5: el método no lo demuestra. Lo reproducible es un cambio local de la interfaz, no del tamaño ni de la geometría global.
4. **¿Residuo individual o cooperativo?** Las mutaciones por sí solas **empeoran** (+3.8); Thr107→Arg gana pero Tyr101→Asp pierde mucho. La RNasa se ajusta (Gln69). La ganancia por "cooperatividad" en residuos no mutados que vimos en r1 no se repite, así que no se puede afirmar.
5. **¿Cambió el mapa energético?** Sí, localmente: 2A depende de Tyr101; 2B de Arg107 y de Gln69 de la RNasa.
6. **¿Qué tan bien lo explica el modelo?** Una réplica: signo y magnitud aciertan. Tres réplicas: no concluyente (+1.4 ± 4.5 vs −2.98). Falta entropía, más muestreo y otro modelo de solvatación.

---

## 11. Preguntas que puede hacer el profe

- **¿Por qué 1 ns, es suficiente?** No; el enunciado lo pide para un flujo comparativo. Por eso hicimos réplicas, y vimos que el ruido supera la señal.
- **¿Por qué los ΔG son −50 si el experimental es −10?** MM/GBSA sin entropía y con solvente continuo infla los valores absolutos; solo se usa la diferencia.
- **¿Por qué usaron los últimos 500 ps?** El sistema ya estaba equilibrado (RMSD plano tras ~200 ps); 101 cuadros dan promedios estables dentro de una trayectoria.
- **¿Por qué el mismo protocolo en ambos?** Para que cualquier diferencia se deba a las mutaciones y no al método.
- **¿Qué es GB?** Generalized Born: trata el agua como un medio continuo; es rápido pero aproximado.
- **¿Por qué compensan EEL y GB?** Poner cargas cerca gana electrostática pero obliga a soltar agua que las estabilizaba.
- **¿Qué falló en el notebook inicial?** El parser de la descomposición mezclaba el residuo N del nanobody con el residuo N de la RNasa. Se corrigió y está en `scripts/analisis_energia.py`.
- **2A y 2B no tienen la misma cantidad de residuos, ¿importa?** 2A trae Gly−1 y Ser0 de más y le falta la Lys1 a la RNasa. Están lejos de la interfaz (>8 Å), efecto ~0.1 kcal/mol; se declara como limitación.
- **¿Qué harían para mejorar?** Más réplicas con estructuras de partida distintas, ≥10 ns, comparar con PB/otro GB, y estimar entropía.

---

## 12. Guion y checklist para presentar

**Orden sugerido (≈10 min):**
1. El problema y la pregunta (sección 1). Mostrar `A_inspeccion/figuras/A3_superposicion.png`.
2. Qué cambia: tabla de 9 mutaciones y cuáles tocan el antígeno (parte A).
3. Cómo se simuló y que está bien hecho: tabla de verificaciones (parte B) y `B8_temperatura`.
4. Qué pasó en la película: RMSD y contactos (parte C). Mostrar `C2_rmsd_complejo` y `C4_salino`.
5. Energía: r1 (−2.2) y luego réplicas (+1.4 ± 4.5): `D_replicas_dG.png`.
6. Qué sí es robusto: `F_mapa_interfaz.png` (Tyr101, Arg107, Gln69).
7. Limitaciones y qué haríamos después.

**Archivos para tener abiertos:**
```bash
xdg-open A_inspeccion/figuras/A3_superposicion.png
xdg-open C_analisis/figuras/C2_rmsd_complejo_2A_vs_2B.png
xdg-open D_F_energia/figuras/D_componentes_ddg.png
xdg-open D_F_energia/figuras/D_replicas_dG.png
xdg-open D_F_energia/figuras/F_mapa_interfaz.png
bash visualizar/pymol.sh visualizar/A_mutaciones.pml
bash visualizar/pymol.sh visualizar/A_interfaz_contactos.pml
bash visualizar/pymol.sh visualizar/F_energia_bfactor.pml
vmd -e visualizar/C_trayectoria.tcl          # película (tras preparar_trayectoria.sh)
xmgrace C_analisis/datos/2A/C2_rmsd_complejo.xvg C_analisis/datos/2B/C2_rmsd_complejo.xvg
less INFORME_FINAL.md
```

**Antes de presentar, comprueba:**
- [ ] Puedes explicar con tus palabras: KD, ΔG, ΔΔG, interfaz, CDR, RMSD, réplica.
- [ ] Sabes por qué −2.2 era engañoso y qué muestran las 3 réplicas.
- [ ] Sabes qué mutaciones tocan el antígeno y por qué Tyr101→Asp es la más importante.
- [ ] `.venv` creado y los scripts corren (`bash scripts/preparar_entorno.sh`).

---

## 13. Problemas frecuentes

| Problema | Solución |
|---|---|
| `ModuleNotFoundError: pandas` | `bash scripts/preparar_entorno.sh` y usa `.venv/bin/python` |
| `xdg-open` no abre nada | Abre la imagen desde el explorador de archivos |
| `gmx: command not found` | GROMACS está en `/usr/bin/gmx`; abre una terminal nueva |
| PyMOL no carga el `.pse` | Usa `bash visualizar/pymol.sh visualizar/A_mutaciones.pml` o `load 01_estructuras/System_2A.pdb` a mano |
| `C_trayectoria.pml` dice que no encuentra `visualizar/tmp/...` | Corre `bash visualizar/preparar_trayectoria.sh` desde la raíz |
| `Invalid selection name "wt"` o `No such file` en PyMOL | Es el sandbox de Flatpak. Abre con `bash visualizar/pymol.sh visualizar/<script>.pml` |
| PyMOL muestra todo en blanco/negro | Escribe `bg_color white` y `orient` |
| xmgrace no ve la curva | Clic derecho → Autoscale, o `Plot > Autoscale` |
| Un `.xvg` no abre | Es texto: `grep -v '^[#@]' archivo.xvg | head` |
| Quiero volver a correr simulaciones | Colab: `B_dinamica/colab/Como_usar_Colab.md` y `D_F_energia/replicas/LEEME.md` |

---

## 14. Visualización manual en la consola de PyMOL

Para armar tú mismo las vistas para el profe. Pega las líneas **una por una** en la consola de PyMOL. Las medidas que sustentan lo que verás están en `A_inspeccion/tablas/analisis_interfaz.txt` (se regeneran con `pymol -cq -d "run visualizar/analisis_interfaz.py"`) y su interpretación, en `INFORME_FINAL.md`.

### 14.1 Cargar y superponer
```
reinitialize
cd /home/mayday3003/Documents/githubrepos/genetic-engineering
load 01_estructuras/System_2A.pdb, wt
load 01_estructuras/System_2B.pdb, mut
align mut and chain A and name CA, wt and chain A and name CA, cycles=0
hide everything
show cartoon
color palegreen, chain A
color gray70, wt and chain B
color cyan, mut and chain B
set cartoon_transparency, 0.6
```
`wt` = 2A (inicial), `mut` = 2B (madurada). Cadena A = RNasa, cadena B = nanobody. El `align` debe dar ~0.64 Å (se superpone sobre la RNasa).

### 14.2 Seis objetos: interfaz y mutaciones, antes y después
Un **objeto** se enciende y apaga con un clic; una **selección** (entre paréntesis en el panel) es solo una lista. `create` copia una selección a un objeto.
```
select t1, byres (wt and chain B) within 4 of (wt and chain A)
select t2, byres (wt and chain A) within 4 of (wt and chain B)
select t3, byres (mut and chain B) within 4 of (mut and chain A)
select t4, byres (mut and chain A) within 4 of (mut and chain B)
select t5, wt and chain B and resi 28+29+101+102+104+105+106+107+110
select t6, mut and chain B and resi 28+29+101+102+104+105+106+107+110
create inter_nb_2A, t1
create inter_rnasa_2A, t2
create inter_nb_2B, t3
create inter_rnasa_2B, t4
create mut_2A, t5
create mut_2B, t6
delete t1
delete t2
delete t3
delete t4
delete t5
delete t6
```
Resultado esperado: 13 y 15 residuos en la interfaz de 2A (nanobody y RNasa), 14 y 15 en 2B, y 9 mutaciones en cada versión.

### 14.3 Estilo con las cargas (licorice = bastones finos)
```
hide everything, inter_nb_2A or inter_rnasa_2A or inter_nb_2B or inter_rnasa_2B or mut_2A or mut_2B
show licorice, inter_nb_2A or inter_rnasa_2A or inter_nb_2B or inter_rnasa_2B
show sticks, mut_2A or mut_2B
set stick_radius, 0.12, inter_nb_2A or inter_rnasa_2A or inter_nb_2B or inter_rnasa_2B
set stick_radius, 0.25, mut_2A or mut_2B
color gray70, inter_nb_2A
color cyan, inter_nb_2B
color palegreen, inter_rnasa_2A or inter_rnasa_2B
color grey40, mut_2A
color deepteal, mut_2B
color blue, (inter_nb_2A or inter_rnasa_2A or inter_nb_2B or inter_rnasa_2B or mut_2A or mut_2B) and resn ARG+LYS
color red, (inter_nb_2A or inter_rnasa_2A or inter_nb_2B or inter_rnasa_2B or mut_2A or mut_2B) and resn ASP+GLU
set label_size, 18
set label_color, white
label mut_2A and name CA, resn+resi
label mut_2B and name CA, resn+resi
```
**Azul = carga positiva (Arg, Lys). Rojo = negativa (Asp, Glu).** Fino = interfaz, grueso = mutación. Con fondo blanco usa `set label_color, black`.

### 14.4 Antes, después y superpuestas (escenas)
```
disable wt
disable mut
disable inter_nb_2B
disable inter_rnasa_2B
disable mut_2B
orient inter_nb_2A
scene 1_antes_2A, store
disable inter_nb_2A
disable inter_rnasa_2A
disable mut_2A
enable inter_nb_2B
enable inter_rnasa_2B
enable mut_2B
scene 2_despues_2B, store
enable inter_nb_2A
enable mut_2A
scene 3_superpuestas, store
save visualizar/interfaz_antes_despues.pse
```
Para moverte: `scene 1_antes_2A, recall` (y los otros dos nombres). Como el `orient` se hizo antes de guardar, la cámara no se mueve al alternar.

### 14.5 Qué debes ver y cómo leerlo
- **`mut_2A` (las 9 posiciones antes):** 2 azules (Arg104, Arg106) y 2 rojos (Glu102, Asp105). **`mut_2B` (después):** 2 azules (Arg107, Arg110) y 1 rojo (Asp101).
- **Interfaz del nanobody (`inter_nb_*`):** 2A solo tiene azules (Arg104, Arg106); 2B tiene dos azules y un rojo (Asp101). Los rojos Glu102 y Asp105 de `mut_2A` **no** están en la interfaz (a 4.8 y 5.9 Å).
- **Interfaz de la RNasa:** Lys61 (azul) y Glu111 (rojo), igual en 2A y 2B.
- El resultado depende del corte de 4 Å. Con 5 Å el Glu102 entra a la interfaz de 2A.
- Tres grupos para entender mutaciones frente a interfaz (5 mutadas que tocan, 4 mutadas que no tocan, 9 que tocan sin mutar): ver `INFORME_FINAL.md`.

### 14.6 Medir distancias
Un contacto concreto (átomo con átomo):
```
distance sal_2B, (mut and chain B and resi 107 and name NE), (mut and chain A and resi 111 and name OE1)
distance sal_2A, (wt and chain B and resi 106 and name NE), (wt and chain A and resi 111 and name OE2)
distance asp_thr, (mut and chain B and resi 101 and name OD1), (mut and chain A and resi 70 and name N)
distance thr_gly, (mut and chain B and resi 106 and name OG1), (mut and chain A and resi 112 and name N)
distance y27_2A, (wt and chain B and resi 27 and name OH), (wt and chain A and resi 60 and name O)
distance y27_2B, (mut and chain B and resi 27 and name OH), (mut and chain A and resi 60 and name O)
```
Valores esperados: 3.11, 3.34, 3.07, 3.10, 3.48 y 2.64 Å. Ojo: esas son distancias del **cristal**; en la dinámica el acortamiento de Tyr27–Gln60 no persiste (ocupación 9 % en 2A y 2 % en 2B). Para borrar una: `delete sal_2B`.

**Error típico:** `distance d, (selección grande), (selección grande), mode=0` dibuja **todas las parejas átomo–átomo** (miles de líneas amarillas). Para contactos polares usa `mode=2` con un corte (`distance pol, A, B, 3.5, mode=2`) o mide átomos concretos como arriba. Para la distancia mínima de cada mutación: `run visualizar/distancias_mutaciones.py`.

### 14.7 Superficie electrostática (rojo = negativo, azul = positivo)
```
create nb2A, wt and chain B
create nb2B, mut and chain B
util.protein_vacuum_esp("nb2A", mode=2, quiet=0)
util.protein_vacuum_esp("nb2B", mode=2, quiet=0)
```
Es una aproximación en el vacío: sirve para ver patrones, no valores. Cuenta de cargas: `count_atoms wt and chain B and name CA and resn ARG+LYS` (y `ASP+GLU`, y lo mismo con `mut`): nanobody 12(+)/11(−) en 2A y 12(+)/10(−) en 2B; carga neta **+1 → +2**. La RNasa tiene 14(+)/10(−): neta **+4**.

### 14.8 Guardar y presentar
```
save visualizar/interfaz_antes_despues.pse
png A_inspeccion/figuras/interfaz_antes.png, width=2400, height=1800, dpi=300, ray=1
```
PyMOL no guarda solo: repite el `save` cada vez que termines una vista. Para abrir otro día: `pymol visualizar/interfaz_antes_despues.pse`.

### 14.9 Ideas que debes poder explicar con estas vistas
1. Las mutaciones y la interfaz son **dos listas distintas**; se solapan en 5 posiciones.
2. La interfaz **no crece** (1178 → 1165 Å²): se reorganiza. El lado de la RNasa casi no cambia; el del nanobody sí.
3. El puente salino con Glu111 **se conserva pero cambia de arginina** (106 → 107).
4. Las cargas nuevas de 2B (Asp101, Arg110) **no tienen pareja opuesta cerca**: de ahí que Y101D sea tan desfavorable.
5. 153× de afinidad son solo ~3 kcal/mol, del orden de un puente de H: cambios pequeños pueden ser suficientes. Pero nuestro cálculo de energía **no** lo demostró (ΔΔG = +1.4 ± 4.5).
