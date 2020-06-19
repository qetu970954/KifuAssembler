# dockerfile to generate running environment for kifu assembler
FROM python:3.8

RUN mkdir /KifuAssembler
WORKDIR /KifuAssembler

RUN pip install poetry
RUN poetry config virtualenvs.create false --local
COPY poetry.lock pyproject.toml /KifuAssembler/

RUN poetry install -n
