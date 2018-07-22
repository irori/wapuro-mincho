all: out/jiskan24-2003-1.otf

out/%.otf: bdf/%.bdf out
	python bdf2otf.py --out $@ $<

out/%.svg: bdf/%.bdf
	python bdf2svg.py $< > $@

out:
	mkdir out
