from services.data_loader import DataLoader
from services.validation_service import DataValidator


def test_load_drivers():
    loader = DataLoader()

    drivers = loader.load_drivers("data/drivers.csv")

    assert len(drivers) == 8
    assert drivers[0].driver_id == "D101"
    assert drivers[0].driver_name == "Arun"


def test_load_trips():
    loader = DataLoader()

    trips = loader.load_trips("data/trips.csv")

    assert len(trips) == 15
    assert trips[0].trip_id == "T1001"
    assert trips[0].driver_id == "D101"


def test_load_activities():
    loader = DataLoader()

    activities = loader.load_activities(
        "data/driver_activity.csv"
    )

    assert len(activities) == 20
    assert activities[0].driver_id == "D101"


def test_validate_drivers():
    validator = DataValidator()

    valid, message = validator.validate_file(
        "data/drivers.csv",
        "drivers"
    )

    assert valid is True
    assert message == "Validation successful."


def test_validate_trips():
    validator = DataValidator()

    valid, message = validator.validate_file(
        "data/trips.csv",
        "trips"
    )

    assert valid is True
    assert message == "Validation successful."


def test_validate_activities():
    validator = DataValidator()

    valid, message = validator.validate_file(
        "data/driver_activity.csv",
        "activities"
    )

    assert valid is True
    assert message == "Validation successful."


def test_invalid_dataset_type():
    validator = DataValidator()

    valid, message = validator.validate_file(
        "data/drivers.csv",
        "invalid"
    )

    assert valid is False
    assert message == "Invalid dataset type."


def test_missing_file():
    validator = DataValidator()

    valid, message = validator.validate_file(
        "data/missing.csv",
        "drivers"
    )

    assert valid is False
    assert message == "File not found."