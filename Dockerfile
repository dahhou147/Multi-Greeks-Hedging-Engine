FROM python:3.10-slim
WORKDIR /Option_Hedging_Webb
COPY . .
RUN pip install poetry
RUN poetry install
CMD ["pytest", "tests/"]
