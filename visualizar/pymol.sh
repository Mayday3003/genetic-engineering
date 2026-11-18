#!/bin/bash
# Abre PyMOL desde la raíz del proyecto, sea el instalado por Flatpak o el del sistema.
# Con Flatpak, PyMOL vive en un "sandbox" y NO ve tus carpetas salvo que se le dé permiso;
# este script se lo da solo para la carpeta del proyecto.
# Uso (desde cualquier carpeta):  bash visualizar/pymol.sh visualizar/A_mutaciones.pml
RAIZ=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$RAIZ"
if ! command -v pymol >/dev/null 2>&1 && flatpak info org.pymol.PyMOL >/dev/null 2>&1; then
    exec flatpak run --filesystem="$RAIZ" org.pymol.PyMOL "$@"
else
    exec pymol "$@"
fi
