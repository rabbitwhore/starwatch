from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Domains, WhoisService, DomainExpiration
from app import db
import json
bp = Blueprint('main', __name__)
from datetime import datetime
import pytz

@bp.route('/', methods=['GET', 'POST'])
def index():
    sweden_timezone = pytz.timezone('Europe/Stockholm')
    current_date = datetime.now(sweden_timezone)
    already_exists = False
    if request.method == 'POST':
        name = request.form.get('name')
        
        de = DomainExpiration()
        if '.' in name:
            domain, tld = de.extract_domain_and_tld(name)
            domain = domain.capitalize()
        else:
            already_exists = True
            domains = Domains.query.all()
            return render_template('index.html', domains=domains, already_exists=already_exists)
        name = f"{domain}.{tld}"
        existing_domain = Domains.query.filter_by(name=name).first()
        if existing_domain or tld == None:
            already_exists = True
            domains = Domains.query.all()
            return render_template('index.html', domains=domains, already_exists=already_exists)
        
        # Get Who is information
        whois_service = WhoisService()
        response = whois_service.query_domain(name)
        # Create a new domain
        result2 = response['response1']['result']
        available = response['response2']['result']
        registrar = "" if result2 == 'not found' else result2.get('registrar')
        creation_date = "" if result2 == 'not found' else result2.get('creation_date')
        updated_date = "" if result2 == 'not found' or result2.get('updated_date') == None else result2.get('updated_date')
        transfer_date = "" if result2 == 'not found' or  result2.get('transfer_date') == None else result2.get('transfer_date')
        expiration_date = "" if result2 == 'not found' else result2.get('expiration_date')
        name_servers = "" if result2 == 'not found' else result2.get('name_servers')
        last_updated = str(current_date)
        
        new_domain = Domains(name=name, available=available, registrar=registrar, creation_date=creation_date[:10], updated_date=updated_date[:10], transfer_date=transfer_date[:10], expiration_date=expiration_date[:10], name_servers=name_servers, last_updated=last_updated[:19])
        db.session.add(new_domain)
        db.session.commit()
        
        return redirect(url_for('main.index'))

    # Get all domains from the database
    domains = Domains.query.all()
    return render_template('index.html', domains=domains, already_exists=already_exists)
@bp.route('/remove_domain/<int:domain_id>', methods=['POST'])
def remove_domain(domain_id):
    domain = Domains.query.get_or_404(domain_id)
    db.session.delete(domain)
    db.session.commit()

    return redirect(url_for('main.index'))

@bp.route('/update_domain/<int:domain_id>', methods=['POST'])
def update_domain(domain_id):
    sweden_timezone = pytz.timezone('Europe/Stockholm')
    current_date = datetime.now(sweden_timezone)
    domain = Domains.query.filter_by(id=domain_id).first()
    whois_service = WhoisService()
    response = whois_service.query_domain(domain.name)
    # Create or update the domain
    print(response)
    result2 = response['response1']['result']
    available = response['response2']['result']
    registrar = "" if result2 == 'not found' else result2.get('registrar')
    creation_date = "" if result2 == 'not found' else result2.get('creation_date')
    updated_date = "" if result2 == 'not found' or result2.get('updated_date') is None else result2.get('updated_date')
    transfer_date = "" if result2 == 'not found' or result2.get('transfer_date') is None else result2.get('transfer_date')
    expiration_date = "" if result2 == 'not found' else result2.get('expiration_date')
    name_servers = "" if result2 == 'not found' else result2.get('name_servers')
    if name_servers  != "": 
        name_servers = ' '.join(name_servers)
    else:
        name_servers = ""
    last_updated = str(current_date)
    if domain:
    # Update the existing domain
        domain.available = available
        domain.registrar = registrar
        domain.creation_date = creation_date[:10]
        domain.updated_date = updated_date[:10]
        domain.transfer_date = transfer_date[:10]
        domain.expiration_date = expiration_date[:10]
        domain.name_servers = name_servers
        domain.last_updated = last_updated[:19]
    db.session.commit()
    return redirect(url_for('main.index'))