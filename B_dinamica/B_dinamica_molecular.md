# B. Dinámica molecular

**Estado: completa.** Corridas definitivas de 2A y 2B hechas en Colab (A100, GROMACS 2025.3), en `2A_colab/` y `2B_colab/`. La carpeta `2A/` es la corrida local de prueba, pausada en 734 ps.

Cada sistema se simula **con exactamente el mismo protocolo**. Los archivos de cada simulación van en `2A/` y `2B/`.

- Tutorial base: [Lysozyme in Water (mdtutorials.com)](http://www.mdtutorials.com/gmx/lysozyme/)
- Protocolo de clase usado como referencia: `../referencia_clase_gromacs/`
- Parámetros de simulación: `mdp/` (copias de los de clase más `md.mdp` para la producción)
- Versión: GROMACS 2026.0

## Cambio a Colab (decisión del 4 de noviembre)
La CPU local rinde ~6 ns/día (~11 h para los dos sistemas), así que las corridas definitivas de **2A y 2B** se hacen en Colab con una GPU A100. Instrucciones: `colab/Como_usar_Colab.md`.

- **Mismo protocolo:** se usan los mismos `mdp/`. Del notebook de un compañero (`ColabBiologia.ipynb`) solo se reutilizó la instalación y las banderas de GPU, no sus parámetros.
- **Por qué se repite 2A:** Colab usa GROMACS 2025.3 y un `.tpr` de 2026.0 no se puede continuar ahí. Repetirlo deja los dos sistemas con la misma versión y hardware.
- **Corrida local de 2A:** queda en `2A/`, pausada en 734 ps, como prueba. Sus valores quedan al final de este documento, solo como referencia.
- **Comprobado localmente para 2B (hasta B4):** carga +6 (RNasa +4, nanobody +2), 6 CL⁻, 29 204 aguas y las mismas His que 2A (12 HID, 48 HIE, 105 HID, 119 HIE).

## Decisiones del protocolo (y por qué)

| Decisión | Valor | Justificación |
|---|---|---|
| Campo de fuerza | **AMBER99SB-ILDN** | Es el mismo de clase (`referencia_clase_gromacs/topol.top`). El tutorial usa CHARMM36, pero AMBER es la familia nativa de gmx_MMPBSA (partes D–F), lo que evita problemas de conversión de topología. |
| Modelo de agua | **TIP3P** | Es el agua con la que se parametrizó AMBER99SB-ILDN y la misma de clase. |
| Hidrógenos | `-ignh` | Los PDB entregados **no traen hidrógenos** (0 átomos H), así que `pdb2gmx` los añade según el campo de fuerza. Es el mismo comando que en clase (`todo.txt`). |
| Histidinas | Asignación automática de `pdb2gmx` | La RNasa tiene His12, His48, His105 y His119 (His12 e His119 son catalíticas). Se anotará qué tautómero asignó `pdb2gmx` en cada sistema para comprobar que coincide. |
| Extremos | Se conservan tal como vienen | 2A tiene Gly−1 y Ser0 (tag) en el nanobody; 2B tiene Lys1 en la RNasa. Las estructuras se entregaron "limpias y listas", así que no se modifican. Están lejos de la interfaz: la distancia mínima a la otra cadena es 8.6 Å para Gly−1/Ser0 (2A) y 12.6 Å para Lys1 (2B). |
| Caja | Cúbica, 1.0 nm de distancia al borde | Igual al tutorial y a la clase. 1.0 nm evita que la proteína se vea a sí misma a través de la PBC con cutoffs de 1.2 nm. |
| Iones | Solo neutralizar (`-neutral`) | Igual al tutorial y a la clase. La carga neta **difiere** entre sistemas (2B tiene unas +2 más: Lys1, y el CDR3 pasa de carga 0 a +1), así que el número de iones también diferirá. Es esperable. |
| Minimización | Steepest descent, Fmax < 1000 kJ/mol/nm | Criterio estándar del tutorial. |
| NVT | 100 ps, 298 K, V-rescale, con restricciones de posición | 298 K, que es la temperatura del ΔΔGexp del enunciado (298.15 K). |
| NPT | 500 ps, 1 bar, C-rescale, con restricciones de posición | Igual a clase. Es más largo que el del tutorial (100 ps), lo que da mejor estabilización de la densidad. |
| Producción | 1 ns, sin restricciones, coordenadas cada 1 ps (1000 frames) | Lo pide el enunciado. Guardar cada 1 ps deja suficientes snapshots para elegir la ventana de gmx_MMPBSA. |

> **Nota para discutir con el profesor:** los `.mdp` de clase vienen de la versión CHARMM del tutorial (`vdw-modifier = force-switch`, `rvdw = 1.2`, `DispCorr = No`). Para AMBER lo usual es `rvdw = 1.0` con `DispCorr = EnerPres`. Se mantienen los parámetros de clase por consistencia con el curso, y como se aplican **igual a 2A y 2B**, la comparación es válida.

## Paso a paso

Todos los comandos se ejecutan **dentro de la carpeta del sistema** (`2A/` o `2B/`). Se hace primero 2A completo y después se repite igual en 2B, cambiando solo el PDB de entrada.

### B1. Topología (`pdb2gmx`)
```bash
cd B_dinamica/2A
gmx pdb2gmx -f ../../01_estructuras/System_2A.pdb -o complex.gro -p topol.top -ff amber99sb-ildn -water tip3p -ignh
```
- Qué hace: lee el PDB, añade hidrógenos y escribe la estructura en formato GROMACS (`complex.gro`), la topología (`topol.top` más un `.itp` por cadena) y las restricciones de posición (`posre_*.itp`).
- `-ff` y `-water` evitan el menú interactivo y dejan el comando reproducible.
- Qué revisar:
  - Que no haya errores ni warnings.
  - La línea `Total charge` de cada cadena.
  - En `topol.top`, la sección `[ molecules ]` (deben aparecer las dos cadenas).
  - Cómo quedó cada HIS (HID, HIE o HIP).

### B2. Caja (`editconf`)
```bash
gmx editconf -f complex.gro -o complex_newbox.gro -c -d 1.0 -bt cubic
```

### B3. Solvatación (`solvate`)
```bash
gmx solvate -cp complex_newbox.gro -cs spc216.gro -o complex_solv.gro -p topol.top
```

### B4. Iones (`grompp` + `genion`)
```bash
gmx grompp -f ../mdp/ions.mdp -c complex_solv.gro -p topol.top -o ions.tpr
gmx genion -s ions.tpr -o complex_solv_ions.gro -p topol.top -pname NA -nname CL -neutral
```
Cuando lo pida, elegir el grupo **SOL**: se reemplazan moléculas de agua por iones.

### B5. Minimización
```bash
gmx grompp -f ../mdp/minim.mdp -c complex_solv_ions.gro -p topol.top -o em.tpr
gmx mdrun -v -deffnm em
gmx energy -f em.edr -o potential.xvg      # elegir: 10 (Potential) y 0
python3 ../../scripts/graficar_xvg.py potential.xvg --desde 5 -o ../figuras/B5_potencial_2A.png
```

### B6. Equilibración NVT
```bash
gmx grompp -f ../mdp/nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -v -deffnm nvt
gmx energy -f nvt.edr -o temperature.xvg   # elegir: Temperature
```

### B7. Equilibración NPT
```bash
gmx grompp -f ../mdp/npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -v -deffnm npt
gmx energy -f npt.edr -o pressure.xvg      # elegir: Pressure
gmx energy -f npt.edr -o density.xvg       # elegir: Density
gmx energy -f npt.edr -o volume.xvg        # elegir: Volume
```

### B8. Producción (1 ns)
```bash
gmx grompp -f ../mdp/md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
gmx mdrun -v -deffnm md
```

**Parar y continuar:** presionar Ctrl+C una sola vez y esperar a que GROMACS escriba `md.cpt`. Para retomar, sin repetir `grompp`:
```bash
gmx mdrun -v -deffnm md -cpi md.cpt
```
La simulación termina en el paso 500000 (1000 ps). Para ver hasta dónde llegó: `gmx check -f md.cpt`.

## Registro de resultados (corridas definitivas en Colab)

| Etapa | 2A | 2B |
|---|---|---|
| Carga total | +4 (RNasa +3, nanobody +1) | +6 (RNasa +4, nanobody +2) |
| HIS asignadas | 12 HID, 48 HIE, 105 HID, 119 HIE | Iguales |
| Caja cúbica (nm) | 9.73406 | 9.75176 |
| Aguas / iones | 28 895 / 4 CL⁻ | 29 204 / 6 CL⁻ |
| Minimización: pasos / Fmax / Epot (kJ/mol) | 1331 / 897.1 / −1.4166e6 | 1383 / 778.9 / −1.4352e6 |
| NVT: T (K), 20–100 ps | 298.10 (RMSD 1.04) | 298.03 (RMSD 1.02) |
| NPT, 100–500 ps: P (bar) | 4.4 ± 5.4 | 9.9 ± 4.4 |
| NPT, 100–500 ps: densidad (kg/m³) / volumen (nm³) | 993.97 / 914.43 | 993.88 / 923.70 |
| Producción: T (K) / P (bar) / densidad (kg/m³) | 297.98 / 6.1 ± 2.3 / 993.76 | 298.00 / 2.8 ± 2.9 / 993.30 |
| Producción: frames / rendimiento | 1001 frames, 1 ns / 228.6 ns/día | 1001 frames, 1 ns / 219.1 ns/día |

Los ± de presión son el error estimado por `gmx energy`. Las fluctuaciones instantáneas de presión son de ~80 bar en los dos sistemas.

### Verificaciones
- Minimización: **cumple** en los dos (Fmax < 1000).
- Temperatura: **cumple,** ~298 K en todas las etapas.
- Densidad y volumen: **cumple,** estables y casi iguales entre sistemas. La densidad es típica de TIP3P.
- Presión: **razonable.** Los promedios quedan unos bares por encima de 1 bar, pequeños frente a las fluctuaciones. El NPT de 2B (9.9 ± 4.4) es el más alejado.
- Producción: **cumple.** Las dos terminaron 1 ns completo y el complejo no se separó (distancia mínima entre cadenas ~1.7 Å, ver parte C).

### Figuras
- `figuras/`: gráficas B5–B7 de la corrida local de prueba de 2A.
- `../C_analisis/figuras/B5_potencial_2A_vs_2B.png`: energía potencial durante la minimización, 2A vs 2B.
- `../C_analisis/figuras/B8_*`: temperatura y densidad de producción, 2A vs 2B.
- Datos de todas las etapas de Colab: `../C_analisis/datos/<sistema>/`.

### Corrida local de prueba de 2A (no definitiva)
Minimización: 1604 pasos, Fmax 919.7. NVT 298.05 ± 0.89 K. NPT: 993.9 kg/m³. Producción detenida en 734 ps a ~6.9 ns/día.
