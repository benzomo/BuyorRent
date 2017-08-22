# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 19:04:38 2017

@author: benmo
"""

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty, StringProperty
import kivy
kivy.require('1.10.0')


class HeaderCell(Label):
    pass


class TableHeader(ScrollView):
    """Fixed table header that scrolls x with the data table"""
    header = ObjectProperty(None)

    def __init__(self, list_dicts=None, *args, **kwargs):
        super(TableHeader, self).__init__(*args, **kwargs)

        titles = list_dicts[0].keys()

        for title in titles:
            self.header.add_widget(HeaderCell(text=title))


class ScrollCell(BoxLayout):
    text = StringProperty(None)
    is_even = BooleanProperty(None)


class TableData(RecycleView):
    nrows = NumericProperty(None)
    ncols = NumericProperty(None)
    rgrid = ObjectProperty(None)

    def __init__(self, list_dicts=[], *args, **kwargs):
        self.nrows = len(list_dicts)
        self.ncols = len(list_dicts[0])

        super(TableData, self).__init__(*args, **kwargs)

        self.data = []
        for i, ord_dict in enumerate(list_dicts):
            is_even = i % 2 == 0
            row_vals = ord_dict.values()
            for text in row_vals:
                self.data.append({'text': text, 'is_even': is_even})


class Table(BoxLayout):

    def __init__(self, list_dicts=[], *args, **kwargs):

        super(Table, self).__init__(*args, **kwargs)
        self.orientation = "vertical"

        self.header = TableHeader(list_dicts=list_dicts)
        self.table_data = TableData(list_dicts=list_dicts)

        self.table_data.fbind('scroll_x', self.scroll_with_header)

        self.add_widget(self.header)
        self.add_widget(self.table_data)

    def scroll_with_header(self, obj, value):
        self.header.scroll_x = value


if __name__ == '__main__':
    from kivy.app import App
    from collections import OrderedDict

    class RtableApp(App):
        def build(self):
            data = []

            keys = ["Title Col: {}".format(i + 1) for i in range(15)]

            for nrow in range(30):
                row = OrderedDict.fromkeys(keys)
                for i, key in enumerate(keys):
                    row[key] = "c: {}, r: {}".format(i + 1, nrow + 1)
                    
                data.append(row)

            return Table(list_dicts=data)

    RtableApp().run()