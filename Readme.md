# NOTE: Discontinued

## Stock Scrape App
Web app that scrapes Nepse stocks and perform technical analysis.

### Technology Used
- Django
- Selenium and Beautiful Soup 4
- Plotly Dash
- Celery
- Celery beat
- Redis

### Features
- Scrapes stock info dynamically if not present in the database.
- Plots close price graph
- Performs MACD Analysis
- Cronjob to scrape all symbols (from symbols.json file)
  - NOTE: You need to configure this in django admin and both celery worker and celery-beat server should be up and running.
  - This will take some time to scrape all the data


### How to run
- Install redis, lxml on your system
- Make your virtual environment and install from requirements.txt ( <code> pip install -r requirements.txt </code> )
- In one terminal tab, run <code> python manage.py makemigrations && python manage.py migrate</code>
- run <code> python manage.py createsuperuser </code> and fill the information to create <b> admin </b> user
- In next terminal tab, run <code> redis-server </code>
- In another terminal tab, run <code> celery -A scrape.celery.app worker -l INFO </code> to start celery worker process.
- Make sure server and celery worker is started correctly. 
- Open your browser and visit http://localhost:8000/

