FROM python:3.8.5
WORKDIR /code    
COPY . ./        
RUN pip install -r /code/telegram_bot_requirements.txt
WORKDIR /code/telegram_bot_project
CMD python telegram_bot_app/bot.py
