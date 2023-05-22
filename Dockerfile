FROM alpine:3.18.0
RUN apk update && apk upgrade && apk add python3 --no-cache
RUN mkdir /app
COPY actionserver /app/actionserver
COPY app.py /app
COPY requirements.txt /app
RUN cd /app ; python3 -m venv venv
RUN /app/venv/bin/python -m pip install pip --upgrade && /app/venv/bin/python -m pip install -r /app/requirements.txt
USER guest
#EXPOSE 5555
CMD /app/venv/bin/python /app/app.py