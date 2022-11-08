FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
EXPOSE 8050
CMD ["python", "/app/app.py"] #CMD gunicorn -b 0.0.0.0:80 app.app:server

#FROM python:3.9-slim
#WORKDIR /app
##ADD . /app
## copy over the requirements file and run pip install to install the packages
##into your container at the directory defined above

#RUN pip install --no-cache-dir -r requirements.txt --user
#EXPOSE 8050
#CMD ["python", "app.py"]