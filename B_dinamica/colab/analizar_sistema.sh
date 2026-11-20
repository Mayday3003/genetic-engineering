#!/bin/bash
# Verificaciones de B y calculos de la parte C para un sistema.
# Uso: analizar_sistema.sh <2A|2B> <raiz del proyecto>
# Cadena 1 = antigeno (RNasa, cadena A); cadena 2 = nanobody (cadena B).
set -euo pipefail

SIS=$1
RAIZ=$2
SIM=$RAIZ/B_dinamica/$SIS
DATOS=$RAIZ/C_analisis/datos/$SIS
mkdir -p "$DATOS"
cd "$SIM"

echo "=== Verificaciones de $SIS ==="
RESUMEN=$DATOS/resumen_verificaciones.txt
: > "$RESUMEN"
energia() {  # energia <archivo.edr> <termino> <salida.xvg> [-b inicio]
    printf '%s\n0\n' "$2" | gmx energy -f "$1" -o "$DATOS/$3" ${4:-} 2>&1 \
        | grep -E "^$2" | sed "s/^/$3: /" | tee -a "$RESUMEN"
}
energia em.edr  Potential   B5_potencial.xvg
energia nvt.edr Temperature B6_temperatura.xvg "-b 20"
energia npt.edr Pressure    B7_presion.xvg "-b 100"
energia npt.edr Density     B7_densidad.xvg "-b 100"
energia npt.edr Volume      B7_volumen.xvg "-b 100"
energia md.edr  Temperature B8_temperatura.xvg
energia md.edr  Pressure    B8_presion.xvg
energia md.edr  Density     B8_densidad.xvg
grep -E "^(SOL|NA|CL) " topol.top | tee -a "$RESUMEN"
grep "Performance:" md.log | tee -a "$RESUMEN"

echo "=== C1 correccion de PBC ==="
printf 'q\n' | gmx make_ndx -f md.tpr -o sistema.ndx > /dev/null 2>&1
printf 'Protein\n' | gmx convert-tpr -s md.tpr -n sistema.ndx -o proteina.tpr
printf 'Protein\nProtein\n' | gmx trjconv -s md.tpr -n sistema.ndx -f md.xtc -o proteina.xtc -pbc nojump -center
printf 'splitch 1\n"Protein_chain1" & "C-alpha"\n"Protein_chain2" & "C-alpha"\nq\n' \
    | gmx make_ndx -f proteina.tpr -o proteina.ndx > /dev/null 2>&1
ANT=Protein_chain1
NB=Protein_chain2
CA_ANT='Protein_chain1_&_C-alpha'
CA_NB='Protein_chain2_&_C-alpha'

echo "=== C2 RMSD (referencia: inicio de la produccion) ==="
rmsd() {  # rmsd <grupo de ajuste> <grupo medido> <salida.xvg>
    printf '%s\n%s\n' "$1" "$2" | gmx rms -s proteina.tpr -f proteina.xtc -n proteina.ndx -tu ps -o "$DATOS/$3"
}
rmsd C-alpha   C-alpha   C2_rmsd_complejo.xvg
rmsd "$CA_NB"  "$CA_NB"  C2_rmsd_nanobody.xvg
rmsd "$CA_ANT" "$CA_ANT" C2_rmsd_antigeno.xvg
# Ajusta sobre el antigeno y mide el nanobody: cuanto se mueve uno respecto al otro
rmsd "$CA_ANT" "$CA_NB"  C2_rmsd_nanobody_sobre_antigeno.xvg

echo "=== C3 contactos de la interfaz ==="
printf '%s\n%s\n' "$NB" "$ANT" | gmx mindist -s proteina.tpr -f proteina.xtc -n proteina.ndx -d 0.4 \
    -od "$DATOS/C3_distancia_minima.xvg" -on "$DATOS/C3_contactos_4A.xvg"
gmx hbond -s proteina.tpr -f proteina.xtc -n proteina.ndx \
    -r "group \"$NB\"" -t "group \"$ANT\"" -num "$DATOS/C3_puentes_H.xvg"

echo "=== C4 pares de A5 a lo largo del tiempo ==="
par() {  # par <residuo nb> <atomo nb> <residuo RNasa> <atomo RNasa> <salida.xvg>
    gmx distance -s proteina.tpr -f proteina.xtc -n proteina.ndx -oall "$DATOS/$5" \
        -select "group \"$NB\" and resid $1 and name $2 plus group \"$ANT\" and resid $3 and name $4"
}
par 27 OH 60 O   C4_Tyr27_Gln60.xvg
par 106 O 112 N  C4_res106_Gly112.xvg
par 107 O 115 OH C4_res107_Tyr115.xvg
if [ "$SIS" = 2A ]; then
    par 106 CZ 111 CD C4_salino_Arg_Glu111.xvg
else
    par 107 CZ 111 CD C4_salino_Arg_Glu111.xvg
    par 101 CG 70 N   C4_Asp101_Thr70.xvg
    par 106 OG1 112 N C4_Thr106_Gly112.xvg
fi
rm -f "$DATOS"/\#* ./\#*
echo "=== $SIS analizado: resultados en $DATOS ==="
