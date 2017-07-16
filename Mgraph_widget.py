# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 21:25:10 2017

@author: benmo
"""
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
    