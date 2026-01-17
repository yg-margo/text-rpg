"""Тесты для игровых сущностей"""

import pytest
import allure

from src.entities import Weapon, Armor, Player, Enemy, Room


@allure.feature("Игровые сущности")
@allure.story("Оружие")
class TestWeapon:
    """Тесты для класса Weapon"""

    @allure.title("Создание оружия с корректными параметрами")
    @allure.description("Проверка создания экземпляра оружия и корректности его атрибутов")
    @pytest.mark.parametrize(
        "name,description,damage,hit_chance",
        [
            (
                "Опасная дубина",
                "крепкая сосновая ветка с вбитым ржавым гвоздем на конце.",
                5,
                75,
            ),
            (
                "Обглоданная кость",
                "Бедренная кость, возможно предыдущего приключенца или большого животного.",
                5,
                50,
            ),
            (
                "Ржавый нож",
                "Раньше это был отличный кухонный нож, но теперь это ржавый кусок металла. "
                "Даже страшно подумать, что будет, если таким порезаться.",
                4,
                75,
            ),
            (
                "Лопата могильщика",
                "Добротная лопата, которой можно возделывать землю или рыть могилы.",
                5,
                50,
            ),
        ],
    )
    def test_weapon_creation(self, name, description, damage, hit_chance):
        """Создание оружия с различными параметрами из дизайн‑документа"""
        with allure.step(f"Создание оружия '{name}'"):
            weapon = Weapon(name, description, damage, hit_chance)
        with allure.step("Проверка имени оружия"):
            assert weapon.name == name
        with allure.step("Проверка описания оружия"):
            assert weapon.description == description
        with allure.step("Проверка урона оружия"):
            assert weapon.damage == damage
        with allure.step("Проверка шанса попадания"):
            assert weapon.hit_chance == hit_chance

    @allure.title("Строковое представление оружия")
    @allure.description("Проверка метода __repr__ для оружия")
    def test_weapon_repr(self, sample_weapon):
        """Проверка строкового представления оружия"""
        with allure.step("Получение строкового представления"):
            repr_str = repr(sample_weapon)
        with allure.step("Проверка наличия имени в представлении"):
            assert sample_weapon.name in repr_str
        with allure.step("Проверка наличия урона в представлении"):
            assert str(sample_weapon.damage) in repr_str


@allure.feature("Игровые сущности")
@allure.story("Броня")
class TestArmor:
    """Тесты для класса Armor"""

    @allure.title("Создание брони с корректными параметрами")
    @allure.description("Проверка создания экземпляра брони и корректности его атрибутов")
    @pytest.mark.parametrize(
        "name,description,defense",
        [
            (
                "Легкий кожаный доспех",
                "Сшитый из крыс кожаный доспех. Пахнет ужасно, но вроде бы защищает от урона.",
                2,
            ),
            (
                "Рваные лохмотья",
                "Сложно уже сказать, что это за одежда была раньше. Теперь это однородная грязная масса, которая прилипла к телу.",
                1,
            ),
            (
                "Кожаные доспехи",
                "Незамысловатые кожаные доспехи, которые от времени частично ссохлись и потрескались.",
                3,
            ),
            (
                "Набедренная повязка",
                "Небольшой лоскут ткани, который с трудом справляется с тем, чтобы скрыть причиндалы.",
                0,
            ),
        ],
    )
    def test_armor_creation(self, name, description, defense):
        """Создание брони из набора сущностей дизайн‑документа"""
        with allure.step(f"Создание брони '{name}'"):
            armor = Armor(name, description, defense)
        with allure.step("Проверка имени брони"):
            assert armor.name == name
        with allure.step("Проверка описания брони"):
            assert armor.description == description
        with allure.step("Проверка защиты брони"):
            assert armor.defense == defense

    @allure.title("Строковое представление брони")
    @allure.description("Проверка метода __repr__ для брони")
    def test_armor_repr(self, sample_armor):
        """Проверка строкового представления брони"""
        with allure.step("Получение строкового представления"):
            repr_str = repr(sample_armor)
        with allure.step("Проверка наличия имени в представлении"):
            assert sample_armor.name in repr_str
        with allure.step("Проверка наличия защиты в представлении"):
            assert str(sample_armor.defense) in repr_str


