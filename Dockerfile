FROM python:3.8.19-alpine

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

CMD ["python", "bot.py"]