FROM pytorch/pytorch as build
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt