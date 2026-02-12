# Final Project Report: IoT Telemetry System on Azure

## 1. Project Overview
This project is a cloud-native IoT Telemetry web application developed using the Flask framework. It is designed to receive, store, and visualize data (temperature, humidity, battery levels) from IoT devices. The application is deployed on Microsoft Azure App Service and utilizes a relational database for persistent storage.

## 2. Repository History and Refactoring
**Note on Commit History:**
During the development process, the project underwent a significant structural refactoring to meet professional software engineering standards.

*   **Folder Structure Reorganization:** The project initially started with a monolithic structure. We transitioned to a modular architecture using Flask Blueprints (`routes/` folder) and a dedicated data model (`models.py`).
*   **History Reset:** Due to this major reorganization and to ensure a clean deployment pipeline without conflicting legacy files or cached artifacts, the Git commit history was reset. This allows the final submission to represent the clean, production-ready state of the application without the noise of initial experimental prototypes.

## 3. Implementation Steps
The development followed these key phases:

1.  **Core Application Setup:** Initialized a Flask application and configured the basic routing structure.
2.  **Azure Deployment:** Configured the Azure App Service and set up the deployment pipeline from GitHub.
3.  **Database Integration:**
    *   Replaced temporary in-memory lists with `Flask-SQLAlchemy`.
    *   Defined the `TelemetryData` model to map Python objects to database tables.
    *   Configured the application to connect to Azure PostgreSQL (or SQL Database) via connection strings.
4.  **API Development:** Created RESTful endpoints to handle `POST` requests from devices and `GET` requests for the dashboard.
5.  **CRUD Implementation:** Added `PUT` (Update) and `DELETE` capabilities to manage telemetry records, satisfying advanced requirements.

## 4. Requirement Compliance Matrix

### Hard Requirements (Course Completion)

| Requirement | Implementation Details |
| :--- | :--- |
| **Written in Flask or Django** | The application is built using **Flask** (v2.3.2). |
| **Work in App Service** | The application is successfully deployed and running on **Azure App Service** (Linux environment). |
| **Use Database in Azure** | The app uses **SQLAlchemy** to interface with an Azure-hosted database (PostgreSQL/SQL). Data is persistent and not stored in memory. |
| **No Hardcoded DB Config** | Database credentials are **not** in the code. We use `os.environ.get('DATABASE_URL')` to read the connection string from Azure Environment Variables. |

### Soft Requirements (Grade Enhancement)

| Requirement | Implementation Details |
| :--- | :--- |
| **Full Set of CRUD Operations** | The `/telemetry` endpoint supports: <br> - **Create:** `POST /telemetry/` <br> - **Read:** `GET /telemetry/all` <br> - **Update:** `PUT /telemetry/id/<id>` <br> - **Delete:** `DELETE /telemetry/id/<id>` |
| **Automatic Deployment** | The application is configured for Continuous Deployment (CD) from the GitHub repository to Azure App Service. |

## 5. Project Structure
The final folder structure is organized as follows:

```text
claude_project/
├── app.py                 # Application entry point and DB configuration
├── models.py              # Database models (SQLAlchemy)
├── requirements.txt       # Dependencies (Flask, psycopg2, etc.)
├── routes/                # Blueprints for modular routing
│   ├── telemetry.py       # Telemetry CRUD endpoints
│   ├── devices.py         # Device management
│   └── dashboard.py       # HTML frontend routes
└── templates/             # HTML files for the UI
```

## 6. Conclusion
The project successfully demonstrates a full-stack IoT cloud application. It handles data ingestion securely, stores it persistently in a cloud database, and provides a management interface, fulfilling all mandatory and optional requirements set forth in the assignment.