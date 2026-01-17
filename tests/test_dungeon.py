"""Тесты для генератора подземелья"""
import pytest
import allure

from src.dungeon import DungeonGenerator
from src.entities import Player, Enemy, Room


@allure.feature("Генератор подземелья")
@allure.story("Инициализация генератора")
class TestDungeonGeneratorInit:
    """Тесты инициализации генератора подземелья"""

    @allure.title("Инициализация генератора")
    @allure.description("Проверка корректной инициализации генератора подземелья")
    def test_generator_initialization(self, dungeon_generator):
        """Проверка загрузки всех JSON файлов"""
        with allure.step("Проверка загрузки данных игрока"):
            assert dungeon_generator.player_data is not None
            assert isinstance(dungeon_generator.player_data, dict)
        with allure.step("Проверка загрузки данных врагов"):
            assert dungeon_generator.enemies_data is not None
            assert isinstance(dungeon_generator.enemies_data, dict)
        with allure.step("Проверка загрузки данных комнат"):
            assert dungeon_generator.rooms_data is not None
            assert isinstance(dungeon_generator.rooms_data, dict)

    @allure.title("Загрузка JSON файлов")
    @allure.description("Проверка метода загрузки JSON файлов")
    @pytest.mark.parametrize(
        "filename,expected_keys",
        [
            ("player.json", ["health", "names", "weapon", "armor"]),
            ("enemies.json", ["enemies", "attack_messages"]),
            ("rooms.json", ["descriptions", "victory_messages"]),
        ],
    )
    def test_load_json(self, dungeon_generator, filename, expected_keys):
        """Проверка загрузки JSON и наличия ключей"""
        with allure.step(f"Загрузка файла {filename}"):
            data = dungeon_generator._load_json(filename)
        with allure.step("Проверка типа данных"):
            assert isinstance(data, dict)
        for key in expected_keys:
            with allure.step(f"Проверка наличия ключа '{key}'"):
                assert key in data

    @allure.title("Ошибка при отсутствии файла")
    @allure.description("Проверка выброса исключения при отсутствии JSON файла")
    def test_load_json_file_not_found(self):
        """Проверка обработки отсутствующего файла"""
        with allure.step("Попытка создать генератор с несуществующей директорией"):
            with pytest.raises(FileNotFoundError):
                generator = DungeonGenerator(data_dir="non_existent_directory")
                generator._load_json("player.json")


