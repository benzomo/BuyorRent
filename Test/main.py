'''
Buy vs. Rent
============

'''
import kivy
# kivy.require('1.8.1')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListView


from kivy.garden.graph import Graph, MeshLinePlot
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivy import FigureCanvas, NavigationToolbar2Kivy
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg, NavigationToolbar2Kivy
from kivy.utils import get_color_from_hex as rgb
from collections import OrderedDict
from numpy import sin
import math
import numpy as np
import os
from kivy.factory import Factory
from kivy.lang import Builder, Parser, ParserException
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from functools import partial
import plot
import rtable as rt
from random import sample
from string import ascii_lowercase
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
import housingCalc as hc 

CATALOG_ROOT = os.path.dirname(__file__)

global datapd
global dataHeader
global in_v
global infl, mterm_res, mterm_inc, rate_m, rate_mkt, rate_mkt0, lev_res, lev_inc, rent_paid, rent_income, propTax, appr_nominal, maint_th, maint_h, maint_c, maint_ap, util_th, util_h, util_c, util_ap, fees_th, fees_h, fees_c, fees_ap
global lev, levI, n_income, savings0, m_term, m_termI, t_max, p_price, p_priceI, isInv, notRent
global max_year
max_year = 30

lev = 3
levI = 3
n_income = 50000
savings0 = 250000
m_term = 25
m_termI = 25
t_max = 30
p_price = 500000
p_priceI = 500000

isInv = 0
notRent = 0

infl = [0.02, 0.02, 0.02, 'infl']
mterm_res = [10, 25, 30, 'mterm_res']
mterm_inc = [10, 15, 25, 'mterm_inc']
rate_m = [0.03, 0.04, 0.05, 'rate_m']
rate_mkt = [0.04, 0.06, 0.08, 'rate_mkt']
rate_mkt0 = [0.025, 0.04, 0.05, 'rate_mkt0']
lev_res = [1, 4, 9, 'lev_res']
lev_inc = [1, 4, 9, 'lev_inc']
rent_paid = [1200, 1300, 1900, 'rent_paid']
rent_income = [1100, 1650, 1750, 'rent_income']
propTax = [0.006, 0.007, 0.01, 'propTax']
appr_nominal = [0.01, 0.02, 0.03, 'appr_nominal']
maint_th = [0.0025, 0.0025, 0.0025, 'maint_th']
maint_h = [0.0075, 0.0075, 0.0075, 'maint_h']
maint_c = [0.001, 0.001, 0.001, 'maint_c']
maint_ap = [0, 0, 0, 'maint_ap']
util_th = [150, 200, 350, 'util_th']
util_h = [250, 350, 500, 'util_h']
util_c = [75, 110, 150, 'util_c']
util_ap = [0, 0, 0, 'util_ap']
fees_th = [100, 200, 300, 'fees_th']
fees_h = [0, 0, 0, 'fees_h']
fees_c = [375, 500, 650, 'fees_c']
fees_ap = [0, 0, 0, 'fees_ap']

datapd, n_data = hc.simulate(lev, levI, n_income, savings0, m_term, t_max, p_price, m_termI, p_priceI, isInv, notRent)
dataHeader = datapd.columns.values
in_v = hc.varTable(infl, mterm_res, mterm_inc, rate_m, rate_mkt, rate_mkt0, lev_res, lev_inc, rent_paid, rent_income, propTax, appr_nominal, maint_th, maint_h, maint_c, maint_ap, util_th, util_h, util_c, util_ap, fees_th, fees_h, fees_c, fees_ap)

in_v = in_v[['Variable', 'Med']]

# Config.set('graphics', 'width', '1024')
# Config.set('graphics', 'height', '768')

'''List of classes that need to be instantiated in the factory from .kv files.
'''

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty, StringProperty
import kivy
kivy.require('1.10.0')



class GridLayout1(GridLayout):
    def __init__(self, *args, **kwargs):
        super(GridLayout1, self).__init__(*args, **kwargs)

        try:
            self.text_in1.text = str(5555)
        except Exception as e:
            pass


    def calc(self, x, y):
        try:
            n_income = int(x)  - int(y)
        except Exception as e:
            n_income = 'ERROR'
        return n_income


