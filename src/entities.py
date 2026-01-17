"""Игровые сущности: Игрок, Противник, Оружие, Броня, Комната подземелья"""
from typing import Optional


class Weapon:
    """Сущность оружия"""

    def __init__(self, name: str, description: str, damage: int, hit_chance: int):
        self.name = name
        self.description = description
        self.damage = damage
        self.hit_chance = hit_chance

    def __repr__(self):
        return f"Weapon({self.name}, damage={self.damage}, hit_chance={self.hit_chance}%)"


class Armor:
    """Сущность брони"""

    def __init__(self, name: str, description: str, defense: int):
        self.name = name
        self.description = description
        self.defense = defense

    def __repr__(self):
        return f"Armor({self.name}, defense={self.defense})"


class Character:
    """Базовый класс персонажа (общий для игрока и противников)"""

    def __init__(
        self,
        name: str,
        health: int,
        weapon: Weapon,
        armor: Armor,
        description: str = "",
    ):
        self.name = name
        self.max_health = health
        self.current_health = health
        self.weapon = weapon
        self.armor = armor
        self.description = description

    def is_alive(self) -> bool:
        """Проверка, жив ли персонаж (здоровье > 0)"""
        return self.current_health > 0

    def take_damage(self, damage: int) -> int:
        """Получение урона и возвращение фактического нанесенного урона с учетом брони"""
        actual_damage = max(0, damage - self.armor.defense)
        self.current_health = max(0, self.current_health - actual_damage)
        return actual_damage

    def get_health_bar(
        self,
        length: int = 20,
        filled_char: str = "█",
        empty_char: str = "░",
    ) -> str:
        """Генерация текстовой «полоски здоровья»"""
        if self.max_health == 0:
            return empty_char * length
        filled_length = int(length * self.current_health / self.max_health)
        bar = filled_char * filled_length + empty_char * (length - filled_length)
        return bar

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, HP={self.current_health}/{self.max_health})"


class Player(Character):
    """Класс игрока"""

    def __init__(
        self,
        name: str,
        health: int,
        weapon: Weapon,
        armor: Armor,
        description: str = "",
        death_descriptions: list = None,
    ):
        super().__init__(name, health, weapon, armor, description)
        if death_descriptions is None or not death_descriptions:
            self.death_descriptions = ["Пал в бою!"]
        else:
            self.death_descriptions = death_descriptions


class Enemy(Character):
    """Класс противника"""

    def __init__(
        self,
        name: str,
        health: int,
        weapon: Weapon,
        armor: Armor,
        description: str = "",
        death_description: str = "",
    ):
        super().__init__(name, health, weapon, armor, description)
        self.death_description = death_description
        self.defeated = False  # флаг, что враг уже побеждён (для логики комнат)

    def defeat(self):
        """Отметить противника как поверженного"""
        self.defeated = True


class Room:
    """Комната подземелья"""

    def __init__(self, room_type: str, description: str, enemy: Optional[Enemy] = None):
        self.room_type = room_type
        self.description = description
        self.enemy = enemy
        self.visited = False

    def has_alive_enemy(self) -> bool:
        """Проверка, есть ли в комнате живой (и ещё не помеченный побеждённым) враг"""
        return (
            self.enemy is not None
            and not self.enemy.defeated
            and self.enemy.is_alive()
        )

    def mark_visited(self):
        """Пометить комнату как посещённую"""
        self.visited = True

    def __repr__(self):
        enemy_status = f", Enemy={self.enemy.name}" if self.enemy else ""
        return f"Room({self.room_type}{enemy_status})"