#!/bin/bash
# Extrae el primer cuadro de cada simulación (solo proteína), con letras de cadena
# (A = RNasa, B = nanobody), para abrir la trayectoria en PyMOL o VMD.
# Crea visualizar/tmp/{2A,2B}_inicio.pdb (no se sube a git).
# Uso (desde la raíz):  bash visualizar/preparar_trayectoria.sh
set -e
mkdir -p visualizar/tmp
for s in 2A 2B; do
  D=B_dinamica/${s}_colab
  echo 0 | gmx trjconv -s $D/proteina.tpr -f $D/proteina.xtc -dump 0 -o visualizar/tmp/${s}_raw.pdb > /dev/null 2>&1
  # átomos de la cadena 1 (RNasa) según el índice
  N=$(awk '/^\[/{g=($2=="Protein_chain1")} g&&!/^\[/{n+=NF} END{print n}' $D/proteina.ndx)
  awk -v n=$N '/^(ATOM|HETATM)/{i++; $0=substr($0,1,21) (i<=n?"A":"B") substr($0,23)} {print}' \
      visualizar/tmp/${s}_raw.pdb > visualizar/tmp/${s}_inicio.pdb
  rm visualizar/tmp/${s}_raw.pdb
  echo "visualizar/tmp/${s}_inicio.pdb listo (cadena A: $N átomos)"
done
