from flask import Flask, render_template
import os

app = Flask(__name__)

from routes.devices import devices_bp, devices_store
from routes.telemetry import telemetry_bp, telemetry_store
from routes.dashboard import dashboard_bp

app.register_blueprint(devices_bp)
app.register_blueprint(telemetry_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def home():
    device_count = len(devices_store)
    telemetry_count = len(telemetry_store)
    return render_template('home.html', device_count=device_count, telemetry_count=telemetry_count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
