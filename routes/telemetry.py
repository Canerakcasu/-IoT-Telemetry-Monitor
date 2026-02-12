from flask import Blueprint, request, jsonify
from datetime import datetime

telemetry_bp = Blueprint('telemetry', __name__, url_prefix='/telemetry')

# Temporary storage (for testing before database integration)
telemetry_store = []

@telemetry_bp.route('/', methods=['POST'])
def receive_telemetry():
    """Receive telemetry data from IoT devices"""
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
        telemetry_store.append(data)
        
        return jsonify({'status': 'success', 'message': 'Telemetry data received'}), 201
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@telemetry_bp.route('/<device_id>', methods=['GET'])
def get_device_telemetry(device_id):
    """Get telemetry data for a specific device"""
    device_data = [t for t in telemetry_store if t.get('device_id') == device_id]
    return jsonify({'device_id': device_id, 'telemetry': device_data}), 200

@telemetry_bp.route('/all', methods=['GET'])
def get_all_telemetry():
    """Get all telemetry data"""
    return jsonify({'total': len(telemetry_store), 'telemetry': telemetry_store}), 200
