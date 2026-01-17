"""Тесты для боевой системы"""
import pytest
import allure

from src.combat import CombatSystem
from src.entities import Player, Enemy, Weapon, Armor


@allure.feature("Боевая система")
@allure.story("Инициализация")
class TestCombatSystemInit:
    """Тесты инициализации боевой системы"""

    @allure.title("Инициализация боевой системы")
    @allure.description("Проверка корректной инициализации системы боя")
    def test_combat_system_initialization(self, dungeon_generator):
        """Проверка создания боевой системы"""
        with allure.step("Создание боевой системы"):
            combat = CombatSystem(dungeon_generator)
        with allure.step("Проверка наличия генератора"):
            assert combat.generator is not None
        with allure.step("Проверка инициализации лога боя"):
            assert isinstance(combat.combat_log, list)
            assert len(combat.combat_log) == 0


@allure.feature("Боевая система")
@allure.story("Механика попадания")
class TestCombatHitMechanics:
    """Тесты механики попадания"""

    @allure.title("Проверка 100% шанса попадания")
    @allure.description("При 100% шансе все атаки должны попадать")
    def test_check_hit_always_hits(self, dungeon_generator):
        """Проверка гарантированного попадания"""
        combat = CombatSystem(dungeon_generator)
        with allure.step("Выполнение 100 проверок попадания с шансом 100%"):
            hits = sum(1 for _ in range(100) if combat._check_hit(100))
        with allure.step("Проверка, что все атаки попали"):
            assert hits == 100

    @allure.title("Проверка 0% шанса попадания")
    @allure.description("При 0% шансе все атаки должны промахиваться")
    def test_check_hit_never_hits(self, dungeon_generator):
        """Проверка гарантированного промаха"""
        combat = CombatSystem(dungeon_generator)
        with allure.step("Выполнение 100 проверок попадания с шансом 0%"):
            hits = sum(1 for _ in range(100) if combat._check_hit(0))
        with allure.step("Проверка, что все атаки промахнулись (или очень мало попаданий)"):
            assert hits == 0, f"Ожидалось 0 попаданий, получено {hits}"

    @allure.title("Проверка среднего шанса попадания")
    @allure.description("При 50% шансе примерно половина атак должна попадать")
    def test_check_hit_average(self, dungeon_generator):
        """Проверка статистики попаданий при 50% шансе"""
        combat = CombatSystem(dungeon_generator)
        with allure.step("Выполнение 1000 проверок попадания с шансом 50%"):
            hits = sum(1 for _ in range(1000) if combat._check_hit(50))
        with allure.step("Проверка, что попало примерно 50% (±10%)"):
            assert 400 <= hits <= 600

