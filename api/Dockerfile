FROM python:3.12-slim

WORKDIR /app
RUN pip install uv
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

COPY . /app

RUN uv -n sync

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]