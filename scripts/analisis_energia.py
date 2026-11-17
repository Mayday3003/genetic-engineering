"""D-F. Análisis de los resultados de gmx_MMPBSA para 2A y 2B.

Uso: python scripts/analisis_energia.py [carpeta_resultados] [carpeta_salida]
Por defecto lee D_F_energia/resultados_mmgbsa/{2A,2B}/ y escribe en D_F_energia/.

En el CSV de descomposición los residuos vienen como "R::TYR:101" / "L::GLN:101"
(sin letra de cadena): R = receptor = nanobody (Protein_chain2),
L = ligando = RNasa A (Protein_chain1). La clave por residuo es (R/L, número).
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RES = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "D_F_energia/resultados_mmgbsa"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / "D_F_energia"
FIG = OUT / "figuras"
TAB = OUT / "tablas"
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)

DDG_EXP = -2.98
CADENA = {"R": "NB", "L": "RNasa"}
MUTADOS = {28, 29, 101, 102, 104, 105, 106, 107, 110}
plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False})


def block_sem(x, n=5):
    medias = [b.mean() for b in np.array_split(np.asarray(x, float), n)]
    return float(np.std(medias, ddof=1) / np.sqrt(n))


def delta_por_frame(ruta):
    """Tabla por frame de 'Delta Energy Terms' en FINAL_RESULTS_MMPBSA.csv."""
    filas, cab, dentro = [], None, False
    for row in csv.reader(open(ruta, encoding="utf-8")):
        c = row[0].strip() if row else ""
        if c == "Delta Energy Terms":
            dentro = True
        elif dentro and c == "Frame #":
            cab = row
        elif dentro and cab and c.isdigit():
            filas.append(row)
        elif dentro and cab:
            break
    return pd.DataFrame(filas, columns=cab).drop(columns="Frame #").astype(float)


def decomp(ruta):
    """{(cadena, num): {res, TOTAL[], vdW[], Ele[], Polar[], NoPolar[]}} de la sección DELTAS/TDC."""
    cols = ["vdW", "Ele", "Polar", "NoPolar", "TOTAL"]
    datos, seccion, tdc = {}, None, False
    for row in csv.reader(open(ruta, encoding="utf-8")):
        c = row[0].strip() if row else ""
        if c in ("Complex:", "Receptor:", "Ligand:", "DELTAS:"):
            seccion = c
        elif c.startswith("Total Decomposition"):
            tdc = True
        elif c.startswith(("Sidechain", "Backbone")):
            tdc = False
        elif seccion == "DELTAS:" and tdc and c.isdigit():
            rl, _, nombre, num = row[1].split(":")
            r = datos.setdefault((CADENA[rl], int(num)), {"res": nombre})
            for k, v in zip(cols, row[3:8]):
                r.setdefault(k, []).append(float(v))
    return datos


lineas = []
def log(s=""):
    print(s)
    lineas.append(s)


# ---------- D y E: componentes globales ----------
d = {s: delta_por_frame(RES / s / "FINAL_RESULTS_MMPBSA.csv") for s in ("2A", "2B")}
terminos = {"VDWAALS": "ΔE vdW", "EEL": "ΔE electrostática", "EGB": "ΔG solv. polar (GB)",
            "ESURF": "ΔG solv. no polar", "GGAS": "ΔG gas", "GSOLV": "ΔG solv", "TOTAL": "ΔG unión"}
filas = []
for k, nombre in terminos.items():
    a, b = d["2A"][k], d["2B"][k]
    ea, eb = block_sem(a), block_sem(b)
    filas.append(dict(termino=nombre, dG_2A=a.mean(), sem_2A=ea, dG_2B=b.mean(), sem_2B=eb,
                      ddG=b.mean() - a.mean(), ddG_sem=float(np.hypot(ea, eb))))
g = pd.DataFrame(filas)
g.round(2).to_csv(TAB / "componentes.csv", index=False)
log("=== D y E. Componentes (kcal/mol; ± = SEM por bloques, 5 bloques) ===")
log(g.round(2).to_string(index=False))
tot = g.set_index("termino").loc["ΔG unión"]
el = g.set_index("termino").loc[["ΔE electrostática", "ΔG solv. polar (GB)"], "ddG"].sum()
log(f"\nΔΔG_calc = {tot.ddG:+.2f} ± {tot.ddG_sem:.2f} kcal/mol   ΔΔG_exp = {DDG_EXP:+.2f}")
log(f"ΔΔ(EEL + EGB) = {el:+.2f} kcal/mol")

fig, ax = plt.subplots(figsize=(7.5, 3.6), layout="constrained")
p = g[g.termino.isin(["ΔE vdW", "ΔE electrostática", "ΔG solv. polar (GB)", "ΔG solv. no polar", "ΔG unión"])][::-1]
ax.barh(p.termino, p.ddG, xerr=p.ddG_sem, color=["#2a9d8f" if v < 0 else "#e76f51" for v in p.ddG],
        height=0.55, error_kw=dict(lw=1))
ax.axvline(0, color="#444", lw=1)
ax.axvline(DDG_EXP, color="#1d3557", ls="--", lw=1.2, label=f"ΔΔG exp = {DDG_EXP}")
ax.legend(frameon=False)
ax.set(xlabel="ΔΔG = 2B − 2A (kcal/mol)", title="D–E. Cambio por componente")
fig.savefig(FIG / "D_componentes_ddg.png")
plt.close(fig)

t = np.linspace(500, 1000, len(d["2A"]))
fig, ax = plt.subplots(figsize=(7.5, 3.2), layout="constrained")
for s, lbl, col in (("2A", "2A (inicial)", "#6c757d"), ("2B", "2B (madurada)", "#2a9d8f")):
    y = d[s]["TOTAL"].to_numpy()
    ax.plot(t, y, alpha=0.35, lw=1, color=col)
    ax.plot(t, pd.Series(y).rolling(10, min_periods=1, center=True).mean(), lw=2, color=col,
            label=f"{lbl}: media {y.mean():.1f}")
ax.set(xlabel="Tiempo (ps)", ylabel="ΔG unión (kcal/mol)", title="D. ΔG de unión en la ventana analizada")
ax.legend(frameon=False)
fig.savefig(FIG / "D_serie_tiempo_dG.png")
plt.close(fig)

# ---------- F: descomposición por residuo ----------
r = {s: decomp(RES / s / "FINAL_DECOMP_MMPBSA.csv") for s in ("2A", "2B")}
filas = []
for k in sorted(set(r["2A"]) | set(r["2B"])):
    a, b = r["2A"].get(k), r["2B"].get(k)
    m = lambda x, c: float(np.mean(x[c])) if x else 0.0
    cat = ("Mutado" if k[0] == "NB" and k[1] in MUTADOS else "NB no mutado") if k[0] == "NB" else "RNasa"
    fila = dict(cadena=k[0], num=k[1], res_2A=a["res"] if a else "-", res_2B=b["res"] if b else "-",
                categoria=cat, dG_2A=m(a, "TOTAL"), dG_2B=m(b, "TOTAL"))
    fila["ddG"] = fila["dG_2B"] - fila["dG_2A"]
    fila["ddG_sem"] = float(np.hypot(block_sem(a["TOTAL"]) if a else 0, block_sem(b["TOTAL"]) if b else 0))
    for c in ("vdW", "Ele", "Polar", "NoPolar"):
        fila[f"dd_{c}"] = m(b, c) - m(a, c)
    filas.append(fila)
df = pd.DataFrame(filas)
df.round(3).to_csv(TAB / "descomposicion_por_residuo.csv", index=False)

def etiqueta(x):
    mut = f"→{x.res_2B}" if "-" not in (x.res_2A, x.res_2B) and x.res_2A != x.res_2B else ""
    return f"{x.cadena}:{x.res_2A if x.res_2A != '-' else x.res_2B}{x.num}{mut}"

cols = ["cadena", "num", "res_2A", "res_2B", "dG_2A", "dG_2B", "ddG", "ddG_sem", "dd_vdW", "dd_Ele", "dd_Polar"]
log("\n=== F. Posiciones mutadas ===")
log(df[df.categoria == "Mutado"][cols].round(2).to_string(index=False))
log("\n=== F. Top 20 |ΔΔG_i| ===")
top = df.reindex(df.ddG.abs().sort_values(ascending=False).index)
log(top.head(20)[cols + ["categoria"]].round(2).to_string(index=False))
log("\n=== F. Suma de ΔΔG_i por región ===")
for cat in ("Mutado", "NB no mutado", "RNasa"):
    log(f"{cat:14s} {df[df.categoria == cat].ddG.sum():+.2f} kcal/mol")
log(f"{'Total':14s} {df.ddG.sum():+.2f} kcal/mol (la descomposición no suma exactamente el ΔΔG global)")
for s in ("2A", "2B"):
    h = df.nsmallest(10, f"dG_{s}")
    log(f"\nHotspots {s}: " + ", ".join(f"{c}:{n}{x} ({v:.1f})" for c, n, x, v in
                                         zip(h.cadena, h.res_2A if s == "2A" else h.res_2B, h.num, h[f"dG_{s}"])))
log("\nResiduos presentes en un solo sistema: " +
    ", ".join(etiqueta(x) for x in df[(df.res_2A == "-") | (df.res_2B == "-")].itertuples()))

t18 = top.head(18)[::-1]
fig, ax = plt.subplots(figsize=(7.5, 5.5), layout="constrained")
colores = ["#2a9d8f" if v < 0 else "#e76f51" for v in t18.ddG]
ax.barh([etiqueta(x) for x in t18.itertuples()], t18.ddG, xerr=t18.ddG_sem, color=colores, height=0.65,
        error_kw=dict(lw=1))
ax.axvline(0, color="#444", lw=1)
ax.set(xlabel="ΔΔG_i = ΔG_i(2B) − ΔG_i(2A) (kcal/mol)", title="F. Residuos que más cambian su contribución")
fig.savefig(FIG / "F_top_ddg_residuo.png")
plt.close(fig)

# Mapa de la interfaz: ΔG_i en 2A vs 2B de residuos con |ΔG_i| > 0.5 en algún sistema
sel = df[(df.dG_2A.abs() > 0.5) | (df.dG_2B.abs() > 0.5)].sort_values(["cadena", "num"])
fig, axs = plt.subplots(1, 2, figsize=(10, 4.5), layout="constrained", sharey=True,
                        gridspec_kw=dict(width_ratios=[(sel.cadena == "NB").sum(), (sel.cadena == "RNasa").sum()]))
for ax, cad in zip(axs, ("NB", "RNasa")):
    s = sel[sel.cadena == cad]
    x = np.arange(len(s))
    ax.bar(x - 0.2, s.dG_2A, 0.4, color="#6c757d", label="2A")
    ax.bar(x + 0.2, s.dG_2B, 0.4, color="#2a9d8f", label="2B")
    ax.set_xticks(x, [f"{a}{n}" + (f"/{b}" if a != b else "") for a, b, n in zip(s.res_2A, s.res_2B, s.num)],
                  rotation=90, fontsize=7)
    ax.axhline(0, color="#444", lw=0.8)
    ax.set_title("Nanobody" if cad == "NB" else "RNasa A")
axs[0].set_ylabel("ΔG_i (kcal/mol)")
axs[0].legend(frameon=False)
fig.suptitle("F. Mapa energético de la interfaz (|ΔG_i| > 0.5 en algún sistema)")
fig.savefig(FIG / "F_mapa_interfaz.png")
plt.close(fig)

(TAB / "resumen_energia.txt").write_text("\n".join(lineas) + "\n", encoding="utf-8")
print(f"\nGuardado en {FIG} y {TAB}")
