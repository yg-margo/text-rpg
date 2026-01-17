"""Боевая система с режимом автобоя"""

import random
from typing import Tuple, List

from src.entities import Player, Enemy
from src.dungeon import DungeonGenerator


class CombatSystem:
    """Отвечает за проведение боя между игроком и противником"""

    def __init__(self, dungeon_generator: DungeonGenerator):
        self.generator = dungeon_generator
        self.combat_log: List[str] = []

    @staticmethod
    def _check_hit(hit_chance: int) -> bool:
        """Проверка, попала ли атака, исходя из шанса попадания"""
        roll = random.randint(1, 100)
        return hit_chance >= roll

    def _attack(self, attacker, defender, is_player_attacking: bool) -> Tuple[bool, int]:
        """Выполнить одну атаку"""
        hit = self._check_hit(attacker.weapon.hit_chance)
        if hit:
            actual_damage = defender.take_damage(attacker.weapon.damage)
            return True, actual_damage
        else:
            return False, 0

    def auto_battle(self, player: Player, enemy: Enemy) -> bool:
        """
        Запустить автоматический бой между игроком и противником.

        Возвращает:
            True – если победил игрок,
            False – если победил противник (или ничья, где игрок отступает).
        """
        self.combat_log = []
        max_rounds = 100
        round_count = 0

        self.combat_log.append("=" * 50)
        self.combat_log.append("Состояние здоровья у вас:")
        self.combat_log.append(f"{player.name}. Здоровье: {player.current_health}/{player.max_health}")
        self.combat_log.append(f"\033[92m{player.get_health_bar()}\033[0m")
        self.combat_log.append("")
        self.combat_log.append("Состояние здоровья у противника:")
        self.combat_log.append(f"{enemy.name}. Здоровье: {enemy.current_health}/{enemy.max_health}")
        self.combat_log.append(f"\033[91m{enemy.get_health_bar()}\033[0m")
        self.combat_log.append("")
        self.combat_log.append("Вы решительно бросаетесь на противника. Завязался бой!")
        self.combat_log.append("=" * 50)

        while player.is_alive() and enemy.is_alive() and round_count < max_rounds:
            round_count += 1

            self.combat_log.append("\nВы наносите удар!")
            player_hit, player_damage = self._attack(player, enemy, True)
            if player_hit:
                msg = self.generator.get_attack_message(
                    "player_hit",
                    damage=player_damage,
                    target=enemy.name,
                )
                self.combat_log.append(msg)
            else:
                msg = self.generator.get_attack_message(
                    "player_miss",
                    target=enemy.name,
                )
                self.combat_log.append(msg)

            self.combat_log.append("\nСостояние здоровья у противника:")
            self.combat_log.append(f"{enemy.name}. Здоровье: {enemy.current_health}/{enemy.max_health}")
            self.combat_log.append(f"\033[91m{enemy.get_health_bar()}\033[0m")

            if not enemy.is_alive():
                break

            self.combat_log.append(f"\n{enemy.name} наносит ответный удар. Берегитесь!")
            enemy_hit, enemy_damage = self._attack(enemy, player, False)
            if enemy_hit:
                msg = self.generator.get_attack_message(
                    "enemy_hit",
                    damage=enemy_damage,
                    attacker=enemy.name,
                )
                self.combat_log.append(msg)
            else:
                msg = self.generator.get_attack_message(
                    "enemy_miss",
                    attacker=enemy.name,
                )
                self.combat_log.append(msg)

            self.combat_log.append("\nСостояние здоровья у вас:")
            self.combat_log.append(f"{player.name}. Здоровье: {player.current_health}/{player.max_health}")
            self.combat_log.append(f"\033[92m{player.get_health_bar()}\033[0m")

        if round_count >= max_rounds:
            self.combat_log.append("\n" + "=" * 50)
            self.combat_log.append("Бой затянулся! Ничья по времени.")
            if player.current_health > enemy.current_health:
                self.combat_log.append(f"Но {enemy.name} отступает первым!")
                enemy.defeat()
                return True
            else:
                self.combat_log.append("Вы вынуждены отступить...")
                return False

        self.combat_log.append("\n" + "=" * 50)
        if player.is_alive():
            victory_msg = self.generator.get_victory_message(enemy)
            self.combat_log.append(victory_msg)
            enemy.defeat()
            return True
        else:
            death_msg = random.choice(player.death_descriptions)
            self.combat_log.append(f"Вы погибли... {death_msg}")
            return False

    def get_combat_log(self) -> str:
        """Вернуть форматированный текстовый лог боя одной строкой"""
        return "\n".join(self.combat_log)
