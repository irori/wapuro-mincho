SOURCE := bdf/jiskan24-2003-1.bdf
TARGETS := $(foreach ext, otf woff woff2, dist/wapuro-mincho.$(ext))

all: $(TARGETS) docs/wapuro-mincho.woff2 docs/wapuro-mincho-yoko2x.woff2 docs/wapuro-mincho-tate2x.woff2 docs/wapuro-mincho.subset.woff

$(TARGETS): $(SOURCE)
	./build.sh

docs/wapuro-mincho.woff2: dist/wapuro-mincho.woff2
	cp $< $@

docs/wapuro-mincho-yoko2x.woff2: dist/wapuro-mincho-yoko2x.woff2
	cp $< $@

docs/wapuro-mincho-tate2x.woff2: dist/wapuro-mincho-tate2x.woff2
	cp $< $@

docs/wapuro-mincho.subset.woff: dist/wapuro-mincho.woff docs/index.html
	pyftsubset dist/wapuro-mincho.woff --text-file=docs/index.html --output-file=$@ --flavor=woff

test:
	python -m unittest discover -s converter -p '*_test.py'