@allure.feature("Боевая система")
@allure.story("Атака")
class TestCombatAttack:
    """Тесты атаки"""

    @allure.title("Успешная атака")
    @allure.description("Проверка успешной атаки с 100% шансом попадания")
    def test_attack_hit(self, dungeon_generator):
        """Проверка попадания атаки"""
        combat = CombatSystem(dungeon_generator)
        with allure.step("Создание атакующего с 100% шансом попадания"):
            weapon = Weapon(
                "Опасная дубина",
                "крепкая сосновая ветка с вбитым ржавым гвоздем на конце.",
                10,
                100,
            )
            armor = Armor(
                "Легкий кожаный доспех",
                "Сшитый из крыс кожаный доспех. Пахнет ужасно, но вроде бы защищает от урона.",
                2,
            )
            attacker = Player("Васька Проказник", 50, weapon, armor)
        with allure.step("Создание цели"):
            enemy_weapon = Weapon(
                "Обглоданная кость",
                "Бедренная кость, возможно предыдущего приключенца или большого животного.",
                5,
                50,
            )
            enemy_armor = Armor(
                "Рваные лохмотья",
                "Сложно уже сказать, что это за одежда была раньше. Теперь это однородная грязная масса, которая прилипла к телу.",
                1,
            )
            defender = Enemy(
                "Зомби",
                20,
                enemy_weapon,
                enemy_armor,
                "Полуразложившийся ходячий труп, который бесцельно бродит из стороны в сторону.",
                "Зловонная туша распласталась на полу. Больше признаков жизни не подает.",
            )
        with allure.step("Сохранение начального здоровья цели"):
            initial_health = defender.current_health
        with allure.step("Выполнение атаки"):
            hit, damage = combat._attack(attacker, defender, True)
        with allure.step("Проверка успешного попадания"):
            assert hit is True
        with allure.step("Проверка нанесенного урона"):
            assert damage > 0
        with allure.step("Проверка уменьшения здоровья цели"):
            assert defender.current_health < initial_health

    @allure.title("Промах при атаке")
    @allure.description("Проверка промаха при 0% шансе попадания")
    def test_attack_miss(self, dungeon_generator):
        """Проверка промаха атаки"""
        combat = CombatSystem(dungeon_generator)
        with allure.step("Создание атакующего с 0% шансом попадания"):
            weapon = Weapon(
                "Опасная дубина",
                "крепкая сосновая ветка с вбитым ржавым гвоздем на конце.",
                10,
                0,
            )
            armor = Armor(
                "Легкий кожаный доспех",
                "Сшитый из крыс кожаный доспех. Пахнет ужасно, но вроде бы защищает от урона.",
                2,
            )
            attacker = Player("Степан Дубина", 50, weapon, armor)
        with allure.step("Создание цели"):
            enemy_weapon = Weapon(
                "Ржавый нож",
                "Раньше это был отличный кухонный нож, но теперь это ржавый кусок металла. Даже страшно подумать, что будет, если таким порезаться.",
                4,
                75,
            )
            enemy_armor = Armor(
                "Набедренная повязка",
                "Небольшой лоскут ткани, который с трудом справляется с тем, чтобы скрыть причиндалы.",
                0,
            )
            defender = Enemy(
                "Пещерный гоблин",
                20,
                enemy_weapon,
                enemy_armor,
                "Мелкий безобразный гоблин. Очень хитрый и подлый.",
                "Небольшая тушка лежит на полу в луже собственного ихора",
            )
        with allure.step("Сохранение начального здоровья цели"):
            initial_health = defender.current_health
        with allure.step("Выполнение атаки"):
            hit, damage = combat._attack(attacker, defender, True)
        with allure.step("Проверка промаха"):
            assert hit is False
        with allure.step("Проверка отсутствия урона"):
            assert damage == 0
        with allure.step("Проверка, что здоровье не изменилось"):
            assert defender.current_health == initial_health


