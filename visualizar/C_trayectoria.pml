# Parte B/C: película de 1 ns de 2A y 2B (proteína, PBC corregida).
# Requiere antes:  bash visualizar/preparar_trayectoria.sh
# Uso:  pymol visualizar/C_trayectoria.pml      (botones de play abajo a la derecha)
reinitialize
load visualizar/tmp/2A_inicio.pdb, sim2A
load_traj B_dinamica/2A_colab/proteina.xtc, sim2A
load visualizar/tmp/2B_inicio.pdb, sim2B
load_traj B_dinamica/2B_colab/proteina.xtc, sim2B
bg_color white
hide everything
show cartoon
# chain A = RNasa, chain B = nanobody (si la PDB no trae cadenas, se colorea por segmento)
color palegreen, chain A
color gray70, sim2A and chain B
color cyan, sim2B and chain B
# Sin esto, 2A y 2B quedarían encimados: se separan
translate [60,0,0], sim2B, state=0, camera=0
select interfaz_mut, (sim2A or sim2B) and chain B and resi 29+101+106+107+110
show sticks, interfaz_mut
color red, interfaz_mut and elem C
orient
set movie_fps, 15
# mplay   (quita el # para que empiece sola)
