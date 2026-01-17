"""Тесты для игрового контроллера"""
import pytest
import allure
from unittest.mock import patch

from src.controller import GameController
from src.entities import Weapon, Armor, Enemy


@allure.feature("Игровой контроллер")
@allure.story("Инициализация")
class TestGameControllerInit:
    """Тесты инициализации контроллера"""

    @allure.title("Инициализация контроллера")
    @allure.description("Проверка корректной инициализации игрового контроллера")
    def test_controller_initialization(self, dungeon_generator):
        """Проверка начального состояния контроллера"""
        with allure.step("Создание контроллера"):
            controller = GameController(dungeon_generator)
        with allure.step("Проверка наличия генератора"):
            assert controller.generator is not None
        with allure.step("Проверка наличия боевой системы"):
            assert controller.combat_system is not None
        with allure.step("Проверка отсутствия игрока"):
            assert controller.player is None
        with allure.step("Проверка пустого подземелья"):
            assert controller.dungeon == []
        with allure.step("Проверка начальной позиции"):
            assert controller.current_position == 0
        with allure.step("Проверка флага запуска"):
            assert controller.running is False

    @allure.title("Инициализация игры")
    @allure.description("Проверка инициализации игры с созданием игрока и подземелья")
    @pytest.mark.parametrize("num_rooms", [2, 3, 5, 10])
    def test_initialize_game(self, dungeon_generator, num_rooms):
        """Проверка инициализации игры с разным количеством комнат"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step(f"Инициализация игры с {num_rooms} комнатами"):
                    controller.initialize_game(num_rooms=num_rooms)
        with allure.step("Проверка создания игрока"):
            assert controller.player is not None
        with allure.step(f"Проверка количества комнат: {num_rooms}"):
            assert len(controller.dungeon) == num_rooms
        with allure.step("Проверка стартовой позиции"):
            assert controller.current_position == 0
        with allure.step("Проверка флага запуска игры"):
            assert controller.running is True


@allure.feature("Игровой контроллер")
@allure.story("Навигация")
class TestGameControllerNavigation:
    """Тесты навигации по подземелью"""

    @allure.title("Получение текущей комнаты")
    @allure.description("Проверка получения текущей комнаты игрока")
    def test_get_current_room(self, dungeon_generator):
        """Проверка получения текущей комнаты"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=3)
        with allure.step("Получение текущей комнаты"):
            room = controller.get_current_room()
        with allure.step("Проверка соответствия комнаты"):
            assert room == controller.dungeon[0]
        with allure.step("Проверка типа стартовой комнаты"):
            assert room.room_type == "St"

    @allure.title("Движение вперед")
    @allure.description("Проверка перехода в следующую комнату")
    def test_execute_action_forward(self, dungeon_generator):
        """Проверка движения вперед"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=5)
        with allure.step("Сохранение начальной позиции"):
            initial_position = controller.current_position
        with allure.step("Выполнение действия 'forward'"):
            result = controller.execute_action("forward")
        with allure.step("Проверка успешности действия"):
            assert result is True
        with allure.step("Проверка увеличения позиции"):
            assert controller.current_position == initial_position + 1

    @allure.title("Движение назад")
    @allure.description("Проверка возврата в предыдущую комнату")
    def test_execute_action_back(self, dungeon_generator):
        """Проверка движения назад"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=5)
        with allure.step("Перемещение в комнату 2"):
            controller.current_position = 2
            initial_position = controller.current_position
        with allure.step("Выполнение действия 'back'"):
            result = controller.execute_action("back")
        with allure.step("Проверка успешности действия"):
            assert result is True
        with allure.step("Проверка уменьшения позиции"):
            assert controller.current_position == initial_position - 1


