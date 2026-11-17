#!/bin/bash
# Una réplica de MD (NVT -> NPT -> producción de 1 ns) a partir del sistema YA minimizado.
# Solo cambia la semilla de las velocidades iniciales (gen_seed del NVT); el resto del protocolo
# (.mdp, topología, caja, iones, minimización) es idéntico al de B_dinamica/.
# Uso: replica.sh <2A|2B> <n_replica> <semilla> <carpeta_entradas> <carpeta_salida>
#   entradas/<sis>/{em.gro,topol.top,*.itp}  entradas/mdp/{nvt,npt,md}.mdp
set -euo pipefail
SIS=$1; REP=$2; SEED=$3; IN=$4; OUT=$5
D=$OUT/${SIS}_r${REP}
[ -f "$D/proteina.xtc" ] && { echo "=== ${SIS}_r${REP} ya terminada ==="; exit 0; }
mkdir -p "$D"; cd "$D"
cp "$IN/$SIS"/{em.gro,topol.top} .
cp "$IN/$SIS"/*.itp .
sed "s/^gen_seed.*/gen_seed                = $SEED/" "$IN/mdp/nvt.mdp" > nvt.mdp
cp "$IN/mdp/npt.mdp" "$IN/mdp/md.mdp" .
GPU="-nb gpu -pme gpu -bonded gpu"

echo "=== ${SIS}_r${REP}: NVT (semilla $SEED) ==="
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr -maxwarn 0
gmx mdrun -deffnm nvt $GPU
echo "=== ${SIS}_r${REP}: NPT ==="
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -deffnm npt $GPU
echo "=== ${SIS}_r${REP}: produccion 1 ns ==="
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
gmx mdrun -deffnm md $GPU

echo "=== ${SIS}_r${REP}: correccion de PBC (igual que C1) ==="
echo q | gmx make_ndx -f md.tpr -o sistema.ndx > /dev/null
echo Protein | gmx convert-tpr -s md.tpr -n sistema.ndx -o proteina.tpr
printf 'Protein\nProtein\n' | gmx trjconv -s md.tpr -n sistema.ndx -f md.xtc -o proteina.xtc -pbc nojump -center
printf 'splitch 1\nq\n' | gmx make_ndx -f proteina.tpr -o proteina.ndx > /dev/null

# Verificaciones minimas de B (temperatura, densidad, presión de la producción)
for t in Temperature Density Pressure; do
  printf '%s\n0\n' "$t" | gmx energy -f md.edr -o "B8_${t,,}.xvg" 2>&1 | { grep "^$t" || true; } | sed "s/^/${SIS}_r${REP} /"
done
rm -f \#* *.trr md.cpt md_prev.cpt
echo "=== ${SIS}_r${REP} terminada ==="
