import base64
import copy
import importlib.metadata
import inspect
import logging
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import types
from string import Template

import rich
import typer
from typing_extensions import Annotated, List

app = typer.Typer()
__version__ = importlib.metadata.version("tex2im")


@app.command()
def main(
    latex_snippet_or_file: Annotated[
        List[str],
        typer.Argument(
            help="LaTeX snippet or filename conotainting latex code to compile."
        ),
    ] = None,
    version: Annotated[bool, typer.Option(help="Show version number.")] = False,
    verbose: Annotated[
        bool, typer.Option("-v", "--verbose", help="Log information.")
    ] = False,
    debug: Annotated[
        bool, typer.Option("-d", "--debug", help="Log debug information.")
    ] = False,
    keep_files: Annotated[
        bool, typer.Option("-k", "--keep-files", help="Keep generated files.")
    ] = False,
    font_size: Annotated[
        int, typer.Option("-s", "--font-size", help="Document font size.")
    ] = 12,
    text_color: Annotated[
        str,
        typer.Option(
            "-t",
            "--text-color",
            help="Text color. Color support provided by xcolor. Arguments may be a pre-defined xcolor color, such as 'blue', or specify one of the supported xcolor modes as 'mode:arg', such 'HTML:FF7F00'. See xcolor package for supported modes. ",
        ),
    ] = "black",
    background_color: Annotated[
        str,
        typer.Option(
            "-b",
            "--background-color",
            help="Background color. See --text-color for argument types.",
        ),
    ] = "white",
    preamble: Annotated[
        str,
        typer.Option(
            "-x", "--preamble", help="Read additional preamble lines from file."
        ),
    ] = None,
    no_preamble: Annotated[
        bool,
        typer.Option(
            "--no-preamble",
            help="Do not read preamble lines from special files, read lines only from --preamble option if given.",
        ),
    ] = False,
    no_equation_environment: Annotated[
        bool,
        typer.Option(
            "-n",
            "--equation-environment",
            help="Do not wrap snippet in equation environment. Useful if you want to use your own environment.",
        ),
    ] = False,
    no_comment: Annotated[
        bool,
        typer.Option(
            "-C",
            "--no-comment",
            help="Do not embed latex snippet into comment field of output image. Sometimes `convert` does not have 'permission' to uset the comment field.",
        ),
    ] = False,
    anti_aliasing: Annotated[
        int,
        typer.Option(
            "-a",
            "--anti-aliasing",
            help="Turn anti-aliasing on/off. If -1, anti-aliasing will be turned off if for transparent background, and on otherwise.",
        ),
    ] = 1,
    border: Annotated[
        int, typer.Option("-B", "--border", help="Size of border, in pixels.")
    ] = 0,
    density: Annotated[
        str,
        typer.Option(
            "-D", "--density", help="Output image density, in pixels per inch."
        ),
    ] = "150x150",
    transparent_background: Annotated[
        bool,
        typer.Option(
            "-z", "--transparent-background", help="Make background transparent."
        ),
    ] = False,
    output_format: Annotated[
        str,
        typer.Option(
            "-f",
            "--output-format",
            help="Output image file format. This can be any file extension that ImageMagick's convert command knows about.",
        ),
    ] = "png",
    output_basename: Annotated[
        str,
        typer.Option(
            "-o",
            "--output-basename",
            help="Basename to use for output filename. Image format extension will be appended.",
        ),
    ] = None,
    pdflatex_option: Annotated[
        List[str],
        typer.Option(
            "--pdflatex-option",
            help="DEPRECATED! Use --latex-cmd-template instead.",
        ),
    ] = [],
    stdout: Annotated[
        bool,
        typer.Option("--stdout", help="Write the image to stdout instead of a file."),
    ] = False,
    latex_cmd_template: Annotated[
        str,
        typer.Option(
            "--latex-cmd-template",
            help="Template string that will be 'rendered' to produce the latex command used to compile the image. The template string should contain a placeholder named '$INPUT_FILE' which will be used to insert the latex source file into the command.",
        ),
    ] = "pdflatex -interaction=nonstopmode $INPUT_FILE",
) -> int:
    """
    A utility for creating image files from latex snippets.
    """

    if version:
        rich.print(f"version: {__version__}")
        raise typer.Exit(0)

    LATEX_CMD_TEMPLATE = Template(latex_cmd_template)
    latex_cmd = LATEX_CMD_TEMPLATE.safe_substitute(INPUT_FILE="out.tex")

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    configs = []
    current_frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(current_frame)
    for i, f in enumerate(latex_snippet_or_file):
        config = {arg: values[arg] for arg in args}
        config["latex_snippet_or_file"] = f
        config["idx"] = i if len(latex_snippet_or_file) > 1 else None
        config["latex_cmd"] = latex_cmd
        configs.append(types.SimpleNamespace(**config))

    for config in configs:
        make_image(config)

    raise typer.Exit(0)


