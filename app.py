from flask import Flask, render_template
import os
from models import db, TelemetryData

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

from routes.devices import devices_bp, devices_store
from routes.telemetry import telemetry_bp
from routes.dashboard import dashboard_bp

app.register_blueprint(devices_bp)
app.register_blueprint(telemetry_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def home():
    device_count = len(devices_store)
    telemetry_count = TelemetryData.query.count()
    return render_template('home.html', device_count=device_count, telemetry_count=telemetry_count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
