FROM acidrain/python-poetry:3.9-slim
WORKDIR /code
COPY pyproject.toml poetry.lock  ./
RUN poetry config virtualenvs.path ./venvs && poetry config virtualenvs.in-project true
RUN poetry install --no-root
COPY app /code/app
CMD ["poetry", "run", "python", "app/main.py"]