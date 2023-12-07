# syntax=docker/dockerfile:1.4.3-labs
FROM alpine:3.16 as builder
ENV PYROOT=/venv
ENV PYTHONUSERBASE=$PYROOT
# WORKDIR /
RUN <<EOF
  apk update
  apk add --no-cache bc cargo gcc libffi-dev musl-dev openssl-dev rust python3-dev py3-pip
  pip3 install --no-cache-dir --no-compile poetry==1.2.0 wheel==0.37.1
EOF

COPY . /

RUN <<EOF
  poetry lock
  poetry export --without-hashes --format=requirements.txt > requirements.txt
  poetry build
  cp dist/*.whl .
  pip3 wheel -r requirements.txt
EOF

FROM alpine:3.16 as default
COPY --from=builder /*.whl /wheels/
RUN <<EOF
    apk add --update-cache --no-cache --virtual build-deps py3-pip
    apk add --update-cache --no-cache python3 git
    pip3 install --no-cache-dir /wheels/*.whl
    rm -rf /wheels
    apk del build-deps
EOF

WORKDIR /role
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["--version"]

