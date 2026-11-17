# Réplicas de MD + MM/GBSA

Objetivo: pasar de 1 réplica a 3 por sistema (r1 = corrida original; r2, r3 nuevas) para estimar el error de muestreo real del ΔΔG.

**Diseño:** las réplicas parten del sistema ya construido y minimizado (`B_dinamica/*_colab/em.gro`); solo cambia la semilla de las velocidades del NVT (1002 y 1003). Mismos `.mdp`, mismo protocolo, misma ventana (500–1000 ps, 101 snapshots) y mismos parámetros de GB. Limitación: comparten la estructura de partida y la caja, así que miden el muestreo dinámico, no la incertidumbre de la estructura cristalográfica.

## Pasos
1. `Colab_replicas_1_MD.ipynb` en Colab con **A100**. Sube `D_F_energia/replicas_inputs.zip`. Descarga `replicas_md.zip` (≈ 55 MB).
2. `Colab_replicas_2_MMPBSA.ipynb` (runtime CPU). Sube `replicas_md.zip`. Descarga `resultados_replicas_mmgbsa.zip`.
3. Descomprime en `D_F_energia/replicas/resultados/` (deben quedar `2A_r2/mmgbsa/FINAL_*`, etc.).
4. `python scripts/analisis_replicas.py` → `tablas/resumen_replicas.txt`, `tablas/descomposicion_replicas.csv`, `figuras/D_replicas_dG.png`.
5. Actualiza `D_F_energia_libre.md` e `INFORME_FINAL.md` con la media ± error entre réplicas y qué residuos del ΔΔG_i son significativos.

## Estado de la verificación
El script de análisis se probó con datos simulados (copias de r1). Los notebooks y `replica.sh` **no se han ejecutado en Colab**: la sintaxis está revisada, pero si una celda falla, copia el error.
