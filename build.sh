#!/bin/sh
convert="python src/convert.py"
source="bdf/jiskan24-2003-1.bdf bdf/jiskan24-2000-2.bdf"
ufo=dist/wapuro-mincho.ufo

$convert --out $ufo $source

for ext in $*
do
    $convert --out dist/wapuro-mincho.$ext $ufo
    $convert --style=v2x --out dist/wapuro-mincho-tate2x.$ext $ufo
    $convert --style=h2x --out dist/wapuro-mincho-yoko2x.$ext $ufo
done

rm $ufo
