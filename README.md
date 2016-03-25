# Description

Tex2im is a simple tool that converts LaTeX formulas into high resolution
pixmap graphics for inclusion in text processors or presentations.
It was written by Andreas Reigber and his official releases are still available at
http://www.nought.de/tex2im.php.

This fork was created to add a few features (such as embedding the LaTeX code in the image metadata
so that it can be extracted later if needed), and the last release official release was in 2004.

With tex2im you can write files containing only the formula in latex mathmode
and transform them to many different graphic formats. latex2html can do
something similar, but only on whole documents. This is the direct solution.


# Changes:


Anreas Reigber Releases:

Version 1.8: Support for non-formula mode and eps-graphics, bugfix for eqnarray formulas
Version 1.7: Tex2im can now process multiple files
Version 1.6: Removed necessity of generating an input file
Version 1.5: Transparency support
Version 1.4: Support for extra header lines and user specific default settings
Version 1.3: Fixed incompabilities with older versions of bash and convert
Version 1.2: Fixed tempfile problems on Redhat & Solaris
Version 1.1: Added color support
Version 1.0: Initial release

Newer Versions:

See the commit log.

# Examples:

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


Usage:

tex2im [options] inputfile(s)

The content of input file should be plain latex mathmode code! 
Alternatively, a string containing the latex code can be specified.

Options:
-v        show version
-h        show help
-o file   specifies output filename, 
          default is inputfile with new extension
-f expr   specifies output format, 
          possible examples: gif, jpg, tif......
          all formates supported by "convert" should work, 
          default: png
-r expr   specifies desired resolution in dpi, 
          possible examples: 100x100, 300x300, 200x150, 
          default is 150x150
-b expr   specifies the background color
          default: white
-t expr   specifies the text color
          default: black
-x file   file containing extra header lines of latex.
          default: ~/.tex2im_header
-n        no-formula mode (do not wrap in eqnarray* environment)
          default: off
-a        change status of antialiasing
          default is on for normal mode and
          off for transparent mode
-z        transparent background
          default: off

For user specific default values, tex2im reads the file '.tex2imrc'
in your home-directorty. To change a value, put inside one or more 
of the following 7 commands:

   resolution="150x150"
   format="png"
   color1="white"
   color2="black"
   extra_header="~/.tex2im_header"
   trans=0
   aa=1

In the file '~/.tex2im_header', additional latex header lines can
be put, for example '\usepackage{amsmath}' or your own definitions.

The transparency implementation of imagemagic has some problems in
combination with antialiasing. Therefore, by default, antialiasing
is off in transparent mode. If you switch it on via the -a flag you
can expect pixels with something between background and text color
around the letters. This can look good if the background used in
tex2im and the one of your document are identical, but also very bad
if this is not the case. True antialising with transparency seems not
to be possible. Just play around a bit to find the optimal settings.

# Installation:

To use tex2im, you need latex and convert (part of image magic) installed.
For color support, also the latex color style is needed.
To install tex2im, download the archive, uncompress it, and place the contained script "tex2im" in a directory in your path and make it executable. In details:

    > tar xzf tex2im.tar.gz
    > mv tex2im/tex2im /path/of/your/choice
    > chmod 755 /path/of/your/choice/tex2im

For reporting errors, comments or contributions, please mail me.


Acknowledgments:

Bernd Rinn for integrating the extra header lines, user specific 
default settings, the non-formula mode and some bugfixes
Laurent Ferro-Famil for some hints about processing multiple files
Many others for giving useful ideas, reporting errors and motivating me

