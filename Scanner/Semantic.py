from lema import *
from pathlib import Path
from typing import List, Set
from anytree import Node

def translate_to_python(root: Node, output_path: str = "edicion_video.txt", init: int =1):
    lines: List[str] = []
    indent_level = 0
    loaded_resources: Set[str] = set()
    if(init):
        traducction(root)
        return 
    def emit(line: str, indent_delta: int = 0):
        nonlocal indent_level
        lines.append("    " * indent_level + line)
        indent_level += indent_delta

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
        if node.name in {"==","!=","<","<=",">",">=","+","-","*","/","%","="} and len(node.children) == 2:
            l = expr(node.children[0])
            r = expr(node.children[1])
            return f"({l} {node.name} {r})"
        if node.name == "vid" and node.children:
            path = node.children[0].name.strip('"')
            varname = Path(path).stem.replace('.', '_')
            if varname not in loaded_resources:
                emit(f"{varname} = VideoFileClip(r'{path}')")
                loaded_resources.add(varname)
            return varname
        if node.name == "img" and node.children:
            path = node.children[0].name.strip('"')
            varname = Path(path).stem.replace('.', '_')
            if varname not in loaded_resources:
                emit(f"{varname} = ImageClip(r'{path}')")
                loaded_resources.add(varname)
            return varname
        return " ".join(expr(c) for c in node.children)

    def walk(node: Node):
        lbl = node.name

        if lbl == "group":
            ch = node.children
            if len(ch) == 3 and ch[1].name == "=":
                target = ch[0].name
                emit(f"{target} = {expr(ch[2])}")
                return
            for c in ch:
                walk(c)
            return

        if lbl == "if" and len(node.children) >= 2:
            cond, body = node.children[0], node.children[1]
            emit(f"if {expr(cond)}:", indent_delta=1)
            walk(body)
            emit("", indent_delta=-1)
            if len(node.children) == 3:
                emit("else:", indent_delta=1)
                walk(node.children[2])
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
            emit(f"{node.children[0].name} = {expr(node.children[1])}")
            return
        if lbl == "+" and len(node.children) == 2:
            c, v = node.children[0].name, node.children[1].name
            emit(f"{c} = {c}.fl_image(lambda img: vfx.colorx(img, 1 + {v}))")
            return
        if lbl == "-" and len(node.children) == 2:
            c, v = node.children[0].name, node.children[1].name
            emit(f"{c} = {c}.fl_image(lambda img: vfx.colorx(img, 1 - {v}))")
            return
        if lbl == "*" and len(node.children) == 2:
            c, v = node.children[0].name, node.children[1].name
            emit(f"{c} = {c}.fx(vfx.speedx, {v})")
            return
        if lbl == "/" and len(node.children) == 2:
            c, v = node.children[0].name, node.children[1].name
            emit(f"{c} = {c}.fx(vfx.speedx, 1/{v})")
            return
        if lbl == "%" and len(node.children) == 1:
            c = node.children[0].name
            emit(f"{c} = {c}.subclip(0, max(0, {c}.duration - 60))")
            return

        if lbl == "print" and node.children:
            emit(f"print({expr(node.children[0])})")
            return
        if lbl == "save" and len(node.children) == 2:
            c = node.children[0].name
            fn = node.children[1].name.strip('"')
            emit(f"{c}.write_videofile(r'{fn}')")
            return
        if lbl == "concat" and len(node.children) == 2:
            a, b = node.children[0].name, node.children[1].name
            emit(f"{a} = concatenate_videoclips([{a}, {b}])")
            return

        for c in node.children:
            walk(c)

    # 1) Header
    emit("from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, vfx")
    emit("")

    # 2) Walk AST
    walk(root)
    emit("")
    emit("# Fin del script")

    # 3) Write to file
    script = "\n".join(lines)
    print(script)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"✅ Script generado en {output_path}")
