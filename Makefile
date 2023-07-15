SOURCE := bdf/jiskan24-2003-1.bdf
TARGETS := $(foreach ext, otf woff2, dist/wapuro-mincho.$(ext))

all: $(TARGETS) docs/wapuro-mincho.woff2 docs/wapuro-mincho-yoko2x.woff2 docs/wapuro-mincho-tate2x.woff2 docs/wapuro-mincho.subset.woff2

$(TARGETS): $(SOURCE)
	./build.sh

docs/%.woff2: dist/%.woff2
	cp $< $@

docs/wapuro-mincho.subset.woff2: dist/wapuro-mincho.woff2 docs/index.html
	pyftsubset dist/wapuro-mincho.woff2 --text-file=docs/index.html --output-file=$@ --flavor=woff2

test:
	python -m unittest discover -s converter -p '*_test.py'
