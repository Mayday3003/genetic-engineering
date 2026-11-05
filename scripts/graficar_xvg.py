#!/usr/bin/env python3
"""Grafica uno o varios archivos .xvg de GROMACS en la misma figura.

Uso:
    python3 graficar_xvg.py archivo.xvg [otro.xvg ...] [opciones]

Opciones:
    -o salida.png      guarda la figura (si no se da, solo la muestra)
    --etiquetas 2A 2B  nombre de cada curva en la leyenda (en el mismo orden)
    --desde 5          ignora los puntos con x < 5 (útil en minimización)
    --ymin / --ymax    límites del eje y
"""
import argparse
import re

import matplotlib.pyplot as plt
import numpy as np


def leer_xvg(ruta):
    """Devuelve (x, y, etiqueta_x, etiqueta_y, titulo) de un .xvg."""
    xs, ys = [], []
    meta = {"xaxis": "x", "yaxis": "y", "title": ruta}
    with open(ruta) as f:
        for linea in f:
            if linea.startswith("#"):          # comentarios de GROMACS
                continue
            if linea.startswith("@"):          # metadatos de xmgrace: títulos de ejes
                m = re.match(r'@\s+(xaxis|yaxis|title)\s+(?:label\s+)?"(.*)"', linea)
                if m:
                    meta[m.group(1)] = m.group(2).replace("\\S", "").replace("\\N", "")
                continue
            columnas = linea.split()
            xs.append(float(columnas[0]))
            ys.append(float(columnas[1]))      # primera serie de datos
    return np.array(xs), np.array(ys), meta["xaxis"], meta["yaxis"], meta["title"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("archivos", nargs="+")
    p.add_argument("-o", "--salida")
    p.add_argument("--etiquetas", nargs="+")
    p.add_argument("--desde", type=float)
    p.add_argument("--ymin", type=float)
    p.add_argument("--ymax", type=float)
    a = p.parse_args()

    etiquetas = a.etiquetas or a.archivos
    plt.figure(figsize=(7, 4))
    for ruta, etiqueta in zip(a.archivos, etiquetas):
        x, y, xlab, ylab, titulo = leer_xvg(ruta)
        if a.desde is not None:
            x, y = x[x >= a.desde], y[x >= a.desde]
        plt.plot(x, y, lw=1, label=f"{etiqueta} (prom. {y.mean():.4g})")

    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(titulo)
    plt.ylim(a.ymin, a.ymax)
    plt.legend()
    plt.tight_layout()
    if a.salida:
        plt.savefig(a.salida, dpi=300)
        print("Figura guardada en", a.salida)
    else:
        plt.show()


if __name__ == "__main__":
    main()
