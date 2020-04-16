FROM python:3.7

RUN apt-get update

RUN apt-get install unzip

WORKDIR /usr/src/youtube-trending

COPY requirements.txt ./

COPY . .

RUN mkdir data out

RUN sudo apt install tesseract-ocr

# ADD https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo-tiny.h5 data
ADD https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5 data

# Keep it as last (url can change and reset cache)
ADD https://www.cs.put.poznan.pl/kmiazga/students/ped/data.zip data
RUN unzip data/data.zip

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]