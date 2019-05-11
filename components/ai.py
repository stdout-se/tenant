from random import randint
from typing import List

from game_messages import Message


class BaseAI:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, game_map, entities) -> List:
        raise NotImplementedError

    def to_json(self):
        json_data = {
            'name': self.__class__.__name__
        }

        return json_data

    @classmethod
    def from_json(cls, *args, **kwargs):
        return cls()


class BasicMonster(BaseAI):
    def take_turn(self, target, game_map, entities):
        results = []

        monster = self.owner

        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results


class ConfusedMonster(BaseAI):
    def __init__(self, previous_ai, number_of_turns=10):
        super().__init__()

        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, game_map, entities):
        results = []

        monster = self.owner

        if self.number_of_turns > 0:
            random_x = monster.x + randint(0, 2) - 1
            random_y = monster.y + randint(0, 2) - 1

            if random_x != monster.x and random_y != monster.y:
                monster.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            monster.ai = self.previous_ai
            results.append({
                'message': Message(f'The {monster.name} is no longer confused')
            })

        return results

    def to_json(self):
        json_data = {
            'name': self.__class__.__name__,
            'previous_ai': self.previous_ai.__class__.__name__,
            'number_of_turns': self.number_of_turns
        }

        return json_data

    @classmethod
    def from_json(cls, json_data: dict, owner):
        previous_ai_name = json_data.get('previous_ai')
        number_of_turns = json_data.get('number_of_turns')

        if previous_ai_name == 'BasicMonster':
            previous_ai = BasicMonster()
            previous_ai.owner = owner
        else:
            previous_ai = None

        return cls(previous_ai, number_of_turns)
