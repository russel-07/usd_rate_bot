FROM python:3.8.5
WORKDIR /code    
COPY . ./        
RUN pip install -r /code/backend_requirements.txt
WORKDIR /code/backend_project
CMD gunicorn backend_project.wsgi:application --bind 0.0.0.0:8000
