import json

class TheaterSeating:
    def __init__(self, performance_data=None):
        self.performance_data = performance_data
        self.zones = {
            "балкон_1": [],
            "балкон_2": [],
            "балкон_3": [],
        }
        self.price_categories = {
            "червоний": 800.0,
            "синій": 600.0,
            "зелений": 500.0,
            "жовтий": 400.0,
            "фіолетовий": 300.0,
        }
        self.reserved_seats = []  # Список заброньованих місць
        self._generate_seats()

    def _generate_seats(self):
        for row in range(1, 4):
            for seat in range(1, 11):
                self.zones["балкон_1"].append({
                    "row": row,
                    "seat": seat,
                    "price_category": "синій",
                    "status": "вільне"
                })

        for row in range(1, 4):
            for seat in range(1, 11):
                self.zones["балкон_2"].append({
                    "row": row,
                    "seat": seat,
                    "price_category": "жовтий",
                    "status": "вільне"
                })

        for row in range(1, 4):
            for seat in range(1, 11):
                self.zones["балкон_3"].append({
                    "row": row,
                    "seat": seat,
                    "price_category": "фіолетовий",
                    "status": "вільне"
                })

    def get_seats_in_zone(self, zone):
        seats = self.zones.get(zone, [])
        for seat in seats:
            seat["status"] = "reserved" if (zone, seat["row"], seat["seat"]) in self.reserved_seats else "вільне"
        return seats

    def reserve_seat(self, zone, row, seat):
        seats = self.zones.get(zone)
        if not seats:
            raise ValueError(f"Зона {zone} не знайдена.")

        for seat_info in seats:
            if seat_info["row"] == row and seat_info["seat"] == seat:
                if seat_info["status"] == "reserved":
                    raise ValueError(f"Місце {row}-{seat} у зоні {zone} вже зарезервовано.")
                seat_info["status"] = "reserved"
                self.reserved_seats.append((zone, row, seat))
                return
        raise ValueError(f"Місце {row}-{seat} у зоні {zone} не знайдено.")

    def get_price(self, zone, row, seat):
        seats = self.zones.get(zone)
        if not seats:
            raise ValueError(f"Зона {zone} не знайдена.")

        for seat_info in seats:
            if seat_info["row"] == row and seat_info["seat"] == seat:
                return self.price_categories[seat_info["price_category"]]
        raise ValueError(f"Місце {row}-{seat} у зоні {zone} не знайдено.")

    def get_price_by_category(self, category):
        return self.price_categories.get(category.lower())

    def is_seat_reserved(self, zone, row, seat):
        """Перевіряє, чи місце заброньоване."""
        return (zone, row, seat) in self.reserved_seats

    def load_reserved_seats(self, reserved_seats):
        """Завантажує список заброньованих місць і оновлює статуси."""
        self.reserved_seats = reserved_seats
        for zone in self.zones:
            for seat in self.zones[zone]:
                seat["status"] = "reserved" if (zone, seat["row"], seat["seat"]) in self.reserved_seats else "вільне"