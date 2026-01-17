"""Игровой контроллер — управляет игровым циклом и вводом пользователя"""

from typing import List, Optional

from src.entities import Player, Room
from src.dungeon import DungeonGenerator
from src.combat import CombatSystem


class GameController:
    """Управляет ходом игры и взаимодействием с игроком"""

    def __init__(self, dungeon_generator: DungeonGenerator):
        self.generator = dungeon_generator
        self.combat_system = CombatSystem(dungeon_generator)
        self.player: Optional[Player] = None
        self.dungeon: List[Room] = []
        self.current_position: int = 0
        self.running: bool = False

    def initialize_game(self, num_rooms: int = 5):
        """Инициализировать игру: создать игрока и подземелье"""
        self.player = self.generator.create_player()
        self.dungeon = self.generator.generate_dungeon(num_rooms)
        self.current_position = 0
        self.running = True

        print("\n" + "=" * 70)
        print("Добро пожаловать в текстовое подземелье!")
        print("=" * 70)
        print(f"\nВы - {self.player.name}")
        print(self.player.description)
        print(f"\nВаше оружие: {self.player.weapon.name}")
        print(f"  {self.player.weapon.description}")
        print(
            f"  Урон: {self.player.weapon.damage}, "
            f"Шанс попадания: {self.player.weapon.hit_chance}%"
        )
        print(f"\nВаша броня: {self.player.armor.name}")
        print(f"  {self.player.armor.description}")
        print(f"  Защита: {self.player.armor.defense}")
        print(f"\nВаше здоровье: {self.player.current_health}/{self.player.max_health}")
        print("\n" + "=" * 70)
        input("\nНажмите Enter, чтобы начать приключение...")

    def get_current_room(self) -> Room:
        """Вернуть текущую комнату, в которой находится игрок"""
        return self.dungeon[self.current_position]

    def display_room(self):
        """Вывести информацию о текущей комнате на экран"""
        room = self.get_current_room()
        room.mark_visited()

        print("\n" + "=" * 70)
        print(f"Комната {self.current_position + 1} из {len(self.dungeon)}")
        print("=" * 70)
        print(f"Перед вами: {room.description}")

        if room.has_alive_enemy():
            print(f"\nОпасность! В комнате находится: {room.enemy.name}")
            print(f"   {room.enemy.description}")
            print(f"   Здоровье врага: {room.enemy.current_health}/{room.enemy.max_health}")
        elif room.enemy and room.enemy.defeated:
            print(f"\nТруп поверженного {room.enemy.name} лежит на полу.")
        else:
            print("\nКомната пуста и безопасна.")

    def get_available_actions(self) -> dict:
        """Получить список доступных действий в текущей комнате"""
        actions = {}
        action_num = 1
        room = self.get_current_room()

        if room.room_type != "Ex" and not room.has_alive_enemy():
            actions[action_num] = ("forward", "Пойти дальше")
            action_num += 1

        if room.room_type != "St":
            actions[action_num] = ("back", "Вернуться назад")
            action_num += 1

        if room.has_alive_enemy():
            actions[action_num] = ("attack", "Атаковать")
            action_num += 1

        if room.room_type == "Ex":
            actions[action_num] = ("exit", "Выйти из подземелья")
            action_num += 1

        return actions

    @staticmethod
    def display_actions(actions: dict):
        """Вывести список доступных действий игроку"""
        print("\nВы можете:")
        for num, (_, description) in actions.items():
            print(f"  {num}. {description}")

    @staticmethod
    def get_user_input(actions: dict) -> Optional[str]:
        """Получить и проверить ввод пользователя"""
        while True:
            try:
                user_input = input("\nВаши действия: ").strip()
                choice = int(user_input)
                if choice in actions:
                    return actions[choice][0]
                else:
                    print(f"Неверный выбор. Введите число от 1 до {len(actions)}.")
            except ValueError:
                print("Пожалуйста, введите число.")
            except KeyboardInterrupt:
                print("\n\nИгра прервана пользователем.")
                return "quit"

    def execute_action(self, action: str) -> bool:
        """Выполнить выбранное игроком действие"""
        if action == "forward":
            self.current_position += 1
            print("\n➡Вы осторожно движетесь в следующую комнату...")
            return True

        elif action == "back":
            self.current_position -= 1
            print("\nВы возвращаетесь в предыдущую комнату...")
            return True

        elif action == "attack":
            room = self.get_current_room()
            if room.has_alive_enemy():
                print("\nБой начинается!")
                player_won = self.combat_system.auto_battle(self.player, room.enemy)
                print(self.combat_system.get_combat_log())
                if not player_won:
                    print("\n" + "=" * 70)
                    print("Игра окончена")
                    print("=" * 70)
                    return False
                else:
                    print("\nВраг повержен! Можете двигаться дальше.")
            return True

        elif action == "exit":
            print("\n" + "=" * 70)
            print("Поздравляем! Вы успешно прошли подземелье!")
            print("=" * 70)
            print(f"\nВы выходите на свет живым и невредимым, {self.player.name}!")
            print(f"Оставшееся здоровье: {self.player.current_health}/{self.player.max_health}")
            print("\nСпасибо за игру!")
            self.running = False
            return False

        elif action == "quit":
            print("\nДо свидания!")
            self.running = False
            return False

        return True

    def run(self):
        """Основной игровой цикл"""
        if not self.running:
            print("Игра не инициализирована. Вызовите initialize_game() сначала")
            return

        while self.running:
            self.display_room()
            actions = self.get_available_actions()
            self.display_actions(actions)
            action = self.get_user_input(actions)
            if action is None:
                continue
            should_continue = self.execute_action(action)
            if not should_continue:
                self.running = False
                break
