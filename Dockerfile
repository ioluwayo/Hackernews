FROM python:3
RUN mkdir Hackernews
WORKDIR Hackernews
COPY . .
RUN pip install --upgrade pip
RUN pip install .
CMD tail -f /dev/null