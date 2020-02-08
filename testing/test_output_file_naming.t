  $ ${TESTDIR}/tex2im '\nabla' && ls
  out.png
  $ rm out.png; ${TESTDIR}/tex2im '\nabla' -f jpg && ls
  out.jpg
  $ rm out.jpg; ${TESTDIR}/tex2im '\nabla' 'x = 0' && ls
  out-0.png
  out-1.png
  $ rm out-*.png
  $ ${TESTDIR}/tex2im '\nabla' -o my_name && ls
  my_name.png
  $ rm my_name.png
  $ ${TESTDIR}/tex2im '\nabla' -o my_name -f jpg && ls
  my_name.jpg
  $ rm my_name.jpg
  $ ${TESTDIR}/tex2im '\nabla' -o my_name.png && ls
  my_name.png
  $ rm my_name.png
  $ echo '\nabla' > eq-1.tex
  $ echo "x = 0"  > eq-2.tex
  $ ${TESTDIR}/tex2im eq-*.tex && ls
  eq-1.png
  eq-1.tex
  eq-2.png
  eq-2.tex
  $ rm eq-*; ${TESTDIR}/tex2im '\nabla' -f html && ls
  out.html
  $ rm *.html
