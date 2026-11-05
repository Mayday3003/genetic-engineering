#!/bin/bash
# Persistencia de la interfaz (parte C): distancia minima por residuo del nanobody
# a la RNasa, y distancias minimas entre atomos polares de los pares de A5.
# Uso (desde la raiz del proyecto): bash scripts/persistencia_interfaz.sh <2A|2B>
set -euo pipefail
SIS=$1
SIM=B_dinamica/${SIS}_colab
DATOS=$PWD/C_analisis/datos/$SIS
cd "$SIM"
NB='group "Protein_chain2"'
ANT='group "Protein_chain1"'
pd() {  # pd <salida.xvg> <seleccion nanobody> <seleccion RNasa>
    gmx pairdist -s proteina.tpr -f proteina.xtc -n proteina.ndx -cutoff 1.5 -refgrouping all -selgrouping all \
        -o "$DATOS/$1" -ref "$2" -sel "$3"
}
gmx pairdist -s proteina.tpr -f proteina.xtc -n proteina.ndx -cutoff 1.5 -refgrouping res -selgrouping all \
    -o "$DATOS/C3_distancia_por_residuo.xvg" -ref "$NB and not name \"H.*\"" -sel "$ANT and not name \"H.*\""
if [ "$SIS" = 2A ]; then ARG=106; else ARG=107; fi
pd C4_min_salino.xvg "$NB and resid $ARG and name NE NH1 NH2" "$ANT and resid 111 and name OE1 OE2"
pd C4_min_res101_Thr70.xvg "$NB and resid 101 and name OD1 OD2 OH" "$ANT and resid 70 and name N"
pd C4_min_res106_Gly112_lateral.xvg "$NB and resid 106 and name OG1 NE NH1 NH2" "$ANT and resid 112 and name N"
