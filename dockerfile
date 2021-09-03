FROM pytorch/pytorch as build
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get -y dist-upgrade
RUN apt install -y netcat
RUN chmod +x wait-for
RUN pip3 install -r requirements.txt