@allure.feature("Игровой контроллер")
@allure.story("Доступные действия")
class TestGameControllerActions:
    """Тесты доступных действий"""

    @allure.title("Действия в стартовой пустой комнате")
    @allure.description("Проверка доступных действий в начале игры")
    def test_get_available_actions_start_room_empty(self, dungeon_generator):
        """Проверка действий в стартовой комнате"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=3)
        with allure.step("Получение доступных действий"):
            actions = controller.get_available_actions()
            action_types = [action[0] for action in actions.values()]
        with allure.step("Проверка наличия действия 'forward'"):
            assert "forward" in action_types
        with allure.step("Проверка отсутствия действия 'back'"):
            assert "back" not in action_types
        with allure.step("Проверка отсутствия действия 'attack'"):
            assert "attack" not in action_types
        with allure.step("Проверка отсутствия действия 'exit'"):
            assert "exit" not in action_types

    @allure.title("Действия в комнате с врагом")
    @allure.description("Проверка доступных действий при наличии врага")
    def test_get_available_actions_with_enemy(self, dungeon_generator):
        """Проверка действий в комнате с врагом"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=5)
        with allure.step("Перемещение в комнату 1"):
            controller.current_position = 1
            room = controller.get_current_room()
        with allure.step("Добавление врага в комнату"):
            weapon = Weapon(
                "Ржавый нож",
                "Раньше это был отличный кухонный нож, но теперь это ржавый кусок металла. Даже страшно подумать, что будет, если таким порезаться.",
                4,
                75,
            )
            armor = Armor(
                "Кожаные доспехи",
                "Незамысловатые кожаные доспехи, которые от времени частично ссохлись и потрескались.",
                3,
            )
            enemy = Enemy(
                "Скелет",
                20,
                weapon,
                armor,
                "Обыкновенный бродячий костяк. Творение некромантов самоучек.",
                "Груда костей, рассыпалась по всей комнате.",
            )
            room.enemy = enemy
        with allure.step("Получение доступных действий"):
            actions = controller.get_available_actions()
            action_types = [action[0] for action in actions.values()]
        with allure.step("Проверка наличия действия 'attack'"):
            assert "attack" in action_types
        with allure.step("Проверка отсутствия действия 'forward'"):
            assert "forward" not in action_types
        with allure.step("Проверка наличия действия 'back'"):
            assert "back" in action_types

    @allure.title("Действия в выходной комнате")
    @allure.description("Проверка доступных действий в последней комнате")
    def test_get_available_actions_exit_room(self, dungeon_generator):
        """Проверка действий в выходной комнате"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=3)
        with allure.step("Перемещение в выходную комнату"):
            controller.current_position = len(controller.dungeon) - 1
        with allure.step("Получение доступных действий"):
            actions = controller.get_available_actions()
            action_types = [action[0] for action in actions.values()]
        with allure.step("Проверка наличия действия 'exit'"):
            assert "exit" in action_types
        with allure.step("Проверка отсутствия действия 'forward'"):
            assert "forward" not in action_types
        with allure.step("Проверка наличия действия 'back'"):
            assert "back" in action_types

    @allure.title("Действия после победы над врагом")
    @allure.description("Проверка, что после победы можно двигаться дальше")
    def test_get_available_actions_after_enemy_defeated(self, dungeon_generator):
        """Проверка действий после победы"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=5)
        with allure.step("Перемещение в комнату 1"):
            controller.current_position = 1
            room = controller.get_current_room()
        with allure.step("Добавление побежденного врага"):
            weapon = Weapon(
                "Ржавый нож",
                "Раньше это был отличный кухонный нож, но теперь это ржавый кусок металла. Даже страшно подумать, что будет, если таким порезаться.",
                4,
                75,
            )
            armor = Armor(
                "Кожаные доспехи",
                "Незамысловатые кожаные доспехи, которые от времени частично ссохлись и потрескались.",
                3,
            )
            enemy = Enemy(
                "Побежденный враг",
                20,
                weapon,
                armor,
                "Враг",
                "Мертв",
            )
            enemy.defeat()
            room.enemy = enemy
        with allure.step("Получение доступных действий"):
            actions = controller.get_available_actions()
            action_types = [action[0] for action in actions.values()]
        with allure.step("Проверка наличия действия 'forward'"):
            assert "forward" in action_types
        with allure.step("Проверка отсутствия действия 'attack'"):
            assert "attack" not in action_types


