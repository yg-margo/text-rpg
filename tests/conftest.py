"""Конфигурация pytest и фикстуры для тестирования"""

import pytest
from pathlib import Path

from src.entities import Weapon, Armor, Player, Enemy, Room
from src.dungeon import DungeonGenerator


@pytest.fixture(scope="session")
def data_dir() -> str:
    """
    Путь к реальной директории с игровыми JSON‑данными.

    Используем настоящие файлы из каталога 'data', которые соответствуют
    дизайн‑документу.
    """
    tests_dir = Path(__file__).resolve().parent
    project_root = tests_dir.parent
    data_path = project_root / "data"

    if not data_path.exists():
        raise FileNotFoundError(
            f"Директория с данными не найдена: {data_path}. "
            "Убедитесь, что каталог 'data' находится в корне проекта."
        )

    return str(data_path)


@pytest.fixture
def dungeon_generator(data_dir: str) -> DungeonGenerator:
    """
    Генератор подземелья, работающий с реальными JSON‑данными из каталога data.
    """
    return DungeonGenerator(data_dir=data_dir)

@pytest.fixture
def sample_weapon() -> Weapon:
    """Фикстура: создание тестового оружия"""
    return Weapon(
        name="Опасная дубина",
        description="крепкая сосновая ветка с вбитым ржавым гвоздем на конце.",
        damage=5,
        hit_chance=75,
    )


@pytest.fixture
def sample_armor() -> Armor:
    """Фикстура: создание тестовой брони"""
    return Armor(
        name="Легкий кожаный доспех",
        description=(
            "Сшитый из крыс кожаный доспех. Пахнет ужасно, но вроде бы "
            "защищает от урона."
        ),
        defense=2,
    )


@pytest.fixture
def sample_player(sample_weapon, sample_armor) -> Player:
    """Фикстура: создание тестового игрока"""
    return Player(
        name="Васька Проказник",
        health=10,
        weapon=sample_weapon,
        armor=sample_armor,
        description=(
            "Вы сирота, живущая на улице. Единственный способ улучшить свою жизнь "
            "для вас, это найти что-то ценное в опасных и заброшенных местах."
        ),
        death_descriptions=[
            "Ваша кончина была долгой и мучительной. Вы успели тысячу раз пожалеть, "
            "что ввязались во всё это...",
            "Ваша кончина была быстрой. Вы даже не поняли, как погибли.",
        ],
    )


@pytest.fixture
def sample_enemy(sample_weapon, sample_armor) -> Enemy:
    """Фикстура: создание тестового врага"""
    return Enemy(
        name="Скелет",
        health=50,
        weapon=sample_weapon,
        armor=sample_armor,
        description="Обыкновенный бродячий костяк. Творение некромантов самоучек.",
        death_description="Груда костей, рассыпалась по всей комнате.",
    )


@pytest.fixture
def weak_enemy() -> Enemy:
    """Фикстура: создание слабого врага"""
    weapon = Weapon(
        name="Палка",
        description="Старая палка, едва пригодная для драки.",
        damage=1,
        hit_chance=50,
    )
    armor = Armor(
        name="Рваные лохмотья",
        description=(
            "Сложно уже сказать, что это за одежда была раньше. Теперь это однородная "
            "грязная масса, которая прилипла к телу."
        ),
        defense=0,
    )
    return Enemy(
        name="Пещерный гоблин",
        health=5,
        weapon=weapon,
        armor=armor,
        description="Мелкий безобразный гоблин. Очень хитрый и подлый.",
        death_description="Небольшая тушка лежит на полу в луже собственного ихора",
    )


@pytest.fixture
def strong_enemy() -> Enemy:
    """Фикстура: создание сильного врага"""
    weapon = Weapon(
        name="Лопата могильщика",
        description="Добротная лопата, которой можно возделывать землю или рыть могилы.",
        damage=50,
        hit_chance=100,
    )
    armor = Armor(
        name="Кожаные доспехи",
        description=(
            "Незамысловатые кожаные доспехи, которые от времени частично "
            "ссохлись и потрескались."
        ),
        defense=10,
    )
    return Enemy(
        name="Зомби",
        health=100,
        weapon=weapon,
        armor=armor,
        description="Полуразложившийся ходячий труп, который бесцельно бродит из стороны в сторону.",
        death_description="Зловонная туша распласталась на полу. Больше признаков жизни не подает.",
    )


@pytest.fixture
def empty_room() -> Room:
    """Фикстура: создание пустой комнаты"""
    return Room("Rm", "Пустая темная комната", None)


@pytest.fixture
def room_with_enemy(sample_enemy) -> Room:
    """Фикстура: создание комнаты с врагом"""
    return Room("Rm", "Комната с врагом", sample_enemy)
