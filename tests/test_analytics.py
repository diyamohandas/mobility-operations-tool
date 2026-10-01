from services.data_loader import DataLoader
from services.data_index import DataIndex
from services.validation_service import DataValidator
from services.driver_analyzer import DriverAnalyzer
from services.trip_analyzer import TripAnalyzer
from services.zone_analyzer import ZoneAnalyzer
from services.utilization_analyzer import UtilizationAnalyzer
from services.peak_analyzer import PeakAnalyzer
from services.anomaly_detector import AnomalyDetector


def create_data_index():
    loader = DataLoader()

    drivers = loader.load_drivers(
        "data/drivers.csv"
    )

    trips = loader.load_trips(
        "data/trips.csv"
    )

    activities = loader.load_activities(
        "data/driver_activity.csv"
    )

    return DataIndex(
        drivers=drivers,
        trips=trips,
        activities=activities
    )


def test_driver_index():
    index = create_data_index()

    driver = index.get_driver("D101")

    assert driver is not None
    assert driver.driver_name == "Arun"


def test_trip_index():
    index = create_data_index()

    trip = index.get_trip("T1001")

    assert trip is not None
    assert trip.driver_id == "D101"


def test_driver_trip_index():
    index = create_data_index()

    trips = index.get_driver_trips("D101")

    assert len(trips) == 3


def test_zone_trip_index():
    index = create_data_index()

    trips = index.get_zone_trips("Koramangala")

    assert len(trips) == 3


def test_city_trip_index():
    index = create_data_index()

    trips = index.get_city_trips("Bangalore")

    assert len(trips) == 8


def test_driver_activity_index():
    index = create_data_index()

    activities = index.get_driver_activities("D101")

    assert len(activities) == 5


def test_complete_data_layer():
    loader = DataLoader()
    validator = DataValidator()

    validation_results = validator.validate_all(
        "data/drivers.csv",
        "data/trips.csv",
        "data/driver_activity.csv"
    )

    assert validation_results["drivers"][0] is True
    assert validation_results["trips"][0] is True
    assert validation_results["activities"][0] is True

    drivers = loader.load_drivers(
        "data/drivers.csv"
    )

    trips = loader.load_trips(
        "data/trips.csv"
    )

    activities = loader.load_activities(
        "data/driver_activity.csv"
    )

    index = DataIndex(
        drivers=drivers,
        trips=trips,
        activities=activities
    )

    assert len(index.driver_by_id) == 8
    assert len(index.trip_by_id) == 15
    assert len(index.activities_by_driver) == 7


def create_driver_analyzer():
    loader = DataLoader()

    drivers = loader.load_drivers(
        "data/drivers.csv"
    )

    trips = loader.load_trips(
        "data/trips.csv"
    )

    return DriverAnalyzer(
        drivers,
        trips
    )


def test_total_drivers():
    analyzer = create_driver_analyzer()

    assert analyzer.total_drivers() == 8


def test_active_drivers():
    analyzer = create_driver_analyzer()

    active = analyzer.active_drivers()

    assert len(active) == 6


def test_driver_trip_counts():
    analyzer = create_driver_analyzer()

    counts = analyzer.driver_trip_counts()

    assert counts["D101"] == 3
    assert counts["D102"] == 3


def test_completed_trip_counts():
    analyzer = create_driver_analyzer()

    counts = analyzer.completed_trip_counts()

    assert counts["D101"] == 3
    assert counts.get("D105", 0) == 0
    assert counts.get("D107", 0) == 0


def test_driver_revenue():
    analyzer = create_driver_analyzer()

    revenue = analyzer.driver_revenue()

    assert revenue["D101"] == 910
    assert revenue["D102"] == 920


def test_top_drivers_by_trips():
    analyzer = create_driver_analyzer()

    top_drivers = analyzer.top_drivers_by_trips(3)

    assert len(top_drivers) == 3
    assert (
        top_drivers[0][1]
        >= top_drivers[1][1]
    )


def test_top_drivers_by_revenue():
    analyzer = create_driver_analyzer()

    top_drivers = analyzer.top_drivers_by_revenue(3)

    assert len(top_drivers) == 3
    assert (
        top_drivers[0][1]
        >= top_drivers[1][1]
    )


def test_driver_summary():
    analyzer = create_driver_analyzer()

    summary = analyzer.driver_summary("D101")

    assert summary["driver_id"] == "D101"
    assert summary["total_trips"] == 3
    assert summary["completed_trips"] == 3
    assert summary["revenue"] == 910


def test_driver_summary_invalid_driver():
    analyzer = create_driver_analyzer()

    summary = analyzer.driver_summary("D999")

    assert summary is None


def create_trip_analyzer():
    loader = DataLoader()

    trips = loader.load_trips(
        "data/trips.csv"
    )

    return TripAnalyzer(trips)


def test_total_trips():
    analyzer = create_trip_analyzer()

    assert analyzer.total_trips() == 15


def test_completed_trip_count():
    analyzer = create_trip_analyzer()

    assert analyzer.completed_trip_count() == 12


