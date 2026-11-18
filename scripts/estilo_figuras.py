"""Estilo común de las figuras (mismo que C_analisis/figuras, hechas con scripts/graficar_xvg.py):
colores por defecto de matplotlib (azul = 2A, naranja = 2B), marco completo, líneas finas,
leyenda debajo del gráfico y 300 dpi."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AZUL = "tab:blue"      # 2A
NARANJA = "tab:orange"  # 2B
plt.rcdefaults()

def nueva(ancho=7, alto=4):
    return plt.subplots(figsize=(ancho, alto))

def leyenda_abajo(ax, ncol=2, **kw):
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=ncol, frameon=False, **kw)

def guardar(fig, ruta):
    fig.tight_layout()
    fig.savefig(ruta, dpi=300, bbox_inches="tight")
    plt.close(fig)
