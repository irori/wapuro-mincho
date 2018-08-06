all: dist/wapuro-mincho.otf dist/wapuro-mincho.woff dist/wapuro-mincho.woff2

SOURCE := bdf/jiskan24-2003-1.bdf

dist/wapuro-mincho.otf: $(SOURCE)
	python converter/bdf2otf.py --out $@ $<

dist/wapuro-mincho.ttf: $(SOURCE)
	python converter/bdf2otf.py --out $@ $<

dist/wapuro-mincho.woff: $(SOURCE)
	python converter/bdf2otf.py --out $@ $<

dist/wapuro-mincho.woff2: $(SOURCE)
	python converter/bdf2otf.py --out $@ $<

dist/wapuro-mincho.svg: $(SOURCE)
	python converter/bdf2svg.py $< > $@

docs/wapuro-mincho.subset.woff: dist/wapuro-mincho.woff docs/index.html
	pyftsubset dist/wapuro-mincho.woff --text-file=docs/index.html --output-file=$@ --flavor=woff

test:
	python -m unittest discover -s converter -p '*_test.py'
