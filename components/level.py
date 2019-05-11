import constants


class Level:
    def __init__(self, current_level: int = 1, current_xp: int = 0):
        self.current_level = current_level
        self.current_xp = current_xp

    @property
    def experience_to_next_level(self):
        return constants.level_up_base + self.current_level * constants.level_up_factor

    def add_xp(self, xp: int):
        self.current_xp += xp

        if self.current_xp >= self.experience_to_next_level:
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1

            return True
        else:
            return False

    def to_json(self):
        json_data = {
            'current_level': self.current_level,
            'current_xp': self.current_xp,
        }

        return json_data

    @staticmethod
    def from_json(json_data: dict):
        current_level = json_data.get('current_level')
        current_xp = json_data.get('current_xp')

        level = Level(current_level, current_xp)

        return level
