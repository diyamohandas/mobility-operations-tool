from models.driver import Driver
from models.trip import Trip
from models.zone import Zone
from models.activity import DriverActivity


def test_driver_creation():
    driver = Driver(
        "D102",
        "Rahul",
        "Bangalore",
        "Sedan",
        4.7,
        "Active"
    )

    assert driver.driver_id == "D102"
    assert driver.driver_name == "Rahul"
    assert driver.rating == 4.7


def test_driver_is_active():
    driver = Driver(
        "D102",
        "Rahul",
        "Bangalore",
        "Sedan",
        4.7,
        "Active"
    )

    assert driver.is_active() is True


def test_driver_profile():
    driver = Driver(
        "D102",
        "Rahul",
        "Bangalore",
        "Sedan",
        4.7,
        "Active"
    )

    profile = driver.get_profile()

    assert profile["driver_id"] == "D102"
    assert profile["driver_name"] == "Rahul"
    assert profile["city"] == "Bangalore"


def test_trip_creation():
    trip = Trip(
        "T1001",
        "D102",
        "R501",
        "Bangalore",
        "Koramangala",
        "Indiranagar",
        "2026-09-25 08:00:00",
        "2026-09-25 08:10:00",
        "2026-09-25 08:40:00",
        8.5,
        250,
        "Completed"
    )

    assert trip.trip_id == "T1001"
    assert trip.driver_id == "D102"
    assert trip.fare == 250.0


def test_trip_completed():
    trip = Trip(
        "T1001",
        "D102",
        "R501",
        "Bangalore",
        "Koramangala",
        "Indiranagar",
        "2026-09-25 08:00:00",
        "2026-09-25 08:10:00",
        "2026-09-25 08:40:00",
        8.5,
        250,
        "Completed"
    )

    assert trip.is_completed() is True


def test_trip_duration():
    trip = Trip(
        "T1001",
        "D102",
        "R501",
        "Bangalore",
        "Koramangala",
        "Indiranagar",
        "2026-09-25 08:00:00",
        "2026-09-25 08:10:00",
        "2026-09-25 08:40:00",
        8.5,
        250,
        "Completed"
    )

    assert trip.calculate_duration() == 30.0


def test_trip_fare_per_km():
    trip = Trip(
        "T1001",
        "D102",
        "R501",
        "Bangalore",
        "Koramangala",
        "Indiranagar",
        "2026-09-25 08:00:00",
        "2026-09-25 08:10:00",
        "2026-09-25 08:40:00",
        8.5,
        255,
        "Completed"
    )

    assert round(trip.calculate_fare_per_km(), 2) == 30.0


def test_zone_creation():
    zone = Zone(
        "Z01",
        "Bangalore",
        "Koramangala"
    )

    assert zone.zone_id == "Z01"
    assert zone.city == "Bangalore"
    assert zone.zone_name == "Koramangala"


def test_zone_profile():
    zone = Zone(
        "Z01",
        "Bangalore",
        "Koramangala"
    )

    profile = zone.get_profile()

    assert profile["zone_id"] == "Z01"
    assert profile["city"] == "Bangalore"
    assert profile["zone_name"] == "Koramangala"


def test_driver_activity_creation():
    activity = DriverActivity(
        "D102",
        "2026-09-25 08:00:00",
        "Online"
    )

    assert activity.driver_id == "D102"
    assert activity.status == "Online"


def test_driver_activity_datetime():
    activity = DriverActivity(
        "D102",
        "2026-09-25 08:00:00",
        "Online"
    )

    timestamp = activity.get_datetime()

    assert timestamp.year == 2026
    assert timestamp.month == 9
    assert timestamp.day == 25


def test_driver_activity_status():
    online = DriverActivity(
        "D102",
        "2026-09-25 08:00:00",
        "Online"
    )

    offline = DriverActivity(
        "D102",
        "2026-09-25 18:00:00",
        "Offline"
    )

    assert online.is_online() is True
    assert online.is_offline() is False
    assert offline.is_online() is False
    assert offline.is_offline() is True