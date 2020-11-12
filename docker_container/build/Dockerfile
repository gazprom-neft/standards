FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
LABEL maintainer="Roman Kh <rhudor@gmail.com>"

ENV TF_VERSION=1.15

# install system packages
RUN apt-get update && \
    apt-get install -y pkg-config software-properties-common build-essential cmake gfortran \
        libboost-dev libboost-system-dev libboost-filesystem-dev \
        liblapack-dev libatlas-base-dev libopenblas-dev \
        zlib1g-dev liblzma-dev liblz4-dev libzstd-dev libsnappy-dev zip p7zip-full \
        libhdf5-dev libedit-dev \
        libzmq3-dev \
        git wget tmux nano sysstat htop mc \
        python3-pip python3-dev && \
    pip3 install -U pip && \
    hash -r pip3

# update CMake
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | apt-key add - && \
    apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main' && \
    apt-get update && \
    apt-get install cmake -y

# install russian locale
RUN apt-get install -y language-pack-ru && \
    echo ru_RU.UTF8 >> /var/lib/locales/supported.d/local && \
    echo ru_RU.UTF-8 UTF-8 >> /var/lib/locales/supported.d/local

ENV LC_CTYPE=ru_RU.UTF-8
ENV PIP_NO_CACHE_DIR=true

# install python packages
RUN pip3 install -U setuptools && \
    apt-get install -y python3-venv && \
    pip3 install virtualenv && \
    pip3 install pipenv && \
    pip3 install pipreqs && \
    pip3 install cython && \
    pip3 install toolz && \
    pip3 install fsspec && \
    pip3 install cloudpickle && \
    pip3 install dill && \
    pip3 install fastcache && \
    pip3 install python-snappy && \
    pip3 install blosc && \
    pip3 install aiofiles && \
    pip3 install packaging && \
    pip3 install click && \
    pip3 install itsdangerous && \
    pip3 install requests && \
    pip3 install multiprocess && \
    pip3 install psutil && \
    pip3 install eventlet && \
    pip3 install greenlet && \
    pip3 install aiohttp && \
    pip3 install python-socketio && \
    pip3 install flask && \
    pip3 install flask-socketio && \
    pip3 install pytest && \
    pip3 install pytest-aiohttp && \
    pip3 install pytest-flask && \
    pip3 install pytest-cov && \
    pip3 install tox && \
    pip3 install autopep8 && \
    pip3 install -U pylint

# install LLVM and Numba
RUN wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - && \
    apt-add-repository "deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic-8 main" && \
    apt-get update && \
    apt-get install -y llvm-8 && \
    ln -s /usr/bin/llvm-config-8 /usr/bin/llvm-config && \
    pip3 install llvmlite && \
    pip3 install numba

# install data manipulation packages
RUN pip3 install numpy && \
    pip3 install bottleneck && \
    pip3 install numexpr && \
    pip3 install tables && \
    pip3 install h5py && \
    pip3 install pandas && \
    pip3 install feather-format && \
    pip3 install fastparquet && \
    pip3 install dask && \
    pip3 install python-dateutil

# install stats and ML libraries
RUN pip3 install scipy && \
    pip3 install sklearn && \
    pip3 install sklearn-pandas && \
    pip3 install statsmodels && \
    pip3 install pyflux && \
    pip3 install nltk && \
    pip3 install hmmlearn && \
    pip3 install xgboost && \
    pip3 install lightgbm && \
    pip3 install ortools && \
    pip3 install tdigest

# install image libraries
RUN apt-get install -y graphviz libfreetype6-dev libpng-dev libjpeg-dev && \
    pip3 install graphviz && \
    pip3 install opencv-python &&\
    pip3 install matplotlib && \
    pip3 install scikit-image && \
    pip3 install imageio && \
    pip3 install seaborn && \
    pip3 install ggplot && \
    pip3 install bokeh && \
    pip3 install folium && \
    pip3 install vispy && \
    pip3 install plotly && \
    pip3 install tqdm

# install special packages
RUN pip3 install SimpleITK && \
    pip3 install pydicom && \
    pip3 install wfdb && \
    pip3 install PyWavelets && \
    pip3 install pyedflib && \
    pip3 install segyio && \
    pip3 install lasio && \
    pip3 install xlrd

# increase counter to rebuild the image if some library changes
ENV UPDATE_DL 1
# install deep learning libraries
RUN pip3 install tensorflow-gpu==$TF_VERSION && \
    pip3 install --no-deps keras && \
    pip3 install --no-deps edward && \
    pip3 install torch torchvision torchtext && \
    pip3 install pyro-ppl

# install nodejs and npm
RUN apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -y nodejs

# install jupyter and extensions
WORKDIR /jupyter/config
WORKDIR /jupyter/secret
RUN pip3 install jupyter && \
    pip3 install jupyterlab && \
    pip3 install jupyter_contrib_nbextensions && \
    jupyter contrib nbextension install --system && \
    pip3 install ipyvolume && \
    pip3 install jupyterhub && \
    pip3 install -U nbdime && \
    nbdime extensions --enable && \
    jupyter labextension install @jupyterlab/git && \
    pip3 install --upgrade jupyterlab-git && \
    jupyter serverextension enable --py jupyterlab_git && \
    jupyter labextension install @jupyterlab/toc && \
    jupyter labextension install @jupyterlab/github && \
    pip3 install ipywidgets && \
    jupyter nbextension enable --py --sys-prefix widgetsnbextension && \
    jupyter labextension install @jupyter-widgets/jupyterlab-manager && \
    jupyter labextension install plotlywidget && \
    jupyter labextension install jupyterlab-plotly

# install forked libraries
RUN pip3 uninstall -y pillow && \
    CC="cc -mavx2" pip3 install -U --force-reinstall pillow-simd

# install docker
RUN wget https://get.docker.com -q -O /tmp/getdocker && \
    chmod +x /tmp/getdocker && \
    sh /tmp/getdocker

COPY start-notebook.sh /usr/local/bin/start-notebook.sh

WORKDIR /notebooks

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["start-notebook.sh"]
