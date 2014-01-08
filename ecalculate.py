# -*- coding:utf-8 -*-

# Simple calculator for Enlightenment made using EFL Python bindings.
# Created and tested with E18 and Python 2.7.
# (C) 2014 Pyfisch
# Released under the MIT-License.

from functools import partial

from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL
from efl import elementary
from efl.elementary.window import StandardWindow
from efl.elementary.box import Box
from efl.elementary.button import Button
from efl.elementary.entry import Entry
from efl.elementary.table import Table

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZONTAL = EVAS_HINT_EXPAND, 0.0
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZONTAL = EVAS_HINT_FILL, 0.0


class Calculator(StandardWindow):
    def __init__(self):
        self.value1 = ''
        self.value2 = ''
        self.action = None
	StandardWindow.__init__(self, "ECalculate", "ECalculate", autodel=True, size=(300, 300))
        # Create box
        self.box = Box(self, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        self.resize_object_add(self.box)
        self.box.show()
        # Create Input field
        self.field = Entry(self, single_line=True, editable=False,
                           size_hint_weight=EXPAND_HORIZONTAL,
                           size_hint_align=FILL_HORIZONTAL)
        self.box.pack_end(self.field)
        self.field.show()
        # Create table holding the buttons
        self.table = Table(self, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        self.box.pack_end(self.table)
        self.table.show()
        # Create buttons
        self.add_button(x=0, y=0, text='1') 
        self.add_button(x=1, y=0, text='2') 
        self.add_button(x=2, y=0, text='3') 
        self.add_button(x=0, y=1, text='4') 
        self.add_button(x=1, y=1, text='5') 
        self.add_button(x=2, y=1, text='6') 
        self.add_button(x=0, y=2, text='7') 
        self.add_button(x=1, y=2, text='8') 
        self.add_button(x=2, y=2, text='9') 
        self.add_button(x=0, y=3, text='0') 
        self.add_button(x=4, y=0, text='/', action='divide') 
        self.add_button(x=4, y=1, text='*', action='multiply') 
        self.add_button(x=4, y=2, text='-', action='minus') 
        self.add_button(x=4, y=3, text='+', action='plus') 
        self.add_button(x=2, y=3, text='=', action='submit')
        self.add_button(x=1, y=3, text='.', action='point')

        self.show()

    def calculate(self):
        if not (self.value1 and self.value2):
            self.value1 = ''
            self.value2 = ''
            return
        if self.action == 'plus':
            self.value2 = str(float(self.value1) + float(self.value2))
        elif self.action == 'minus':
            self.value2 = str(float(self.value1) - float(self.value2))
        elif self.action == 'multiply':
            self.value2 = str(float(self.value1) * float(self.value2))
        elif self.action == 'divide':
            self.value2 = str(float(self.value1) / float(self.value2))
        else:
            raise Exception("Unbound action.")
        self.value1 = ''
    
    def display(self):
        self.field.text = self.value2
 
    def click_button(self, caller, actiontype):
        if actiontype == 'submit':
            self.calculate()
        elif actiontype == 'point':
            self.value2 += '.'
        elif actiontype:
            if self.action and self.value1:
                self.calculate()
            self.action = actiontype
            self.value1 = self.value2
            self.value2 = ''
        else:
            self.value2 += caller.text
        self.display()
    
    def add_button(self, x, y, text, action=None):
        button = Button(self, text=text,
                        size_hint_weight=EXPAND_BOTH,
                        size_hint_align=FILL_BOTH)
        button.callback_clicked_add(partial(self.click_button,
                                            actiontype=action))
        self.table.pack(button, x, y, 1, 1)
        button.show()
 

if __name__ == "__main__":
    elementary.init()
    Calculator()
    elementary.run()
    elementary.shutdown()
