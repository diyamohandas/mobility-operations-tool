from flask import Flask, render_template, request, redirect, url_for, flash
import os

from services.data_loader import DataLoader
from services.data_index import DataIndex
from services.driver_analyzer import DriverAnalyzer
from services.trip_analyzer import TripAnalyzer
from services.zone_analyzer import ZoneAnalyzer
from services.utilization_analyzer import UtilizationAnalyzer
from services.peak_analyzer import PeakAnalyzer
from services.anomaly_detector import AnomalyDetector
from services.insights_engine import InsightsEngine


app = Flask(__name__)
app.secret_key = "mobility-operations-secret-key"


DATA_DIR = "data"

DRIVERS_FILE = os.path.join(DATA_DIR, "drivers.csv")
TRIPS_FILE = os.path.join(DATA_DIR, "trips.csv")
ACTIVITY_FILE = os.path.join(DATA_DIR, "driver_activity.csv")


def load_application_data():
    loader = DataLoader()

    drivers = loader.load_drivers(DRIVERS_FILE)
    trips = loader.load_trips(TRIPS_FILE)
    activities = loader.load_activities(ACTIVITY_FILE)

    return drivers, trips, activities


def create_services():
    drivers, trips, activities = load_application_data()

    index = DataIndex(
        drivers=drivers,
        trips=trips,
        activities=activities
    )

    driver_analyzer = DriverAnalyzer(
        drivers,
        trips
    )

    trip_analyzer = TripAnalyzer(
        trips
    )

    zone_analyzer = ZoneAnalyzer(
        trips
    )

    utilization_analyzer = UtilizationAnalyzer(
        activities,
        trips
    )

    peak_analyzer = PeakAnalyzer(
        trips
    )

    anomaly_detector = AnomalyDetector(
        trips,
        drivers
    )

    insights_engine = InsightsEngine(
        driver_analyzer=driver_analyzer,
        trip_analyzer=trip_analyzer,
        zone_analyzer=zone_analyzer,
        utilization_analyzer=utilization_analyzer,
        peak_analyzer=peak_analyzer,
        anomaly_detector=anomaly_detector
    )

    return {
        "drivers": drivers,
        "trips": trips,
        "activities": activities,
        "index": index,
        "driver_analyzer": driver_analyzer,
        "trip_analyzer": trip_analyzer,
        "zone_analyzer": zone_analyzer,
        "utilization_analyzer": utilization_analyzer,
        "peak_analyzer": peak_analyzer,
        "anomaly_detector": anomaly_detector,
        "insights_engine": insights_engine
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    services = create_services()

    trip_summary = (
        services["trip_analyzer"].trip_summary()
    )

    driver_count = (
        services["driver_analyzer"].total_drivers()
    )

    zone_count = (
        services["zone_analyzer"].total_zones()
    )

    insights = (
        services["insights_engine"].generate_insights()
    )

    return render_template(
        "dashboard.html",
        summary=trip_summary,
        driver_count=driver_count,
        zone_count=zone_count,
        insights=insights
    )


@app.route("/drivers")
def drivers():
    services = create_services()

    analyzer = services["driver_analyzer"]

    top_drivers = analyzer.top_drivers_by_revenue(10)

    return render_template(
        "driver.html",
        drivers=top_drivers
    )


@app.route("/trips")
def trips():
    services = create_services()

    summary = (
        services["trip_analyzer"].trip_summary()
    )

    return render_template(
        "dashboard.html",
        summary=summary,
        driver_count=services[
            "driver_analyzer"
        ].total_drivers(),
        zone_count=services[
            "zone_analyzer"
        ].total_zones(),
        insights=services[
            "insights_engine"
        ].generate_insights()
    )


@app.route("/zones")
def zones():
    services = create_services()

    analyzer = services["zone_analyzer"]

    zone_data = analyzer.top_zones_by_demand(10)

    return render_template(
        "zone.html",
        zones=zone_data
    )


@app.route("/utilization")
def utilization():
    services = create_services()

    analyzer = services[
        "utilization_analyzer"
    ]

    utilization_data = (
        analyzer.driver_utilization()
    )

    return render_template(
        "utilization.html",
        utilization=utilization_data
    )


@app.route("/cancellations")
def cancellations():
    services = create_services()

    analyzer = services["trip_analyzer"]

    reasons = analyzer.cancellation_reasons()

    return render_template(
        "cancellations.html",
        reasons=reasons
    )


@app.route("/anomalies")
def anomalies():
    services = create_services()

    anomaly_data = (
        services["anomaly_detector"].detect_all()
    )

    return render_template(
        "anomalies.html",
        anomalies=anomaly_data
    )


@app.route("/upload", methods=["POST"])
def upload():
    drivers_file = request.files.get("drivers")
    trips_file = request.files.get("trips")
    activity_file = request.files.get("activity")

    if not drivers_file or not trips_file or not activity_file:
        flash(
            "Please upload all three CSV files.",
            "error"
        )
        return redirect(url_for("index"))

    os.makedirs(DATA_DIR, exist_ok=True)

    drivers_file.save(DRIVERS_FILE)
    trips_file.save(TRIPS_FILE)
    activity_file.save(ACTIVITY_FILE)

    flash(
        "Files uploaded successfully.",
        "success"
    )

    return redirect(url_for("dashboard"))


@app.errorhandler(404)
def page_not_found(error):
    return (
        render_template(
            "index.html",
            error="Page not found."
        ),
        404
    )


@app.errorhandler(500)
def internal_error(error):
    return (
        render_template(
            "index.html",
            error="An internal application error occurred."
        ),
        500
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )