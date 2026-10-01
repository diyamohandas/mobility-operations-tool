from datetime import datetime


class UtilizationAnalyzer:

    def __init__(self, activities, trips):
        self.activities = activities
        self.trips = trips

    def _parse_time(self, value):
        if isinstance(value, datetime):
            return value

        return datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S"
        )

    def online_hours(self, driver_id):
        driver_activities = [
            activity
            for activity in self.activities
            if activity.driver_id == driver_id
        ]

        total_seconds = 0

        for i in range(len(driver_activities) - 1):
            current = driver_activities[i]
            next_activity = driver_activities[i + 1]

            if current.status == "Online":
                start = self._parse_time(
                    current.timestamp
                )
                end = self._parse_time(
                    next_activity.timestamp
                )

                total_seconds += (
                    end - start
                ).total_seconds()

        return total_seconds / 3600

    def trip_hours(self, driver_id):
        completed_trips = [
            trip
            for trip in self.trips
            if (
                trip.driver_id == driver_id
                and trip.is_completed()
            )
        ]

        total_seconds = 0

        for trip in completed_trips:
            start = self._parse_time(
                trip.pickup_time
            )

            end = self._parse_time(
                trip.drop_time
            )

            total_seconds += (
                end - start
            ).total_seconds()

        return total_seconds / 3600

    def idle_hours(self, driver_id):
        online = self.online_hours(driver_id)
        trip = self.trip_hours(driver_id)

        return max(
            online - trip,
            0
        )

    def utilization_rate(self, driver_id):
        online = self.online_hours(driver_id)

        if online == 0:
            return 0

        trip = self.trip_hours(driver_id)

        return (
            trip / online
        ) * 100

    def driver_utilization(self):
        driver_ids = {
            activity.driver_id
            for activity in self.activities
        }

        result = {}

        for driver_id in driver_ids:
            result[driver_id] = {
                "online_hours": self.online_hours(
                    driver_id
                ),
                "trip_hours": self.trip_hours(
                    driver_id
                ),
                "idle_hours": self.idle_hours(
                    driver_id
                ),
                "utilization_rate": self.utilization_rate(
                    driver_id
                )
            }

        return result

    def most_utilized_drivers(self, k=5):
        utilization = self.driver_utilization()

        ranked = sorted(
            utilization.items(),
            key=lambda item: item[1]["utilization_rate"],
            reverse=True
        )

        return ranked[:k]

    def highest_idle_drivers(self, k=5):
        utilization = self.driver_utilization()

        ranked = sorted(
            utilization.items(),
            key=lambda item: item[1]["idle_hours"],
            reverse=True
        )

        return ranked[:k]