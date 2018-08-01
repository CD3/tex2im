  $ ${TESTDIR}/tex2im -h | head -n1
  usage: .* (re)
  $ ${TESTDIR}/tex2im --version
  version: [0-9]+\.[-0-9]+ (re)
  $ ${TESTDIR}/tex2im -v '\nabla'         2>&1 | grep "running ImageMagick"
  .* -antialias .* (re)
  $ ${TESTDIR}/tex2im -v '\nabla' -z      2>&1 | grep "running ImageMagick"
  .* \+antialias .* (re)
  $ ${TESTDIR}/tex2im -v '\nabla'    -a 0 2>&1 | grep "running ImageMagick"
  .* \+antialias .* (re)
  $ ${TESTDIR}/tex2im -v '\nabla' -z -a 0 2>&1 | grep "running ImageMagick"
  .* \+antialias .* (re)
  $ ${TESTDIR}/tex2im -v '\nabla'    -a 1 2>&1 | grep "running ImageMagick"
  .* -antialias .* (re)
  $ ${TESTDIR}/tex2im -v '\nabla' -z -a 1 2>&1 | grep "running ImageMagick"
  .* -antialias .* (re)
  $ ${TESTDIR}/tex2im '\nabla' && ls
  out.png
  $ rm out.png; ${TESTDIR}/tex2im '\nabla' -f jpg && ls
  out.jpg
  $ rm out.jpg; ${TESTDIR}/tex2im '\nabla' 'x = 0' && ls
  out-0.png
  out-1.png
  $ rm out-*.png
  $ echo '\nabla' > eq-1.tex
  $ echo "x = 0"  > eq-2.tex
  $ ${TESTDIR}/tex2im eq-*.tex && ls
  eq-1.png
  eq-1.tex
  eq-2.png
  eq-2.tex
  $ rm eq-*; ${TESTDIR}/tex2im '\nabla' -f html && ls
  out.html





