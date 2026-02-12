from flask import Blueprint, render_template
from routes.devices import devices_store

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/', methods=['GET'])
def dashboard():
    """Main dashboard page - provide available device list to template"""
    # Pass device IDs to the template so the dashboard can select between them
    devices = list(devices_store.keys())
    return render_template('dashboard.html', devices=devices)
