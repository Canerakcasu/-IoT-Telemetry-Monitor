from flask import Blueprint, render_template, request, jsonify

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')

# Temporary storage (for testing before database integration)
devices_store = {
    "sensor001": {
        "device_id": "sensor001",
        "name": "Temperature Sensor - Room 1",
        "location": "Server Room"
    }
}

@devices_bp.route('/', methods=['GET'])
def list_devices():
    """List all devices"""
    return render_template('devices.html', devices=devices_store)

@devices_bp.route('/add', methods=['GET', 'POST'])
def add_device():
    """Add a new device"""
    if request.method == 'POST':
        data = request.form
        device_id = data.get('device_id')
        devices_store[device_id] = {
            'device_id': device_id,
            'name': data.get('name'),
            'location': data.get('location')
        }
        return jsonify({'status': 'success', 'message': 'Device added'}), 201
    
    return render_template('add_device.html')

@devices_bp.route('/<device_id>/edit', methods=['GET', 'POST'])
def edit_device(device_id):
    """Edit a device"""
    if device_id not in devices_store:
        return jsonify({'status': 'error', 'message': 'Device not found'}), 404
    
    if request.method == 'POST':
        data = request.form
        devices_store[device_id].update({
            'name': data.get('name'),
            'location': data.get('location')
        })
        return jsonify({'status': 'success', 'message': 'Device updated'}), 200
    
    return render_template('edit_device.html', device=devices_store[device_id])

@devices_bp.route('/<device_id>/delete', methods=['DELETE'])
def delete_device(device_id):
    """Delete a device"""
    if device_id not in devices_store:
        return jsonify({'status': 'error', 'message': 'Device not found'}), 404
    
    del devices_store[device_id]
    return jsonify({'status': 'success', 'message': 'Device deleted'}), 200
