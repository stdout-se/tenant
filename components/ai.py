from random import randint

from game_messages import Message


class BasicMonster:
    def take_turn(self, target, game_map, entities):
        results = []

        # noinspection PyUnresolvedReferences
        monster = self.owner

        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results


class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    # noinspection PyUnusedLocal
    def take_turn(self, target, game_map, entities):
        results = []

        # noinspection PyUnresolvedReferences
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