@allure.feature("Игровые сущности")
@allure.story("Игрок")
class TestPlayer:
    """Тесты для класса Player"""

    @allure.title("Создание игрока")
    @allure.description("Проверка корректного создания игрока со всеми атрибутами")
    def test_player_creation(self, sample_player, sample_weapon, sample_armor):
        """Создание игрока и проверка его атрибутов"""
        with allure.step("Проверка имени игрока"):
            assert sample_player.name == "Васька Проказник"
        with allure.step("Проверка максимального здоровья (по дизайн‑документу: 10)"):
            assert sample_player.max_health == 10
        with allure.step("Проверка текущего здоровья"):
            assert sample_player.current_health == 10
        with allure.step("Проверка наличия оружия (Опасная дубина)"):
            assert sample_player.weapon == sample_weapon
        with allure.step("Проверка наличия брони (Легкий кожаный доспех)"):
            assert sample_player.armor == sample_armor

    @allure.title("Проверка жизнеспособности игрока")
    @allure.description("Проверка метода is_alive при различных уровнях здоровья")
    @pytest.mark.parametrize(
        "health,expected",
        [
            (10, True),
            (5, True),
            (1, True),
            (0, False),
            (-10, False),
        ],
    )
    def test_player_is_alive(self, sample_player, health, expected):
        """Проверка жизнеспособности при разных уровнях здоровья"""
        with allure.step(f"Установка здоровья на {health}"):
            sample_player.current_health = health
        with allure.step(f"Проверка, что is_alive возвращает {expected}"):
            assert sample_player.is_alive() is expected

    @allure.title("Получение урона игроком")
    @allure.description("Проверка корректного расчета урона с учетом защиты брони")
    @pytest.mark.parametrize(
        "damage,armor_defense,expected_damage,expected_health",
        [
            (15, 5, 10, 0 + (100 - 10)),
            (10, 5, 5, 100 - 5),
            (5, 5, 0, 100),
            (3, 5, 0, 100),
        ],
    )
    def test_player_take_damage(
        self, sample_weapon, damage, armor_defense, expected_damage, expected_health
    ):
        """Проверяет корректный расчёт фактического урона и оставшегося здоровья игрока с учётом защиты брони"""
        with allure.step("Создание игрока с определенной защитой"):
            armor = Armor("Тестовая броня", "Абстрактная броня для теста", armor_defense)
            player = Player("Тестовый герой", 100, sample_weapon, armor)
        with allure.step(f"Нанесение урона {damage}"):
            actual_damage = player.take_damage(damage)
        with allure.step(f"Проверка фактического урона: {expected_damage}"):
            assert actual_damage == expected_damage
        with allure.step(f"Проверка оставшегося здоровья: {expected_health}"):
            assert player.current_health == expected_health

    @allure.title("Здоровье не может быть отрицательным")
    @allure.description("Проверка, что здоровье не опускается ниже нуля")
    def test_player_health_cannot_go_negative(self, sample_player):
        """Проверка минимального значения здоровья"""
        with allure.step("Нанесение урона больше текущего здоровья"):
            sample_player.take_damage(200)
        with allure.step("Проверка, что здоровье равно 0"):
            assert sample_player.current_health == 0
        with allure.step("Проверка, что игрок мертв"):
            assert not sample_player.is_alive()

    @allure.title("Визуализация полоски здоровья")
    @allure.description("Проверка корректного отображения полоски здоровья")
    @pytest.mark.parametrize(
        "current_health,max_health,bar_length,expected_filled",
        [
            (100, 100, 10, 10),  # Полное здоровье
            (50, 100, 10, 5),    # Половина здоровья
            (25, 100, 10, 2),    # Четверть здоровья
            (0, 100, 10, 0),     # Нет здоровья
        ],
    )
    def test_player_health_bar(
        self, sample_weapon, sample_armor, current_health, max_health, bar_length, expected_filled
    ):
        """
        Проверка полоски здоровья
        """
        with allure.step("Создание игрока"):
            player = Player("Герой", max_health, sample_weapon, sample_armor)
            player.current_health = current_health
        with allure.step(f"Генерация полоски здоровья длиной {bar_length}"):
            bar = player.get_health_bar(bar_length)
        with allure.step("Проверка длины полоски"):
            assert len(bar) == bar_length
        with allure.step(f"Проверка количества заполненных символов: {expected_filled}"):
            assert bar.count("█") == expected_filled
        with allure.step(
            f"Проверка количества пустых символов: {bar_length - expected_filled}"
        ):
            assert bar.count("░") == bar_length - expected_filled