def test_cancelled_trip_count():
    analyzer = create_trip_analyzer()

    assert analyzer.cancelled_trip_count() == 3


def test_completion_rate():
    analyzer = create_trip_analyzer()

    assert round(
        analyzer.completion_rate(),
        2
    ) == 80.00


def test_cancellation_rate():
    analyzer = create_trip_analyzer()

    assert round(
        analyzer.cancellation_rate(),
        2
    ) == 20.00


def test_total_revenue():
    analyzer = create_trip_analyzer()

    assert analyzer.total_revenue() == 3425


def test_average_fare():
    analyzer = create_trip_analyzer()

    assert round(
        analyzer.average_fare(),
        2
    ) == 285.42


def test_total_distance():
    analyzer = create_trip_analyzer()

    assert round(
        analyzer.total_distance(),
        2
    ) == 109.0


def test_cancellation_reasons():
    analyzer = create_trip_analyzer()

    reasons = analyzer.cancellation_reasons()

    assert reasons["Rider Cancelled"] == 1
    assert reasons["Driver Cancelled"] == 2


def test_trips_by_city():
    analyzer = create_trip_analyzer()

    city_counts = analyzer.trips_by_city()

    assert city_counts["Bangalore"] == 8
    assert city_counts["Chennai"] == 3
    assert city_counts["Hyderabad"] == 4


def test_revenue_by_city():
    analyzer = create_trip_analyzer()

    revenue = analyzer.revenue_by_city()

    assert revenue["Bangalore"] == 2280
    assert revenue["Chennai"] == 565
    assert revenue["Hyderabad"] == 580


def test_top_cities_by_trips():
    analyzer = create_trip_analyzer()

    top_cities = analyzer.top_cities_by_trips(2)

    assert len(top_cities) == 2
    assert top_cities[0] == (
        "Bangalore",
        8
    )


def test_trip_summary():
    analyzer = create_trip_analyzer()

    summary = analyzer.trip_summary()

    assert summary["total_trips"] == 15
    assert summary["completed_trips"] == 12
    assert summary["cancelled_trips"] == 3
    assert summary["total_revenue"] == 3425


def create_zone_analyzer():
    loader = DataLoader()

    trips = loader.load_trips(
        "data/trips.csv"
    )

    return ZoneAnalyzer(trips)


def test_total_zones():
    analyzer = create_zone_analyzer()

    assert analyzer.total_zones() == 8


def test_trip_count_by_zone():
    analyzer = create_zone_analyzer()

    counts = analyzer.trip_count_by_zone()

    assert counts["Koramangala"] == 3
    assert counts["Whitefield"] == 2


def test_completed_trip_count_by_zone():
    analyzer = create_zone_analyzer()

    counts = analyzer.completed_trip_count_by_zone()

    assert counts["Koramangala"] == 3
    assert counts["Adyar"] == 1


def test_cancelled_trip_count_by_zone():
    analyzer = create_zone_analyzer()

    counts = analyzer.cancelled_trip_count_by_zone()

    assert counts["Adyar"] == 1
    assert counts["Hitech City"] == 1


def test_revenue_by_zone():
    analyzer = create_zone_analyzer()

    revenue = analyzer.revenue_by_zone()

    assert revenue["Koramangala"] == 750
    assert revenue["Whitefield"] == 710


def test_cancellation_rate_by_zone():
    analyzer = create_zone_analyzer()

    rates = analyzer.cancellation_rate_by_zone()

    assert rates["Adyar"] == 50.0
    assert rates["Hitech City"] == 50.0


def test_top_zones_by_demand():
    analyzer = create_zone_analyzer()

    top_zones = analyzer.top_zones_by_demand(3)

    assert len(top_zones) == 3
    assert top_zones[0][0] == "Koramangala"
    assert top_zones[0][1] == 3


def test_top_zones_by_revenue():
    analyzer = create_zone_analyzer()

    top_zones = analyzer.top_zones_by_revenue(3)

    assert len(top_zones) == 3
    assert top_zones[0][0] == "Koramangala"


def test_zone_summary():
    analyzer = create_zone_analyzer()

    summary = analyzer.zone_summary(
        "Koramangala"
    )

    assert summary["zone"] == "Koramangala"
    assert summary["total_trips"] == 3
    assert summary["completed_trips"] == 3
    assert summary["cancelled_trips"] == 0
    assert summary["revenue"] == 750


def test_invalid_zone_summary():
    analyzer = create_zone_analyzer()

    summary = analyzer.zone_summary(
        "Unknown Zone"
    )

    assert summary is None


def create_utilization_analyzer():
    loader = DataLoader()

    activities = loader.load_activities(
        "data/driver_activity.csv"
    )

    trips = loader.load_trips(
        "data/trips.csv"
    )

    return UtilizationAnalyzer(
        activities,
        trips
    )


def test_online_hours():
    analyzer = create_utilization_analyzer()

    hours = analyzer.online_hours("D101")

    assert hours == 10.0


def test_trip_hours():
    analyzer = create_utilization_analyzer()

    hours = analyzer.trip_hours("D101")

    assert round(hours, 2) == 1.75


