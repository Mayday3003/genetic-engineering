"""Parte F, solo las 9 posiciones mutadas y solo la réplica r1.
Las posiciones NO se eligen por su efecto: son las 9 que difieren en la secuencia (parte A).
Uso:  .venv/bin/python scripts/figuras_mutaciones.py
Salida: D_F_energia/figuras/F_mutaciones_{dG,ddG,componentes}_r1.png y tablas/mutaciones_r1.txt
"""
import sys
from pathlib import Path
import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo_figuras import AZUL, NARANJA, nueva, leyenda_abajo, guardar
import matplotlib.pyplot as plt

src = (RAIZ / "scripts/analisis_energia.py").read_text().split("# ---------- D y E")[0]
ns = {"__file__": str(RAIZ / "scripts/analisis_energia.py"), "sys": type("S", (), {"argv": ["x"], "path": sys.path})}
exec(compile(src, "parsers", "exec"), ns)
decomp, block_sem = ns["decomp"], ns["block_sem"]
E = RAIZ / "D_F_energia"
UNA = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
       "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}
POS = [28, 29, 101, 102, 104, 105, 106, 107, 110]
d = {s: decomp(E / "resultados_mmgbsa" / s / "FINAL_DECOMP_MMPBSA.csv") for s in ("2A", "2B")}

filas = []
for p in POS:
    a, b = d["2A"][("NB", p)], d["2B"][("NB", p)]
    nombre = f"{UNA[a['res']]}{p}{UNA[b['res']]}"
    fila = dict(nombre=nombre, g2A=np.mean(a["TOTAL"]), g2B=np.mean(b["TOTAL"]))
    fila["dd"] = fila["g2B"] - fila["g2A"]
    fila["err"] = float(np.hypot(block_sem(a["TOTAL"]), block_sem(b["TOTAL"])))
    for t in ("vdW", "Ele", "Polar", "NoPolar"):
        fila[t] = np.mean(b[t]) - np.mean(a[t])
    filas.append(fila)
nombres = [f["nombre"] for f in filas]
x = np.arange(len(filas))

# 1. ΔG_i en 2A y 2B
fig, ax = nueva(8, 4.2)
ax.bar(x - 0.2, [f["g2A"] for f in filas], 0.4, color=AZUL, label="2A")
ax.bar(x + 0.2, [f["g2B"] for f in filas], 0.4, color=NARANJA, label="2B")
ax.axhline(0, color="k", lw=1)
ax.set_xticks(x, nombres)
ax.set(xlabel="Mutación (aminoácido en 2A, posición, aminoácido en 2B)", ylabel="Contribución del residuo ΔG (kcal/mol)",
       title="Contribución de las 9 posiciones mutadas a la unión (réplica r1)")
leyenda_abajo(ax)
guardar(fig, E / "figuras/F_mutaciones_dG_r1.png")

# 2. ΔΔG_i con error
fig, ax = nueva(8, 4.2)
ax.bar(x, [f["dd"] for f in filas], yerr=[f["err"] for f in filas], color=AZUL, capsize=3, error_kw=dict(lw=1))
ax.axhline(0, color="k", lw=1)
ax.set_xticks(x, nombres)
tot = sum(f["dd"] for f in filas)
ax.set(xlabel="Mutación", ylabel="ΔΔG del residuo = 2B − 2A (kcal/mol)",
       title=f"Cambio de contribución de cada mutación (réplica r1); suma de las 9 = {tot:+.2f}")
guardar(fig, E / "figuras/F_mutaciones_ddG_r1.png")

# 3. Componentes del ΔΔG_i
fig, ax = nueva(9, 4.4)
ancho = 0.2
colores = {"vdW": "tab:blue", "Ele": "tab:orange", "Polar": "tab:green", "NoPolar": "tab:red"}
nombres_t = {"vdW": "vdW", "Ele": "Electrostática", "Polar": "Solvatación polar", "NoPolar": "Solvatación no polar"}
for i, t in enumerate(colores):
    ax.bar(x + (i - 1.5) * ancho, [f[t] for f in filas], ancho, color=colores[t], label=nombres_t[t])
ax.plot(x, [f["dd"] for f in filas], "k_", ms=18, mew=2, label="Total del residuo")
ax.axhline(0, color="k", lw=1)
ax.set_xticks(x, nombres)
ax.set(xlabel="Mutación", ylabel="ΔΔG del residuo por término (kcal/mol)",
       title="Componentes del cambio de cada mutación (réplica r1)")
leyenda_abajo(ax, ncol=5)
guardar(fig, E / "figuras/F_mutaciones_componentes_r1.png")

lin = ["Réplica r1, las 9 posiciones mutadas (kcal/mol). ΔΔG = 2B − 2A; error = SEM por bloques de la trayectoria",
       f"{'mutación':10s}{'ΔG_i 2A':>9s}{'ΔG_i 2B':>9s}{'ΔΔG_i':>8s}{'±':>6s}{'vdW':>8s}{'Elec.':>8s}{'Polar':>8s}{'NoPol.':>8s}"]
for f in filas:
    lin.append(f"{f['nombre']:10s}{f['g2A']:9.2f}{f['g2B']:9.2f}{f['dd']:8.2f}{f['err']:6.2f}{f['vdW']:8.2f}{f['Ele']:8.2f}{f['Polar']:8.2f}{f['NoPolar']:8.2f}")
lin.append(f"{'SUMA':10s}{sum(f['g2A'] for f in filas):9.2f}{sum(f['g2B'] for f in filas):9.2f}{tot:8.2f}")
print("\n".join(lin))
(E / "tablas/mutaciones_r1.txt").write_text("\n".join(lin) + "\n", encoding="utf-8")
