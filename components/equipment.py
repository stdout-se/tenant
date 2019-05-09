from equipment_slots import EquipmentSlots


class Equipment:
    def __init__(self, main_hand=None, off_hand=None):
        self.main_hand = main_hand
        self.off_hand = off_hand

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        # If the equipment is for the main hand
        if slot == EquipmentSlots.MAIN_HAND:
            # If we have the item equipped in the main hand
            if self.main_hand == equippable_entity:
                # Unequip it
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                # If we have something else in our main hand
                if self.main_hand:
                    # Notify that we're replacing it (unequiping it)
                    results.append({'dequipped': self.main_hand})

                # Equip the new item
                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        # If the equipment is for the off hand
        elif slot == EquipmentSlots.OFF_HAND:
            # If we have the item equipped in the off hand
            if self.off_hand == equippable_entity:
                # Unequip it
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                # If we have something else in our off hand
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                # Equip the new item
                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        return results

    def to_json(self):
        if self.main_hand:
            main_hand_json = self.main_hand.to_json()
        else:
            main_hand_json = None

        if self.off_hand:
            off_hand_json = self.off_hand.to_json()
        else:
            off_hand_json = None

        json_data = {
            'main_hand': main_hand_json,
            'off_hand': off_hand_json,
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        from entity import Entity

        main_hand_json = json_data.get('main_hand')
        off_hand_json = json_data.get('off_hand')

        if main_hand_json:
            main_hand = Entity.from_json(main_hand_json)
        else:
            main_hand = None

        if off_hand_json:
            off_hand = Entity.from_json(off_hand_json)
        else:
            off_hand = None

        equipment = Equipment(main_hand, off_hand)

        return equipment
