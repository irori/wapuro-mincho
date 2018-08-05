all: dist/wapuro-mincho.otf dist/wapuro-mincho.woff2

SOURCE := bdf/jiskan24-2003-1.bdf

dist/wapuro-mincho.otf: $(SOURCE) dist
	python converter/bdf2otf.py --out $@ $<

dist/wapuro-mincho.ttf: $(SOURCE) dist
	python converter/bdf2otf.py --out $@ $<

dist/wapuro-mincho.woff2: $(SOURCE) dist
	python converter/bdf2otf.py --out $@ $<

dist/wapuro-mincho.svg: $(SOURCE) dist
	python converter/bdf2svg.py $< > $@

dist:
	mkdir dist

test:
	python -m unittest discover -s converter -p '*_test.py'
