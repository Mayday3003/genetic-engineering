"""Estadística de las series C3 (puentes de H y contactos < 4 Å): ¿es real la diferencia 2A vs 2B?
Uso:  python3 scripts/estadistica_c3.py        (solo requiere numpy)
Escribe C_analisis/datos/estadistica_C3.txt.
Ventana principal: 500–1000 ps. Error = SEM por bloques (5 bloques de 100 ps), igual que en la parte D.
"""
from pathlib import Path
import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
D = RAIZ / "C_analisis/datos"
out = []
def log(s=""):
    print(s); out.append(s)

def serie(s, f):
    a = np.array([[float(x) for x in l.split()] for l in open(D / s / f) if l[0] not in "#@"])
    return a[:, 0], a[:, 1]

def sem_bloques(x, n=5):
    m = np.array([b.mean() for b in np.array_split(x, n)])
    return m.std(ddof=1) / np.sqrt(n)

def sem_por_tamano(x, sizes=(10, 25, 50, 100)):
    r = []
    for s in sizes:
        n = len(x) // s
        r.append(f"{s}:{x[:n*s].reshape(n, s).mean(1).std(ddof=1)/np.sqrt(n):.2f}")
    return " ".join(r)

for nombre, f in (("Puentes de H nanobody–RNasa", "C3_puentes_H.xvg"), ("Pares de átomos a < 4 Å", "C3_contactos_4A.xvg")):
    log(f"=== {nombre} ===")
    x = {}
    for s in ("2A", "2B"):
        t, y = serie(s, f)
        x[s] = y[t >= 500]
        log(f"{s} (500–1000 ps, n={len(x[s])}): media {x[s].mean():.2f} | SD {x[s].std():.2f} | SEM(5 bloques) {sem_bloques(x[s]):.2f} | "
            f"rango {x[s].min():.0f}–{x[s].max():.0f}")
        log(f"    SEM según tamaño de bloque (frames): {sem_por_tamano(x[s])}")
    a, b = x["2A"], x["2B"]
    d = b.mean() - a.mean()
    se = float(np.hypot(sem_bloques(a), sem_bloques(b)))
    sp = np.sqrt((a.var() + b.var()) / 2)
    ps = (b[:, None] > a[None, :]).mean() + 0.5 * (b[:, None] == a[None, :]).mean()
    log(f"Diferencia 2B − 2A = {d:+.2f} ± {se:.2f} | cociente dif/error = {d/se:.1f} | d de Cohen = {d/sp:.2f} | P(2B > 2A) = {ps:.2f}")
    if "H" in f:
        for s in ("2A", "2B"):
            v = x[s]
            dist = ", ".join(f"{int(k)}: {100*(v==k).mean():.0f}%" for k in np.unique(v))
            log(f"    {s} distribución de puentes de H por cuadro → {dist}")
            log(f"    {s} cuadros con ≥ 7: {100*(v>=7).mean():.0f}% | con ≥ 8: {100*(v>=8).mean():.0f}%")
    log()
(D / "estadistica_C3.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
