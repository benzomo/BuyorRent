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
            wid1, nv1 = self.plots()
            self.add_widget(nv1.actionbar)
            self.add_widget(wid1)
            self.add_data()


    def add_data(self):

        self.d["ax0"].set_ylabel('Scores')
        self.d["ax0"].set_title('Scores by group and gender')
        for x in range(1, self.ind):
            mind = "m"
            mind += str(x)
            axind = "ax"
            axind += str(x)
            self.d[axind].plot(self.d[mind][:, 0], self.d[mind][:, 1])
        mind = "m"
        axind = "ax"
        mind += str(self.ind)
        axind += str(self.ind)
        self.d[mind] = self.rand_sin()
        self.d[axind].plot(self.d[mind][:, 0], self.d[mind][:, 1])
        self.ind = self.ind + 1
        print(mind)

        #print(self.d[mind])



    def plots(self):
        global fig
        fig = plt.figure()
        for x in range(0, 11):
            self.d["ax{0}".format(x)] = fig.add_subplot(111)

        def enter_figure(event):
            event.canvas.figure.patch.set_facecolor('red')
            event.canvas.draw()

        def leave_figure(event):
            event.canvas.figure.patch.set_facecolor('blue')
            event.canvas.draw()

        global p_wid, nav

        p_wid = FigureCanvas(fig)
        fig.canvas.mpl_connect('figure_enter_event', enter_figure)
        fig.canvas.mpl_connect('figure_leave_event', leave_figure)
        nav = NavigationToolbar2Kivy(p_wid)
        return p_wid, nav

    def rand_sin(self):
        x = np.linspace(0,101,num=100)
        k = np.random.normal()
        y = sin((x/ k))
        m = [x, y]
        m = np.reshape(m, (2, 100)).T
        return m



    def get_fc(self, i):
        N = 5
        menMeans = (20, 35, 30, 35, 27)
        menStd = (2, 3, 4, 1, 2)

        ind = np.arange(N)  # the x locations for the groups
        width = 0.35  # the width of the bars

        womenMeans = (25, 32, 34, 20, 25)
        womenStd = (3, 5, 2, 3, 3)

        A = [[44.254, 44.114, 44.353, 44.899, 45.082], [-0.934, 0.506, 1.389, 0.938, 0.881]]
        fig, ax = plt.subplots()
        #fig = plt.figure()
        ax = fig.add_subplot(211)

        ax2 = fig.add_subplot(212)
        string = "hello"
        string += str(i)
        ax.text(0.6, 0.5, string, size=50, rotation=30.,
                ha="center", va="center",
                bbox=dict(boxstyle="round",
                          ec=(1., 0.5, 0.5),
                          fc=(1., 0.8, 0.8),
                          )
                )
        rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)
        rects2 = ax.bar(ind + width, womenMeans, width, color='y', yerr=womenStd)
        # ax.bar(ind, menMeans, width, color='r', yerr=menStd)
        # ax.bar(ind + width, womenMeans, width, color='y', yerr=womenStd)
        ax.set_ylabel('Scores')
        ax.set_title('Scores by group and gender')
        ax.set_xticks(ind + width)
        ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
        ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))

        # fig.canvas.mpl_connect('button_press_event', press)
        # fig.canvas.mpl_connect('button_release_event', release)
        # fig.canvas.mpl_connect('key_press_event', keypress)
        # fig.canvas.mpl_connect('key_release_event', keyup)
        # fig.canvas.mpl_connect('motion_notify_event', motionnotify)
        # fig.canvas.mpl_connect('resize_event', resize)
        # fig.canvas.mpl_connect('scroll_event', scroll)
        # fig.canvas.mpl_connect('figure_enter_event', figure_enter)
        # fig.canvas.mpl_connect('figure_leave_event', figure_leave)
        # fig.canvas.mpl_connect('close_event', close)



        ax2.scatter(A[0], A[1], c='g')

        my_mpl_kivy_widget = FigureCanvas(fig)


        def enter_figure(event):
            event.canvas.figure.patch.set_facecolor('red')
            event.canvas.draw()

        def leave_figure(event):
            event.canvas.figure.patch.set_facecolor('blue')
            event.canvas.draw()

        global wid1

        wid1 = my_mpl_kivy_widget
        fig.canvas.mpl_connect('figure_enter_event', enter_figure)
        fig.canvas.mpl_connect('figure_leave_event', leave_figure)

        return wid1

    def add_barplot(self):
        self.add_widget(self.get_fc(7))

    def add_AB(self):
        self.add_widget(NavigationToolbar2Kivy(wid1).actionbar)

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
