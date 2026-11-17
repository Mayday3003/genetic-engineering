# D–F. Energía libre (gmx_MMPBSA): segunda entrega

## Qué se hizo
- Notebook: [`Colab_MMPBSA_Pareja2.ipynb`](Colab_MMPBSA_Pareja2.ipynb) (gmx_MMPBSA 1.7.1, AmberTools 26, GROMACS 2026.3). Entrada: trayectorias sin agua de `B_dinamica/*_colab/` empaquetadas en `datos_md_pareja2.zip`.
- Análisis: [`scripts/analisis_energia.py`](../scripts/analisis_energia.py) (corre en local sobre `resultados_mmgbsa/`, no requiere Colab).
- Resultados crudos: `resultados_mmgbsa/{2A,2B}/FINAL_*` · tablas: `tablas/` · figuras: `figuras/`.

### Parámetros (idénticos en 2A y 2B)
| Parámetro | Valor |
|---|---|
| Receptor / ligando | `Protein_chain2` (nanobody) / `Protein_chain1` (RNasa A) |
| Ventana | 500–1000 ps de la producción (`startframe=501, endframe=1001, interval=5`) → 101 snapshots |
| Modelo | GB-Neck2 (`igb=8`), radios mbondi3 (`PBRadii=4`), `saltcon=0.150` M, 298.15 K |
| Descomposición | `idecomp=2` (1-4 sumado a interno), todos los residuos |
| Entropía | No calculada (se cancela parcialmente en ΔΔG; ver limitaciones) |

```
python scripts/analisis_energia.py
```

## D. ΔΔG calculado vs experimental

| | 2A (inicial) | 2B (madurada) | ΔΔG (2B − 2A) |
|---|---|---|---|
| ΔG unión (kcal/mol) | −50.11 ± 0.48 | −52.33 ± 0.87 | **−2.22 ± 0.99** |
| Experimental | KD 23 nM | KD 0.15 nM | **−2.98** |

± = SEM por bloques (5 bloques de 100 ps). Figuras: `figuras/D_componentes_ddg.png`, `figuras/D_serie_tiempo_dG.png`.

- **Signo correcto** (2B une mejor) y **magnitud del mismo orden** (−2.2 vs −3.0; ~75 % del valor experimental).
- Los ΔG absolutos (~−50) son 4–5 veces más negativos que los experimentales (RT ln KD ≈ −10.4 y −13.4). Es lo esperado en MM/GBSA sin entropía; solo el ΔΔG es interpretable.
- La serie temporal no muestra derivas ni outliers en la ventana.

## E. Componentes

| Término | 2A | 2B | ΔΔ |
|---|---|---|---|
| ΔE vdW | −69.48 | −70.40 | −0.92 ± 0.94 |
| ΔE electrostática | −65.55 | −64.81 | +0.74 ± 5.01 |
| ΔG solv. polar (GB) | +93.54 | +91.52 | −2.01 ± 4.82 |
| ΔG solv. no polar | −8.62 | −8.64 | −0.02 ± 0.12 |
| **ΔΔ(EEL + GB)** | | | **−1.28** |

- La mejora **no** viene de una electrostática directa más fuerte (empeora ligeramente), sino de una **menor penalización de desolvatación polar**. El balance electrostático neto (EEL + GB) aporta ~−1.3 y el empaquetamiento (vdW) ~−0.9.
- EEL y GB por separado tienen errores de ~5 kcal/mol y se compensan entre sí; por eso solo se interpreta su suma.
- El término no polar no cambia: el tamaño de la interfaz enterrada es igual, como se vio en la parte C (número de contactos similar).

## F. Descomposición por residuo

ΔΔG_i = ΔG_i(2B) − ΔG_i(2A). Tabla completa: `tablas/descomposicion_por_residuo.csv`. Figuras: `figuras/F_top_ddg_residuo.png`, `figuras/F_mapa_interfaz.png`.

### Residuos mutados
| Posición | ΔG_i 2A | ΔG_i 2B | ΔΔG_i | Origen |
|---|---|---|---|---|
| Tyr101→Asp | −5.36 | +1.43 | **+6.79** | Pierde un hotspot aromático; el Asp paga +27 de desolvatación frente a −22 de electrostática |
| Arg106→Thr | −3.66 | −1.12 | +2.54 | Se pierde el puente salino Arg106–Glu111 |
| Thr107→Arg | −3.23 | −5.64 | **−2.42** | El Arg107 retoma el puente salino con Glu111 (ver A5) y es el principal hotspot de 2B |
| Tyr29→Trp | −2.49 | −2.69 | −0.20 | Más vdW, compensado por electrostática |
| Asp105→Ala | +0.66 | +0.08 | −0.59 | Se elimina una carga desfavorable |
| Ala28→Pro, Glu102→Ala, Arg104→Val, Gln110→Arg | ≈ 0 | ≈ 0 | ≈ 0 | Fuera del contacto directo; efecto indirecto |

