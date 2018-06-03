from game_messages import Message


# noinspection PyUnresolvedReferences
class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

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
