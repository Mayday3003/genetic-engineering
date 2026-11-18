"""Combina las 3 réplicas por sistema (r1 = corrida original, r2 y r3 = réplicas nuevas).

Uso: python scripts/analisis_replicas.py
Lee D_F_energia/resultados_mmgbsa/{2A,2B}/ (r1) y D_F_energia/replicas/resultados/{2A,2B}_r{2,3}/ .
Reporta ΔG y ΔΔG por réplica y la media ± desviación entre réplicas (error "real" de muestreo),
y la descomposición por residuo promediada entre réplicas.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util

RAIZ = Path(__file__).resolve().parent.parent
E = RAIZ / "D_F_energia"
# reutiliza los parsers de analisis_energia.py sin ejecutar su main
src = (RAIZ / "scripts/analisis_energia.py").read_text().split("# ---------- D y E")[0]
ns = {"__file__": str(RAIZ / "scripts/analisis_energia.py"), "sys": type("S", (), {"argv": ["x"]})}
exec(compile(src, "analisis_energia_parsers", "exec"), ns)
delta_por_frame, decomp = ns["delta_por_frame"], ns["decomp"]

def carpeta(sis, rep):
    return E / "resultados_mmgbsa" / sis if rep == 1 else E / "replicas/resultados" / f"{sis}_r{rep}" / "mmgbsa"

reps = {s: [r for r in (1, 2, 3) if (carpeta(s, r) / "FINAL_RESULTS_MMPBSA.csv").exists()] for s in ("2A", "2B")}
print("Réplicas disponibles:", reps)
if min(len(v) for v in reps.values()) < 2:
    sys.exit("Faltan réplicas (coloca los resultados en D_F_energia/replicas/resultados/).")

terminos = ["VDWAALS", "EEL", "EGB", "ESURF", "TOTAL"]
filas = []
for s in ("2A", "2B"):
    for r in reps[s]:
        d = delta_por_frame(carpeta(s, r) / "FINAL_RESULTS_MMPBSA.csv")
        filas.append(dict(sis=s, rep=r, **{k: d[k].mean() for k in terminos}))
df = pd.DataFrame(filas)
out = []
def log(x=""):
    print(x); out.append(x)

log("=== ΔG por réplica (kcal/mol) ===")
log(df.round(2).to_string(index=False))
m = df.groupby("sis")[terminos].agg(["mean", "std"])
log("\n=== Media ± SD entre réplicas ===")
for s in ("2A", "2B"):
    log(f"{s}: " + "  ".join(f"{k} {m.loc[s,(k,'mean')]:.2f}±{m.loc[s,(k,'std')]:.2f}" for k in terminos))

# ΔΔG: todas las combinaciones 2B_i - 2A_j, y emparejando por número de réplica
a = df[df.sis == "2A"].set_index("rep"); b = df[df.sis == "2B"].set_index("rep")
comb = pd.DataFrame([{k: b.loc[j, k] - a.loc[i, k] for k in terminos} for i in a.index for j in b.index])
log("\n=== ΔΔG = 2B − 2A (kcal/mol), media ± SD de todas las combinaciones de réplicas ===")
for k in terminos:
    log(f"{k:8s} {comb[k].mean():+.2f} ± {comb[k].std():.2f}")
dd = b["TOTAL"].mean() - a["TOTAL"].mean()
se = float(np.hypot(a["TOTAL"].std() / np.sqrt(len(a)), b["TOTAL"].std() / np.sqrt(len(b))))
log(f"\nΔΔG_calc = {dd:+.2f} ± {se:.2f} (error estándar entre réplicas)   ΔΔG_exp = -2.98")
log(f"Réplicas con ΔΔG negativo (2B−2A, combinaciones): {(comb['TOTAL'] < 0).sum()} de {len(comb)}")

# Figura
fig, ax = plt.subplots(figsize=(5.5, 3.6), layout="constrained")
for i, s in enumerate(("2A", "2B")):
    y = df[df.sis == s].TOTAL
    ax.scatter([i] * len(y), y, color=["#6c757d", "#2a9d8f"][i], zorder=3)
    ax.hlines(y.mean(), i - 0.25, i + 0.25, color="k")
ax.set_xticks([0, 1], ["2A (inicial)", "2B (madurada)"])
ax.set(ylabel="ΔG unión (kcal/mol)", title=f"ΔG por réplica (ΔΔG = {dd:+.2f} ± {se:.2f})")
(E / "figuras").mkdir(exist_ok=True)
fig.savefig(E / "figuras/D_replicas_dG.png", dpi=150)

# Descomposición por residuo promediada entre réplicas
def promedio(s):
    acc = {}
    for r in reps[s]:
        for k, v in decomp(carpeta(s, r) / "FINAL_DECOMP_MMPBSA.csv").items():
            acc.setdefault(k, {"res": v["res"], "g": []})["g"].append(np.mean(v["TOTAL"]))
    return acc
pa, pb = promedio("2A"), promedio("2B")
filas = []
for k in sorted(set(pa) & set(pb)):
    ga, gb = pa[k]["g"], pb[k]["g"]
    filas.append(dict(cadena=k[0], num=k[1], res_2A=pa[k]["res"], res_2B=pb[k]["res"],
                      dG_2A=np.mean(ga), dG_2B=np.mean(gb), ddG=np.mean(gb) - np.mean(ga),
                      ddG_se=float(np.hypot(np.std(ga, ddof=1) / np.sqrt(len(ga)), np.std(gb, ddof=1) / np.sqrt(len(gb))))))
r = pd.DataFrame(filas)
r["significativo"] = r.ddG.abs() > 2 * r.ddG_se
(E / "tablas").mkdir(exist_ok=True)
r.round(3).to_csv(E / "tablas/descomposicion_replicas.csv", index=False)
log("\n=== Top 15 |ΔΔG_i| promediado entre réplicas (significativo = |ΔΔG_i| > 2·error entre réplicas) ===")
t = r.reindex(r.ddG.abs().sort_values(ascending=False).index).head(15)
log(t.round(2).to_string(index=False))
log(f"\nΣΔΔG_i mutados: {r[(r.cadena=='NB') & r.num.isin([28,29,101,102,104,105,106,107,110])].ddG.sum():+.2f} | "
    f"NB no mutado: {r[(r.cadena=='NB') & ~r.num.isin([28,29,101,102,104,105,106,107,110])].ddG.sum():+.2f} | "
    f"RNasa: {r[r.cadena=='RNasa'].ddG.sum():+.2f}")

# Figura: residuos que más cambian (media de las 3 réplicas); las barras con borde grueso son significativas
t15 = r.reindex(r.ddG.abs().sort_values(ascending=False).index).head(15)[::-1]
def etiq(x):
    mut = f"→{x.res_2B}" if x.res_2A != x.res_2B else ""
    return f"{x.cadena}:{x.res_2A}{x.num}{mut}"
fig, ax = plt.subplots(figsize=(7.5, 5.5), layout="constrained")
ax.barh([etiq(x) for x in t15.itertuples()], t15.ddG, xerr=t15.ddG_se,
        color=["#2a9d8f" if v < 0 else "#e76f51" for v in t15.ddG], height=0.65,
        edgecolor=["black" if sg else "none" for sg in t15.significativo], linewidth=1.6, error_kw=dict(lw=1))
ax.axvline(0, color="#444", lw=1)
ax.set(xlabel="ΔΔG_i = ΔG_i(2B) − ΔG_i(2A) (kcal/mol), media de 3 réplicas ± error entre réplicas",
       title="F. Residuos que más cambian (borde negro = |ΔΔG_i| > 2× error)")
fig.savefig(E / "figuras/F_top_ddg_replicas.png", dpi=150)

(E / "tablas/resumen_replicas.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
