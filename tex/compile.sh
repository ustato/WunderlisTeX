platex ${1}.tex
pythontex ${1}
platex ${1}.tex
dvipdfmx ${1}
rm -rf ${1}.aux ${1}.log ${1}.dvi ${1}.pytxcode ${1}.synctex*
rm -rf pythontex-files-${1} __pycache__ script.tex.aux
