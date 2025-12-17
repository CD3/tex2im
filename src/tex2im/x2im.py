import base64
import importlib
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import typer
from typing_extensions import Annotated, List

app = typer.Typer()
__version__ = importlib.metadata.version("tex2im")


# a text-list class for accumulating lines of text
# without having to do .append(...)
class tlist(list):
    def __iadd__(self, item):
        if isinstance(item, list):
            for i in item:
                self.append(i)
        else:
            self.append(item)
        return self


@app.command()
def typst(
    snippet_or_file: Annotated[
        str,
        typer.Argument(help="snippet or filename conotainting code to compile."),
    ] = [],
    version: Annotated[bool, typer.Option(help="Show version number.")] = False,
    verbose: Annotated[
        bool, typer.Option("-v", "--verbose", help="Log information.")
    ] = False,
    debug: Annotated[
        bool, typer.Option("-d", "--debug", help="Log debug information.")
    ] = False,
    format: Annotated[
        str, typer.Option("-f", "--output-format", help="Output image format.")
    ] = "png",
    output_basename: Annotated[
        str,
        typer.Option(
            "-o",
            "--output-basename",
            help="Output file basename. Image format extension will be appended.",
        ),
    ] = None,
    border: Annotated[
        int, typer.Option("-B", "--border", help="Size of border, in pixels.")
    ] = 0,
    density: Annotated[
        str,
        typer.Option(
            "-D", "--density", help="Output image density, in pixels per inch."
        ),
    ] = "150x150",
):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    if verbose:
        print("typst2im")

    tmpdir = Path(tempfile.mkdtemp(prefix="x2im-"))
    curdir = Path(os.getcwd())

    input_file = Path(snippet_or_file)
    if input_file.exists():
        snippet = input_file.read_text()
        output_file = input_file.absolute().with_suffix("." + format)
    else:
        snippet = snippet_or_file
        output_file = curdir / f"out.{format}"
    if output_basename:
        output_file = (curdir / output_basename).with_suffix("." + format)
    input_file = tmpdir / "in.typ"
    aux_file = tmpdir / "aux.pdf"

    os.chdir(tmpdir)

    lines = tlist()
    lines += snippet

    input_file.write_text("\n".join(lines))

    typst_cmd = ["typst", "compile", input_file, aux_file]

    ret = subprocess.run(typst_cmd)
    if ret.returncode != 0:
        raise typer.Exit(ret.returncode)

    convert_cmd = ["convert", "-trim"]
    convert_cmd += ["-border", str(border)]
    convert_cmd += ["-density", density]
    convert_cmd += [aux_file]

    if format == "html":
        convert_cmd.append("x2im-tmp.png")
    else:
        convert_cmd.append(output_file)

    ret = subprocess.run(convert_cmd)
    if ret.returncode != 0:
        raise typer.Exit(ret.returncode)

    if format == "html":
        img = Path("x2im-tmp.png").read_bytes()
        code = base64.b64encode(img).decode("utf-8")
        text = rf"""<img src="data:image/{format};base64,{code}">"""
        output_file.write_text(text)


@app.command()
def latex():
    pass
    print("Use tex2im command")
