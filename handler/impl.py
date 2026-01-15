
from models import Client
from parking import ParkingLot
from handler.abc import ParkingEventHandler


class ParkingEventHandlerImpl(ParkingEventHandler):

    def handle_arrival(self, client: Client, parking_lot: ParkingLot):
        """Обработка прибытия машины для парковки."""
        try:
            if parking_lot.park_client(client):
                print(f"{client.plate} припарковался")
            else:
                print(f"{client.plate} не смог найти место")
        except Exception:
            pass

    def handle_departure(self, client: Client, parking_lot: ParkingLot):
        """Обработка отбытия машины с парковки."""
        try:
            if parking_lot.remove_client(client):
                print(f"{client.plate} уехал с парковки")
            else:
                print(f"{client.plate} не был на парковке")
        except Exception:
            pass
