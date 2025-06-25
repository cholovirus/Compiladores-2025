import google.generativeai as genai
from anytree import RenderTree
from anytree import Node
def tree_to_string(root):
    return "\n".join(f"{pre}{node.name}" for pre, _, node in RenderTree(root))


genai.configure(api_key="API_key")
gemini = genai.GenerativeModel("gemini-2.0-flash")
def traducction(root: Node,output_path: str = "edicion_video.txt"):
    arbol = tree_to_string(root)

    PROMPT_AST_TRANSLATOR = """
        Eres un generador de código Python especializado en la biblioteca `moviepy.editor`, diseñado para traducir árboles de sintaxis abstracta (AST) de edición de video.

        Tu única tarea es **transformar el AST proporcionado en un script Python válido y ejecutable**. No debes incluir explicaciones, comentarios, ni texto adicional; solo el código Python.
        
        ---
        ### 📌 Reglas de Traducción del AST

        Aplica estas reglas estrictas para la traducción de nodos:

        * **`video + number`**:  Traduce a: `vfx.colorx(video, 1 + number / 10)`
        * **`video - number`**:  Traduce a: `vfx.colorx(video, 1 - number / 10)`
        * **`video * number`**:  Traduce a: `video.fx(vfx.speedx, factor=number)`
        * **`video / number`**:  Traduce a: `video.fx(vfx.speedx, factor=1/number)`
        * **`vid("ruta")`**:  Traduce a: `VideoFileClip("ruta")`
        * **`img("ruta")`**:  Traduce a: `ImageClip("ruta").set_duration(1)` (Asegúrate de que `segundos` esté definido en el AST o se derive lógicamente).
        * **`save("ruta")`**:  Traduce a: `video.write_videofile("ruta")`
        * **`concat(v1, v2)`**:  Traduce a: `var = concatenate_videoclips([v1, v2])` (Acepta cualquier número de argumentos).

        ---
        ### ⚙️ Instrucciones de Generación de Código

        1.  **Importaciones Obligatorias**: El script Python generado debe comenzar siempre con la siguiente línea:
            ```python
            from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, vfx
            ```
        2.  **Recorrido y Estructura**: Recorre el AST recursivamente. Genera el código Python línea por línea, asegurando la **indentación correcta** para bloques anidados (como `if`, `for`, definiciones de funciones, etc.).
        3.  **Manejo de Variables**: Las asignaciones y el uso de variables deben seguir la sintaxis estándar de Python.
        4.  **Flujo de Control**: Las estructuras `if` y `for` deben traducirse directamente a sus equivalentes de Python, manteniendo su lógica y sintaxis.
        5.  **Aplicación de Operaciones**: Asegúrate de que cada operación se aplique al clip o variable correcto, según lo dicte la estructura del AST.
        6.  **Salida Exclusiva**: Tu respuesta final debe ser **solo el código Python**, sin preámbulo ni postámbulo.
        7.  **Sin ningún tipo de formato de bloque de código Markdown (es decir, NO uses \`\`\`python ni \`\`\`). La salida debe ser directamente el texto del código.


        ---
        **Cuando estés listo, proporciona el AST que deseas traducir.**
        
    """

    
    PROMPT_AST_TRANSLATOR += arbol

    #print(prompt_entorno)
    entorno = gemini.generate_content(PROMPT_AST_TRANSLATOR).text.strip()

    print(entorno)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(entorno)