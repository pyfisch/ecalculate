# -*- coding:utf-8 -*-

# Simple calculator for Enlightenment made using EFL Python bindings.
# Created and tested with E18 and Python 2.7.
# (C) 2014 Pyfisch
# Released under the MIT-License.

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


class CButton(Button):
    def __init__(self, window, text, x, y, action=None):
        Button.__init__(self, window, text=str(text),
                        size_hint_weight=EXPAND_BOTH,
                        size_hint_align=FILL_BOTH)
        self.action = action
        self.window = window
        self.callback_clicked_add(self.clicked)
        self.window.table.pack(self, x, y, 1, 1)
        self.show()
    
    def clicked(self, caller):
        #TODO: Probably I should move this to the Calculator class
        if self.action == 'submit':
            self.window.calculate()
        elif self.action:
            if self.window.action and self.window.value1:
                self.window.calculate()
            self.window.action = self.action
            self.window.value1 = self.window.value2
            self.window.value2 = ''
        else:
            if self.action == 'point':
                self.window.value2 += '.'
            else:
                self.window.value2 += self.text
        self.window.display()


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
        CButton(self, x=0, y=0, text='1') 
        CButton(self, x=1, y=0, text='2') 
        CButton(self, x=2, y=0, text='3') 
        CButton(self, x=0, y=1, text='4') 
        CButton(self, x=1, y=1, text='5') 
        CButton(self, x=2, y=1, text='6') 
        CButton(self, x=0, y=2, text='7') 
        CButton(self, x=1, y=2, text='8') 
        CButton(self, x=2, y=2, text='9') 
        CButton(self, x=0, y=3, text='0') 
        CButton(self, x=4, y=0, text='/', action='divide') 
        CButton(self, x=4, y=1, text='*', action='multiply') 
        CButton(self, x=4, y=2, text='-', action='minus') 
        CButton(self, x=4, y=3, text='+', action='plus') 
        CButton(self, x=2, y=3, text='=', action='submit')
        CButton(self, x=1, y=3, text='.', action='point')

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


if __name__ == "__main__":
    elementary.init()
    Calculator()
    elementary.run()
    elementary.shutdown()
