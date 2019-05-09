class Stairs:
    def __init__(self, floor):
        self.floor = floor  # Which floor does this stair lead to?

    def to_json(self):
        json_data = {
            'floor': self.floor
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        floor = json_data.get('floor')

        stairs = Stairs(floor)

        return stairs
