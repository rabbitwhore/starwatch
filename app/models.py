from app import db
import requests
import json
from datetime import datetime, timedelta
import re
class Domains(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    available = db.Column(db.String(100), nullable=True)
    registrar = db.Column(db.String(100), nullable=True)
    creation_date = db.Column(db.String(100), nullable=True)
    updated_date = db.Column(db.String(100), nullable=True)
    transfer_date = db.Column(db.String(100), nullable=True)
    expiration_date = db.Column(db.String(100), nullable=True)
    name_servers = db.Column(db.String(255), nullable=True)
    last_updated = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f"<Domains {self.name}>"

    def __init__(self, name, available, registrar, creation_date, updated_date, transfer_date, expiration_date, name_servers, last_updated):
        self.name = name
        self.available = available
        self.registrar = registrar
        self.creation_date = creation_date
        self.updated_date = updated_date
        self.transfer_date = transfer_date
        self.expiration_date = expiration_date
        if name_servers  != "":
            self.name_servers = ' '.join(name_servers)
        else:
            self.name_servers = ""
        self.last_updated = last_updated
class WhoisService:
    def query_domain(self, domain):
        url1 = f"https://api.apilayer.com/whois/query?domain={domain}"
        url2 = f"https://api.apilayer.com/whois/check?domain={domain}"
        payload = {}
        headers= {
        "apikey": "dHEWr9AC5rAPNqdUl0CK41Nd1hauUiKE"
        }
        response1 = requests.request("GET", url1, headers=headers, data = payload)
        response2 = requests.request("GET", url2, headers=headers, data = payload)
        status_code = response1.status_code
        data = {}
        data['response1'] =  json.loads(response1.text)
        data['response2'] =  json.loads(response2.text) 
        return data
class DomainExpiration:
    def expiration_before_date(self, expiration_date, days_before):
        date_format = "%Y-%m-%d"
        input_date = datetime.strptime(expiration_date, date_format).date()

        one_month_before = input_date - timedelta(days=days_before)
        formatted_date = one_month_before.strftime(date_format)
        print(f"One month before {expiration_date} is {formatted_date}.")
        return formatted_date
    def extract_domain_and_tld(self, url):
        # Regular expression to match the domain name and top-level domain (TLD)
        pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+)\.([a-zA-Z0-9.-]+)\/?'

        # Extract the domain name and TLD using regex
        match = re.search(pattern, url)
        if match:
            domain = match.group(1)
            tld = match.group(2)
            return domain, tld
        else:
            return None, None