if __name__ == "__main__":
    typer.run(main)


# a text-list class for accumulating lines of text
class tlist(list):
    def __iadd__(self, item):
        if isinstance(item, list):
            for i in item:
                self.append(i)
        else:
            self.append(item)
        return self


def make_image(config):
    # create a tmp dir to work in
    curdir = os.getcwd()
    tmpdir = tempfile.mkdtemp(prefix="tex2im-")
    logging.info("created {}".format(tmpdir))

    # check if snippet is actually a filename or not
    latex_snippet = config.latex_snippet_or_file
    input_file = None
    if os.path.isfile(latex_snippet):
        input_file = os.path.abspath(latex_snippet)
        logging.info("{} is a file, reading now".format(input_file))
        with open(input_file) as f:
            # read lines, but remove comments
            lines = filter(lambda x: not re.match(r"\s*#", x), f.readlines())
            latex_snippet = "".join(lines).strip()

    logging.info("LaTeX snippet: {}".format(latex_snippet))

    logging.info("creating temp directory")

    os.chdir(tmpdir)

    latex_lines = tlist()

    # preamble
    latex_lines += r"\documentclass[%dpt]{article}" % config.font_size
    latex_lines += r"\usepackage{xcolor}"
    latex_lines += r"\pagestyle{empty}"

    toks = config.text_color.split(":")
    if len(toks) == 1:
        latex_lines += r"\colorlet{text_color}{%s}" % config.text_color
    else:
        latex_lines += r"\definecolor{text_color}{%s}{%s}" % (*toks,)

    toks = config.background_color.split(":")
    if len(toks) == 1:
        latex_lines += r"\colorlet{background_color}{%s}" % config.background_color
    else:
        latex_lines += r"\definecolor{background_color}{%s}{%s}" % (*toks,)

    latex_lines += r"\pagecolor{background_color}"

    # look for a preamble file to load
    preamble_file_candidates = [config.preamble]
    if not config.no_preamble:
        preamble_file_candidates += [
            os.path.join(curdir, ".tex2im_preamble"),
            os.path.join(os.getenv("HOME"), ".tex2im_preamble"),
            os.path.join(os.getenv("HOME"), ".tex2im_header"),
        ]
    for preamble in preamble_file_candidates:
        if preamble is not None and os.path.isfile(preamble):
            with open(preamble, "r") as f:
                latex_lines += f.readlines()
            break

    # document
    latex_lines += r"\begin{document}{"
    latex_lines += r"\color{text_color}"
    if not config.no_equation_environment:
        latex_lines += r"\begin{eqnarray*}"

    # snippet
    latex_lines += latex_snippet

    # end document
    if not config.no_equation_environment:
        latex_lines += r"\end{eqnarray*}"
    latex_lines += r"}\end{document}"

    logging.info("writing LaTeX document to {}/out.tex".format(tmpdir))
    with open("out.tex", "w") as f:
        f.write("\n".join(latex_lines))

    # TODO: detect image files in the latex snippet make them available in the tempdir
    latex_cmd = config.latex_cmd

    logging.info("running LaTeX: {}".format(latex_cmd))
    res = subprocess.run(
        latex_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if res.returncode:
        logging.error("LaTeX command returned non-zero status")
        logging.error("LaTeX command: {}".format(latex_cmd))
        logging.error("LaTeX input (out.tex):")
        logging.error("\n".join(latex_lines))
        logging.error("LaTeX output:")
        logging.error(res.stdout.decode("utf-8"))

    # convert to ouput image format
    convert_cmd = "convert -trim -border {BORDER} -bordercolor {BORDERCOLOR} +adjoin -density {DENSITY}".format(
        BORDER=config.border,
        BORDERCOLOR=config.background_color,
        DENSITY=config.density,
    )
    if config.anti_aliasing == -1 and config.transparent_background:
        convert_cmd += " +antialias"
    elif config.anti_aliasing == -1 and not config.transparent_background:
        convert_cmd += " -antialias"
    elif config.anti_aliasing == 0:
        convert_cmd += " +antialias"
    else:
        convert_cmd += " -antialias"

    if config.transparent_background:
        convert_cmd += " -transparent {}".format(config.background_color)

    # determine output image filename
    output_basename = (
        pathlib.Path(config.output_basename)
        if config.output_basename is not None
        else None
    )
    output_dir = pathlib.Path(curdir)

    # check if output_basename is actually a directory
    if output_basename is not None:
        if not output_basename.is_absolute():
            output_basename = output_dir / output_basename

        if output_basename.is_dir():
            output_dir = pathlib.Path(output_basename)
            output_basename = None

    if output_basename is None:
        if input_file is not None:
            output_basename, _ = os.path.splitext(input_file)
        else:
            output_basename = "out"

    if input_file is None and config.idx is not None:
        output_basename = str(output_basename) + "-%d" % config.idx

    output_ext = config.output_format
    if output_ext.lower() == "html":
        output_ext = "png"
    if not output_ext.startswith("."):
        output_ext = "." + output_ext

    if not output_dir.exists():
        pass

    output_file = (output_dir / output_basename).with_suffix(output_ext)

    # # check for repeated extension.
    # if output_file.endswith("{0}.{0}".format(output_ext)):
    #   output_file,_ = os.path.splitext( output_file )

    # split output file name into directory a filename parts
    output_dir, output_file = os.path.split(output_file)
    if output_dir == "":
        output_dir = curdir

    # add comment containing LaTeX
    comment_lines = tlist()
    comment_lines += (
        "# This image was created with tex2im (https://github.com/CD3/tex2im)"
    )
    comment_lines += "# " + " ".join(
        map(lambda a: rf'"{a}"' if sum([c in a for c in " "]) else a, sys.argv)
    ).replace("\\", "\\\\")
    comment_lines += latex_snippet.replace("\\", "\\\\")
    comment_lines += ""
    if not config.no_comment:
        convert_cmd += " -comment '{COMMENT}'".format(COMMENT="\n".join(comment_lines))

    # convert image create by LaTeX to format requested
    convert_cmd += " out.pdf"
    convert_cmd += " {}".format(output_file)

    logging.info("running ImageMagick: {}".format(convert_cmd))
    res = subprocess.run(
        convert_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if res.returncode:
        logging.error("convert command returned non-zero status")
        logging.error("convert command: {}".format(convert_cmd))
        logging.error("convert output:")
        logging.error(res.stdout.decode("utf-8"))

    # if output format was html, convert the png we created
    # to an embedded html tag
    if config.output_format == "html":
        with open(output_file, "rb") as f:
            text = f.read()
        code = base64.b64encode(text).decode("utf-8")
        text = r"""<img src="data:image/{fmt};base64,{code}" {opts}>""".format(
            fmt="png", code=code, opts=""
        )
        basename, _ = os.path.splitext(output_file)
        output_file = "{}.{}".format(basename, "html")
        with open(output_file, "w") as f:
            f.write(text)

    # write latex code to image metadata
    # comment_lines = tlist()
    # comment_lines += "# This image was created with tex2im (https://github.com/CD3/tex2im)"
    # comment_lines += latex_snippet
    # exiftool_cmd = "exiftool -comment='{COMMENT}' {FILE}".format(COMMENT='<newline>'.join(comment_lines),FILE=output_file)
    # res = subprocess.run( exiftool_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
    # if res.returncode:
    # logging.error("exiftool command returned non-zero status")
    # logging.error("exiftool command: {}".format(exiftool_cmd))
    # logging.error("exiftool output:")
    # logging.error(res.stdout.decode('utf-8'))

    # copy image to working directory or print to stdout
    if config.stdout:
        with open(output_file, "rb") as f:
            os.write(sys.stdout.fileno(), f.read())

    else:
        logging.info(
            "copying file back to {}".format(os.path.join(curdir, output_file))
        )
        shutil.copyfile(output_file, os.path.join(output_dir, output_file))

    os.chdir(curdir)
    if config.keep_files:
        print("Generated files were written to {}.".format(tmpdir))
    else:
        shutil.rmtree(tmpdir)
        logging.info("deleted {}".format(tmpdir))
