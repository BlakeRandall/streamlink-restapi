FROM python:3.10
WORKDIR /app/

RUN apt update && \
    apt install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements/ ./requirements/
COPY ./requirements.txt ./requirements.txt

RUN python -m ensurepip --upgrade && \
    python -m pip install --upgrade pip && \
    python -m pip install --upgrade --requirement ./requirements.txt

COPY ./streamlinkrestapi/ ./streamlinkrestapi
COPY ./uwsgi.yml ./uwsgi.yml

EXPOSE 8080/tcp

ENTRYPOINT ["uwsgi"]
CMD ["--yaml", "uwsgi.yml"]
