# D–F. Energía libre (gmx_MMPBSA): segunda entrega

**Estado: sin empezar.** gmx_MMPBSA todavía no está instalado.

- D. ΔΔGcalc = ΔG(2B) − ΔG(2A), comparado con ΔΔGexp = −2.98 kcal/mol
- E. Componentes energéticos (VDW, EEL, EGB/EPB, ESURF)
- F. Descomposición por residuo: ΔΔGi = ΔGi(2B) − ΔGi(2A)

Hipótesis heredadas de la parte A:
- El puente salino con Glu111 pasa de Arg106 a Arg107: ¿cambia su contribución?
- Asp101 y Thr106 forman puentes de H nuevos en 2B.
- Trp29, Thr30 y Arg110 tocan la RNasa sin formar puentes de H: ¿aportan por vdW o electrostática?
- La interfaz pasa de 10 a 12 contactos polares: ¿se traduce en una energía más favorable o la compensa la desolvatación?
- 2B tiene más carga positiva (+6 esperada frente a +4 en 2A): revisar EEL junto con la solvatación polar, nunca por separado.
- La MD debilita parte de lo visto en el cristal (puente salino, Tyr115): ¿la energía de 2B sigue siendo más favorable pese a esas pérdidas?
- Usar la trayectoria de `B_dinamica/*_colab/`, con la misma ventana y número de snapshots en los dos sistemas.
