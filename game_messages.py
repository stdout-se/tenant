import textwrap
from typing import Tuple

import colors
import constants


class Message:
    def __init__(self, text: str, color: Tuple[int, int, int] = colors.white):
        self.text = text
        self.color = color

    def to_json(self):
        json_data = {
            'text': self.text,
            'color': self.color
        }

        return json_data

    @classmethod
    def from_json(cls, json_data: dict):
        text = json_data.get('text')
        color = json_data.get('color')

        if color:
            message = cls(text, color)
        else:
            message = cls(text)

        return message


class MessageLog:
    def __init__(self):
        self.messages = []

    def add_message(self, message: Message):
        # Split the message if necessary, to multiple lines
        new_msg_lines = textwrap.wrap(message.text, constants.message_width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == constants.message_height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))

    def to_json(self):
        json_data = {
            'messages': [message.to_json() for message in self.messages]
        }

        return json_data

    @classmethod
    def from_json(cls, json_data: dict):
        messages_json = json_data.get('messages')

        message_log = cls()

        for message_json in messages_json:
            message_log.add_message(Message.from_json(message_json))

        return message_log
