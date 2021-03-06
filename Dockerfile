FROM python:3.6-slim-stretch
#MAINTAINER Will Siffer <wsiffer@purdue.edu>
RUN apt-get update -y
RUN apt-get install -y python3 python-pip-whl python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt 
RUN pip3 install rpi_ws281x adafruit-circuitpython-neopixel
RUN python3 -m pip install --force-reinstall adafruit-blinka
#RUN rm -f app.db
#RUN python3 ./db_create.py
RUN chmod +x OLEDinstall.sh
ENTRYPOINT ["OLEDinstall.sh"]
RUN pip3 install wiringpi
RUN pip3 install spidev
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["main.py"]
