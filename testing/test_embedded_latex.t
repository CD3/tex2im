  $ ${TESTDIR}/tex2im 'x = 0'
  $ identify -format '%[comment]' out.png
  # This image was .* (re)
  x = 0
