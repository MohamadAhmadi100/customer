FROM python:3.9

WORKDIR /customer

COPY ./README.md /customer/README.md

COPY ./requirements.txt /customer/requirements.txt

COPY ./.env /customer/.env

COPY ./config.py /customer/config.py

COPY ./setup.py /customer/setup.py

COPY ./customer /customer/app

RUN pip install -e /customer/.

CMD ["python", "/customer/app/main.py"]
