#!/bin/bash
# Genera las figuras 2A vs 2B en C_analisis/figuras con titulos y ejes en espanol.
# Uso (desde la raiz del proyecto): bash scripts/figuras_2A_vs_2B.sh

T="Tiempo (ps)"

# figura <dato> <titulo> <eje y> [opciones extra]
figura() {
    dato=$1; titulo=$2; eje_y=$3; shift 3
    python3 scripts/graficar_xvg.py C_analisis/datos/2A/$dato.xvg C_analisis/datos/2B/$dato.xvg \
        --etiquetas 2A 2B --leyenda-abajo --titulo "$titulo" --xlabel "$T" --ylabel "$eje_y" \
        -o C_analisis/figuras/${dato}_2A_vs_2B.png "$@"
}

figura B5_potencial "Energía potencial durante la minimización" "Energía potencial (kJ/mol)" \
    --desde 5 --sin-promedio --xlabel "Paso de minimización"
figura B8_temperatura "Temperatura durante la producción" "Temperatura (K)"
figura B8_densidad "Densidad durante la producción" "Densidad (kg/m³)"
figura C2_rmsd_complejo "RMSD de Cα del complejo" "RMSD (nm)"
figura C2_rmsd_nanobody "RMSD de Cα del nanobody (ajustado sobre sí mismo)" "RMSD (nm)"
figura C2_rmsd_antigeno "RMSD de Cα del antígeno (ajustado sobre sí mismo)" "RMSD (nm)"
figura C2_rmsd_nanobody_sobre_antigeno "RMSD de Cα del nanobody ajustando sobre el antígeno" "RMSD (nm)"
figura C3_contactos_4A "Contactos nanobody–RNasa a menos de 4 Å" "Pares de átomos en contacto"
figura C3_puentes_H "Puentes de hidrógeno nanobody–RNasa" "Número de puentes de H"
figura C3_distancia_minima "Distancia mínima nanobody–RNasa" "Distancia (nm)"
figura C4_salino_Arg_Glu111 "Distancia Arg (CZ) – Glu111 (CD)" "Distancia (nm)"
figura C4_Tyr27_Gln60 "Distancia Tyr27 (OH) – Gln60 (O)" "Distancia (nm)"