@allure.feature("Игровые сущности")
@allure.story("Враг")
class TestEnemy:
    """Тесты для класса Enemy"""

    @allure.title("Создание врага")
    @allure.description("Проверка корректного создания врага со всеми атрибутами")
    def test_enemy_creation(self, sample_enemy):
        """Создание врага и проверка его атрибутов"""
        with allure.step("Проверка имени врага"):
            assert sample_enemy.name == "Скелет"
        with allure.step("Проверка максимального здоровья"):
            assert sample_enemy.max_health == 50
        with allure.step("Проверка текущего здоровья"):
            assert sample_enemy.current_health == 50
        with allure.step("Проверка флага поражения"):
            assert sample_enemy.defeated is False
        with allure.step("Проверка описания смерти"):
            assert sample_enemy.death_description == "Груда костей, рассыпалась по всей комнате."

    @allure.title("Поражение врага")
    @allure.description("Проверка метода defeat для врага")
    def test_enemy_defeat(self, sample_enemy):
        """Проверка поражения врага"""
        with allure.step("Проверка начального состояния"):
            assert sample_enemy.defeated is False
        with allure.step("Вызов метода defeat"):
            sample_enemy.defeat()
        with allure.step("Проверка, что враг помечен как побежденный"):
            assert sample_enemy.defeated is True

    @allure.title("Получение урона врагом")
    @allure.description("Проверка корректного расчета урона для врага")
    @pytest.mark.parametrize(
        "damage,expected_actual_damage,expected_health",
        [
            (10, 7, 43),  # 10 - 3 (защита) = 7 урона
            (5, 2, 48),   # 5 - 3 = 2 урона
            (3, 0, 50),   # 3 - 3 = 0 урона
            (1, 0, 50),   # Урон меньше защиты
        ],
    )
    def test_enemy_take_damage(self, damage, expected_actual_damage, expected_health):
        """Проверка получения урона врагом"""
        with allure.step("Создание врага"):
            weapon = Weapon("Обглоданная кость", "Кость врага", 8, 70)
            armor = Armor("Кожаные доспехи", "Броня врага", 3)
            enemy = Enemy("Скелет", 50, weapon, armor, "Скелет", "Груда костей, рассыпалась по всей комнате.")
        with allure.step(f"Нанесение урона {damage}"):
            actual_damage = enemy.take_damage(damage)
        with allure.step(f"Проверка фактического урона: {expected_actual_damage}"):
            assert actual_damage == expected_actual_damage
        with allure.step(f"Проверка оставшегося здоровья: {expected_health}"):
            assert enemy.current_health == expected_health


@allure.feature("Игровые сущности")
@allure.story("Комната")
class TestRoom:
    """Тесты для класса Room"""

    @allure.title("Создание пустой комнаты")
    @allure.description("Проверка создания комнаты без врагов")
    def test_room_creation_empty(self):
        """Создание пустой комнаты"""
        with allure.step("Создание комнаты типа 'Rm'"):
            room = Room("Rm", "Темная комната", None)
        with allure.step("Проверка типа комнаты"):
            assert room.room_type == "Rm"
        with allure.step("Проверка описания комнаты"):
            assert room.description == "Темная комната"
        with allure.step("Проверка отсутствия врага"):
            assert room.enemy is None
        with allure.step("Проверка флага посещения"):
            assert room.visited is False

    @allure.title("Создание комнаты с врагом")
    @allure.description("Проверка создания комнаты с врагом")
    def test_room_creation_with_enemy(self, sample_enemy):
        """Создание комнаты с врагом"""
        with allure.step("Создание комнаты с врагом"):
            room = Room("Rm", "Темная комната", sample_enemy)
        with allure.step("Проверка наличия врага"):
            assert room.enemy == sample_enemy
        with allure.step("Проверка, что в комнате живой враг"):
            assert room.has_alive_enemy() is True

    @allure.title("Проверка наличия живого врага")
    @allure.description("Проверка метода has_alive_enemy в различных сценариях")
    def test_room_has_alive_enemy(self, sample_enemy):
        """Проверка наличия живого врага в комнате"""
        with allure.step("Создание комнаты с живым врагом"):
            room = Room("Rm", "Темная комната", sample_enemy)
        with allure.step("Проверка наличия живого врага"):
            assert room.has_alive_enemy() is True
        with allure.step("Враг побежден"):
            sample_enemy.defeat()
        with allure.step("Проверка, что живого врага нет"):
            assert room.has_alive_enemy() is False
        with allure.step("Возвращение флага defeated и убийство врага"):
            sample_enemy.defeated = False
            sample_enemy.current_health = 0
        with allure.step("Проверка, что мертвый враг не считается живым"):
            assert room.has_alive_enemy() is False

    @allure.title("Отметка комнаты как посещенной")
    @allure.description("Проверка метода mark_visited")
    def test_room_mark_visited(self, empty_room):
        """Проверка отметки комнаты как посещенной"""
        with allure.step("Проверка начального состояния"):
            assert empty_room.visited is False
        with allure.step("Отметка комнаты как посещенной"):
            empty_room.mark_visited()
        with allure.step("Проверка флага visited"):
            assert empty_room.visited is True

    @allure.title("Типы комнат")
    @allure.description("Проверка различных типов комнат (St, Rm, Ex)")
    @pytest.mark.parametrize(
        "room_type,description",
        [
            ("St", "Стартовая комната"),
            ("Rm", "Обычная комната"),
            ("Ex", "Выходная комната"),
        ],
    )
    def test_room_types(self, room_type, description):
        """Проверка создания комнат разных типов"""
        with allure.step(f"Создание комнаты типа '{room_type}'"):
            room = Room(room_type, description, None)
        with allure.step(f"Проверка типа комнаты: {room_type}"):
            assert room.room_type == room_type
        with allure.step("Проверка описания"):
            assert room.description == description
