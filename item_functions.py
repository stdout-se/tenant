import colors
from components.ai import ConfusedMonster
from game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({
            'consumed': False,
            'message': Message('You are already at full health', colors.yellow)
        })
    else:
        entity.fighter.heal(amount)
        results.append({
            'consumed': True,
            'message': Message('Your wounds start to feel better', colors.green)
        })

    return results


def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []
    target = None

    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and game_map.fov[entity.x, entity.y]:
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({
            'consumed': True,
            'target': target,
            'message': Message(f'A lightning bolt strikes the {target.name}, dealing {damage} damage')
        })
        results.extend(target.fighter.take_damage(damage))

    else:
        results.append({
            'consumed': False,
            'target': None,
            'message': Message('No emeny is close enough to strike')
        })

    return results


# noinspection PyUnusedLocal
def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({
            'consumed': False,
            'message': Message('You cannot target a tile outside your field of view', colors.yellow)
        })
        return results

    results.append({
        'consumed': True,
        'message': Message(f'The fireball explodes, burning everything within {radius} tiles!', colors.orange)
    })

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({
                'message': Message(f'The {entity.name} gets burned for {damage} hit points', colors.orange)
            })
            results.extend(entity.fighter.take_damage(damage))

    return results


# noinspection PyUnusedLocal
def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({
            'consumed': False,
            'message': Message('You cannot target a tile outside your field of view', colors.yellow)
        })
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({
                'consumed': True,
                'message': Message(f'The eyes of the {entity.name} looks vacant, as he starts to stumble around',
                                   colors.light_green)
            })

            break

    else:
        results.append({
            'consumed': False,
            'message': Message('There is no targetable enemy at that location', colors.yellow)
        })

    return results