@allure.feature("Игровой контроллер")
@allure.story("Выполнение действий")
class TestGameControllerActionExecution:
    """Тесты выполнения действий"""

    @allure.title("Выход из подземелья")
    @allure.description("Проверка завершения игры при выходе")
    def test_execute_action_exit(self, dungeon_generator):
        """Проверка действия выхода"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=3)
        with allure.step("Выполнение действия 'exit'"):
            result = controller.execute_action("exit")
        with allure.step("Проверка, что игра завершилась"):
            assert result is False

    @allure.title("Прерывание игры")
    @allure.description("Проверка действия quit")
    def test_execute_action_quit(self, dungeon_generator):
        """Проверка действия quit"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=3)
        with allure.step("Выполнение действия 'quit'"):
            result = controller.execute_action("quit")
        with allure.step("Проверка, что игра завершилась"):
            assert result is False

    @allure.title("Победа в бою")
    @allure.description("Проверка продолжения игры после победы над врагом")
    def test_execute_action_attack_victory(self, dungeon_generator):
        """Проверка атаки с победой"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=5)
        with allure.step("Создание слабого врага"):
            weapon = Weapon(
                "Ржавый нож",
                "Раньше это был отличный кухонный нож, но теперь это ржавый кусок металла. Даже страшно подумать, что будет, если таким порезаться.",
                1,
                50,
            )
            armor = Armor(
                "Набедренная повязка",
                "Небольшой лоскут ткани, который с трудом справляется с тем, чтобы скрыть причиндалы.",
                0,
            )
            weak_enemy = Enemy(
                "Пещерный гоблин",
                1,
                weapon,
                armor,
                "Слабый",
                "Мертв",
            )
        with allure.step("Добавление врага в текущую комнату"):
            room = controller.get_current_room()
            room.enemy = weak_enemy
        with allure.step("Выполнение действия 'attack'"):
            result = controller.execute_action("attack")
        with allure.step("Проверка продолжения игры"):
            assert result is True
        with allure.step("Проверка, что враг побежден"):
            assert weak_enemy.defeated is True

    @allure.title("Поражение в бою")
    @allure.description("Проверка завершения игры при поражении")
    def test_execute_action_attack_defeat(self, dungeon_generator):
        """Проверка атаки с поражением"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=5)
        with allure.step("Ослабление игрока"):
            controller.player.current_health = 1
            controller.player.weapon.damage = 1
        with allure.step("Создание сильного врага"):
            weapon = Weapon(
                "Обглоданная кость",
                "Бедренная кость, возможно предыдущего приключенца или большого животного.",
                100,
                100,
            )
            armor = Armor(
                "Кожаные доспехи",
                "Незамысловатые кожаные доспехи, которые от времени частично ссохлись и потрескались.",
                50,
            )
            strong_enemy = Enemy(
                "Зомби",
                100,
                weapon,
                armor,
                "Сильный",
                "Мертв",
            )
        with allure.step("Добавление врага в текущую комнату"):
            room = controller.get_current_room()
            room.enemy = strong_enemy
        with allure.step("Выполнение действия 'attack'"):
            result = controller.execute_action("attack")
        with allure.step("Проверка завершения игры"):
            assert result is False


