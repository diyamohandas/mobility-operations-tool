class Zone:
    def __init__(self, zone_id, city, zone_name):
        self._zone_id = zone_id
        self._city = city
        self._zone_name = zone_name

    @property
    def zone_id(self):
        return self._zone_id

    @property
    def city(self):
        return self._city

    @property
    def zone_name(self):
        return self._zone_name

    def get_profile(self):
        return {
            "zone_id": self._zone_id,
            "city": self._city,
            "zone_name": self._zone_name
        }

    def __repr__(self):
        return (
            f"Zone("
            f"zone_id='{self._zone_id}', "
            f"city='{self._city}', "
            f"zone_name='{self._zone_name}')"
        )