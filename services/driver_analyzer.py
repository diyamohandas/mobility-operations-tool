from collections import Counter


class DriverAnalyzer:
    def __init__(self, drivers, trips):
        self.drivers = drivers
        self.trips = trips

    def total_drivers(self):
        return len(self.drivers)

    def active_drivers(self):
        return [
            driver
            for driver in self.drivers
            if driver.is_active()
        ]

    def inactive_drivers(self):
        return [
            driver
            for driver in self.drivers
            if not driver.is_active()
        ]

    def driver_trip_counts(self):
        trip_counts = Counter(
            trip.driver_id
            for trip in self.trips
        )

        return dict(trip_counts)

    def completed_trip_counts(self):
        trip_counts = Counter(
            trip.driver_id
            for trip in self.trips
            if trip.is_completed()
        )

        return dict(trip_counts)

    def driver_revenue(self):
        revenue = {}

        for trip in self.trips:
            if trip.is_completed():
                revenue[trip.driver_id] = (
                    revenue.get(trip.driver_id, 0)
                    + trip.fare
                )

        return revenue

    def average_driver_rating(self):
        if not self.drivers:
            return 0

        total_rating = sum(
            driver.rating
            for driver in self.drivers
        )

        return total_rating / len(self.drivers)

    def top_drivers_by_trips(self, k=5):
        trip_counts = self.completed_trip_counts()

        return sorted(
            trip_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )[:k]

    def top_drivers_by_revenue(self, k=5):
        revenue = self.driver_revenue()

        return sorted(
            revenue.items(),
            key=lambda item: item[1],
            reverse=True
        )[:k]

    def driver_summary(self, driver_id):
        driver = next(
            (
                driver
                for driver in self.drivers
                if driver.driver_id == driver_id
            ),
            None
        )

        if driver is None:
            return None

        driver_trips = [
            trip
            for trip in self.trips
            if trip.driver_id == driver_id
        ]

        completed_trips = [
            trip
            for trip in driver_trips
            if trip.is_completed()
        ]

        revenue = sum(
            trip.fare
            for trip in completed_trips
        )

        return {
            "driver_id": driver.driver_id,
            "driver_name": driver.driver_name,
            "city": driver.city,
            "vehicle_type": driver.vehicle_type,
            "rating": driver.rating,
            "status": driver.status,
            "total_trips": len(driver_trips),
            "completed_trips": len(completed_trips),
            "revenue": revenue
        }