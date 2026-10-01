class DataIndex:
    def __init__(self, drivers=None, trips=None, activities=None):
        self.drivers = drivers or []
        self.trips = trips or []
        self.activities = activities or []

        self.driver_by_id = {}
        self.trip_by_id = {}
        self.trips_by_driver = {}
        self.trips_by_zone = {}
        self.trips_by_city = {}
        self.activities_by_driver = {}

        self.build_indexes()

    def build_indexes(self):
        self.driver_by_id = {
            driver.driver_id: driver
            for driver in self.drivers
        }

        self.trip_by_id = {
            trip.trip_id: trip
            for trip in self.trips
        }

        self.trips_by_driver = {}

        for trip in self.trips:
            self.trips_by_driver.setdefault(
                trip.driver_id,
                []
            ).append(trip)

        self.trips_by_zone = {}

        for trip in self.trips:
            self.trips_by_zone.setdefault(
                trip.pickup_zone,
                []
            ).append(trip)

        self.trips_by_city = {}

        for trip in self.trips:
            self.trips_by_city.setdefault(
                trip.city,
                []
            ).append(trip)

        self.activities_by_driver = {}

        for activity in self.activities:
            self.activities_by_driver.setdefault(
                activity.driver_id,
                []
            ).append(activity)

    def get_driver(self, driver_id):
        return self.driver_by_id.get(driver_id)

    def get_trip(self, trip_id):
        return self.trip_by_id.get(trip_id)

    def get_driver_trips(self, driver_id):
        return self.trips_by_driver.get(driver_id, [])

    def get_zone_trips(self, zone):
        return self.trips_by_zone.get(zone, [])

    def get_city_trips(self, city):
        return self.trips_by_city.get(city, [])

    def get_driver_activities(self, driver_id):
        return self.activities_by_driver.get(driver_id, [])