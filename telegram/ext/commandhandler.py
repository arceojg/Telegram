#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2016
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

""" This module contains the CommandHandler class """

from .handler import Handler
from telegram import Update
from telegram.utils.deprecate import deprecate


class CommandHandler(Handler):
    """
    Handler class to handle Telegram commands. Commands are Telegram messages
    that start with ``/``, optionally followed by an ``@`` and the bot's
    name and/or some additional text.

    Args:
        command (str): The name of the command this handler should listen for.
        callback (function): A function that takes ``bot, update`` as
            positional arguments. It will be called when the ``check_update``
            has determined that an update should be processed by this handler.
        pass_args (optional[bool]): If the handler should be passed the
            arguments passed to the command as a keyword argument called `
            ``args``. It will contain a list of strings, which is the text
            following the command split on spaces. Default is ``False``
        pass_update_queue (optional[bool]): If the handler should be passed the
            update queue as a keyword argument called ``update_queue``. It can
            be used to insert updates. Default is ``False``
    """

    def __init__(self, command, callback, pass_args=False,
                 pass_update_queue=False):
        super(CommandHandler, self).__init__(callback, pass_update_queue)
        self.command = command
        self.pass_args = pass_args

    def check_update(self, update):
        return (isinstance(update, Update) and
                update.message and
                update.message.text and
                update.message.text.startswith('/') and
                update.message.text[1:].split(' ')[0].split('@')[0] ==
                self.command)

    def handle_update(self, update, dispatcher):
        optional_args = self.collect_optional_args(dispatcher)

        if self.pass_args:
            optional_args['args'] = update.message.text.split(' ')[1:]

        self.callback(dispatcher.bot, update, **optional_args)

    # old non-PEP8 Handler methods
    m = "telegram.CommandHandler."
    checkUpdate = deprecate(check_update, m + "checkUpdate", m + "check_update")
    handleUpdate = deprecate(handle_update, m + "handleUpdate", m + "handle_update")
