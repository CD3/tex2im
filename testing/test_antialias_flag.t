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
