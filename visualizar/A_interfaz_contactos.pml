# Parte A: interfaz nanobody–RNasa y contactos polares (puentes de H / salinos).
# Uso (desde la raíz):  bash visualizar/pymol.sh visualizar/A_interfaz_contactos.pml
reinitialize
load 01_estructuras/System_2A.pdb, wt
load 01_estructuras/System_2B.pdb, mut
align mut and chain A and name CA, wt and chain A and name CA, cycles=0
bg_color white
hide everything
show cartoon
color palegreen, chain A
color gray70, wt and chain B
color cyan, mut and chain B
set cartoon_transparency, 0.4
# Interfaz: residuos del nanobody a <= 4 Å de la RNasa (criterio del informe)
select interfaz_2A, byres (wt and chain B) within 4 of (wt and chain A)
select interfaz_2B, byres (mut and chain B) within 4 of (mut and chain A)
show sticks, interfaz_2A or interfaz_2B
color gray40, interfaz_2A and elem C
color teal, interfaz_2B and elem C
# Contactos polares (O/N a <= 3.5 Å) entre nanobody y RNasa
dist contactos_2A, (wt and chain B), (wt and chain A), 3.5, mode=2
dist contactos_2B, (mut and chain B), (mut and chain A), 3.5, mode=2
color yellow, contactos_2A
color red, contactos_2B
hide labels, contactos_2A
hide labels, contactos_2B
# Residuos clave
select clave_antigeno, mut and chain A and resi 60+62+69+70+73+111+112+115
show sticks, clave_antigeno
label clave_antigeno and name CA, resn+resi
set label_size, 14
set label_color, black
disable contactos_2A
disable interfaz_2A
orient
zoom interfaz_2B, 6
