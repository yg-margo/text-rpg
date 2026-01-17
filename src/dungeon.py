"""Генератор и менеджер подземелья"""

import json
import random
from pathlib import Path
from typing import List

from src.entities import Player, Enemy, Room, Weapon, Armor


class DungeonGenerator:
    """Генерирует подземелье и игровые сущности на его основе"""

    def __init__(self, data_dir: str = "data"):
        """
        :param data_dir: путь к директории с JSON-файлами данных
                         (player.json, enemies.json, rooms.json)
        """
        self.data_dir = Path(data_dir)
        self.player_data = self._load_json("player.json")
        self.enemies_data = self._load_json("enemies.json")
        self.rooms_data = self._load_json("rooms.json")

    def _load_json(self, filename: str) -> dict:
        """Загружает и парсит JSON-файл с данными"""
        file_path = self.data_dir / filename
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def create_player(self) -> Player:
        """Создает сущность игрока на основе данных из player.json"""
        name = random.choice(self.player_data["names"])
        description = random.choice(self.player_data["descriptions"])
        health = self.player_data["health"]

        weapon_data = self.player_data["weapon"]
        weapon = Weapon(
            weapon_data["name"],
            weapon_data["description"],
            weapon_data["damage"],
            weapon_data["hit_chance"],
        )

        armor_data = self.player_data["armor"]
        armor = Armor(
            armor_data["name"],
            armor_data["description"],
            armor_data["defense"],
        )

        return Player(
            name,
            health,
            weapon,
            armor,
            description,
            self.player_data["death_descriptions"],
        )

    def create_enemy(self) -> Enemy:
        """Создает случайного противника на основе enemies.json"""
        enemy_data = random.choice(self.enemies_data["enemies"])

        weapon_data = enemy_data["weapon"]
        weapon = Weapon(
            weapon_data["name"],
            weapon_data["description"],
            weapon_data["damage"],
            weapon_data["hit_chance"],
        )

        armor_data = enemy_data["armor"]
        armor = Armor(
            armor_data["name"],
            armor_data["description"],
            armor_data["defense"],
        )

        return Enemy(
            enemy_data["name"],
            enemy_data["health"],
            weapon,
            armor,
            enemy_data["description"],
            enemy_data["death_description"],
        )

    def create_room(self, room_type: str, has_enemy: bool = False) -> Room:
        """Создает сущность комнаты"""
        description = random.choice(self.rooms_data["descriptions"])
        enemy = self.create_enemy() if has_enemy else None
        return Room(room_type, description, enemy)

    def generate_dungeon(self, num_rooms: int = 5, enemy_probability: float = 0.6) -> List[Room]:
        """Генерирует подземелье в виде списка комнат"""
        if num_rooms < 2:
            raise ValueError("Dungeon must have at least 2 rooms (start and exit)")

        dungeon = [self.create_room("St", has_enemy=False)]

        for _ in range(num_rooms - 2):
            has_enemy = random.random() < enemy_probability
            dungeon.append(self.create_room("Rm", has_enemy=has_enemy))

        dungeon.append(self.create_room("Ex", has_enemy=False))

        return dungeon

    def get_victory_message(self, enemy: Enemy) -> str:
        """Получает случайное сообщение о победе над противником"""
        template = random.choice(self.rooms_data["victory_messages"])
        return template.format(enemy=enemy.name, death_desc=enemy.death_description)

    def get_attack_message(self, message_type: str, **kwargs) -> str:
        """Получает случайное сообщение о результате атаки"""
        template = random.choice(self.enemies_data["attack_messages"][message_type])
        return template.format(**kwargs)