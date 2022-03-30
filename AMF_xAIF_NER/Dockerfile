FROM python:3

RUN mkdir -p /home/amf_noop
WORKDIR /home/amf_noop

RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt
# RUN pip install gunicorn
RUN python -m spacy download en_core_web_sm

ADD app app
ADD routes.py .
# ADD boot.sh ./
# RUN chmod +x boot.sh

ENV FLASK_APP app

EXPOSE 5000
# ENTRYPOINT ["./boot.sh"]
ENTRYPOINT python routes.py
