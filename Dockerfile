FROM python:3.8

RUN mkdir /KifuAssembler
WORKDIR /KifuAssembler

RUN pip install poetry
RUN poetry config virtualenvs.create false --local
COPY poetry.lock pyproject.toml /KifuAssembler/

# to prevent poetry from installing my actual app,
# and keep docker able to cache layers
RUN poetry install -n