@allure.feature("Генератор подземелья")
@allure.story("Создание сущностей")
class TestDungeonGeneratorEntities:
    """Тесты создания игровых сущностей"""

    @allure.title("Создание игрока")
    @allure.description("Проверка корректного создания игрока из JSON данных")
    def test_create_player(self, dungeon_generator):
        """Создание игрока с данными из JSON"""
        with allure.step("Создание игрока"):
            player = dungeon_generator.create_player()
        with allure.step("Проверка типа объекта"):
            assert isinstance(player, Player)
        with allure.step("Проверка, что имя из списка допустимых"):
            assert player.name in dungeon_generator.player_data["names"]
        with allure.step("Проверка здоровья игрока"):
            assert player.max_health == dungeon_generator.player_data["health"]
            assert player.current_health == player.max_health
        with allure.step("Проверка наличия оружия"):
            assert player.weapon is not None
            assert player.weapon.name == dungeon_generator.player_data["weapon"]["name"]
        with allure.step("Проверка наличия брони"):
            assert player.armor is not None
            assert player.armor.name == dungeon_generator.player_data["armor"]["name"]

    @allure.title("Создание врага")
    @allure.description("Проверка корректного создания врага из JSON данных")
    def test_create_enemy(self, dungeon_generator):
        """Создание врага с данными из JSON"""
        with allure.step("Создание врага"):
            enemy = dungeon_generator.create_enemy()
        with allure.step("Проверка типа объекта"):
            assert isinstance(enemy, Enemy)
        with allure.step("Проверка имени врага"):
            assert enemy.name != ""
            assert len(enemy.name) > 0
        with allure.step("Проверка здоровья врага"):
            assert enemy.max_health > 0
            assert enemy.current_health == enemy.max_health
        with allure.step("Проверка наличия оружия"):
            assert enemy.weapon is not None
        with allure.step("Проверка наличия брони"):
            assert enemy.armor is not None
        with allure.step("Проверка описания смерти"):
            assert enemy.death_description != ""

    @allure.title("Создание пустой комнаты")
    @allure.description("Проверка создания комнаты без врагов")
    def test_create_room_empty(self, dungeon_generator):
        """Создание пустой комнаты"""
        with allure.step("Создание пустой комнаты"):
            room = dungeon_generator.create_room("Rm", has_enemy=False)
        with allure.step("Проверка типа объекта"):
            assert isinstance(room, Room)
        with allure.step("Проверка типа комнаты"):
            assert room.room_type == "Rm"
        with allure.step("Проверка отсутствия врага"):
            assert room.enemy is None
        with allure.step("Проверка, что описание из списка допустимых"):
            assert room.description in dungeon_generator.rooms_data["descriptions"]

    @allure.title("Создание комнаты с врагом")
    @allure.description("Проверка создания комнаты с врагом")
    def test_create_room_with_enemy(self, dungeon_generator):
        """Создание комнаты с врагом"""
        with allure.step("Создание комнаты с врагом"):
            room = dungeon_generator.create_room("Rm", has_enemy=True)
        with allure.step("Проверка типа объекта"):
            assert isinstance(room, Room)
        with allure.step("Проверка наличия врага"):
            assert room.enemy is not None
        with allure.step("Проверка типа врага"):
            assert isinstance(room.enemy, Enemy)


@allure.feature("Генератор подземелья")
@allure.story("Генерация подземелья")
class TestDungeonGeneration:
    """Тесты генерации подземелья"""

    @allure.title("Генерация подземелья с корректной структурой")
    @allure.description("Проверка правильной структуры сгенерированного подземелья")
    @pytest.mark.parametrize("num_rooms", [2, 3, 5, 10])
    def test_generate_dungeon_structure(self, dungeon_generator, num_rooms):
        """Генерация подземелья различного размера"""
        with allure.step(f"Генерация подземелья из {num_rooms} комнат"):
            dungeon = dungeon_generator.generate_dungeon(num_rooms=num_rooms)
        with allure.step("Проверка количества комнат"):
            assert len(dungeon) == num_rooms
        with allure.step("Проверка, что первая комната - стартовая"):
            assert dungeon[0].room_type == "St"
        with allure.step("Проверка, что последняя комната - выходная"):
            assert dungeon[-1].room_type == "Ex"
        with allure.step("Проверка, что средние комнаты обычные"):
            for room in dungeon[1:-1]:
                assert room.room_type == "Rm"

    @allure.title("Минимальный размер подземелья")
    @allure.description("Проверка генерации подземелья минимального размера (2 комнаты)")
    def test_generate_dungeon_minimum_size(self, dungeon_generator):
        """Генерация минимального подземелья"""
        with allure.step("Генерация подземелья из 2 комнат"):
            dungeon = dungeon_generator.generate_dungeon(num_rooms=2)
        with allure.step("Проверка количества комнат"):
            assert len(dungeon) == 2
        with allure.step("Проверка стартовой комнаты"):
            assert dungeon[0].room_type == "St"
        with allure.step("Проверка выходной комнаты"):
            assert dungeon[1].room_type == "Ex"

    @allure.title("Ошибка при недопустимом размере подземелья")
    @allure.description("Проверка выброса исключения при попытке создать подземелье из 1 комнаты")
    @pytest.mark.parametrize("invalid_size", [0, 1, -1])
    def test_generate_dungeon_invalid_size(self, dungeon_generator, invalid_size):
        """Проверка обработки недопустимого размера"""
        with allure.step(f"Попытка создать подземелье из {invalid_size} комнат"):
            with pytest.raises(ValueError, match="at least 2 rooms"):
                dungeon_generator.generate_dungeon(num_rooms=invalid_size)

    @allure.title("Стартовая и выходная комнаты без врагов")
    @allure.description("Проверка, что первая и последняя комнаты всегда пусты")
    def test_generate_dungeon_start_and_exit_no_enemies(self, dungeon_generator):
        """Проверка отсутствия врагов в стартовой и выходной комнатах"""
        with allure.step("Генерация подземелья"):
            dungeon = dungeon_generator.generate_dungeon(num_rooms=5)
        with allure.step("Проверка стартовой комнаты"):
            assert dungeon[0].enemy is None
        with allure.step("Проверка выходной комнаты"):
            assert dungeon[-1].enemy is None

    @allure.title("Вероятность появления врагов")
    @allure.description("Проверка, что враги появляются согласно заданной вероятности")
    @pytest.mark.parametrize(
        "enemy_probability,num_rooms",
        [
            (0.0, 10),   # Нет врагов
            (1.0, 10),   # Все комнаты с врагами
        ],
    )
    def test_generate_dungeon_enemy_probability(
        self, dungeon_generator, enemy_probability, num_rooms
    ):
        """Проверка вероятности появления врагов"""
        with allure.step(f"Генерация подземелья с вероятностью врагов {enemy_probability}"):
            dungeon = dungeon_generator.generate_dungeon(
                num_rooms=num_rooms,
                enemy_probability=enemy_probability,
            )
        middle_rooms = dungeon[1:-1]
        rooms_with_enemies = sum(1 for room in middle_rooms if room.enemy is not None)
        if enemy_probability == 0.0:
            with allure.step("Проверка, что нет врагов в средних комнатах"):
                assert rooms_with_enemies == 0
        elif enemy_probability == 1.0:
            with allure.step("Проверка, что все средние комнаты имеют врагов"):
                assert rooms_with_enemies == len(middle_rooms)


