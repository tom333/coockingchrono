from kivy.lang import Builder
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList

Builder.load_string(
    """
<DrawerList>
"""
)


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
