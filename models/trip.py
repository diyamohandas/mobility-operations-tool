from datetime import datetime


class Trip:
    def __init__(
        self,
        trip_id,
        driver_id,
        rider_id,
        city,
        pickup_zone,
        drop_zone,
        request_time,
        pickup_time,
        drop_time,
        distance_km,
        fare,
        status,
        cancellation_reason=""
    ):
        self._trip_id = trip_id
        self._driver_id = driver_id
        self._rider_id = rider_id
        self._city = city
        self._pickup_zone = pickup_zone
        self._drop_zone = drop_zone
        self._request_time = request_time
        self._pickup_time = pickup_time
        self._drop_time = drop_time
        self._distance_km = float(distance_km)
        self._fare = float(fare)
        self._status = status
        self._cancellation_reason = cancellation_reason

    @property
    def trip_id(self):
        return self._trip_id

    @property
    def driver_id(self):
        return self._driver_id

    @property
    def rider_id(self):
        return self._rider_id

    @property
    def city(self):
        return self._city

    @property
    def pickup_zone(self):
        return self._pickup_zone

    @property
    def drop_zone(self):
        return self._drop_zone

    @property
    def request_time(self):
        return self._request_time

    @property
    def pickup_time(self):
        return self._pickup_time

    @property
    def drop_time(self):
        return self._drop_time

    @property
    def distance_km(self):
        return self._distance_km

    @property
    def fare(self):
        return self._fare

    @property
    def status(self):
        return self._status

    @property
    def cancellation_reason(self):
        return self._cancellation_reason

    def is_completed(self):
        return self._status.lower() == "completed"

    def calculate_duration(self):
        if not self._pickup_time or not self._drop_time:
            return None

        pickup = self._parse_datetime(self._pickup_time)
        drop = self._parse_datetime(self._drop_time)

        if not pickup or not drop:
            return None

        duration = drop - pickup
        return duration.total_seconds() / 60

    def calculate_fare_per_km(self):
        if self._distance_km <= 0:
            return None

        return self._fare / self._distance_km

    @staticmethod
    def _parse_datetime(value):
        if isinstance(value, datetime):
            return value

        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d-%m-%Y %H:%M:%S",
            "%d-%m-%Y %H:%M"
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except (ValueError, TypeError):
                continue

        return None

    def get_summary(self):
        return {
            "trip_id": self._trip_id,
            "driver_id": self._driver_id,
            "rider_id": self._rider_id,
            "city": self._city,
            "pickup_zone": self._pickup_zone,
            "drop_zone": self._drop_zone,
            "distance_km": self._distance_km,
            "fare": self._fare,
            "status": self._status,
            "cancellation_reason": self._cancellation_reason
        }

    def __repr__(self):
        return (
            f"Trip("
            f"trip_id='{self._trip_id}', "
            f"driver_id='{self._driver_id}', "
            f"status='{self._status}')"
        )