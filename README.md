# 🧠 Proyecto Compilador - LL(1) en Python

Este proyecto es una implementación educativa de un **compilador simple en Python** que incluye las siguientes fases:

- **Scanner (Análisis léxico)**
- **Parser (Análisis sintáctico)**
- **Tablas LL(1) para parsing predictivo**
- **Manejo de errores sintácticos**
- **Traducción de un pseudo-código tipo Markdown a HTML** *(opcional/futuro)*

---

## 🧩 Estructura del proyecto

    ├── code.txt # Código fuente de ejemplo (pseudo-código)
    ├── main.py # Script principal: ejecuta scanner + parser
    ├── scanner.py # Scanner/analizador léxico
    ├── parser.py # Parser/analizador sintáctico con LL(1)
    ├── ll1_table.tsv # Tabla de parsing LL(1)
    ├── ll1_First_Follow.tsv # Tabla de FIRST/FOLLOW
    ├── test_main.py # Pruebas de integración estilo main.py
    ├── test_scanner.py # Pruebas específicas del scanner
    ├── test_parser.py # Pruebas específicas del parser
    ├── test_integracion.py # Pruebas de integración completa

---

## ⚙️ Requisitos

Este proyecto está hecho **completamente en Python puro**. Solo se usa la biblioteca estándar, por lo que no es necesario instalar nada con `pip`.

- Python 3.7 o superior

---

### 📦 Dependencias de Python

Instálalas con:

```bash
python -m pip install -r requirements.txt
```

### Contenido mínimo de requirements.txt

```bash
anytree>=2.8.0
tabulate
```

## 📌 Requisito adicional para exportar árboles como imagen

El proyecto usa Graphviz para exportar el árbol de análisis sintáctico en formato .png o .pdf.

Descarga Graphviz desde:
<https://graphviz.org/download/>

Durante la instalación, asegúrate de marcar la opción que agrega Graphviz al PATH.

Verifica que esté correctamente instalado con:

```bash
dot -V
```

Deberías ver algo como:

```bash
dot - graphviz version 8.2.1 (2024-01-01)
```

## ▶️ Cómo ejecutar el compilador

1. Asegúrate de tener todos los archivos `.tsv` y `code.txt` en el mismo directorio.
2. Ejecuta el programa principal:

```bash
python main.py
```

### Esto mostrará

- Los tokens generados por el scanner.

- El análisis del parser, incluyendo errores o confirmación de aceptación.

## ✅ Cómo ejecutar las pruebas

El proyecto incluye pruebas para cada componente, organizadas en archivos separados:

### 🔍 1. Ejecutar las pruebas del main.py

```bash
python test_main.py
```

### 🔎 2. Probar solo el scanner

```bash
python test_scanner.py
```

### 🔧 3. Probar el parser y sus funciones

```bash
python test_parser.py
````

### 🔗 4. Pruebas de integración (scanner + parser)

```bash
python test_integracion.py
```

### Cada prueba incluye mensajes visuales como

- ✅ [PASSED] Nombre de la prueba
- ❌ [FAILED] Detalle del error

### 📚 Descripción técnica

- Scanner: Reconoce identificadores, números, strings, operadores, delimitadores, tipos y palabras clave.

- Parser: Implementa un análisis sintáctico descendente LL(1) con tabla predictiva y manejo de errores usando conjuntos FOLLOW.

- Tablas TSV: Usadas para alimentar dinámicamente las reglas del parser (ll1_table.tsv) y los conjuntos FIRST/FOLLOW (ll1_First_Follow.tsv).

### 🚀 Estado del proyecto

- ✅ Scanner y Parser funcionales
- ✅ Tablas configurables por archivo
- ✅ Manejo de errores sintácticos
- ✅ Pruebas completas de unidad e integración