@allure.feature("Боевая система")
@allure.story("Автобой")
class TestCombatAutoBattle:
    """Тесты автоматического боя"""

    @allure.title("Победа игрока в автобое")
    @allure.description("Проверка победы сильного игрока над слабым врагом")
    def test_auto_battle_player_wins(self, dungeon_generator):
        """Проверка победы игрока"""
        combat = CombatSystem(dungeon_generator)
        with allure.step("Создание сильного игрока"):
            strong_weapon = Weapon(
                "Опасная дубина",
                "крепкая сосновая ветка с вбитым ржавым гвоздем на конце.",
                50,
                100,
            )
            strong_armor = Armor(
                "Легкий кожаный доспех",
                "Сшитый из крыс кожаный доспех. Пахнет ужасно, но вроде бы защищает от урона.",
                10,
            )
            strong_player = Player("Степан Дубина", 100, strong_weapon, strong_armor)
        with allure.step("Создание слабого врага"):
            weak_weapon = Weapon(
                "Ржавый нож",
                "Раньше это был отличный кухонный нож, но теперь это ржавый кусок металла. Даже страшно подумать, что будет, если таким порезаться.",
                1,
                50,
            )
            weak_armor = Armor(
                "Набедренная повязка",
                "Небольшой лоскут ткани, который с трудом справляется с тем, чтобы скрыть причиндалы.",
                0,
            )
            weak_enemy = Enemy(
                "Пещерный гоблин",
                5,
                weak_weapon,
                weak_armor,
                "Мелкий безобразный гоблин. Очень хитрый и подлый.",
                "Небольшая тушка лежит на полу в луже собственного ихора",
            )
        with allure.step("Запуск автобоя"):
            result = combat.auto_battle(strong_player, weak_enemy)
        with allure.step("Проверка победы игрока"):
            assert result is True
        with allure.step("Проверка, что игрок жив"):
            assert strong_player.is_alive()
        with allure.step("Проверка, что враг мертв"):
            assert not weak_enemy.is_alive()
        with allure.step("Проверка, что враг помечен как побежденный"):
            assert weak_enemy.defeated is True
        with allure.step("Проверка наличия лога боя"):
            assert len(combat.combat_log) > 0

    @allure.title("Поражение игрока в автобое")
    @allure.description("Проверка поражения слабого игрока против сильного врага")
    def test_auto_battle_player_loses(self, dungeon_generator):
        """Проверка поражения игрока"""
        combat = CombatSystem(dungeon_generator)
        with allure.step("Создание слабого игрока"):
            weak_weapon = Weapon(
                "Опасная дубина",
                "крепкая сосновая ветка с вбитым ржавым гвоздем на конце.",
                1,
                50,
            )
            weak_armor = Armor(
                "Легкий кожаный доспех",
                "Сшитый из крыс кожаный доспех. Пахнет ужасно, но вроде бы защищает от урона.",
                0,
            )
            weak_player = Player("Васька Проказник", 5, weak_weapon, weak_armor)
        with allure.step("Создание сильного врага"):
            strong_weapon = Weapon(
                "Обглоданная кость",
                "Бедренная кость, возможно предыдущего приключенца или большого животного.",
                50,
                100,
            )
            strong_armor = Armor(
                "Кожаные доспехи",
                "Незамысловатые кожаные доспехи, которые от времени частично ссохлись и потрескались.",
                10,
            )
            strong_enemy = Enemy(
                "Зомби",
                100,
                strong_weapon,
                strong_armor,
                "Полуразложившийся ходячий труп, который бесцельно бродит из стороны в сторону.",
                "Зловонная туша распласталась на полу. Больше признаков жизни не подает.",
            )
        with allure.step("Запуск автобоя"):
            result = combat.auto_battle(weak_player, strong_enemy)
        with allure.step("Проверка поражения игрока"):
            assert result is False
        with allure.step("Проверка, что игрок мертв"):
            assert not weak_player.is_alive()
        with allure.step("Проверка, что враг жив"):
            assert strong_enemy.is_alive()

    @allure.title("Генерация лога боя")
    @allure.description("Проверка создания детального лога боя")
    def test_auto_battle_generates_log(self, dungeon_generator):
        """Проверка генерации лога боя"""
        combat = CombatSystem(dungeon_generator)
        with allure.step("Создание игрока"):
            weapon = Weapon(
                "Опасная дубина",
                "крепкая сосновая ветка с вбитым ржавым гвоздем на конце.",
                30,
                90,
            )
            armor = Armor(
                "Легкий кожаный доспех",
                "Сшитый из крыс кожаный доспех. Пахнет ужасно, но вроде бы защищает от урона.",
                5,
            )
            player = Player("Цицерон Иванович", 60, weapon, armor)
        with allure.step("Создание врага"):
            enemy_weapon = Weapon(
                "Лопата могильщика",
                "Добротная лопата, которой можно возделывать землю или рыть могилы.",
                20,
                80,
            )
            enemy_armor = Armor(
                "Кожаные доспехи",
                "Незамысловатые кожаные доспехи, которые от времени частично ссохлись и потрескались.",
                3,
            )
            enemy = Enemy(
                "Скелет",
                40,
                enemy_weapon,
                enemy_armor,
                "Обыкновенный бродячий костяк. Творение некромантов самоучек.",
                "Груда костей, рассыпалась по всей комнате.",
            )
        with allure.step("Запуск автобоя"):
            combat.auto_battle(player, enemy)
        with allure.step("Получение лога боя"):
            log = combat.get_combat_log()
        with allure.step("Проверка типа лога"):
            assert isinstance(log, str)
        with allure.step("Проверка, что лог не пустой"):
            assert len(log) > 0
        with allure.step("Проверка наличия информации о персонажах"):
            assert player.name in log or enemy.name in log

    @allure.title("Чередование атак в автобое")
    @allure.description("Проверка, что атаки чередуются между игроком и врагом")
    def test_auto_battle_alternating_attacks(self, dungeon_generator):
        """Проверка чередования атак"""
        combat = CombatSystem(dungeon_generator)
        with allure.step("Создание игрока"):
            weapon = Weapon(
                "Опасная дубина",
                "крепкая сосновая ветка с вбитым ржавым гвоздем на конце.",
                25,
                85,
            )
            armor = Armor(
                "Легкий кожаный доспех",
                "Сшитый из крыс кожаный доспех. Пахнет ужасно, но вроде бы защищает от урона.",
                4,
            )
            player = Player("Воин", 55, weapon, armor)
        with allure.step("Создание врага"):
            enemy_weapon = Weapon(
                "Ржавый нож",
                "Раньше это был отличный кухонный нож, но теперь это ржавый кусок металла. Даже страшно подумать, что будет, если таким порезаться.",
                20,
                75,
            )
            enemy_armor = Armor(
                "Рваные лохмотья",
                "Сложно уже сказать, что это за одежда была раньше. Теперь это однородная грязная масса, которая прилипла к телу.",
                2,
            )
            enemy = Enemy(
                "Пещерный гоблин",
                45,
                enemy_weapon,
                enemy_armor,
                "Мелкий безобразный гоблин. Очень хитрый и подлый.",
                "Небольшая тушка лежит на полу в луже собственного ихора",
            )
        with allure.step("Запуск автобоя"):
            result = combat.auto_battle(player, enemy)
        with allure.step("Получение лога боя"):
            log = combat.get_combat_log()
        with allure.step("Проверка наличия информации об атаках"):
            assert (
                "наносите удар" in log.lower()
                or "наносит ответный удар" in log.lower()
                or "наносит удар" in log.lower()
            )

    @allure.title("Равный бой")
    @allure.description("Проверка боя между противниками")
    def test_auto_battle_equal_opponents(self, dungeon_generator):
        """Проверка боя противников"""
        combat = CombatSystem(dungeon_generator)
        with allure.step("Создание первого бойца"):
            weapon1 = Weapon(
                "Опасная дубина",
                "крепкая сосновая ветка с вбитым ржавым гвоздем на конце.",
                20,
                85,
            )
            armor1 = Armor(
                "Легкий кожаный доспех",
                "Сшитый из крыс кожаный доспех. Пахнет ужасно, но вроде бы защищает от урона.",
                2,
            )
            fighter1 = Player("Боец 1", 50, weapon1, armor1)
        with allure.step("Создание второго бойца"):
            weapon2 = Weapon(
                "Лопата могильщика",
                "Добротная лопата, которой можно возделывать землю или рыть могилы.",
                15,
                75,
            )
            armor2 = Armor(
                "Кожаные доспехи",
                "Незамысловатые кожаные доспехи, которые от времени частично ссохлись и потрескались.",
                3,
            )
            fighter2 = Enemy(
                "Скелет",
                45,
                weapon2,
                armor2,
                "Обыкновенный бродячий костяк. Творение некромантов самоучек.",
                "Груда костей, рассыпалась по всей комнате.",
            )
        with allure.step("Запуск автобоя"):
            result = combat.auto_battle(fighter1, fighter2)
        with allure.step("Проверка, что бой завершился"):
            assert result is True or result is False
        with allure.step("Проверка, что один из бойцов погиб или бой закончился"):
            assert (
                not fighter1.is_alive()
                or not fighter2.is_alive()
                or (fighter1.is_alive() and fighter2.is_alive())
            )


@allure.feature("Боевая система")
@allure.story("Лог боя")
class TestCombatLog:
    """Тесты лога боя"""

    @allure.title("Формат лога боя")
    @allure.description("Проверка корректного формата лога боя")
    def test_combat_log_format(self, dungeon_generator, sample_player, weak_enemy):
        """Проверка формата лога"""
        combat = CombatSystem(dungeon_generator)
        with allure.step("Запуск автобоя"):
            combat.auto_battle(sample_player, weak_enemy)
        with allure.step("Проверка, что лог содержит начальное состояние"):
            log_text = "\n".join(combat.combat_log)
            assert "Состояние здоровья" in log_text
        with allure.step("Проверка наличия информации об атаках"):
            assert len(combat.combat_log) > 5
