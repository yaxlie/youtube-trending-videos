FROM python:3.7

WORKDIR /usr/src/youtube-trending

RUN mkdir data out

# RUN wget -O data/yolo.h5 https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5
RUN wget https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo-tiny.h5 -O ./data/yolo-tiny.h5
RUN wget https://www.cs.put.poznan.pl/kmiazga/students/ped/youtube_data.zip -O ./data/youtube_data.zip

COPY requirements.txt ./

RUN pip install -r requirements.txt

RUN \
	apt-get update && \ 
	apt-get install tesseract-ocr -y && \
	apt-get install unzip

RUN unzip data/youtube_data.zip -d data && \
	mv data/youtube_data/* data/

COPY . .

RUN python download.py

CMD [ "python", "./main.py" ]
