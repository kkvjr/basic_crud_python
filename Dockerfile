FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer="Paulo Mota <paulo@kissplatform.com>"

RUN pip install fastapi uvicorn gunicorn

COPY . .

RUN  pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn"  , "app.main:app", "--host", "0.0.0.0", "--port", "80","--workers","100","--reload"]