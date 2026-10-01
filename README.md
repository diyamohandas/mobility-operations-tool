# Mobility Operations Intelligence Tool

A Flask-based mobility operations analytics platform designed to help operations teams analyze drivers, trips, zones, utilization, cancellations, and operational anomalies through a web-based dashboard.

## Project Overview

The **Mobility Operations Intelligence Tool** converts raw mobility operations data into actionable operational analytics.

The application processes:
- Driver information
- Trip information
- Driver activity information

It provides dedicated pages for:
- Dashboard
- Drivers
- Trips
- Zones
- Driver Utilization
- Cancellations
- Operational Anomalies
- Operational Insights

## Key Features

### Driver Analytics
- Total driver count
- Active and inactive drivers
- Total trips by driver
- Completed trips by driver
- Driver revenue
- Average driver rating
- Top drivers by completed trips
- Top drivers by revenue
- Individual driver summaries

### Trip Analytics
- Total trips
- Completed trips
- Cancelled trips
- Total revenue
- Average fare
- Total distance
- Revenue by city
- Cancellation reasons
- Trip summaries

### Zone Analytics
- Total number of zones
- Trip count by zone
- Revenue by zone
- Top zones by demand
- Top zones by revenue
- Zone-level summaries

### Driver Utilization
- Online hours
- Trip hours
- Idle hours
- Driver utilization rate
- Driver activity analysis

### Cancellation Analytics
- Cancellation counts
- Cancellation reasons
- Driver cancellation patterns
- Rider cancellation patterns

### Operational Anomaly Detection
- High fare trips
- Long distance trips
- Long duration trips
- Driver cancellation anomalies

### Operational Insights
The Insights Engine combines driver, trip, zone, utilization, peak-demand, and anomaly analytics to provide a consolidated operational view.

### CSV Data Upload
The application supports uploading:
- `drivers.csv`
- `trips.csv`
- `driver_activity.csv`

Uploaded files replace the corresponding datasets in the `data/` directory.

## Technology Stack

- Python 3.12
- Flask
- pytest
- HTML5
- CSS3
- Jinja2
- CSV data processing

## Project Architecture

```text
CSV Data
   |
   v
Data Loader
   |
   v
Data Models
   |
   v
Data Index
   |
   v
Analytics Services
   |
   +----------------------+
   |                      |
   v                      v
Driver Analyzer       Trip Analyzer
   |                      |
   v                      v
Zone Analyzer        Utilization Analyzer
   |                      |
   +----------+-----------+
              |
              v
       Peak Analyzer
              |
              v
      Anomaly Detector
              |
              v
       Insights Engine
              |
              v
        Flask Application
              |
              v
        Web Dashboard
```

## Project Structure

```text
mobility-operations-tool/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── drivers.csv
│   ├── trips.csv
│   └── driver_activity.csv
│
├── models/
│
├── services/
│   ├── anomaly_detector.py
│   ├── data_index.py
│   ├── data_loader.py
│   ├── driver_analyzer.py
│   ├── insights_engine.py
│   ├── peak_analyzer.py
│   ├── trip_analyzer.py
│   ├── utilization_analyzer.py
│   ├── validation_service.py
│   └── zone_analyzer.py
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── driver.html
│   ├── zone.html
│   ├── utilization.html
│   ├── cancellations.html
│   └── anomalies.html
│
├── tests/
│   ├── test_analytics.py
│   ├── test_models.py
│   └── test_validation.py
│
└── utils/
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/diyamohandas/mobility-operations-tool.git
```

### 2. Navigate to the Project

```bash
cd mobility-operations-tool
```

### 3. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 4. Activate the Virtual Environment

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Application Routes

| Page | Route | Description |
|---|---|---|
| Home | `/` | Application landing page |
| Dashboard | `/dashboard` | Overall operational overview |
| Drivers | `/drivers` | Driver analytics |
| Trips | `/trips` | Trip analytics |
| Zones | `/zones` | Zone analytics |
| Utilization | `/utilization` | Driver utilization |
| Cancellations | `/cancellations` | Cancellation analytics |
| Anomalies | `/anomalies` | Operational anomaly detection |

## Testing

Run the complete test suite:

```bash
pytest
```

The completed project currently passes:

```text
82 passed
```

The tests cover:
- Models
- Validation
- Driver analytics
- Trip analytics
- Zone analytics
- Utilization analytics
- Peak analytics
- Anomaly detection
- Operational insights

## Operational Workflow

```text
1. Load CSV files
        |
        v
2. Validate and parse data
        |
        v
3. Create domain models
        |
        v
4. Build data indexes
        |
        v
5. Run analytics
        |
        v
6. Detect operational anomalies
        |
        v
7. Generate operational insights
        |
        v
8. Display results through Flask UI
```

## Example Operational Questions

### Driver Performance
- Which drivers completed the most trips?
- Which drivers generated the most revenue?
- Which drivers are active?
- What is the average driver rating?

### Trip Performance
- What is the total revenue?
- What is the average fare?
- How many trips were cancelled?
- What are the major cancellation reasons?

### Zone Performance
- Which zones have the highest demand?
- Which zones generate the most revenue?
- How many trips originate from a particular zone?

### Utilization
- How many hours are drivers online?
- How much time is spent on trips?
- How much time is idle?
- Which drivers have lower utilization?

### Anomaly Detection
- Are there unusually expensive trips?
- Are there unusually long-distance trips?
- Are there unusually long-duration trips?
- Are particular drivers showing elevated cancellation activity?

## Future Enhancements

- Interactive charts and visualizations
- Date-range filtering
- City-level filtering
- Driver search
- Zone search
- Export analytics to CSV/Excel
- Database integration
- REST API endpoints
- Authentication and role-based access
- Real-time mobility data integration
- Automated anomaly alerts
- Production deployment using Gunicorn
- Cloud deployment

## Repository

GitHub:

https://github.com/diyamohandas/mobility-operations-tool

## Author

**Diya Mohandas N T**

## License

This project was developed for educational and project-assignment purposes.
