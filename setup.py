# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["sphinx_pyproject_poetry"]

package_data = {"": ["*"]}

install_requires = [
    "dom-toml>=0.6.0,<0.7.0",
    "domdf-python-tools>=3.6.0,<4.0.0",
]

setup_kwargs = {
    "name": "sphinx-pyproject-poetry",
    "version": "0.0.0",
    "description": "",
    "long_description": '# sphinx-pyproject-poetry\n\nMove some of your Sphinx configuration into pyproject.toml created by poetry\n\n## sphinx-pyproject との違い\n\n[PEP 621](https://peps.python.org/pep-0621/) や\n[PEP 631](https://peps.python.org/pep-0631/) にあるように、\nプロジェクトの設定は pyproject.toml に記載することが求められている。\n\n[poetry](https://python-poetry.org/) は pyproject.toml を自動生成し、\nインストールしたパッケージ情報を（requirements.txt を使うこと無く）\npyproject.toml に記載してくれる。\n\nまた [sphinx-pyproject](https://github.com/sphinx-toolbox/sphinx-pyproject)\n は pyproject.toml を自動的に読み取るので、\n[Sphinx](https://www.sphinx-doc.org/ja/master/) の conf.py に\n設定することで、pyproject.toml を変更するだけで\nドキュメントに記載する値を変更する事が出来る。\n\nこのことによって、バージョン番号を上げる時など、\npyproject.toml の一箇所を変更するだけで、\nパッケージのバージョン番号・ドキュメントのバージョン番号の両方を\n変更できる、ように思われる。\n\nしかし poetry は\n[基本的な必須情報](https://cocoatomo.github.io/poetry-ja/pyproject/)\n（name, version, description, authors）を\npyproject.toml の `[tool.poetry]` セクションに設定してしまう。\n\nこれに対し sphinx-pyproject は、PEP に定義されているように、\n基本的な必須情報は `[project]` セクションに設定されているものとして読み込む。\n（もちろん sphinx-pyproject に poetry の事情を汲み取る義理は無い）\n\nこの問題は poetry 側の問題であり、これを解決するよう\n[issue](https://github.com/python-poetry/poetry/issues/3332) も作られている。\nしかしこの issue の議論を見る限り、この問題が解決される気配は無い。\n\npyproject.toml に `[project]` と `[tool.poetry]` の両方を設定することが\n最も早い解決法だが、同じファイルであっても２箇所に同じ設定があるのは、\nやはりとても気持ちが悪い。\n\nそこで sphinx-pyproject 側を修正し、\n無理やり `[project]` ではなく `[tool.poetry]` を読み込むようにしたのが、\nsphinx-pyproject-poetry である。\n\nまた sphinx-pyproject では、\nauthors および maintainers の項目は table として設定することを前提としている。\n\n```\n[[project.authors]]\nname = "1st Author"\n\n[[project.authors]]\nname = "2nd Author"\n```\n\nしかし poetry では `1st author <1st.author@domain>` の形の配列で指定する。\n\n```\n[tool.poetry]\nauthors = ["1st Author <1st.author@domain>", "2nd Author <2nd.author@domain>"]\n```\n\nこの問題についても sphinx-pyproject-poetry では poetry の形式を前提として、\nauthors および maintainers の項目を読み取る。\n\n## 使い方\n\n使い方は sphinx-pyproject と全く同じである。\n\n```\n# conf.py\n\nimport os\nimport sys\n\nfrom sphinx_pyproject_poetry import SphinxConfig\n\nsys.path.insert(0, os.path.abspath(".."))\nconfig = SphinxConfig("../pyproject.toml", globalns=globals())\nproject = config.name\nrelease = config.version\n```\n\nSphinx の conf.py を上記のように修正し、\npyproject.toml の `[tool.pyproject]` に項目を書くだけで、\nconf.py における設定を完了することが出来る。\n\nname, version, description, authors, maintainers の５つの項目は\n`[tool.poetry]` から読み込む。\nそして authors と maintainers の２つの項目は併せて\nauthor という名前で保持される。\n\nconf.py における設定項目は、\n[www.sphinx-doc.org](https://www.sphinx-doc.org/ja/master/usage/configuration.html)\nに記載されている。\n',
    "author": "Tetsutaro Maruyama",
    "author_email": "tetsutaro.maruyama@gmail.com",
    "maintainer": "None",
    "maintainer_email": "None",
    "url": "None",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.10,<4.0",
}


setup(**setup_kwargs)
