  $ x2im typst 'nabla' && ls
  out.png
  $ rm *
  $ echo 'nabla' > eq-1.typ
  $ x2im typst eq-1.typ && ls
  eq-1.png
  eq-1.typ
  $ rm *; x2im typst 'nabla' -f jpg && ls
  out.jpg
#  $ rm out.jpg; x2im typst 'nabla' 'x = 0' && ls
#  out-0.png
#  out-1.png
  $ rm *
  $ x2im typst 'nabla' -o my_name && ls
  my_name.png
  $ rm *
  $ x2im typst 'nabla' -o my_name -f jpg && ls
  my_name.jpg
  $ rm *
  $ x2im typst 'nabla' -o my_name.png && ls
  my_name.png
  $ rm *
  $ x2im typst 'nabla' -f html && ls
  out.html
  $ rm *
# 
#  Write to different directory
#  $ mkdir images
#  $ x2im typst '\nabla' -o images && ls
#  images
#  $ ls images
#  out.png
#  $ rm -r images
# 
#  $ mkdir images
#  $ x2im typst '\nabla' -o images/my_name && ls
#  images
#  $ ls images
#  my_name.png
#  $ rm -r images
# 
# 
#  $ echo '\nabla' > eq-1.tex
#  $ echo "x = 0"  > eq-2.tex
#  $ x2im typst eq-*.tex && ls
#  eq-1.png
#  eq-1.tex
#  eq-2.png
#  eq-2.tex
