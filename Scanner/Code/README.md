# Uso de archivo `.txt` para cargar código

Este documento explica cómo crear un archivo `.txt` para luego llamarlo desde tu proyecto.

---

## Variables definidas en `main.py`

En el archivo `main.py` se definen las siguientes variables para cargar el archivo:

```python
nombre = "code.txt"
ruta_archivo = ruta_archivo / "Code" / nombre
```

## Ejemplo

Archivo de texto: `code.txt`

```plaintext
if(a == b){
   
    video stream = vid("ll1_table.mp4");
    video adio = vid("pedro.mp4");
    image correcto = img("correcto.mp4");
    image reinicio = img("reinicio.mp4");
}
```