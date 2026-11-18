# Parte B/C en VMD: película de 1 ns.
# Requiere antes:  bash visualizar/preparar_trayectoria.sh
# Uso (desde la raíz):  vmd -e visualizar/C_trayectoria.tcl
foreach s {2A 2B} {
    mol new visualizar/tmp/${s}_inicio.pdb type pdb waitfor all
    mol addfile B_dinamica/${s}_colab/proteina.xtc type xtc waitfor all
    mol rename top "sim$s"
    mol delrep 0 top
    # RNasa (cadena A) y nanobody (cadena B)
    mol representation NewCartoon
    mol color ColorID 7
    mol selection "chain A"
    mol addrep top
    mol color ColorID [expr {$s eq "2A" ? 2 : 10}]
    mol selection "chain B"
    mol addrep top
    # mutaciones en sticks rojos
    mol representation Licorice 0.3
    mol color ColorID 1
    mol selection "chain B and resid 28 29 101 102 104 105 106 107 110"
    mol addrep top
}
# Mover 2B al lado de 2A para poder compararlos
mol top 1
set sel [atomselect 1 all]
$sel moveby {60 0 0}
display projection Orthographic
display resetview
puts "2A (id 0, gris) y 2B (id 1, cian). Usa el control de animación (Extensions > ...) o la barra del pie de la ventana principal."
