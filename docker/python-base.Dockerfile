# base-python/Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY function.py .
CMD ["python", "function.py"]
