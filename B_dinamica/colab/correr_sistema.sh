#!/bin/bash
# Corre B1-B8 para un sistema.
# Uso: correr_sistema.sh <2A|2B> <raiz del proyecto>

SIS=$1
RAIZ=$2
MDP=$RAIZ/B_dinamica/mdp
GPU="-nb gpu -pme gpu -bonded gpu"

cd "$RAIZ/B_dinamica/$SIS"

# B1 Topologia
gmx pdb2gmx -f "$RAIZ/01_estructuras/System_$SIS.pdb" -o complex.gro -p topol.top -ff amber99sb-ildn -water tip3p -ignh

# B2 Caja
gmx editconf -f complex.gro -o complex_newbox.gro -c -d 1.0 -bt cubic

# B3 Solvatacion
gmx solvate -cp complex_newbox.gro -cs spc216.gro -o complex_solv.gro -p topol.top

# B4 Iones
gmx grompp -f "$MDP/ions.mdp" -c complex_solv.gro -p topol.top -o ions.tpr
echo SOL | gmx genion -s ions.tpr -o complex_solv_ions.gro -p topol.top -pname NA -nname CL -neutral

# B5 Minimizacion
gmx grompp -f "$MDP/minim.mdp" -c complex_solv_ions.gro -p topol.top -o em.tpr
gmx mdrun -deffnm em -nb gpu

# B6 Equilibracion NVT
gmx grompp -f "$MDP/nvt.mdp" -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt $GPU

# B7 Equilibracion NPT
gmx grompp -f "$MDP/npt.mdp" -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -deffnm npt $GPU

# B8 Produccion
gmx grompp -f "$MDP/md.mdp" -c npt.gro -t npt.cpt -p topol.top -o md.tpr
gmx mdrun -deffnm md $GPU
