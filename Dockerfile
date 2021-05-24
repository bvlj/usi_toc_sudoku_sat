FROM python:3-alpine

RUN mkdir /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY solver /app/solver
ENTRYPOINT [ "python" ]
CMD [ "solver/app.py" ]
