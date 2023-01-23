# sphinx-pyproject-poetry

Move some of your Sphinx configuration into pyproject.toml created by poetry

## sphinx-pyproject との違い

[PEP 621](https://peps.python.org/pep-0621/) や
[PEP 631](https://peps.python.org/pep-0631/) にあるように、
プロジェクトの設定は pyproject.toml に記載することが求められている。

[poetry](https://python-poetry.org/) は pyproject.toml を自動生成し、
インストールしたパッケージ情報を（requirements.txt を使うこと無く）
pyproject.toml に記載してくれる。

また [sphinx-pyproject](https://github.com/sphinx-toolbox/sphinx-pyproject)
 は pyproject.toml を自動的に読み取るので、
[Sphinx](https://www.sphinx-doc.org/ja/master/) の conf.py に
設定することで、pyproject.toml を変更するだけで
ドキュメントに記載する値を変更する事が出来る。

このことによって、バージョン番号を上げる時など、
pyproject.toml の一箇所を変更するだけで、
パッケージのバージョン番号・ドキュメントのバージョン番号の両方を
変更できる、ように思われる。

しかし poetry は
[基本的な必須情報](https://cocoatomo.github.io/poetry-ja/pyproject/)
（name, version, description, authors）を
pyproject.toml の `[tool.poetry]` セクションに設定してしまう。

これに対し sphinx-pyproject は、PEP に定義されているように、
基本的な必須情報は `[project]` セクションに設定されているものとして読み込む。
（もちろん sphinx-pyproject に poetry の事情を汲み取る義理は無い）

この問題は poetry 側の問題であり、これを解決するよう
[issue](https://github.com/python-poetry/poetry/issues/3332) も作られている。
しかしこの issue の議論を見る限り、この問題が解決される気配は無い。

pyproject.toml に `[project]` と `[tool.poetry]` の両方を設定することが
最も早い解決法だが、同じファイルであっても２箇所に同じ設定があるのは、
やはりとても気持ちが悪い。

そこで sphinx-pyproject 側を修正し、
無理やり `[project]` ではなく `[tool.poetry]` を読み込むようにしたのが、
sphinx-pyproject-poetry である。

また sphinx-pyproject では、
authors および maintainers の項目は table として設定することを前提としている。

```
[[project.authors]]
name = "1st Author"

[[project.authors]]
name = "2nd Author"
```

しかし poetry では `1st author <1st.author@domain>` の形の配列で指定する。

```
[tool.poetry]
authors = ["1st Author <1st.author@domain>", "2nd Author <2nd.author@domain>"]
```

この問題についても sphinx-pyproject-poetry では poetry の形式を前提として、
authors および maintainers の項目を読み取る。

## 使い方

使い方は sphinx-pyproject と全く同じである。

```
# conf.py

import os
import sys

from sphinx_pyproject_poetry import SphinxConfig

sys.path.insert(0, os.path.abspath(".."))
config = SphinxConfig("../pyproject.toml", globalns=globals())
project = config.name
release = config.version
```

Sphinx の conf.py を上記のように修正し、
pyproject.toml の `[tool.pyproject]` に項目を書くだけで、
conf.py における設定を完了することが出来る。

name, version, description, authors, maintainers の５つの項目は
`[tool.poetry]` から読み込む。
そして authors と maintainers の２つの項目は併せて
author という名前で保持される。

conf.py における設定項目は、
[www.sphinx-doc.org](https://www.sphinx-doc.org/ja/master/usage/configuration.html)
に記載されている。
