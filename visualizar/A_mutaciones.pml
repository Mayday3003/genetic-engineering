# Parte A: superposición de 2A y 2B y localización de las 9 mutaciones.
# Uso (desde la raíz del proyecto):  pymol visualizar/A_mutaciones.pml
# Colores: antígeno (RNasa) verde pálido, nanobody 2A gris, nanobody 2B cian, mutaciones: 2A naranja, 2B rojo.
reinitialize
load 01_estructuras/System_2A.pdb, wt
load 01_estructuras/System_2B.pdb, mut
# Superponer sobre el antígeno (cadena A) sin descartar outliers (igual que en el informe: 0.64 Å)
align mut and chain A and name CA, wt and chain A and name CA, cycles=0
bg_color white
hide everything
show cartoon
color palegreen, chain A
color gray70, wt and chain B
color cyan, mut and chain B
set cartoon_transparency, 0.35, chain A
# Las 9 mutaciones
select mutaciones_2A, wt and chain B and resi 28+29+101+102+104+105+106+107+110
select mutaciones_2B, mut and chain B and resi 28+29+101+102+104+105+106+107+110
show sticks, mutaciones_2A or mutaciones_2B
color orange, mutaciones_2A and elem C
color red, mutaciones_2B and elem C
label mutaciones_2B and name CA, resn+resi   # solo se etiqueta 2B
set label_size, 16
set label_position, (0,0,6)
set label_color, black
# CDR1 (26-33) y CDR3 (99-112) del nanobody 2B
select CDR1, mut and chain B and resi 26-33
select CDR3, mut and chain B and resi 99-112
disable CDR1
disable CDR3
orient
zoom mutaciones_2B, 12
