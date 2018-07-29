all: out/jiskan24-2003-1.otf

out/%.otf: bdf/%.bdf out
	python converter/bdf2otf.py --out $@ $<

out/%.ttf: bdf/%.bdf out
	python converter/bdf2otf.py --out $@ $<

out/%.woff2: bdf/%.bdf out
	python converter/bdf2otf.py --out $@ $<

out/%.svg: bdf/%.bdf
	python converter/bdf2svg.py $< > $@

out:
	mkdir out

test:
	python -m unittest discover -s converter -p '*_test.py'
