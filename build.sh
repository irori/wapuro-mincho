#!/bin/sh
convert="python converter/convert.py"
source="bdf/jiskan24-2003-1.bdf bdf/jiskan24-2000-2.bdf"

for ext in $*
do
    $convert --out dist/wapuro-mincho.$ext $source
    $convert --style=v2x --out dist/wapuro-mincho-tate2x.$ext $source
    $convert --style=h2x --out dist/wapuro-mincho-yoko2x.$ext $source
done
