'''
Buy vs. Rent
============

'''
import kivy
# kivy.require('1.8.1')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.graph import Graph, MeshLinePlot
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivy import FigureCanvas, NavigationToolbar2Kivy
from kivy.utils import get_color_from_hex as rgb
from numpy import sin
import numpy as np
import os
import math
from kivy.factory import Factory
from kivy.lang import Builder, Parser, ParserException
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from functools import partial
import plot

CATALOG_ROOT = os.path.dirname(__file__)


# Config.set('graphics', 'width', '1024')
# Config.set('graphics', 'height', '768')

'''List of classes that need to be instantiated in the factory from .kv files.
'''


class Mgraph(GridLayout):
    def __init__(self, *args, **kwargs):
        super(Mgraph, self).__init__(*args, **kwargs)
        #self.add_widget(nav1.actionbar)
        #self.add_barplot()

        self.ind =1
        self.d = {}
        for x in range(1, 11):
            self.d["m{0}".format(x)] = []


    def create_graph(self):
        try:
            self.remove_widget(p_wid)
            self.remove_widget(nav.actionbar)
            wid, nv = self.plots()
            self.add_widget(nv.actionbar)
            self.add_widget(wid)
            self.add_data()
        except Exception as e:
            #wid1, nv1 = self.plots()
            #self.add_widget(nv1.actionbar)
            #self.add_widget(wid1)
            #self.add_data()
            a = plot.runit2()
            a.show()
            




CONTAINER_KVS = os.path.join(CATALOG_ROOT, 'container_kvs')
CONTAINER_CLASSES = [c[:-3] for c in os.listdir(CONTAINER_KVS)
    if c.endswith('.kv')]

class Container(BoxLayout):
    '''
                 Build Containers
    '''

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.previous_text = open(self.kv_file).read()
        parser = Parser(content=self.previous_text)
        widget = Factory.get(parser.root.name)()
        Builder._apply_rule(widget, parser.root, parser.root)
        self.add_widget(widget)

    @property
    def kv_file(self):
        '''Get the name of the kv file, a lowercase version of the class
        name.
        '''
        return os.path.join(CONTAINER_KVS, self.__class__.__name__ + '.kv')


for class_name in CONTAINER_CLASSES:
    globals()[class_name] = type(class_name, (Container,), {})



class Catalog(BoxLayout):

    #screen_manager = ObjectProperty()


    def __init__(self, **kwargs):
        self._previously_parsed_text = ''
        super(Catalog, self).__init__(**kwargs)
        self.show_kv(None, 'Home')
        #self.carousel = None


    def show_kv(self, instance, value):

        self.screen_manager.current = value




class BuyorRentApp(App):
    '''The kivy App that runs the main root. All we do is build a catalog
    widget into the root.'''

    def build(self):

        return Catalog()

   #def on_pause(self):
        #return True

if __name__ == "__main__":
    BuyorRentApp().run()
