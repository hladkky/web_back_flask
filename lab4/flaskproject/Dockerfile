FROM python
COPY . /app
WORKDIR /app

ENV FLASK_APP=__init__.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install -r requirements.txt

CMD ["flask", "run"]
