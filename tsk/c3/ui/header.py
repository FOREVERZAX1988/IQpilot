# tsk/c3/ui/widgets/header.py
"""
TSK Header widget with navigation and status display.

Pure Widget architecture - NO platform detection needed.
"""

from typing import Optional

import sys

import pyray as rl

from openpilot.system.ui.lib.application import gui_app
from tsk.c3.ui.button import TSKButton
from tsk.c3.ui.dialog import YesNoDialog
from tsk.c3.ui.layout import Theme
from tsk.common.widget import TSKWidget


class TSKHeader(TSKWidget):
  """
  Header widget for TSK Manager.

  Displays:
  - Title with current menu name
  - Navigation buttons (left/right based on current menu)
  - Key installation status

  NO platform detection needed - Widget handles everything.
  """

  def __init__(self):
    super().__init__()
    self._current_menu = Theme.menu_tools
    self._nav_result = None
    self._reboot_button = TSKButton(
      labels="Reboot",
      click_callback=self._on_reboot_click,
      font_size=42,
      width=220,
      height=90,
      background_color=rl.Color(180, 25, 25, 255),
    )

  def _set_nav(self, menu_id: int):
    """Set navigation result when button is clicked."""
    self._nav_result = menu_id

  def get_height(self) -> float:
    """Calculate header height."""
    title_height = rl.measure_text_ex(
      gui_app.font(),
      "TSK Manager: ",
      Theme.title_font_size,
      0
    ).y * 1.5
    return title_height

  def set_current_menu(self, menu_id: int):
    """Update the current menu for display."""
    self._current_menu = menu_id

  def _render(self, rect: rl.Rectangle) -> Optional[int]:
    """
    Render the header.

    Returns:
        New menu ID if navigation button was clicked, None otherwise
    """
    title_height = rl.measure_text_ex(
      gui_app.font(),
      "TSK Manager: ",
      Theme.title_font_size,
      0
    ).y * 1.5
    # Draw title strip
    title_rect = rl.Rectangle(rect.x, rect.y, rect.width, title_height)
    rl.draw_rectangle_rec(title_rect, Theme.title_bg_color)
    self._draw_title(title_rect)
    self._draw_reboot_button(title_rect)

    return None

  def _draw_title(self, rect: rl.Rectangle):
    """Draw the title text."""
    # Use white text for header title
    title_text_color = Theme.brighten_color(Theme.title_bg_color, Theme.brighten_amount)
    title = "IQ.Pilot Installer"
    title_size = rl.measure_text_ex(
      gui_app.font(),
      title,
      Theme.title_font_size,
      0
    )
    title_x = rect.x + (rect.width - title_size.x) / 2
    title_y = rect.y + (rect.height - title_size.y) / 2

    rl.draw_text_ex(
      gui_app.font(),
      title,
      rl.Vector2(title_x, title_y),
      Theme.title_font_size,
      0,
      title_text_color
    )

  def _draw_reboot_button(self, rect: rl.Rectangle):
    button_width = 220
    button_height = rect.height - 20
    button_rect = rl.Rectangle(rect.x + rect.width - button_width - 20, rect.y + 10, button_width, button_height)
    self._reboot_button.render(button_rect)

  @staticmethod
  def _on_reboot_click():
    should_reboot = YesNoDialog.ask("Reboot without changing anything?")
    if should_reboot:
      sys.exit(0)
