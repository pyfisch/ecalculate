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

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZONTAL = EVAS_HINT_EXPAND, 0.0
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZONTAL = EVAS_HINT_FILL, 0.0


class CBox(Box):
    def __init__(self, *args, **kwargs):
        if not 'horizontal' in kwargs:
            kwargs['horizontal'] = False
        Box.__init__(self,
                     kwargs['window'], 
                     horizontal=kwargs['horizontal'],
                     size_hint_weight=EXPAND_BOTH,
                     size_hint_align=FILL_BOTH)
        for i in args:
            self.pack_end(i)

    def show(self):
        Box.show(self)
        for i in self.children:
            i.show()


class CButton(Button):
    def __init__(self, window, text, action=None):
        Button.__init__(self, window, text=str(text),
                        size_hint_weight=EXPAND_BOTH,
                        size_hint_align=FILL_BOTH)
        self.action = action
        self.window = window
        self.callback_clicked_add(self.clicked)
    
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


class CEntry(Entry):
    def __init__(self, window):
        Entry.__init__(self, window,
                       size_hint_weight=EXPAND_HORIZONTAL,
                       size_hint_align=FILL_HORIZONTAL,
                       single_line=True,
                       editable=False)


class Calculator(StandardWindow):
    def __init__(self):
        self.value1 = ''
        self.value2 = ''
        self.action = None
	StandardWindow.__init__(self, "ECalculate", "ECalculate", autodel=True, size=(300, 300))
        self.mainbox = Box(self, size_hint_weight=EXPAND_BOTH)
        self.resize_object_add(self.mainbox)
        self.mainbox.show()
        self.entry_field = CEntry(self)
        #TODO: A real grid should be used here.
	grid = CBox(self.entry_field,
                    CBox(CButton(self, 1),
                         CButton(self, 2),
                         CButton(self, 3),
	                 CButton(self, '/', 'divide'),
                         window=self,
                         horizontal=True,
                        ),
                    CBox(CButton(self, 4),
                         CButton(self, 5),
                         CButton(self, 6),
	                 CButton(self, '*', 'multiply'),
                         window=self,
                         horizontal=True,
                        ),
                    CBox(CButton(self, 7),
                         CButton(self, 8),
                         CButton(self, 9),
	                 CButton(self, '-', 'minus'),
                         window=self,
                         horizontal=True,
                        ),
                    CBox(CButton(self, 0),
                         CButton(self, '.', 'point'),
                         CButton(self, '=', 'submit'),
	                 CButton(self, '+', 'plus'),
                         window=self,
                         horizontal=True,
                        ),
                    window=self,
        )
        self.resize_object_add(grid)
        grid.show()
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
        self.entry_field.text = self.value2


if __name__ == "__main__":
    elementary.init()
    Calculator()
    elementary.run()
    elementary.shutdown()
