"""Análisis cuantitativo de la interfaz nanobody–RNasa en los cristales 2A y 2B.
Uso (desde cualquier carpeta):
    pymol -cq -d "run /ruta/al/proyecto/visualizar/analisis_interfaz.py"
Escribe A_inspeccion/tablas/analisis_interfaz.txt (y lo imprime).
Cubre: área enterrada, pares de átomos, composición y cargas de cada lado de la interfaz,
cargas con distintos cortes de distancia, contactos polares N/O a <= 3.5 Å (comunes y nuevos)
y distancia mínima de cada posición mutada a la RNasa.
"""
import math, os
import numpy as np
from pymol import cmd

RAIZ = next(d for d in (os.getcwd(), os.path.expanduser("~/Documents/githubrepos/genetic-engineering"))
            if os.path.isdir(os.path.join(d, "01_estructuras")))
OUT = os.path.join(RAIZ, "A_inspeccion/tablas/analisis_interfaz.txt")
MUT = [28, 29, 30, 101, 102, 104, 105, 106, 107, 110]
CLASES = {"aromáticos (Tyr,Trp,Phe)": "TYR TRP PHE", "apolares (Gly,Ala,Val,Ile,Leu,Met,Pro)": "GLY ALA VAL ILE LEU MET PRO",
          "polares neutros (Ser,Thr,Asn,Gln,Cys,His)": "SER THR ASN GLN CYS HIS", "positivos (Arg,Lys)": "ARG LYS",
          "negativos (Asp,Glu)": "ASP GLU"}
lineas = []
def log(s=""):
    print(s); lineas.append(s)

for s in ("2A", "2B"):
    cmd.load(os.path.join(RAIZ, f"01_estructuras/System_{s}.pdb"), f"s{s}")
cmd.remove("hydrogens")
cmd.set("dot_solvent", 1); cmd.set("dot_density", 4)

def residuos(sel):
    r = []
    cmd.iterate(sel + " and name CA", "r.append((int(resi), resn))", space={"r": r})
    return sorted(r)

def coords(sel):
    return cmd.get_coords(sel)

def interfaz(o, lado, corte):
    otro = "A" if lado == "B" else "B"
    cmd.select("tmp_i", f"byres ({o} and chain {lado}) within {corte} of ({o} and chain {otro})")
    r = residuos("tmp_i"); cmd.delete("tmp_i"); return r

log("=== 1. Tamaño de la interfaz (cristal) ===")
for s in ("2A", "2B"):
    o = f"s{s}"
    cmd.create(o + "_A", o + " and chain A"); cmd.create(o + "_B", o + " and chain B")
    bsa = cmd.get_area(o + "_A") + cmd.get_area(o + "_B") - cmd.get_area(o)
    d = np.sqrt(((coords(o + " and chain A")[:, None] - coords(o + " and chain B")[None]) ** 2).sum(-1))
    log(f"{s}: área enterrada {bsa:.0f} Å²  | pares de átomos pesados a < 4 Å: {(d < 4).sum()}")

log("\n=== 2. Composición de cada lado de la interfaz (corte 4 Å) ===")
for s in ("2A", "2B"):
    for lado, nombre in (("B", "Nanobody"), ("A", "RNasa")):
        r = interfaz(f"s{s}", lado, 4)
        cuenta = {k: sum(1 for _, n in r if n in v.split()) for k, v in CLASES.items()}
        log(f"{s} {nombre} ({len(r)} residuos): " + "; ".join(f"{k.split(' ')[0]} {c}" for k, c in cuenta.items()))

log("\n=== 3. Cargas en la interfaz según el corte de distancia ===")
for s in ("2A", "2B"):
    for corte in (4, 5, 6):
        partes = []
        for lado, nombre in (("B", "NB"), ("A", "RNasa")):
            r = interfaz(f"s{s}", lado, corte)
            pos = [f"{n.title()}{i}" for i, n in r if n in ("ARG", "LYS")]
            neg = [f"{n.title()}{i}" for i, n in r if n in ("ASP", "GLU")]
            partes.append(f"{nombre} (+){pos or '-'} (-){neg or '-'}")
        log(f"{s} corte {corte} Å: " + " | ".join(partes))

log("\n=== 4. Contactos polares N/O a <= 3.5 Å entre cadenas ===")
pares = {}
for s in ("2A", "2B"):
    o = f"s{s}"; lista = []
    atB = []; atA = []
    cmd.iterate_state(1, f"{o} and chain B and (elem N or elem O)", "atB.append((resn, int(resi), name, (x, y, z)))", space={"atB": atB})
    cmd.iterate_state(1, f"{o} and chain A and (elem N or elem O)", "atA.append((resn, int(resi), name, (x, y, z)))", space={"atA": atA})
    for b in atB:
        for a in atA:
            dd = math.dist(b[3], a[3])
            if dd <= 3.5:
                lista.append((int(b[1]), f"{b[0].title()}{b[1]}:{b[2]}", f"{a[0].title()}{a[1]}:{a[2]}", dd))
    pares[s] = sorted(lista)
    log(f"{s}: {len(lista)} contactos")
    for _, x, y, d in pares[s]:
        log(f"   {x:14s} – {y:14s} {d:.2f} Å")

log("\n=== 5. Distancia mínima de cada posición del nanobody a la RNasa (Å) ===")
log("posición |  2A            |  2B")
for p in MUT:
    fila = []
    for s in ("2A", "2B"):
        o = f"s{s}"
        r = coords(f"{o} and chain B and resi {p}"); a = coords(f"{o} and chain A")
        d = np.sqrt(((r[:, None] - a[None]) ** 2).sum(-1)).min()
        n = [rn for _, rn in residuos(f"{o} and chain B and resi {p}")][0].title()
        fila.append(f"{n}{p} {d:.1f}{' toca' if d <= 4 else '     '}")
    log(f"  {p:<6} |  {fila[0]:15s}|  {fila[1]}")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write("\n".join(lineas) + "\n")
print("\nGuardado en", OUT)
