import json
from zipfile import ZipFile, ZIP_LZMA

from constants import save_filename
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_utils import GameMap


def save_game(player, entities, game_map, message_log, game_state):
    data = {
        'player_index': entities.index(player),
        'entities': [entity.to_json() for entity in entities],
        'game_map': game_map.to_json(),
        'message_log': message_log.to_json(),
        'game_state': game_state.value
    }

    json_data = json.dumps(data, indent=4)

    with ZipFile(save_filename, 'w', compression=ZIP_LZMA) as savezip:
        savezip.writestr('savegame.json', data=json_data)


def load_game():
    with ZipFile(save_filename, 'r') as savezip:
        json_bytes = savezip.read('savegame.json')

    json_data = json_bytes.decode('utf-8')
    data = json.loads(json_data)

    player_index = data['player_index']
    entities_json = data['entities']
    game_map_json = data['game_map']
    message_log_json = data['message_log']
    game_state_json = data['game_state']

    entities = [Entity.from_json(entity_json) for entity_json in entities_json]
    player = entities[player_index]
    game_map = GameMap.from_json(game_map_json)
    message_log = MessageLog.from_json(message_log_json)
    game_state = GameStates(game_state_json)

    return player, entities, game_map, message_log, game_state
