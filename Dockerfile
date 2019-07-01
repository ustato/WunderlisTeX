FROM python:latest


ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NOWARNINGS yes

# 必要なパッケージを追加
RUN apt-get -y update --fix-missing \
    && apt-get -y upgrade \
    && apt-get install -y wget bzip2 ca-certificates busybox-static \
       libglib2.0-0 libxext6 libsm6 libxrender1 cron ffmpeg emacs \
       texlive-lang-cjk xdvik-ja evince \
       texlive-fonts-recommended texlive-fonts-extra

# タイムゾーン設定
ENV TZ=Asia/Tokyo


# スクリプト保存ディレクトリ
RUN mkdir /root/git_repository
RUN mkdir /root/tex

# Pythontexをコンパイル
WORKDIR /root/git_repository
RUN git clone https://github.com/gpoore/pythontex.git

WORKDIR /root/git_repository/pythontex/pythontex
RUN echo y | latex pythontex.ins
RUN mktexlsr

# 各種スクリプトと設定ファイルを追加
WORKDIR /root/tex
ADD tex/todolist.py /root/tex/todolist.py
ADD tex/secret.yaml /root/tex/secret.yaml
ADD requirements.txt /root/tex/requirements.txt

# texのスタイル
ADD tex/additional.sty /root/tex/additional.sty

# Pythonライブラリをインストール
RUN pip install -r requirements.txt


# TeXをコンパイル
ADD tex/test.tex /root/tex/test.tex
RUN platex test.tex
RUN pythontex test
RUN platex test.tex
RUN dvipdfmx test
RUN rm -rf test.aux test.log test.dvi test.pytxcode test.synctex*
RUN rm -rf pythontex-files-test __pycache__ script.tex.aux


# PDFをFlaskアプリで見れるようにする
ADD script/download_flask.py /root/tex/download_flask.py
RUN python download_flask.py
