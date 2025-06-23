from anytree import Node
from typing import List
from pathlib import Path


def translate_to_python(root: Node, output_path: str = "edicion_video.py"):
    """
    Recorre el AST reducido y escribe un script Python para edición de video.
    """
    lines: List[str] = []
    indent_level = 0

    def emit(line: str, indent_delta: int = 0):
        nonlocal indent_level
        lines.append("    " * indent_level + line)
        indent_level += indent_delta

    # 1) Cabecera: imports
    emit("from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, vfx")
    emit("")

    # 2) Pre-carga de fuentes (vid y img)
    def collect_sources(node: Node, vids: set, imgs: set):
        if node.name == "vid" and node.children:
            vids.add(node.children[0].name.strip('"'))
        if node.name == "img" and node.children:
            imgs.add(node.children[0].name.strip('"'))
        for c in node.children:
            collect_sources(c, vids, imgs)

    vids, imgs = set(), set()
    collect_sources(root, vids, imgs)
    for path in vids:
        name = Path(path).stem
        emit(f"{name} = VideoFileClip(r'{path}')")
    for path in imgs:
        name = Path(path).stem
        emit(f"{name} = ImageClip(r'{path}')")
    emit("")

    # 3) Helper para expresiones infijas y llamadas vid/img
    def expr(node: Node) -> str:
        if node.name == "group" and len(node.children) == 2:
            left, opnode = node.children
            if opnode.name in {"==","!=","<","<=",">",">=","+","-","*","/","%","="} and len(opnode.children) == 1:
                right = opnode.children[0]
                return f"({expr(left)} {opnode.name} {expr(right)})"
        if node.name == "group":
            return " ".join(expr(c) for c in node.children)
        if not node.children:
            return node.name
        if node.name in {"==","!=","<","<=",">",">=","+","-","*","/","%","="} and len(node.children) >= 2:
            left = expr(node.children[0])
            right = expr(node.children[1])
            return f"({left} {node.name} {right})"
        if node.name == "vid" and node.children:
            p = node.children[0].name.strip('"')
            return f"VideoFileClip(r'{p}')"
        if node.name == "img" and node.children:
            p = node.children[0].name.strip('"')
            return f"ImageClip(r'{p}')"
        return " ".join(expr(c) for c in node.children)

    # 4) Recorrido principal para traducir cada nodo
    def walk(node: Node):
        lbl = node.name
        if lbl in {"group", ""}:
            for ch in node.children:
                walk(ch)
            return

        if lbl == "if" and len(node.children) >= 2:
            cond, body = node.children[0], node.children[1]
            emit(f"if {expr(cond)}:", indent_delta=1)
            if body.name == "group":
                for stmt in body.children:
                    walk(stmt)
            else:
                walk(body)
            emit("", indent_delta=-1)
            if len(node.children) == 3:
                emit("else:", indent_delta=1)
                else_body = node.children[2]
                if else_body.name == "group":
                    for stmt in else_body.children:
                        walk(stmt)
                else:
                    walk(else_body)
                emit("", indent_delta=-1)
            return

        if lbl == "for" and len(node.children) == 4:
            init, cond, upd, body = node.children
            walk(init)
            emit(f"while {expr(cond)}:", indent_delta=1)
            walk(body)
            walk(upd)
            emit("", indent_delta=-1)
            return

        if lbl == "=" and len(node.children) == 2:
            target = node.children[0].name
            emit(f"{target} = {expr(node.children[1])}")
            return

        if lbl == "+" and len(node.children) == 2:
            clip, amt = node.children[0].name, node.children[1].name
            emit(f"{clip} = {clip}.fl_image(lambda img: vfx.colorx(img, 1 + {amt}))")
            return

        if lbl == "-" and len(node.children) == 2:
            clip, amt = node.children[0].name, node.children[1].name
            emit(f"{clip} = {clip}.fl_image(lambda img: vfx.colorx(img, 1 - {amt}))")
            return

        if lbl == "*" and len(node.children) == 2:
            clip, factor = node.children[0].name, node.children[1].name
            emit(f"{clip} = {clip}.fx(vfx.speedx, {factor})")
            return

        if lbl == "/" and len(node.children) == 2:
            clip, factor = node.children[0].name, node.children[1].name
            emit(f"{clip} = {clip}.fx(vfx.speedx, 1/{factor})")
            return

        if lbl == "%" and len(node.children) == 1:
            clip = node.children[0].name
            emit(f"{clip} = {clip}.subclip(0, max(0, {clip}.duration - 60))")
            return

        if lbl == "print" and node.children:
            emit(f"print({expr(node.children[0])})")
            return

        if lbl == "save" and len(node.children) == 2:
            clip, fn = node.children[0].name, node.children[1].name.strip('"')
            emit(f"{clip}.write_videofile(r'{fn}')")
            return

        if lbl == "concat" and len(node.children) == 2:
            a, b = node.children[0].name, node.children[1].name
            emit(f"{a} = concatenate_videoclips([{a}, {b}])")
            return

        for ch in node.children:
            walk(ch)

    # 5) Iniciar recorrido desde raíz
    walk(root)

    emit("")
    emit("# Fin del script")

    print("\n".join(lines))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Script generado en {output_path}")
