FROM python:latest
WORKDIR /backend
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "hypercorn", "app:app", "--bind", "0.0.0.0:80"]