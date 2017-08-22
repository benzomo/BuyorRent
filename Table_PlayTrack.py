from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, StringProperty, NumericProperty 
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


kv = """

<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (0.4, 0.4, 0.4, 1) if self.selected else (0.5, 0.5, 0.5, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<KivyPlayer>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    orientation: 'vertical'
    BoxLayout:
        Button:
            id: next_track
            text: "Next Track"
            on_release: controller.select_next()
            Button:
                id: previous_track
                text: "Previous Track"
                on_release: controller.select_previous()
        BoxLayout:
            RecycleView:
                id: media_list
                viewclass: 'SelectableLabel'
                scroll_type: ['bars', 'content']
                scroll_wheel_distance: dp(114)
                bar_width: dp(10)
                SelectableRecycleBoxLayout:
                    id: controller
                    key_selection: 'selectable'
                    default_size: None, dp(56)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
                    # multiselect: True
                    touch_multiselect: True
                    spacing: dp(2)
            
         


"""

Builder.load_string(kv)

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''

    def get_nodes(self):
        nodes = self.get_selectable_nodes()
        if self.nodes_order_reversed:
            nodes = nodes[::-1]
        if not nodes:
            return None, None

        selected = self.selected_nodes
        if not selected:  # nothing selected, select the first
            self.select_node(nodes[0])
            return None, None

        if len(nodes) == 1:  # the only selectable node is selected already
            return None, None

        last = nodes.index(selected[-1])
        self.clear_selection()
        return last, nodes

    def select_next(self):
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if last == len(nodes) - 1:
            self.select_node(nodes[0])
        else:
            self.select_node(nodes[last + 1])

    def select_previous(self):
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if not last:
            self.select_node(nodes[-1])
        else:
            self.select_node(nodes[last - 1])


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class KivyPlayer(BoxLayout):
    ''' Main Kivy class for createing the initial BoxLayout '''

    def __init__(self, **kwargs):
        super(KivyPlayer, self).__init__(**kwargs)

        #Set media_list data
        
        self.ids.media_list.data = [{'text': str(x), 'selectable': True} for x in range(100)]


class KivyApp(App):
    def build(self):
        return KivyPlayer()


if __name__ == '__main__':
    KivyApp().run()