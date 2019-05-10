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
