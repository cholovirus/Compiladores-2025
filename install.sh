#!/bin/bash

# Instalar paquetes Python
echo "[INFO] Instalando dependencias de requirements.txt..."
pip install -r requirements.txt

# Verificar si graphviz está instalado (comando 'dot')
if ! command -v dot &> /dev/null
then
    echo "[INFO] Graphviz no está instalado. Instalando con apt..."
    sudo apt update && sudo apt install -y graphviz
else
    echo "[OK] Graphviz ya está instalado."
fi