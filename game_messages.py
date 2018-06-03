import textwrap

import colors
import constants


class Message:
    def __init__(self, text, color=colors.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        # Split the message if necessary, to multiple lines
        new_msg_lines = textwrap.wrap(message.text, constants.message_width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == constants.message_height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))
