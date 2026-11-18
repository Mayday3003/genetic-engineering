#!/bin/bash
# Puentes salinos DENTRO del nanobody (parte C): distancia mínima entre el grupo cargado del Asp/Glu y el del Arg
# a lo largo de la producción, y su ocupación (fracción de cuadros a <= 4 Å entre 200 y 1000 ps).
# Uso (desde la raíz del proyecto):  bash scripts/puentes_salinos_internos.sh
set -euo pipefail
OUT=$PWD/C_analisis/datos
mkdir -p "$OUT/2A" "$OUT/2B"
par() {  # par <sis> <res neg> "<átomos neg>" <res pos> "<átomos pos>" <salida>
    local sel=""
    for a in $3; do for b in $5; do
        sel="$sel group \"Protein_chain2\" and resid $2 and name $a plus group \"Protein_chain2\" and resid $4 and name $b plus"
    done; done
    sel=${sel% plus}
    gmx distance -s B_dinamica/$1_colab/proteina.tpr -f B_dinamica/$1_colab/proteina.xtc \
        -n B_dinamica/$1_colab/proteina.ndx -oall "$OUT/$1/$6.xvg" -select "$sel" > /dev/null 2>&1
    python3 - "$OUT/$1/$6.xvg" "$1 $2–$4" <<'PY'
import sys, statistics as st
f, etiqueta = sys.argv[1:3]
filas = [l.split() for l in open(f) if l[0] not in "#@"]
m = [min(float(x) for x in r[1:]) * 10 for r in filas if float(r[0]) >= 200]
print(f"{etiqueta:12s} distancia mínima media {st.mean(m):4.1f} Å | ocupación (<=4 Å) {100*sum(x<=4 for x in m)/len(m):3.0f} %")
PY
}
NE="NE NH1 NH2"
echo "2B: Asp101 (nuevo) – Arg107";       par 2B 101 "OD1 OD2" 107 "$NE" C4_interno_Asp101_Arg107
echo "2A: Asp105 (framework) – Arg45";    par 2A 105 "OD1 OD2" 45  "$NE" C4_interno_Asp105_Arg45
echo "2A: Glu102 – Arg104";               par 2A 102 "OE1 OE2" 104 "$NE" C4_interno_Glu102_Arg104
