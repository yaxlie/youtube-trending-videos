FROM python:3.7

RUN apt-get update

RUN apt-get install unzip

# TODO: Tesseract install https://github.com/tesseract-ocr/tesseract/wiki + set env path

WORKDIR /usr/src/youtube-trending

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir data out

# ADD https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo-tiny.h5 data
ADD https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5 data

ADD https://www.cs.put.poznan.pl/kmiazga/students/ped/data.zip data

RUN unzip data/data.zip

CMD [ "python", "./main.py" ]