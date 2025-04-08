from .base_motogp_service import MotoGPBaseService

class MotoGPService(MotoGPBaseService):
    def __init__(self, api_url):
        super().__init__(api_url)

    def get_races(self) -> dict:
        endpoint = "/events"
        return self._get_data(endpoint)

    def get_next_race(self) -> dict:
        endpoint = "/events"
        return self._get_data(endpoint)

    def get_previous_race(self) -> dict:
        endpoint = "/events"
        return self._get_data(endpoint)

    def get_rider_standings(self) -> dict:
        endpoint = "/stat/standings-short?class=MotoGP"
        return self._get_data(endpoint)

    def get_next_races(self) -> dict:
        endpoint = "/schedule?filter=upcoming"
        return self._get_data(endpoint)

