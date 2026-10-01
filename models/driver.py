class Driver:
    """
    Represents a mobility driver.

    Stores driver information and provides methods
    related to driver status and profile.
    """

    def __init__(
        self,
        driver_id,
        driver_name,
        city,
        vehicle_type,
        rating,
        status
    ):
        self._driver_id = driver_id
        self._driver_name = driver_name
        self._city = city
        self._vehicle_type = vehicle_type
        self._rating = float(rating)
        self._status = status

    @property
    def driver_id(self):
        return self._driver_id

    @property
    def driver_name(self):
        return self._driver_name

    @property
    def city(self):
        return self._city

    @property
    def vehicle_type(self):
        return self._vehicle_type

    @property
    def rating(self):
        return self._rating

    @property
    def status(self):
        return self._status

    def is_active(self):
        """Return True if the driver is currently active."""
        return self._status.lower() == "active"

    def get_profile(self):
        """Return the driver's profile as a dictionary."""
        return {
            "driver_id": self._driver_id,
            "driver_name": self._driver_name,
            "city": self._city,
            "vehicle_type": self._vehicle_type,
            "rating": self._rating,
            "status": self._status
        }

    def __repr__(self):
        return (
            f"Driver("
            f"driver_id='{self._driver_id}', "
            f"driver_name='{self._driver_name}', "
            f"city='{self._city}', "
            f"status='{self._status}')"
        )