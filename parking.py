"""Модуль с классом ParkingLot и типами автомобилей для парковки."""

from enum import StrEnum

from models import Client, ParkingSpot


class CarType(StrEnum):
    """Типы автомобилей на парковке."""

    REGULAR = "regular"
    ELECTRIC = "electric"
    PREMIUM = "premium"


class ParkingLot:
    """Хранит информацию о местах и клиентах."""

    def __init__(
        self, total_spots: int, electric_spots: int, premium_spots: int
    ) -> None:
        """Инициализирует парковку с заданным количеством мест."""
        self.spots: list[ParkingSpot] = []
        self._init_spots(total_spots, electric_spots, premium_spots)

    def _init_spots(self, total: int, electric: int, premium: int) -> None:
        """Инициализирует список парковочных мест с заданными типами."""
        for spot_id in range(1, total + 1):
            if spot_id <= electric:
                spot_type = CarType.ELECTRIC
            elif spot_id <= electric + premium:
                spot_type = CarType.PREMIUM
            else:
                spot_type = CarType.REGULAR

            self.spots.append(ParkingSpot(spot_id, spot_type, None))

    def park_client(self, client: Client) -> bool:
        """Паркуем клиента на подходящее место."""
        if client.is_parked:
            return True
        if client.car_type == CarType.REGULAR:
            for spot in self.spots:
                if spot.spot_type == CarType.REGULAR and spot.client is None:
                    spot.client = client
                    client.is_parked = True
                    return True
        elif client.car_type == CarType.ELECTRIC:
            for spot in self.spots:
                if spot.spot_type == CarType.ELECTRIC and spot.client is None:
                    spot.client = client
                    client.is_parked = True
                    return True
        elif client.car_type == CarType.PREMIUM:
            for spot in self.spots:
                if spot.client is None and spot.spot_type in (
                    CarType.PREMIUM,
                    CarType.REGULAR,
                ):
                    spot.client = client
                    client.is_parked = True
                    return True
        return False

    def remove_client(self, client: Client) -> bool:
        """Освобождает место клиента."""
        for spot in self.spots:
            if spot.client is client:
                spot.client = None
                client.is_parked = False
                return True
        return False

    def has_cars(self) -> bool:
        """Проверяет, есть ли машины на парковке."""
        return any(spot.client is not None for spot in self.spots)

    def show_status(self) -> None:
        """Выводит текущее состояние парковки в консоль."""
        total_spots = len(self.spots)
        occupied_spots = sum(1 for spot in self.spots if spot.client)

        print(f"\n📊 Парковка: {occupied_spots}/{total_spots} занято")

        for spot in self.spots:
            if spot.client:
                print(
                    f" - Место {spot.id:2}: {spot.spot_type:<8} — "
                    f"{spot.client.plate} ({spot.client.car_type})"
                )
            else:
                print(f" - Место {spot.id:2}: {spot.spot_type:<8} — свободно")
        print()