@allure.feature("Генератор подземелья")
@allure.story("Сообщения")
class TestDungeonMessages:
    """Тесты генерации сообщений"""

    @allure.title("Получение сообщения о победе")
    @allure.description("Проверка генерации сообщения о победе над врагом")
    def test_get_victory_message(self, dungeon_generator):
        """Проверка сообщения о победе"""
        with allure.step("Создание врага"):
            enemy = dungeon_generator.create_enemy()
        with allure.step("Получение сообщения о победе"):
            message = dungeon_generator.get_victory_message(enemy)
        with allure.step("Проверка типа сообщения"):
            assert isinstance(message, str)
        with allure.step("Проверка длины сообщения"):
            assert len(message) > 0
        with allure.step("Проверка наличия имени врага в сообщении"):
            assert enemy.name in message

    @allure.title("Получение сообщений атаки")
    @allure.description("Проверка генерации различных сообщений атаки")
    @pytest.mark.parametrize(
        "message_type,kwargs",
        [
            ("player_hit", {"damage": 5, "target": "Пещерный гоблин"}),
            ("player_miss", {"target": "Пещерный гоблин"}),
            ("enemy_hit", {"damage": 3, "attacker": "Зомби"}),
            ("enemy_miss", {"attacker": "Зомби"}),
        ],
    )
    def test_get_attack_message(self, dungeon_generator, message_type, kwargs):
        """Проверка различных типов сообщений атаки"""
        with allure.step(f"Получение сообщения типа '{message_type}'"):
            message = dungeon_generator.get_attack_message(message_type, **kwargs)
        with allure.step("Проверка типа сообщения"):
            assert isinstance(message, str)
        with allure.step("Проверка длины сообщения"):
            assert len(message) > 0
        for value in kwargs.values():
            with allure.step(f"Проверка наличия '{value}' в сообщении"):
                assert str(value) in message