class HouseInput(ScrollView):
    boolNI = True
    def __init__(self, *args, **kwargs):

        super(HouseInput, self).__init__(*args, **kwargs)


    def update1(self, globals1):
        global lev
        lev = globals1

    def buyprop(self, tb_state):
        global notRent
        if tb_state == 'down':  notRent = 1
        else: notRent = 0

    def buypropI(self, tb_state):
        global isInv
        if tb_state == 'down':  isInv = 1
        else: isInv = 0

    def inputNI(self):
        if self.boolNI == True:  self.boolNI = False
        else: self.boolNI = True

    def UpdateBtn(self, infl, mterm_res, mterm_inc, rate_m, rate_mkt, rate_mkt0, lev_res, lev_inc, rent_paid, rent_income,
                  propTax, appr_nominal, maint_th, maint_h, maint_c, maint_ap, util_th, util_h, util_c, util_ap,
                  fees_th, fees_h, fees_c, fees_ap):
        global in_v

        inv_v = hc.updatevarT(in_v)


        in_v = in_v[['Variable', 'Med']]


class HeaderCell(Label):
    pass



class ScrollCell(BoxLayout):
    text = StringProperty(None)
    is_even = BooleanProperty(None)


class TableHeader(ScrollView):
    """Fixed table header that scrolls x with the data table"""
    header = ObjectProperty(None)

    def __init__(self, list_dicts=None, *args, **kwargs):
        super(TableHeader, self).__init__(*args, **kwargs)

        titles = list_dicts[0].keys()

        for title in titles:
            self.header.add_widget(HeaderCell(text=title))



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


class TableX(BoxLayout):

    def __init__(self, *args, **kwargs):

        super(TableX, self).__init__(*args, **kwargs)
        self.orientation = "vertical"

        self.header = TableHeader(list_dicts=self.create())
        #self.table_data = TableData(list_dicts=self.create())

        #self.table_data.fbind('scroll_x', self.scroll_with_header)

        self.add_widget(self.header)
        #self.add_widget(self.table_data)

    def create(self):
        data = []

        keys = ["Title Col: {}".format(i + 1) for i in range(15)]

        for nrow in range(80):
            row = OrderedDict.fromkeys(keys)
            for i, key in enumerate(keys):
                row[key] = "c: {}, r: {}".format(i + 1, nrow + 1)

            data.append(row)

        return data

    def scroll_with_header(self, obj, value):
        self.header.scroll_x = value


class TableH(RecycleView):
    def __init__(self, *args, **kwargs):
        super(TableH, self).__init__(*args, **kwargs)

        self.data = [{'value': ''.join(x)} for x in dataHeader[[0, 2, 21, 21, 21, 21, 21, 3, 10, 21]]]

    def populate(self):
        self.data = [{'value': ''.join(x)} for x in dataHeader[[0, 2, 21, 21, 21, 21, 21, 3, 10, 21]]]

    def clear(self):
        self.data = []
        
        

class Table1(RecycleView):
    def __init__(self, *args, **kwargs):
        super(Table1, self).__init__(*args, **kwargs)
        

        #self.data = [{'value': ''.join(str(int(np.round(x))))} for x in np.nditer(n_data[:, 0:5], order= 'C')]
        
        self.data = [{'value': ''.join(str(int(np.round(x))))} for x in np.nditer(datapd.ix[:, [0, 2, 21, 21, 21, 21, 21, 3, 10, 21]], order= 'C')]

        
    def populate(self):
        datapd, n_data = hc.simulate(lev, levI, n_income, savings0, m_term, t_max, p_price, m_termI, p_priceI, isInv,
                                     notRent)
        self.data = [{'value': ''.join(str(int(np.round(x))))} for x in
                     np.nditer(datapd.ix[:, [0, 2, 21, 21, 21, 21, 21, 3, 10, 21]], order='C')]
        #dataHeader = datapd.columns.values

    def clear(self):
        self.data = []


class InputRatesHdr(RecycleView):
    def __init__(self, *args, **kwargs):
        super(InputRatesHdr, self).__init__(*args, **kwargs)

        self.data = [{'value': ''.join(x)} for x in in_v]

    def populate(self):
        self.data = [{'value': ''.join(x)} for x in dataHeader]

    def clear(self):
        self.data = []


