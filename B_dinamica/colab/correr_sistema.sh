#!/bin/bash
# Corre B1-B8 para un sistema. Si se interrumpe, al volver a ejecutarlo salta
# las etapas terminadas y retoma la produccion desde el checkpoint.
# Uso: correr_sistema.sh <2A|2B> <raiz del proyecto>
# Variables opcionales: GPU_FLAGS, TRABAJO, HASTA=iones (detenerse tras B4, para pruebas)
set -euo pipefail

SIS=$1
RAIZ=$2
PDB=$RAIZ/01_estructuras/System_$SIS.pdb
MDP=$RAIZ/B_dinamica/mdp
GUARDADO=$RAIZ/B_dinamica/$SIS
TRABAJO=${TRABAJO:-/content/run/$SIS}
GPU_FLAGS=${GPU_FLAGS:--nb gpu -pme gpu -bonded gpu}

mkdir -p "$GUARDADO" "$TRABAJO"
cd "$TRABAJO"
# Trae lo que ya exista en Drive (Colab borra /content al desconectarse)
find "$GUARDADO" -maxdepth 1 -type f -exec cp -n {} . \;

guardar() {  # copia a Drive todo menos los .trr (pesados) y los respaldos #...#
    find . -maxdepth 1 -type f ! -name '#*' ! -name '*.trr' -exec cp -u {} "$GUARDADO"/ \;
}

if [ ! -f complex_solv_ions.gro ]; then
    echo "=== B1 topologia ==="
    gmx pdb2gmx -f "$PDB" -o complex.gro -p topol.top -ff amber99sb-ildn -water tip3p -ignh
    echo "=== B2 caja ==="
    gmx editconf -f complex.gro -o complex_newbox.gro -c -d 1.0 -bt cubic
    echo "=== B3 solvatacion ==="
    gmx solvate -cp complex_newbox.gro -cs spc216.gro -o complex_solv.gro -p topol.top
    echo "=== B4 iones ==="
    gmx grompp -f "$MDP/ions.mdp" -c complex_solv.gro -p topol.top -o ions.tpr
    echo SOL | gmx genion -s ions.tpr -o complex_solv_ions.gro -p topol.top -pname NA -nname CL -neutral
    guardar
fi
[ "${HASTA:-}" = iones ] && exit 0

if [ ! -f em.gro ]; then
    echo "=== B5 minimizacion ==="
    gmx grompp -f "$MDP/minim.mdp" -c complex_solv_ions.gro -p topol.top -o em.tpr
    gmx mdrun -deffnm em -nb gpu
    guardar
fi

if [ ! -f nvt.gro ]; then
    echo "=== B6 NVT ==="
    gmx grompp -f "$MDP/nvt.mdp" -c em.gro -r em.gro -p topol.top -o nvt.tpr
    gmx mdrun -deffnm nvt $GPU_FLAGS
    guardar
fi

if [ ! -f npt.gro ]; then
    echo "=== B7 NPT ==="
    gmx grompp -f "$MDP/npt.mdp" -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
    gmx mdrun -deffnm npt $GPU_FLAGS
    guardar
fi

if [ ! -f md.gro ]; then
    echo "=== B8 produccion ==="
    [ -f md.tpr ] || gmx grompp -f "$MDP/md.mdp" -c npt.gro -t npt.cpt -p topol.top -o md.tpr
    # Copia a Drive cada 2 min mientras corre, para poder retomar
    ( while sleep 120; do guardar; done ) &
    COPIA=$!
    gmx mdrun -deffnm md $GPU_FLAGS -cpi md.cpt -cpt 2
    kill $COPIA
    guardar
fi
echo "=== $SIS terminado ==="
gmx check -f md.xtc 2>&1 | grep -E "Last frame|Coords"
