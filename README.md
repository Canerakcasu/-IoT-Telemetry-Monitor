[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=22568639)

# IoT Telemetry Monitor

Cloud-native platform for collecting, storing, and visualizing telemetry data from IoT devices.

## Technology Stack
- **Backend**: Flask
- **Database**: Azure SQL Database
- **Storage**: Azure Blob Storage
- **Deployment**: Azure App Service
- **CI/CD**: GitHub Actions

## Project Structure
```
iot-telemetry-monitor/
├── app.py
├── requirements.txt
├── .env
├── routes/
├── services/
├── models/
├── templates/
└── static/
```

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env`
3. Run locally: `python app.py`
test