class InputRatesTblc1(RecycleView):
    def __init__(self, *args, **kwargs):
        super(InputRatesTblc1, self).__init__(*args, **kwargs)

        # self.data = [{'value': ''.join(str(int(np.round(x))))} for x in np.nditer(n_data[:, 0:5], order= 'C')]

        self.data = [{'value': ''.join(str(x))} for x in in_v['Med']]



    def populate(self):
        self.data = [{'value': ''.join(str(int(np.round(x))))} for x in
                     np.nditer(datapd.ix[:, [0, 2, 21]], order='C')]
        # dataHeader = datapd.columns.values

    def clear(self):
        self.data = []



class InputRatesTblc2(RecycleView):
    def __init__(self, *args, **kwargs):
        super(InputRatesTblc2, self).__init__(*args, **kwargs)

        # self.data = [{'value': ''.join(str(int(np.round(x))))} for x in np.nditer(n_data[:, 0:5], order= 'C')]

        self.data = [{'value': ''.join(str(x))} for x in in_v['Variable']]


    def populate(self):

        self.data = [{'value': ''.join(str(x))} for x in in_v['Variable']]
        # dataHeader = datapd.columns.values

    def clear(self):
        self.data = []

class InputSummaryHdr(RecycleView):
    def __init__(self, *args, **kwargs):
        super(InputSummaryHdr, self).__init__(*args, **kwargs)

        self.data = [{'value': ''.join(x)} for x in dataHeader[[0, 2, 21, 21, 21, 21, 21, 3, 10, 21]]]

    def populate(self):
        self.data = [{'value': ''.join(x)} for x in dataHeader[[0, 2, 21, 21, 21, 21, 21, 3, 10, 21]]]

    def clear(self):
        self.data = []


class InputSummaryTbl(RecycleView):
    def __init__(self, *args, **kwargs):
        super(InputSummaryTbl, self).__init__(*args, **kwargs)

        # self.data = [{'value': ''.join(str(int(np.round(x))))} for x in np.nditer(n_data[:, 0:5], order= 'C')]

        self.data = [{'value': ''.join(str(int(np.round(x))))} for x in
                     np.nditer(datapd.ix[:, [0, 2, 21, 21, 21, 21, 21, 3, 10, 21]], order='C')]

    def populate(self):
        datapd, n_data = hc.simulate(lev, levI, n_income, savings0, m_term, t_max, p_price, m_termI, p_priceI, isInv,
                                     notRent)
        self.data = [{'value': ''.join(str(int(np.round(x))))} for x in
                     np.nditer(datapd.ix[:, [0, 2, 21, 21, 21, 21, 21, 3, 10, 21]], order='C')]
        # dataHeader = datapd.columns.values

    def clear(self):
        self.data = []


class OutputHdr(RecycleView):
    def __init__(self, *args, **kwargs):
        super(OutputHdr, self).__init__(*args, **kwargs)

        self.data = [{'value': ''.join(x)} for x in dataHeader[[0, 2, 21, 21, 21, 21, 21, 3, 10, 21]]]

    def populate(self):
        self.data = [{'value': ''.join(x)} for x in dataHeader[[0, 2, 21, 21, 21, 21, 21, 3, 10, 21]]]

    def clear(self):
        self.data = []


class OutputTbl(RecycleView):
    def __init__(self, *args, **kwargs):
        super(OutputTbl, self).__init__(*args, **kwargs)

        # self.data = [{'value': ''.join(str(int(np.round(x))))} for x in np.nditer(n_data[:, 0:5], order= 'C')]

        self.data = [{'value': ''.join(str(int(np.round(x))))} for x in
                     np.nditer(datapd.ix[:, [0, 2, 21, 21, 21, 21, 21, 3, 10, 21]], order='C')]

    def populate(self):
        datapd, n_data = hc.simulate(lev, levI, n_income, savings0, m_term, t_max, p_price, m_termI, p_priceI, isInv,
                                     notRent)
        self.data = [{'value': ''.join(str(int(np.round(x))))} for x in
                     np.nditer(datapd.ix[:, [0, 2, 21, 21, 21, 21, 21, 3, 10, 21]], order='C')]
        # dataHeader = datapd.columns.values

    def clear(self):
        self.data = []


class GraphBox(BoxLayout):
    def __init__(self, *args, **kwargs):
        self.wimg1 = Image(source='Picture1.png')
        self.wimg2 = Image(source='Picture2.png')
        self.wimg3 = Image(source='Picture3.png')
        self.wimg4 = Image(source='Picture4.png')

        super(GraphBox, self).__init__(*args, **kwargs)
        #self.size_hint_x = 1.3333333
        self.add_widget(self.wimg1)  
        self.add_widget(self.wimg2)
        self.add_widget(self.wimg4)
        self.add_widget(self.wimg3)

