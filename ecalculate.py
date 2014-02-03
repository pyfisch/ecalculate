# -*- coding:utf-8 -*-

# Simple calculator for Enlightenment made using EFL Python bindings.
# Created and tested with E18 and Python 2.7.
# (C) 2014 Pyfisch
# Released under the MIT-License.

import re

from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL
from efl import elementary
from efl.elementary.window import StandardWindow
from efl.elementary.box import Box
from efl.elementary.button import Button
from efl.elementary.entry import Entry
from efl.elementary.table import Table

__version__ = '0.1.1'

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZONTAL = EVAS_HINT_EXPAND, 0.0
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZONTAL = EVAS_HINT_FILL, 0.0


class Calculator(object):
    def __init__(self):
        """Creates the window and its contents.

        :attribute memory: The first operand.
        :attribute operand: The operand to join the both values.
        :attribute field: The input/display field.
        :attribute table: Formatting table holding the buttons.
        """
        # Create mathematical attributes.
        self.memory = ''
        self.operand = None
        # Create the main window.
	self.window = StandardWindow("eCalculate", "eCalculate", autodel=True, size=(300, 300))
        # Create box that holds all GUI elements.
        box = Box(self.window, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        self.window.resize_object_add(box)
        box.show()
        # Create Input field.
        self.field = Entry(self.window, single_line=True,
                           size_hint_weight=EXPAND_HORIZONTAL,
                           size_hint_align=FILL_HORIZONTAL)
        self.field.markup_filter_append(self.filter_markup)
        box.pack_end(self.field)
        self.field.show()
        # Create table holding the buttons.
        self.table = Table(self.window, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        box.pack_end(self.table)
        self.table.show()
        # Create buttons.
        self.add_button(x=0, y=2, text='1', char='1') 
        self.add_button(x=1, y=2, text='2', char='2') 
        self.add_button(x=2, y=2, text='3', char='3') 
        self.add_button(x=0, y=1, text='4', char='4') 
        self.add_button(x=1, y=1, text='5', char='5') 
        self.add_button(x=2, y=1, text='6', char='6') 
        self.add_button(x=0, y=0, text='7', char='7') 
        self.add_button(x=1, y=0, text='8', char='8') 
        self.add_button(x=2, y=0, text='9', char='9') 
        self.add_button(x=0, y=3, text='0', char='0') 
        self.add_button(x=4, y=0, text='÷', char='/') 
        self.add_button(x=4, y=1, text='×', char='*') 
        self.add_button(x=4, y=2, text='−', char='-') 
        self.add_button(x=4, y=3, text='+', char='+') 
        self.add_button(x=2, y=3, text='=', char='=')
        self.add_button(x=1, y=3, text='.', char='.')
        # Finally show the window.
        self.window.show()

    def add_button(self, x, y, text, char):
        """Add a button to the user interface.

        :param x: The horizontal position in the UI-table.
        :param y: The vertical position in the UI-table.
        :param text: The button label.
        :param action: String what the button should do, resolved into
            a function in self.do_action().
        :param char: Character that is passed along with the action.
        """
        button = Button(self.window, text=text,
                        size_hint_weight=EXPAND_BOTH,
                        size_hint_align=FILL_BOTH)
        button.callback_clicked_add(self.enter_char, char=char)
        self.table.pack(button, x, y, 1, 1)
        button.show()

    def enter_char(self, caller, char):
        """Adds a character to the input field. Called if a button
        is pressed.

        :param caller: The clicked button.
        :param char: The character that should be added to the field.
        """
        self.field.entry_append(char)

    def calculate(self):
        """Do the calculation. This function does not check if the
        values are valid.
        """
        result = self.CALC_ACTIONS[self.operand](float(self.memory), float(self.field.text))
        self.field.text = re.sub('\.0$', '', str(result))
        self.memory = ''

    def filter_markup(self, caller, char, _):
        """Filter the entry field of not allowed characters, check
        that only one point is in the value, do calculations and set
        the operand. Called whenever text is inserted either throught
        the keyboard or by pressing buttons.
        :param caller: The calling object (always self.field).
        :param char: The character entered.
        :param _: I do not know ;-) (Passed automatically, always None?).
        """
        if not char in '1234567890.+-*/=':
            return None
        if char == '.' and ('.' in caller.text or caller.text == ''):
            return None
        if char == '=':
            if self.memory and caller.text:
                self.calculate()
            else:
                self.memory = ''
                caller.text = ''
            return None
        if char in self.CALC_ACTIONS:
            if self.memory and caller.text:
                self.calculate()
            self.operand = char 
            if caller.text:
                self.memory = caller.text
                caller.text = ''
            return None 
        return char 
    
    CALC_ACTIONS = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
        }

if __name__ == "__main__":
    elementary.init()
    Calculator()
    elementary.run()
    elementary.shutdown()
