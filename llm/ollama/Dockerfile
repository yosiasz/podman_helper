FROM python:3.9

ADD train_syslog.py .

RUN pip install ollama

CMD ["ollama", "pull", 'llama3.2"]

CMD ["pyton", "./train_syslog.py"]