class Mgraph(GridLayout):
    def __init__(self, *args, **kwargs):

        self.wimg = Image(source='Picture1.png')

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

            a, fig1, ax1 = plot.runit2()
            fig_kv = FigureCanvas(fig1)
            nav_kv = NavigationToolbar2Kivy(fig_kv)

            #self.add_widget(nav_kv.actionbar)
            self.add_widget(fig_kv)
            #a.show()
            
class GraphCustom(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1


        self.graph_create()
        #self.graph_remove(graph1)


        BL = BoxLayout(size_hint=[1, 0.1])
        self.add_widget(BL)
        self.ratei = TextInput(multiline=False, font_size=16, size_hint=[1, 1], text='1111')
        self.label1 = Label(multiline=False, font_size=16, size_hint=[1, 1], text='Market Return Rate (%)')
        BL.add_widget(self.label1)
        BL.add_widget(self.ratei)
        my_button = Button(
            size_hint_y=1,
            text='OK',
            on_release=lambda a: self.print_txt())

        BL.add_widget(my_button)

    def print_txt(self):
        global variable_0
        variable_0 = self.ratei.text
        print(isInv)

    def graph_remove(self):
        #self.remove_widget(graph1)
        graph1.remove_plot(plot)

    def graph_add(self):
        #self.remove_widget(graph1)
        global plot
        k = np.random.normal()
        plot = MeshLinePlot(color=[0, 0, 0.75, 1])
        plot.points = [(x, sin(x / k)) for x in range(0, 101)]
        graph1.add_plot(plot)


    def graph_create(self):
        global graph1
        graph1 = Graph(
            label_options={'color': rgb('001933'), 'bold': True},
            background_color=rgb('f8f8f2'),
            tick_color=rgb('001933'),
            border_color=rgb('808080'),
            xlabel='X',
            ylabel='Y',
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            x_ticks_major=5,
            y_ticks_major=0.2,
            x_grid=True,
            y_grid=True,
            xmin=-0,
            xmax=30,
            ymin=-1,
            ymax=1)

        k = np.random.normal()
        global plot1
        plot1 = MeshLinePlot(color=[0, 0, 0.75, 1])
        y = (0.5 - 0.2)/30*np.linspace(0, max_year-1, max_year) + 0.2*np.ones(max_year) + np.random.normal(0, 0.05, max_year)
        plot1.points = [(x, y[x]) for x in range(0, 30)]
        graph1.add_plot(plot1)
        self.add_widget(graph1)
        return graph1


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

    #screen_managerL = ObjectProperty()


    def __init__(self, **kwargs):
        self._previously_parsed_text = ''
        super(Catalog, self).__init__(**kwargs)
        self.show_kv(None, "Matrix")
        self.show_kvL(None, "MV_Input")

        #self.carousel = None


    def show_kv(self, instance, value):

        self.screen_manager.current = value

    def show_kvL(self, instance, value):

        self.screen_managerL.current = value


class BuyorRentApp(App):
    '''The kivy App that runs the main root. All we do is build a catalog
    widget into the root.'''
    global datapd
    global dataHeader
    global lev, levI, n_income, savings0, m_term, m_termI, t_max, p_price, p_priceI, isInv, notRent
    global max_year

    max_year = 30
    m_rate = 0.04
    mkt_return = 0.06
    prop_tax = 0.0075
    infl = 0.02
    price_appr30 = 0.25

    down_p = p_price*0.2
    down_pI = p_priceI * 0.2
    lev = (p_price - down_p)/down_p
    levI = (p_priceI - down_pI)/down_pI
    n_income = 50000
    savings0 = 250000
    m_term = 25
    m_termI = 25
    t_max = 30
    p_price = 500000
    p_priceI = 500000

    isInv = 0
    notRent = 0

    datapd, n_data = hc.simulate(lev, levI, n_income, savings0, m_term, t_max, p_price, m_termI, p_priceI, isInv,
                                 notRent)
    dataHeader = datapd.columns.values

    colz = 2
    #rowz = 10


    def build(self):

        return Catalog()

   #def on_pause(self):
        #return True

if __name__ == "__main__":

    BuyorRentApp().run()

