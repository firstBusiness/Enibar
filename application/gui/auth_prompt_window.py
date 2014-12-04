# Copyright (C) 2014 Bastien Orivel <b2orivel@enib.fr>
# Copyright (C) 2014 Arnaud Levaufre <a2levauf@enib.fr>
#
# This file is part of Enibar.
#
# Enibar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Enibar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Enibar.  If not, see <http://www.gnu.org/licenses/>.

"""
Authorization prompt
====================

Provides a decorator ask_auth.
You can use it like that:

.. code-block:: python

    @ask_auth
    def my_func():
        print("Hello world")

It will ask for a login and a password and will call your function only if it
match a combination in database.

"""


from PyQt5 import QtWidgets, uic
from api import users
import api.validator
from database import Cursor
import gui.utils
import settings


def ask_auth(*dargs, fail_callback=None, pass_performer=False):
    """ Decorator to ask for authorization """
    def decorator(func):
        """ Decorator wrapper """
        def wrapper(*args, **kwargs):
            """ Wrapper """
            if pass_performer:
                _performer = ""
            if settings.DEBUG:
                func(*args, **kwargs)
                return
            prompt = AuthPromptWindow(dargs)
            if prompt.is_authorized:
                if pass_performer:
                    kwargs["_performer"] = prompt.user
                func(*args, **kwargs)
            else:
                gui.utils.error("Error", "Erreur d'authentification")
                if fail_callback is not None:
                    fail_callback()
        return wrapper
    return decorator


class AuthPromptWindow(QtWidgets.QDialog):
    """ Authorization prompt class """
    def __init__(self, requirements):
        super().__init__()
        self.requirements = requirements
        self.is_authorized = False
        uic.loadUi('ui/auth_prompt_window.ui', self)
        self.pass_input.set_validator(api.validator.NAME)
        filter_ = ", ".join("{key}=1".format(key=key) for key in requirements)
        self.user = ""

        with Cursor() as cursor:
            cursor.prepare("SELECT * FROM admins WHERE " + filter_)
            cursor.exec_()

        existing_person = False
        while cursor.next():
            self.login_input.addItem(cursor.record().value("login"))
            existing_person = True

        if not existing_person:
            gui.utils.error("Error", "Personne n'a le droit de faire ça")
        else:
            self.login_input.setFocus()
            self.exec()

    def accept(self):
        """ Called when "Login" is clicked """
        self.user = self.login_input.currentText()
        if users.is_authorized(self.user,
                               self.pass_input.text()):
            rights = users.get_rights(self.user)
            for requirement in self.requirements:
                if not rights[requirement]:
                    return super().accept()
            self.is_authorized = True
        else:
            self.is_authorized = False
        return super().accept()

    def on_change(self):
        """  Called when the password input changes
        """
        self.accept_button.setEnabled(self.pass_input.valid)
