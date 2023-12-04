FROM python:3.8.5
WORKDIR /code    
COPY . ./        
RUN pip install -r /code/requirements.txt
WORKDIR /code/usd_rate_bot_project
CMD python manage.py collectstatic --no-input && \
    python manage.py loaddata fixtures.json && \
    # python telegram_bot_app/bot.py && \
    gunicorn usd_rate_bot_project.wsgi:application --bind 0.0.0.0:8000
