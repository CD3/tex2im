  $ tex2im '\nabla' && ls
  out.png
  $ tex2im '\nabla' --stdout > out2.png && ls
  out.png
  out2.png
  $ compare -metric AE out.png out2.png diff.png
  0 (no-eol)
