from functools import partial

from garden.screens.screen_factory import ScreenFactory
from kivy import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.screen import MDScreen
from plyer import notification

Builder.load_string(
    """
#:import TimeWidget widgets.time_input
<MainScreen>
    name: "MainScreen"
    MDBoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: "Chronomètre"
            valign: 'middle'
            halign: 'center'
        MDList:
            id: recipes_list
        TimeInput:
            id: duration
            text: "00:00:00"
            max_text_length: 8
            valign: 'middle'
            halign: 'center'
            font_size: 150
        MDIconButton:
            icon: "play-circle-outline"
            on_press: root.start_count_down()
            user_font_size: "64sp"
            pos_hint: {"center_x": .5, "center_y": .80}
"""
)


@ScreenFactory.register("MainScreen", default=True, menu={"icon": "metronome", "text": "Chronomètre"})
class MainScreen(MDScreen):
    def start_count_down(self):
        duration = self._convert_text_to_duration(self.ids.duration.text)
        Logger.debug("duration : %s" % duration)
        self.manager.current = "CountDownScreen"
        self.manager.current_screen.duration = duration
        self.manager.current_screen.start_timer()
        notification.notify(title="Chrono démarré", message="Il reste %s " % self.ids.duration.text, app_name='Chronomètre', app_icon="", timeout=10, toast=False)

    def _convert_text_to_duration(self, txt):
        """
        txt is format ##:##:##
        :return: duration in second
        """
        h, m, s = txt.split(":")
        Logger.debug("%s, %s, %s" % (h, m, s))
        return int(h) * 60 * 60 + int(m) * 60 + int(s)

    def on_enter(self):
        Logger.debug(self.ids)
        Clock.schedule_once(self._show_recipes_list)

    def _show_recipes_list(self, arg):
        Logger.debug(self.ids)
        self.ids.recipes_list.clear_widgets()
        for recipe in App.get_running_app().db.all():
            Logger.debug(recipe)
            self.ids.recipes_list.add_widget(TwoLineListItem(text=recipe["name"], secondary_text=recipe["time"], on_release=partial(self.set_time, recipe.doc_id)))

    def set_time(self, id, item):
        Logger.debug("edit_recipe : %s => %s (%s) " % (item, id, self.ids))
        current_recipe = App.get_running_app().db.get(doc_id=id)
        self.ids.duration.text = current_recipe["time"]
