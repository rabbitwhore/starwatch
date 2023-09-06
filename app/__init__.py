# app/__init__.py
from datetime import datetime
import pytz

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from .config import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USE_SSL, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
from apscheduler.schedulers.background import BackgroundScheduler


# Initialize extensions
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__, static_url_path='/static')

    # Load configuration from config.py
    app.config.from_pyfile('config.py')

    # Initialize database
    db.init_app(app)

    # Initialize Flask-Mail
    mail.init_app(app)

    # Register blueprints or import routes here
    from app.routes import bp
    app.register_blueprint(bp)

    # Import the models here to avoid circular imports

    
    # Schedule the job to send email
    @app.before_request
    def schedule_email_job():
        if not current_app.config.get('EMAIL_JOB_SCHEDULED'):
            print('Email is running')
            scheduler = BackgroundScheduler(daemon=True)
            scheduler.add_job(send_email, 'interval', minutes=1440, id='email_job', args=[current_app._get_current_object()])
            scheduler.start()
            current_app.config['EMAIL_JOB_SCHEDULED'] = True
        if not current_app.config.get('UPDATE_WHO_IS_JOB_SCHEDULED'):
            print("Update is running")
            scheduler = BackgroundScheduler(daemon=True)
            scheduler.add_job(update_who_is, 'interval', minutes=10080, id='update_who_is_job', args=[current_app._get_current_object()])
            scheduler.start()
            current_app.config['UPDATE_WHO_IS_JOB_SCHEDULED'] = True

    return app
def update_who_is(app):
    with app.app_context():
        from app.models import Domains, WhoisService
        from app import db
        from datetime import datetime
        import pytz
        print("Testing update")
        who_is_service = WhoisService()
        domains = Domains.query.all()
        for domain in domains:
            sweden_timezone = pytz.timezone('Europe/Stockholm')
            current_date = datetime.now(sweden_timezone)
            response = who_is_service.query_domain(domain.name)
            result2 = response['response1']['result']
            available = response['response2']['result']
            registrar = "" if result2 == 'not found' else result2.get('registrar')
            creation_date = "" if result2 == 'not found' else result2.get('creation_date')
            updated_date = "" if result2 == 'not found' or result2.get('updated_date') is None else result2.get('updated_date')
            transfer_date = "" if result2 == 'not found' or result2.get('transfer_date') is None else result2.get('transfer_date')
            expiration_date = "" if result2 == 'not found' else result2.get('expiration_date')
            name_servers = "" if result2 == 'not found' else result2.get('name_servers')
            last_updated = str(current_date)
            if name_servers  != "": 
                name_servers = ' '.join(name_servers)
            else:
                name_servers = ""
            # Update the domain attributes
            domain.available = available
            domain.registrar = registrar
            domain.creation_date = creation_date[:10]
            domain.updated_date = updated_date[:10]
            domain.transfer_date = transfer_date[:10]
            domain.expiration_date = expiration_date[:10]
            domain.name_servers = name_servers
            domain.last_updated = last_updated[:19]
            
        db.session.commit()
def send_email(app):
    with app.app_context():
        from app.models import Domains, DomainExpiration
        print("Testing send_email")
        de = DomainExpiration()
        domains = Domains.query.all()
        sweden_timezone = pytz.timezone('Europe/Stockholm')
        current_date = datetime.now(sweden_timezone).date()
        for domain in domains:
            output = f"Testing domain {domain.name}"
            print(output)
            send_available_email = False
            try:
                month_before = de.expiration_before_date(domain.expiration_date, 30)
                week_before = de.expiration_before_date(domain.expiration_date, 7)
                send_available_email = False
            except ValueError:
                send_available_email = True
                print("Error: The input string does not match the specified format.")
            if current_date == month_before or current_date == week_before:
                # Before this we need to update with the api
                subject = f"<h1>Domain: {domain.name}</h1>"
                msg = Message('Domains', recipients=['olle_norstrom@live.se'])
                html = subject
                body = ""
                html += f"<p>Name: {domain.name}<br>Available: {domain.available}<br>Registrar: {domain.registrar}<br>Creation date: {domain.creation_date}<br>Updated date: {domain.updated_date}<br>Expiration date: {domain.expiration_date}<br>Name servers: {domain.name_servers}<br></p>"    
                msg.body = body
                msg.html = html
                mail.send(msg)
            if send_available_email:
                subject = f"<h1>Domain: {domain.name}</h1>"
                msg = Message('Domains', recipients=['olle_norstrom@live.se'])
                html = subject
                body = ""
                html += f"<p>Name: {domain.name}<br>Available: {domain.available}</p>"    
                msg.body = body
                msg.html = html
                mail.send(msg)