def test_idle_hours():
    analyzer = create_utilization_analyzer()

    hours = analyzer.idle_hours("D101")

    assert round(hours, 2) == 8.25


def test_utilization_rate():
    analyzer = create_utilization_analyzer()

    rate = analyzer.utilization_rate("D101")

    assert round(rate, 2) == 17.50


def test_driver_utilization():
    analyzer = create_utilization_analyzer()

    result = analyzer.driver_utilization()

    assert "D101" in result

    assert "online_hours" in result["D101"]
    assert "trip_hours" in result["D101"]
    assert "idle_hours" in result["D101"]
    assert "utilization_rate" in result["D101"]


def test_most_utilized_drivers():
    analyzer = create_utilization_analyzer()

    result = analyzer.most_utilized_drivers(3)

    assert len(result) == 3

    assert (
        result[0][1]["utilization_rate"]
        >= result[1][1]["utilization_rate"]
    )


def test_highest_idle_drivers():
    analyzer = create_utilization_analyzer()

    result = analyzer.highest_idle_drivers(3)

    assert len(result) == 3

    assert (
        result[0][1]["idle_hours"]
        >= result[1][1]["idle_hours"]
    )


def create_peak_analyzer():
    loader = DataLoader()

    trips = loader.load_trips(
        "data/trips.csv"
    )

    return PeakAnalyzer(trips)


def test_demand_by_hour():
    analyzer = create_peak_analyzer()

    demand = analyzer.demand_by_hour()

    assert demand[8] == 2
    assert demand[10] == 2
    assert demand[14] == 1


def test_completed_demand_by_hour():
    analyzer = create_peak_analyzer()

    demand = analyzer.completed_demand_by_hour()

    assert demand[8] == 2
    assert demand[10] == 2


def test_cancelled_demand_by_hour():
    analyzer = create_peak_analyzer()

    demand = analyzer.cancelled_demand_by_hour()

    assert demand[11] == 1
    assert demand[13] == 1


def test_peak_demand_hour():
    analyzer = create_peak_analyzer()

    peak = analyzer.peak_demand_hour()

    assert peak[1] == 2


def test_top_demand_hours():
    analyzer = create_peak_analyzer()

    result = analyzer.top_demand_hours(3)

    assert len(result) == 3

    assert (
        result[0][1]
        >= result[1][1]
    )


def test_cancellation_rate_by_hour():
    analyzer = create_peak_analyzer()

    rates = analyzer.cancellation_rate_by_hour()

    assert rates[11] == 100.0
    assert rates[13] == 100.0


def test_peak_cancellation_hour():
    analyzer = create_peak_analyzer()

    peak = analyzer.peak_cancellation_hour()

    assert peak[1] == 100.0


def test_peak_cancellation_reasons():
    analyzer = create_peak_analyzer()

    reasons = analyzer.cancellation_reasons()

    assert reasons["Rider Cancelled"] == 1
    assert reasons["Driver Cancelled"] == 2


def test_highest_cancellation_reason():
    analyzer = create_peak_analyzer()

    result = analyzer.highest_cancellation_reason()

    assert result[1] == 2


def test_cancellation_summary():
    analyzer = create_peak_analyzer()

    summary = analyzer.cancellation_summary()

    assert summary["total_trips"] == 15
    assert summary["cancelled_trips"] == 3
    assert summary["cancellation_rate"] == 20.0


def create_anomaly_detector():
    loader = DataLoader()

    trips = loader.load_trips(
        "data/trips.csv"
    )

    drivers = loader.load_drivers(
        "data/drivers.csv"
    )

    return AnomalyDetector(
        trips,
        drivers
    )


def test_high_fare_trips():
    detector = create_anomaly_detector()

    result = detector.high_fare_trips(400)

    assert len(result) == 1
    assert result[0].trip_id == "T1004"


def test_long_distance_trips():
    detector = create_anomaly_detector()

    result = detector.long_distance_trips(10)

    assert len(result) == 3

    trip_ids = {
        trip.trip_id
        for trip in result
    }

    assert trip_ids == {
        "T1002",
        "T1004",
        "T1007"
    }


def test_long_duration_trips():
    detector = create_anomaly_detector()

    result = detector.long_duration_trips(40)

    assert len(result) == 1
    assert result[0].trip_id == "T1004"


def test_driver_cancellation_anomalies():
    detector = create_anomaly_detector()

    result = detector.driver_cancellation_anomalies(1)

    assert "D107" in result
    assert result["D107"] == 2


def test_zone_cancellation_anomalies():
    detector = create_anomaly_detector()

    result = detector.zone_cancellation_anomalies(50)

    assert "Adyar" in result
    assert "Hitech City" in result


def test_detect_all():
    detector = create_anomaly_detector()

    result = detector.detect_all()

    assert "high_fare_trips" in result
    assert "long_distance_trips" in result
    assert "long_duration_trips" in result
    assert "driver_cancellation_anomalies" in result
    assert "zone_cancellation_anomalies" in result