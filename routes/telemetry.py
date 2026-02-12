from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, TelemetryData

telemetry_bp = Blueprint('telemetry', __name__, url_prefix='/telemetry')

@telemetry_bp.route('/', methods=['GET', 'POST'], strict_slashes=False)
def receive_telemetry():
    """Receive telemetry data from IoT devices"""
    if request.method == 'GET':
        return jsonify({'status': 'success', 'message': 'Telemetry endpoint is ready. Send POST request with data.'}), 200

    try:
        data = request.get_json()
        if data is None:
            # Try form data fallback
            data = request.form.to_dict() or {}
        # Normalize keys
        for k in list(data.keys()):
            if isinstance(data[k], str) and data[k].isdigit():
                # convert pure-digit strings to int
                data[k] = int(data[k])
        
        # Validate required fields
        if not data.get('device_id'):
            return jsonify({'status': 'error', 'message': 'device_id required'}), 400
        
        # Add timestamp if not provided
        if 'timestamp' not in data:
            data['timestamp'] = datetime.utcnow().isoformat()

        # Coerce numeric fields when possible
        for fld in ('temperature', 'humidity', 'battery'):
            if fld in data:
                try:
                    data[fld] = float(data[fld]) if ('.' in str(data[fld])) else int(data[fld])
                except Exception:
                    pass

        # Store data
        new_entry = TelemetryData(
            device_id=data['device_id'],
            timestamp=datetime.fromisoformat(data['timestamp']) if isinstance(data['timestamp'], str) else data['timestamp'],
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            battery=data.get('battery')
        )
        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Telemetry data received'}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@telemetry_bp.route('/<device_id>', methods=['GET'])
def get_device_telemetry(device_id):
    """Get telemetry data for a specific device"""
    records = TelemetryData.query.filter_by(device_id=device_id).all()
    return jsonify({'device_id': device_id, 'telemetry': [r.to_dict() for r in records]}), 200

@telemetry_bp.route('/all', methods=['GET'])
def get_all_telemetry():
    """Get all telemetry data"""
    records = TelemetryData.query.all()
    return jsonify({'total': len(records), 'telemetry': [r.to_dict() for r in records]}), 200

@telemetry_bp.route('/id/<int:id>', methods=['PUT'])
def update_telemetry(id):
    """Update a specific telemetry record by ID"""
    record = TelemetryData.query.get(id)
    if not record:
        return jsonify({'status': 'error', 'message': 'Record not found'}), 404

    data = request.get_json() or {}
    
    if 'temperature' in data:
        record.temperature = data['temperature']
    if 'humidity' in data:
        record.humidity = data['humidity']
    if 'battery' in data:
        record.battery = data['battery']
        
    try:
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Record updated', 'data': record.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@telemetry_bp.route('/id/<int:id>', methods=['DELETE'])
def delete_telemetry(id):
    """Delete a specific telemetry record by ID"""
    record = TelemetryData.query.get(id)
    if not record:
        return jsonify({'status': 'error', 'message': 'Record not found'}), 404

    try:
        db.session.delete(record)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Record deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400
