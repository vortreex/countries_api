FROM python:3.12-slim-bookworm

WORKDIR /server
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONPATH="${PYTHONPATH}:/server"
EXPOSE 80
CMD ["python3", "src/server.py"]
