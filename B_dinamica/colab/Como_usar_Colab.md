# Cómo correr las simulaciones en Colab

Las carpetas de Drive las crea el notebook. Solo hay que subir dos archivos.

1. Entra a [colab.research.google.com](https://colab.research.google.com) > *Subir* y elige `Colab_MD_2A_2B.ipynb`.
2. En *Entorno de ejecución > Cambiar tipo de entorno*, elige **A100**.
3. Ejecuta las celdas en orden. La celda 2 reinicia el entorno: es normal.
4. En la celda 4 autoriza Drive y sube `proyecto_2_colab.zip` cuando lo pida.
5. Las celdas 5 y 6 corren 2A y 2B. Las celdas 7 y 8 hacen el análisis y las gráficas.
6. Descarga de `MyDrive/proyecto_2/` lo indicado en la celda 9. Guarda las simulaciones en `B_dinamica/2A_colab/` y `2B_colab/`, y `C_analisis/` en su carpeta local.

**Si se desconecta:** ejecuta otra vez desde la celda 1, saltando la subida del zip (el notebook la omite solo). Las etapas terminadas no se repiten.

**Si una celda muestra `Fatal error`:** no sigas; copia el mensaje para revisarlo.

## Archivos
- `correr_sistema.sh`: etapas B1–B8 de un sistema.
- `analizar_sistema.sh`: verificaciones y cálculos de la parte C.
- `proyecto_2_colab.zip`: PDB, `.mdp` y estos scripts.
