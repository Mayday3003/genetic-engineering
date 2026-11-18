#!/bin/bash
# Crea .venv con lo necesario para los scripts de Python (una sola vez).
# Uso (desde la raíz del proyecto):  bash scripts/preparar_entorno.sh
set -e
python3 -m venv .venv
.venv/bin/pip install -q pandas numpy matplotlib
echo "Listo. Usa: .venv/bin/python scripts/analisis_energia.py"
