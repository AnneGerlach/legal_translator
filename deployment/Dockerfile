
FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /code/requirements.txt



RUN python3 -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /app

WORKDIR /app

# TODO ~~CD to /src or rename src to src to fix import issues~~ Check if this works
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