### Suma por región
| Región | ΣΔΔG_i (kcal/mol) |
|---|---|
| 9 posiciones mutadas | **+5.95** |
| Nanobody no mutado | **−5.38** (Gly99 −2.28, Gly100 −1.82, Tyr27 −0.89, Tyr33 −0.74) |
| RNasa A | **−2.45** (Gln69 −2.05, Lys61 −1.39, Tyr73 −0.76; pierden Tyr115 +1.91, Glu111 +1.19, Asn71 +1.07) |
| Total | −1.88 (la descomposición GB no suma exactamente el ΔΔG global de −2.22) |

### Mapa de hotspots
- **2A:** Tyr101 (NB), Tyr115 (RNasa), Ile32 (NB), Glu111 (RNasa), Arg106 (NB), Thr70 (RNasa).
- **2B:** Arg107 (NB), Ile32 (NB), Thr70 (RNasa), Gln69 (RNasa), Tyr115 (RNasa), Glu111 (RNasa).

## Respuestas (preguntas 3–6)

**3. ¿Cómo explicar >100× de afinidad con estructuras tan parecidas?** El modelo sí distingue los complejos: ΔΔG = −2.2 kcal/mol, del orden del experimental. La diferencia no es geométrica a escala global (RMSD bajos, mismo número de contactos y mismo término no polar), sino de la **calidad electrostática/solvatación y del empaquetamiento local** de la interfaz.

**4. ¿Efecto individual o cooperativo?** Cooperativo. Las mutaciones, sumadas, son **desfavorables (+6 kcal/mol)**: la pérdida de Tyr101 y Arg106 no la compensa por sí solo Arg107. La ganancia aparece en **residuos no mutados** del CDR3 (Gly99, Gly100) y del CDR1 (Tyr27, Tyr33) y en la RNasa (Gln69, Lys61, Tyr73), que se acomodan al nuevo CDR3. Es una redistribución de la interfaz, no la suma de efectos puntuales.

**5. ¿Cambió el mapa energético?** Sí. En 2A la interfaz se apoya en Tyr101 y en el par Tyr115/Glu111 de la RNasa. En 2B el anclaje pasa a Arg107 y a la región Gln69–Thr70 de la RNasa, y Tyr115/Glu111 pierden peso. Esto es coherente con la parte C: el puente salino con Glu111 y la interacción con Tyr115 son menos estables en la MD de 2B. La variante madura tiene una interfaz energéticamente distinta con geometría global similar.

**6. ¿Qué tan bien lo explica el modelo?** Reproduce bien el **signo** y razonablemente la **magnitud** (−2.2 vs −3.0) y da un origen físicamente coherente (desolvatación menos costosa + vdW, con redistribución). Que el acuerdo numérico sea tan cercano debe tomarse con cautela (ver limitaciones): el error real es mayor que el SEM reportado.

## Limitaciones
- **Muestreo:** una sola réplica de 1 ns por sistema y una ventana de 0.5 ns; los 101 snapshots están correlacionados. El SEM por bloques (±1) subestima la incertidumbre real; con réplicas independientes es esperable una dispersión de ±1–2 kcal/mol.
- **Modelo energético:** GB implícito (sin aguas de interfaz explícitas), campo de fuerza fijo, sin entropía configuracional. Los ΔG absolutos no son comparables con el experimento.
- **Composición distinta:** 2A conserva dos residuos de la etiqueta de expresión (Gly−1, Ser0 del nanobody) y le falta la Lys1 de la RNasa, que sí está en 2B. Están lejos de la interfaz y su efecto en la descomposición es ~0.1 kcal/mol, pero es una diferencia entre sistemas no debida a la maduración.
- **Descomposición:** con GB la suma por residuo no es exactamente igual al ΔΔG global (−1.88 vs −2.22), y los términos EEL/GB por residuo son grandes y opuestos; se interpreta solo su suma.

### Mejoras posibles
Réplicas (3+) por sistema; producción más larga; repetir con `igb=5` o PB para ver si el signo se mantiene; estimar la entropía (interaction entropy o C2).

## Nota sobre el notebook
La primera versión del notebook mezclaba en la descomposición el residuo N del nanobody con el residuo N de la RNasa: gmx_MMPBSA etiqueta `R::TYR:101` / `L::GLN:101` sin cadena. El parser ya está corregido (R = nanobody, L = RNasa) y todo el análisis de este documento sale de `scripts/analisis_energia.py`.
