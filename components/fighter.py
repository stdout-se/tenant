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

    def to_json(self):
        json_data = {
            'base_max_hp': self.base_max_hp,
            'hp': self.hp,
            'base_defense': self.base_defense,
            'base_power': self.base_power,
            'xp': self.xp
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        base_max_hp = json_data.get('base_max_hp')
        hp = json_data.get('hp')
        base_defense = json_data.get('base_defense')
        base_power = json_data.get('base_power')
        xp = json_data.get('xp')

        fighter = Fighter(base_max_hp, base_defense, base_power, xp)
        fighter.hp = hp

        return fighter
