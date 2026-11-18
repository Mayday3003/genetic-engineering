# Parte A en VMD: 2A (gris) y 2B (cian) superpuestos sobre el antígeno, mutaciones en rojo/naranja.
# Uso (desde la raíz):  vmd -e visualizar/A_mutaciones.tcl
# Ir a la raíz del proyecto sin importar desde dónde se lance VMD
cd [file join [file dirname [file normalize [info script]]] ..]
mol new 01_estructuras/System_2A.pdb type pdb waitfor all
mol new 01_estructuras/System_2B.pdb type pdb waitfor all
# superponer 2B sobre 2A usando los Cα de la RNasa (cadena A, residuos 2-124: 2A no tiene la Lys1)
set a [atomselect 0 "chain A and resid 2 to 124 and name CA"]
set b [atomselect 1 "chain A and resid 2 to 124 and name CA"]
set M [measure fit $b $a]
[atomselect 1 all] move $M
puts "RMSD antígeno tras superponer: [measure rmsd $b $a] A"
foreach {id colnb colmut} {0 2 3  1 10 1} {
    mol delrep 0 $id
    mol representation NewCartoon
    mol color ColorID 7
    mol selection "chain A"
    mol addrep $id
    mol color ColorID $colnb
    mol selection "chain B"
    mol addrep $id
    mol representation Licorice 0.3
    mol color ColorID $colmut
    mol selection "chain B and resid 28 29 101 102 104 105 106 107 110"
    mol addrep $id
}
display projection Orthographic
display resetview
