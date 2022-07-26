FROM python:3.9

ENV POETRY_VERSION=1.1.12
RUN python -m pip install poetry==$POETRY_VERSION

WORKDIR /code

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.in-project true --local
RUN poetry install --no-dev

COPY . .
EXPOSE 8000
CMD [ "poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]