# ワープロ明朝 (Wāpuro Mincho)

"ワープロ明朝" is a font that reproduced the smoothing algorithm used in the 80-90's Japanese word processors.

![Sample](https://irori.github.io/wapuro-mincho/poster.png)

# Directories
- `bdf` : Contains the base bitmap font (Jiskan24).
- `converter` : Contains a script that generates smoothed outline fonts from bitmap fonts.
- `dist` : Generated fonts are placed in this directory.
- `docs` : Source code of the [web site](https://irori.github.io/wapuro-mincho/).

# Build
Install the dependent libraries with `pip`, and build with `make`.

```
pip install -r requirements.txt
make
```

# License
- The font files in the `bdf` and `dist` directories are public domain.
- The script files in `converter` directory are governed by the [MIT license](LICENSE).
