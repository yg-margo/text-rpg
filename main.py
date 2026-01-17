"""Точка входа в текстовую RPG-игру"""

from src.dungeon import DungeonGenerator
from src.controller import GameController


def main():
    """Главная функция запуска игры"""
    try:
        generator = DungeonGenerator(data_dir="data")
        controller = GameController(generator)
        controller.initialize_game(num_rooms=5)
        controller.run()

    except FileNotFoundError as e:
        print(f"Ошибка: Не удалось найти файл данных - {e}")
    except KeyboardInterrupt:
        print("\n\nИгра прервана. До свидания!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()