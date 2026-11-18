"""Parte E: componentes de energía y su compensación (electrostática frente a solvatación polar).
Uso:  .venv/bin/python scripts/figuras_componentes.py
Lee D_F_energia/resultados_mmgbsa/{2A,2B}/ (r1) y D_F_energia/replicas/resultados/{2A,2B}_r{2,3}/.
Genera D_F_energia/figuras/E_compensacion.png y E_componentes_replicas.png y tablas/componentes_replicas.txt
"""
import sys
from pathlib import Path
import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo_figuras import AZUL, NARANJA, nueva, leyenda_abajo, guardar
import matplotlib.pyplot as plt

# reutiliza el lector de FINAL_RESULTS_MMPBSA.csv
src = (RAIZ / "scripts/analisis_energia.py").read_text().split("# ---------- D y E")[0]
ns = {"__file__": str(RAIZ / "scripts/analisis_energia.py"), "sys": type("S", (), {"argv": ["x"], "path": sys.path})}
exec(compile(src, "parsers", "exec"), ns)
delta = ns["delta_por_frame"]
E = RAIZ / "D_F_energia"

def carpeta(s, r):
    return E / "resultados_mmgbsa" / s if r == 1 else E / "replicas/resultados" / f"{s}_r{r}" / "mmgbsa"

datos = {(s, r): delta(carpeta(s, r) / "FINAL_RESULTS_MMPBSA.csv") for s in ("2A", "2B") for r in (1, 2, 3)}
DDG_EXP = -2.98
out = []
def log(x=""):
    print(x); out.append(x)

# ---- Figura 1: compensación EEL vs EGB por instantánea ----
fig, ax = nueva(7, 4.6)
xs, ys = [], []
for s, col in (("2A", AZUL), ("2B", NARANJA)):
    x = np.concatenate([datos[(s, r)]["EEL"].values for r in (1, 2, 3)])
    y = np.concatenate([datos[(s, r)]["EGB"].values for r in (1, 2, 3)])
    ax.scatter(x, y, s=8, color=col, alpha=0.6, label=s)
    xs += list(x); ys += list(y)
pend, orig = np.polyfit(xs, ys, 1)
r = np.corrcoef(xs, ys)[0, 1]
xx = np.array([min(xs), max(xs)])
ax.plot(xx, pend * xx + orig, "k--", lw=1, label=f"ajuste: pendiente {pend:.2f}, r = {r:.2f}")
ax.set(xlabel="ΔE electrostática (kcal/mol)", ylabel="ΔG solvatación polar, GB (kcal/mol)",
       title="Compensación entre electrostática y solvatación polar (cada punto = una instantánea)")
leyenda_abajo(ax, ncol=3)
guardar(fig, E / "figuras/E_compensacion.png")
log(f"Correlación electrostática–solvatación polar por instantánea (6 corridas, {len(xs)} instantáneas): r = {r:.2f}, pendiente = {pend:.2f}")
for s in ("2A", "2B"):
    eel = np.concatenate([datos[(s, k)]["EEL"].values for k in (1, 2, 3)]); egb = np.concatenate([datos[(s, k)]["EGB"].values for k in (1, 2, 3)])
    log(f"{s}: SD por instantánea: EEL {eel.std():.1f} | GB {egb.std():.1f} | EEL+GB {(eel+egb).std():.1f}")

# ---- Figura 2: ΔΔ por componente con 3 réplicas ----
terminos = [("ΔE vdW", "VDWAALS"), ("ΔE electrostática", "EEL"), ("ΔG solv. polar (GB)", "EGB"),
            ("ΔG solv. no polar", "ESURF"), ("Electrostática + solv. polar", None), ("ΔG de unión", "TOTAL")]
def media_rep(s, k):
    return np.array([(datos[(s, r)]["EEL"].mean() + datos[(s, r)]["EGB"].mean()) if k is None else datos[(s, r)][k].mean() for r in (1, 2, 3)])
nombres, dd, err = [], [], []
log("\nPor componente (media ± SD entre réplicas; ΔΔ = 2B − 2A ± error estándar entre réplicas):")
for n, k in terminos:
    a, b = media_rep("2A", k), media_rep("2B", k)
    d = b.mean() - a.mean(); e = np.hypot(a.std(ddof=1), b.std(ddof=1)) / np.sqrt(3)
    nombres.append(n); dd.append(d); err.append(e)
    log(f"{n:30s} 2A {a.mean():8.2f} ± {a.std(ddof=1):5.2f} | 2B {b.mean():8.2f} ± {b.std(ddof=1):5.2f} | ΔΔ {d:+6.2f} ± {e:4.2f}")
fig, ax = nueva(7, 4.2)
ax.barh(nombres[::-1], dd[::-1], xerr=err[::-1], color=AZUL, height=0.55, capsize=3, error_kw=dict(lw=1))
ax.axvline(0, color="k", lw=1)
ax.axvline(DDG_EXP, color="k", ls="--", lw=1, label=f"ΔΔG experimental ({DDG_EXP})")
leyenda_abajo(ax, ncol=1)
ax.set(xlabel="ΔΔ = 2B − 2A (kcal/mol), media de 3 réplicas ± error entre réplicas",
       title="Cambio de energía por componente (3 réplicas)")
guardar(fig, E / "figuras/E_componentes_replicas.png")
(E / "tablas/componentes_replicas.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("Figuras en", E / "figuras")
