"""Точка входа в симуляцию работы парковочного сервиса."""

import random
import time


from handler.abc import ParkingEventHandler
from handler.impl import ParkingEventHandlerImpl
from models import Client, EventType
from parking import ParkingLot


class ParkingService:
    """Сервис управления событиями и жизненным циклом парковки."""

    def __init__(
        self,
        handler: ParkingEventHandler,
        clients: list[Client],
        parking_lot: ParkingLot,
    ):
        """Инициализирует сервис парковки."""
        self.handler = handler
        self.parking = parking_lot
        self.clients = clients

    def run(self):
        """Запускает симуляцию работы парковочного сервиса."""
        print("🚗 Парковочный сервис запущен...")

        while self.clients:
            client = random.choice(self.clients)

            # 70% шанс, что уедет
            if client.is_parked and random.random() >= 0.7:
                continue

            # 50% шанс, что заедет
            if not client.is_parked and random.random() >= 0.5:
                continue

            # Обработка события
            if client.is_parked:
                print(
                    f"⚡ Событие: {EventType.LEAVE.upper()} — {client.plate}"
                )
                self.handler.handle_departure(client, self.parking)
                if not client.is_parked:
                    self.clients.remove(client)
            else:
                print(
                    f"⚡ Событие: {EventType.ARRIVE.upper()} — {client.plate}"
                )
                self.handler.handle_arrival(client, self.parking)
            self.parking.show_status()
            # Проверяем, не опустела ли парковка
            if not self.clients or not self.parking.has_cars():
                print(
                    "✅ Все клиенты обработаны, парковка пуста. Завершение работы."
                )
                break

            time.sleep(0.3)


if __name__ == "__main__":
    car_types = ["regular", "electric", "premium"]

    plates = [f"A{str(i).zfill(3)}AA" for i in range(1, 51)]

    clients = [Client(plate, random.choice(car_types)) for plate in plates]

    handler = ParkingEventHandlerImpl()
    parking_lot = ParkingLot(20, 2, 2)
    service = ParkingService(handler, clients, parking_lot)
    service.run()
