FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt -U

COPY . .

CMD ["python3", "-m", "checkuser", "--start", "--flask"]