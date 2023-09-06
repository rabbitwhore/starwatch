from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    # Run the Flask application
    #host='192.168.50.19' 
    app.run(debug=True)
