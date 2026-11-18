"""Distancia mínima (Å) de cada posición mutada del nanobody a la RNasa, en 2A y 2B.
Requiere haber cargado antes los objetos 'wt' (2A) y 'mut' (2B), p. ej. con A_mutaciones.pml.
Uso dentro de PyMOL:  run visualizar/distancias_mutaciones.py
"""
import numpy as np
from pymol import cmd

POSICIONES = [28, 29, 30, 101, 102, 104, 105, 106, 107, 110]
print("Posición | 2A (Å)            | 2B (Å)")
for pos in POSICIONES:
    fila = []
    for obj in ("wt", "mut"):
        r = cmd.get_coords(f"{obj} and chain B and resi {pos}")
        a = cmd.get_coords(f"{obj} and chain A")
        d = np.sqrt(((r[:, None, :] - a[None, :, :]) ** 2).sum(-1)).min()
        nombre = cmd.get_model(f"{obj} and chain B and resi {pos} and name CA").atom[0].resn
        fila.append(f"{nombre}{pos:<4} {d:4.1f}{' TOCA' if d <= 4 else '     '}")
    print(f"  {pos:<7}| {fila[0]} | {fila[1]}")
print("(TOCA = algún átomo a 4 Å o menos de la RNasa; la 30 no está mutada, pero entra en 2B)")
