from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
import datetime


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
