from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView
from kivy.base import runTouchApp

liste = [{'Member': 'true', 'id': 'adresse1@example.com'}, {'Member': 'true', 'id': 'adresse1@example.com'}]
mail = ', '.join(d['id'] for d in liste)
members = ', '.join(d['Member'] for d in liste)

l = mail.split(',')
l2 = members.split(',')


class MainView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.columns = 2
        
        self.add_widget(ListView(item_strings=l))
        self.add_widget(ListView(item_strings=l2))


if __name__ == '__main__':
    runTouchApp(MainView()) 