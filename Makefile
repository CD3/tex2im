copy-to-bin:
	install tex2im ~/bin
	install im2tex ~/bin

upload-to-pypi:
	pipenv run python setup.py sdist
	pipenv run twine upload dist/*
