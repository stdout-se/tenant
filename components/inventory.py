import colors
from game_messages import Message


class Inventory:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full', colors.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message(f'You pick up the {item.name}!', colors.light_blue)
            })

            self.items.append(item)

        return results

    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})

            else:
                results.append({
                    Message(f'The {item_entity.name} cannot be used', colors.yellow)
                })
        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                # noinspection PyUnresolvedReferences
                item_use_results = item_component.use_function(self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        # noinspection PyUnresolvedReferences
        owner = self.owner

        if owner.equipment.main_hand == item or owner.equipment.off_hand == item:
            owner.equipment.toggle_equip(item)

        item.x = owner.x
        item.y = owner.y

        self.remove_item(item)
        results.append({
            'item_dropped': item,
            'message': Message(f'You dropped the {item.name}', colors.yellow)
        })

        return results

    def to_json(self):
        json_data = {
            'capacity': self.capacity,
            'items': [item.to_json() for item in self.items]
        }

        return json_data

    @classmethod
    def from_json(cls, json_data: dict):
        from entity import Entity

        capacity = json_data.get('capacity')
        items_json = json_data.get('items')

        items = [Entity.from_json(item_json) for item_json in items_json]

        inventory = cls(capacity)
        inventory.items = items

        return inventory
