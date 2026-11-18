"""Figuras para interpretar la parte C (RMSD, puentes de H y contactos), 2A vs 2B, en Å y con las ventanas marcadas.
Uso:  .venv/bin/python scripts/figuras_explicativas.py
Salida: C_analisis/figuras/explicativas/
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
D = RAIZ / "C_analisis/datos"
OUT = RAIZ / "C_analisis/figuras/explicativas"
OUT.mkdir(parents=True, exist_ok=True)
COL = {"2A": "#6c757d", "2B": "#2a9d8f"}
NOM = {"2A": "2A (inicial)", "2B": "2B (madurada)"}
plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False, "font.size": 9})

def ser(s, f):
    a = np.array([[float(x) for x in l.split()] for l in open(D / s / f) if l[0] not in "#@"])
    return a[:, 0], a[:, 1]

def sem(x, n=5):
    return np.std([b.mean() for b in np.array_split(x, n)], ddof=1) / np.sqrt(n)

def media_movil(y, k):
    return np.convolve(y, np.ones(k) / k, mode="valid")

# ---------- 1. RMSD ----------
paneles = [("C2_rmsd_complejo.xvg", "Complejo completo", "forma + posición de todo"),
           ("C2_rmsd_nanobody.xvg", "Nanobody (ajustado sobre sí mismo)", "solo su forma interna"),
           ("C2_rmsd_antigeno.xvg", "RNasa (ajustada sobre sí misma)", "solo su forma interna"),
           ("C2_rmsd_nanobody_sobre_antigeno.xvg", "Nanobody ajustando sobre la RNasa", "posición del nanobody respecto a la RNasa")]
fig, axs = plt.subplots(2, 2, figsize=(10, 6.5), layout="constrained")
for ax, (f, titulo, sub) in zip(axs.flat, paneles):
    ax.axvspan(0, 200, color="#e9ecef", zorder=0)
    ax.axvspan(500, 1000, color="#fff3cd", zorder=0)
    for s in ("2A", "2B"):
        t, y = ser(s, f); y = y * 10
        ax.plot(t, y, color=COL[s], lw=0.6, alpha=0.5)
        ax.plot(t[19:], media_movil(y, 20), color=COL[s], lw=1.8, label=f"{NOM[s]}: {y[t >= 500].mean():.2f} Å")
        ax.hlines(y[t >= 500].mean(), 500, 1000, color=COL[s], ls="--", lw=1)
    ax.set(title=f"{titulo}\n({sub})", xlabel="Tiempo (ps)", ylabel="RMSD de Cα (Å)", xlim=(0, 1000), ylim=(0, None))
    ax.legend(frameon=False, loc="lower right", title="media 500–1000 ps")
fig.suptitle("RMSD: gris = equilibración inicial (no se interpreta), amarillo = ventana de análisis. Línea gruesa = media móvil de 20 ps")
fig.savefig(OUT / "RMSD_4_paneles.png"); plt.close(fig)

# ---------- 2 y 3. Puentes de H y contactos ----------
def figura(f, nombre, ylabel, fname, entero):
    fig = plt.figure(figsize=(10.5, 6.5), layout="constrained")
    gs = fig.add_gridspec(2, 3)
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, 0]); ax3 = fig.add_subplot(gs[1, 1]); ax4 = fig.add_subplot(gs[1, 2])
    ax1.axvspan(0, 200, color="#e9ecef", zorder=0); ax1.axvspan(500, 1000, color="#fff3cd", zorder=0)
    datos = {}
    for s in ("2A", "2B"):
        t, y = ser(s, f); datos[s] = (t, y)
        ax1.plot(t, y, color=COL[s], lw=0.4, alpha=0.35)
        ax1.plot(t[49:], media_movil(y, 50), color=COL[s], lw=2, label=f"{NOM[s]} (media móvil de 50 ps)")
    ax1.set(title=f"{nombre} en el tiempo: la línea gruesa muestra la tendencia; el ruido fino es normal",
            xlabel="Tiempo (ps)", ylabel=ylabel, xlim=(0, 1000))
    ax1.legend(frameon=False, ncol=2, loc="upper left")
    x = {s: datos[s][1][datos[s][0] >= 500] for s in datos}
    # histograma
    if entero:
        vals = np.arange(min(v.min() for v in x.values()), max(v.max() for v in x.values()) + 1)
        for i, s in enumerate(("2A", "2B")):
            fr = [(x[s] == v).mean() * 100 for v in vals]
            ax2.bar(vals + (i - 0.5) * 0.4, fr, 0.4, color=COL[s], label=NOM[s])
    else:
        for s in ("2A", "2B"):
            ax2.hist(x[s], bins=30, alpha=0.6, color=COL[s], density=True, label=NOM[s])
    ax2.set(title="Distribución (500–1000 ps)", xlabel=ylabel, ylabel="% de cuadros" if entero else "densidad")
    ax2.legend(frameon=False)
    # medias con error
    for i, s in enumerate(("2A", "2B")):
        ax3.errorbar(i, x[s].mean(), yerr=sem(x[s]), fmt="o", color=COL[s], capsize=5, ms=8)
        ax3.text(i, x[s].mean(), f"  {x[s].mean():.2f} ± {sem(x[s]):.2f}", va="bottom", fontsize=9)
    d = x["2B"].mean() - x["2A"].mean(); se = np.hypot(sem(x["2A"]), sem(x["2B"]))
    ax3.set_xticks([0, 1], ["2A", "2B"]); ax3.set_xlim(-0.6, 1.9)
    ax3.set(title=f"Media ± error (5 bloques)\nΔ = {d:+.2f} ± {se:.2f}  ({d/se:.1f}× el error)", ylabel=ylabel)
    # medias por bloques de 100 ps
    ed = np.arange(0, 1000, 100)
    for s in ("2A", "2B"):
        t, y = datos[s]
        ax4.plot(ed + 50, [y[(t >= a) & (t < a + 100)].mean() for a in ed], "o-", color=COL[s], label=NOM[s])
    ax4.axvspan(0, 200, color="#e9ecef", zorder=0)
    ax4.set(title="Media por bloques de 100 ps", xlabel="Tiempo (ps)", ylabel=ylabel)
    fig.savefig(OUT / fname); plt.close(fig)

figura("C3_puentes_H.xvg", "Puentes de H nanobody–RNasa", "N.º de puentes de H", "Puentes_H_analisis.png", True)
figura("C3_contactos_4A.xvg", "Pares de átomos a < 4 Å", "N.º de pares de átomos", "Contactos_analisis.png", False)
print("Figuras en", OUT)
