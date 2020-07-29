FROM python:alpine3.7
COPY . /bartender
WORKDIR /bartender
RUN pip install -r ./requirements.txt
EXPOSE 5000
CMD python ./main.py