@allure.feature("Игровой контроллер")
@allure.story("Ввод пользователя")
class TestGameControllerUserInput:
    """Тесты обработки ввода пользователя"""

    @allure.title("Корректный ввод")
    @allure.description("Проверка обработки корректного ввода")
    def test_get_user_input_valid(self, dungeon_generator):
        """Проверка валидного ввода"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=3)
        with allure.step("Создание списка действий"):
            actions = {1: ("forward", "Пойти дальше"), 2: ("back", "Назад")}
        with patch("builtins.input", return_value="1"):
            with allure.step("Ввод значения '1'"):
                result = controller.get_user_input(actions)
        with allure.step("Проверка результата"):
            assert result == "forward"

    @allure.title("Некорректный ввод с последующим корректным")
    @allure.description("Проверка повторного запроса при неверном вводе")
    def test_get_user_input_invalid_then_valid(self, dungeon_generator):
        """Проверка обработки неверного ввода"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=3)
        with allure.step("Создание списка действий"):
            actions = {1: ("forward", "Пойти дальше")}
        with patch("builtins.input", side_effect=["5", "abc", "1"]):
            with patch("builtins.print"):
                with allure.step("Ввод неверных значений '5', 'abc', затем '1'"):
                    result = controller.get_user_input(actions)
        with allure.step("Проверка результата после корректного ввода"):
            assert result == "forward"

    @allure.title("Прерывание ввода")
    @allure.description("Проверка обработки KeyboardInterrupt")
    def test_get_user_input_keyboard_interrupt(self, dungeon_generator):
        """Проверка обработки прерывания"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=3)
        with allure.step("Создание списка действий"):
            actions = {1: ("forward", "Пойти дальше")}
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            with patch("builtins.print"):
                with allure.step("Симуляция прерывания"):
                    result = controller.get_user_input(actions)
        with allure.step("Проверка возврата 'quit'"):
            assert result == "quit"


@allure.feature("Игровой контроллер")
@allure.story("Отображение")
class TestGameControllerDisplay:
    """Тесты отображения информации"""

    @allure.title("Отображение комнаты помечает её как посещенную")
    @allure.description("Проверка, что display_room помечает комнату visited")
    def test_display_room_marks_visited(self, dungeon_generator):
        """Проверка отметки посещения комнаты"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=3)
        with allure.step("Получение текущей комнаты"):
            room = controller.get_current_room()
        with allure.step("Проверка, что комната не посещена"):
            assert room.visited is False
        with patch("builtins.print"):
            with allure.step("Отображение комнаты"):
                controller.display_room()
        with allure.step("Проверка, что комната помечена как посещенная"):
            assert room.visited is True

    @allure.title("Отображение доступных действий")
    @allure.description("Проверка метода display_actions")
    def test_display_actions(self, dungeon_generator):
        """Проверка отображения действий"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=3)
        with allure.step("Создание списка действий"):
            actions = {
                1: ("forward", "Пойти дальше"),
                2: ("back", "Вернуться назад"),
            }
        with patch("builtins.print") as mock_print:
            with allure.step("Отображение действий"):
                controller.display_actions(actions)
            with allure.step("Проверка, что print был вызван"):
                assert mock_print.called


@allure.feature("Игровой контроллер")
@allure.story("Игровой цикл")
class TestGameControllerGameLoop:
    """Тесты игрового цикла"""

    @allure.title("Быстрая победа - выход сразу")
    @allure.description("Проверка прохождения игры с немедленным выходом")
    def test_run_game_loop_exit_immediately(self, dungeon_generator):
        """Проверка немедленного выхода"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры с 2 комнатами"):
                    controller.initialize_game(num_rooms=2)
        with allure.step("Перемещение в выходную комнату"):
            controller.current_position = len(controller.dungeon) - 1
        # Симулируем выбор действия "exit" (обычно это пункт 1 в выходной комнате)
        with patch("builtins.input", return_value="1"):
            with patch("builtins.print"):
                with allure.step("Запуск игрового цикла"):
                    actions = controller.get_available_actions()
                    action_types = [action[0] for action in actions.values()]
                    if "exit" in action_types:
                        controller.execute_action("exit")
        with allure.step("Проверка, что игра завершена"):
            assert controller.running is False

    @allure.title("Игра не инициализирована")
    @allure.description("Проверка обработки запуска неинициализированной игры")
    def test_run_game_not_initialized(self, dungeon_generator):
        """Проверка запуска без инициализации"""
        controller = GameController(dungeon_generator)
        with patch("builtins.print") as mock_print:
            with allure.step("Попытка запуска неинициализированной игры"):
                controller.run()
            with allure.step("Проверка вывода сообщения об ошибке"):
                mock_print.assert_called()

    @allure.title("Полное прохождение игры")
    @allure.description("Проверка полного цикла игры от начала до конца")
    def test_run_full_game_walkthrough(self, dungeon_generator):
        """Проверка полного прохождения"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры с 3 комнатами"):
                    controller.initialize_game(num_rooms=3)
        with allure.step("Очистка комнат от врагов для свободного прохода"):
            for room in controller.dungeon:
                room.enemy = None
        with patch("builtins.input", side_effect=["1", "1", "1"]):
            with patch("builtins.print"):
                with allure.step("Прохождение всех комнат"):
                    actions1 = controller.get_available_actions()
                    action1 = controller.get_user_input(actions1)
                    controller.execute_action(action1)
                    actions2 = controller.get_available_actions()
                    action2 = controller.get_user_input(actions2)
                    controller.execute_action(action2)
        with allure.step("Проверка, что игрок достиг выходной комнаты"):
            assert controller.current_position == 2


@allure.feature("Игровой контроллер")
@allure.story("Интеграционные тесты")
class TestGameControllerIntegration:
    """Интеграционные тесты контроллера"""

    @allure.title("Сценарий: движение вперед-назад")
    @allure.description("Проверка навигации туда-обратно")
    def test_integration_forward_and_back(self, dungeon_generator):
        """Интеграционный тест навигации"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=4)
        with allure.step("Перемещение вперед на позицию 1"):
            controller.execute_action("forward")
            assert controller.current_position == 1
        with allure.step("Перемещение вперед на позицию 2"):
            controller.execute_action("forward")
            assert controller.current_position == 2
        with allure.step("Перемещение назад на позицию 1"):
            controller.execute_action("back")
            assert controller.current_position == 1
        with allure.step("Перемещение назад на позицию 0"):
            controller.execute_action("back")
            assert controller.current_position == 0

    @allure.title("Сценарий: бой и продвижение")
    @allure.description("Проверка боя с врагом и дальнейшего продвижения")
    def test_integration_combat_and_progress(self, dungeon_generator):
        """Интеграционный тест боя и продвижения"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=4)
        with allure.step("Перемещение в комнату 1"):
            controller.execute_action("forward")
        with allure.step("Добавление слабого врага"):
            weapon = Weapon(
                "Ржавый нож",
                "Раньше это был отличный кухонный нож, но теперь это ржавый кусок металла. Даже страшно подумать, что будет, если таким порезаться.",
                1,
                50,
            )
            armor = Armor(
                "Набедренная повязка",
                "Небольшой лоскут ткани, который с трудом справляется с тем, чтобы скрыть причиндалы.",
                0,
            )
            weak_enemy = Enemy(
                "Пещерный гоблин",
                1,
                weapon,
                armor,
                "Слабый",
                "Мертв",
            )
            controller.get_current_room().enemy = weak_enemy
        with allure.step("Атака врага"):
            result = controller.execute_action("attack")
            assert result is True
        with allure.step("Проверка победы"):
            assert weak_enemy.defeated is True
        with allure.step("Продвижение дальше после победы"):
            result = controller.execute_action("forward")
            assert result is True
            assert controller.current_position == 2

    @allure.title("Сценарий: несколько боев подряд")
    @allure.description("Проверка серии боев в разных комнатах")
    def test_integration_multiple_combats(self, dungeon_generator):
        """Интеграционный тест множественных боев"""
        controller = GameController(dungeon_generator)
        with patch("builtins.input", return_value=""):
            with patch("builtins.print"):
                with allure.step("Инициализация игры"):
                    controller.initialize_game(num_rooms=5)
        # Первый бой
        with allure.step("Первый бой в комнате 1"):
            controller.execute_action("forward")
            weapon1 = Weapon(
                "Ржавый нож",
                "Раньше это был отличный кухонный нож, но теперь это ржавый кусок металла. Даже страшно подумать, что будет, если таким порезаться.",
                1,
                50,
            )
            armor1 = Armor(
                "Набедренная повязка",
                "Небольшой лоскут ткани, который с трудом справляется с тем, чтобы скрыть причиндалы.",
                0,
            )
            enemy1 = Enemy(
                "Пещерный гоблин",
                2,
                weapon1,
                armor1,
                "Враг 1",
                "Мертв",
            )
            controller.get_current_room().enemy = enemy1
            controller.execute_action("attack")
            assert enemy1.defeated is True
        # Второй бой
        with allure.step("Второй бой в комнате 2"):
            controller.execute_action("forward")
            weapon2 = Weapon(
                "Лопата могильщика",
                "Добротная лопата, которой можно возделывать землю или рыть могилы.",
                2,
                50,
            )
            armor2 = Armor(
                "Кожаные доспехи",
                "Незамысловатые кожаные доспехи, которые от времени частично ссохлись и потрескались.",
                0,
            )
            enemy2 = Enemy(
                "Скелет",
                3,
                weapon2,
                armor2,
                "Враг 2",
                "Мертв",
            )
            controller.get_current_room().enemy = enemy2
            controller.execute_action("attack")
            assert enemy2.defeated is True
        with allure.step("Проверка, что игрок все еще жив"):
            assert controller.player.is_alive()
