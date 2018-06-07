from game_messages import Message


# noinspection PyUnresolvedReferences
class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp

    @property
    def is_alive(self):
        return self.hp > 0

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({
                'dead': self.owner,
                'xp': self.xp,
            })

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        attacker = self.owner.name.capitalize()

        if damage > 0:
            target.fighter.take_damage(damage)
            results.append({
                'message': Message(f'{attacker} attacks {target.name} for {damage} hit points')
            })
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({
                'message': Message(f'{attacker} attacks {target.name}, but does no damage')
            })

        return results
