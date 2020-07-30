# Description

Tex2im is a simple tool that converts LaTeX formulas into high resolution
pixmap graphics for inclusion in text processors or presentations.
The original script written by Andreas Reigber in bash, and his official releases are still available at
http://www.nought.de/tex2im.php.

Version 2.0 was a complete rewrite in Python. While the Python script shares the same interface (it accepts mostly the same command line options),
it does not share any code, other than the `convert` command that is ran to generate the final image.

# Examples:

These examples were written by Andreas Reigber for his original script, and they still
work with version 2.

Let's play around in the examples directory. Just type:

    > tex2im examples/example1.tex

And you'll get a nice formula in a file named "example1.png"
If you need color, look at example 2:

    > tex2im -b yellow -t blue examples/example2.tex

This time, the result is a color formula.

    > tex2im "\sum_{i=0}^5 x_i^2"

generates a file named 'out.png', containing the formula

    > tex2im *.tex

this is how multiple files can be processed.

Note that example4.tex needs the '-n' (no-formula) option when processed.


You can place additional preamble lines in the file '~/.tex2im_preamble'. These
will be appended to the preamble that gets generated before running `latex`.

The transparency implementation of imagemagic has some problems in
combination with antialiasing. Therefore, by default, antialiasing
is off in transparent mode. If you switch it on via the -a flag you
can expect pixels with something between background and text color
around the letters. This can look good if the background used in
`tex2im` and the one of your document are identical, but also very bad
if this is not the case. True antialising with transparency seems not
to be possible. Just play around a bit to find the optimal settings.

# Installation:

To use `tex2im`, you need `pdflatex` and `convert` (part of image magic) installed.
For color support, also the latex color style is needed.
You can install `tex2im` with `pip`

```
> pip3 install tex2im
```

or just copy the `tex2im` file in this repository to a directory in your PATH.

```
> cp tex2im/tex2im /path/of/your/choice
> chmod 755 /path/of/your/choice/tex2im
````


