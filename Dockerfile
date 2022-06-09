FROM pharmbio/cellprofiler:v4.1.3

RUN python3 -m pip install jupyterlab==3.2.4
RUN pip3 install tensorflow-compression==2.8.0
RUN pip3 install tensorflow_datasets==4.5.2
