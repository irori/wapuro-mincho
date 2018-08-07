# ワープロ明朝

「ワープロ明朝」は、パブリックドメインの明朝体ビットマップフォント
jiskan24 をベースに、ワープロ専用機風の拡大処理を再現したフォントです。

![サンプル](https://irori.github.io/wapuro-mincho/poster.png)

# 各ディレクトリの説明
- `bdf` : 変換元のビットマップフォントが入っています。
- `converter` : ビットマップフォントを読み込み、スムージング処理を行ってアウトラインフォントを生成するスクリプトが入っています。
- `dist` : 生成されたフォントが入っています。
- `docs` : [ウェブサイト](https://irori.github.io/wapuro-mincho/)のソースです。

# ビルド方法
Python2が必要です（依存ライブラリのbdflibがPython3未対応のため）。

`pip`で依存ライブラリをインストールして、`make`でビルドします。

```
pip install -r requirements.txt
make
```


# ライセンス
- `bdf`, `dist` ディレクトリ内のフォントファイルはパブリックドメインです。
- `converter` ディレクトリ内のスクリプトは[MITライセンス](LICENSE)です。
