FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir /apython
RUN mkdir /examples

COPY apython/* ./apython
COPY examples/* ./examples

# cause trouble from grpc-requests install
# COPY setup.py setup.py
# RUN python3 setup.py install
RUN pip3 install protobuf
RUN pip3 install grpc-requests
RUN pip3 install google-cloud

ENTRYPOINT [ "python3" ]
