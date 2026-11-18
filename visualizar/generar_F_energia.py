"""Genera visualizar/F_energia_bfactor.pml: colorea System_2B según ΔΔG_i (2B − 2A) por residuo.
Azul = el residuo contribuye MÁS favorablemente en 2B; rojo = MENOS favorablemente.
Usa la descomposición promediada entre las 3 réplicas (la robusta).
Uso:  python3 visualizar/generar_F_energia.py   (no necesita librerías extra)
"""
import csv
from pathlib import Path

raiz = Path(__file__).resolve().parent.parent
filas = list(csv.DictReader(open(raiz / "D_F_energia/tablas/descomposicion_replicas.csv")))
cad = {"NB": "B", "RNasa": "A"}
L = ["# Parte F: ΔΔG por residuo sobre la estructura de 2B (generado por generar_F_energia.py)",
     "# Uso:  pymol visualizar/F_energia_bfactor.pml",
     "reinitialize", "load 01_estructuras/System_2B.pdb, mut", "bg_color white",
     "hide everything", "show cartoon", "alter all, b=0"]
for r in filas:
    L.append(f"alter chain {cad[r['cadena']]} and resi {r['num']}, b={float(r['ddG']):.3f}")
L += ["rebuild", "spectrum b, blue_white_red, mut, minimum=-3, maximum=3",
      "set cartoon_transparency, 0.0",
      "# Residuos con cambio significativo (|ddG| > 2 veces el error entre réplicas) y |ddG| > 0.7"]
sig = [r for r in filas if r["significativo"] == "True" and abs(float(r["ddG"])) > 0.7]
for r in sig:
    L.append(f"show sticks, chain {cad[r['cadena']]} and resi {r['num']}")
    L.append(f"label chain {cad[r['cadena']]} and resi {r['num']} and name CA, "
             f"\"{r['res_2B'].capitalize()}{r['num']} ({float(r['ddG']):+.1f})\"")
L += ["set label_size, 16", "set label_color, black", "orient",
      "zoom (chain B and resi 101+106+107) or (chain A and resi 69), 15",
      "# Para ver solo la interfaz:  hide cartoon, not (byres chain B within 8 of chain A)"]
(raiz / "visualizar/F_energia_bfactor.pml").write_text("\n".join(L) + "\n")
print("Residuos etiquetados:", ", ".join(f"{r['cadena']}:{r['res_2B']}{r['num']}" for r in sig))
