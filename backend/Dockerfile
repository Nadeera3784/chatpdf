FROM python:3.12

WORKDIR /backend

RUN python3 -m venv /opt/venv

COPY requirements.txt .

RUN . /opt/venv/bin/activate && pip install -r requirements.txt

COPY . .

CMD . /opt/venv/bin/activate && exec python main.py