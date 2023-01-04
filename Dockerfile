FROM python:3.9

WORKDIR /code

ADD src ./src
ADD setup.py .
ADD README.md .

RUN python3 setup.py build
RUN python3 setup.py install

ENTRYPOINT ["capital-gains"]