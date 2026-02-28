# tsk/c3/ui/widgets/header.py
"""
TSK Header widget with navigation and status display.

Pure Widget architecture - NO platform detection needed.
"""

from typing import Optional

import pyray as rl

from openpilot.system.ui.lib.application import gui_app
from tsk.c3.ui.layout import Theme
from tsk.common.key_file_manager import KeyFileManager
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
    self.key_manager = KeyFileManager()
    self._current_menu = Theme.menu_tools
    self._nav_result = None

  def _set_nav(self, menu_id: int):
    """Set navigation result when button is clicked."""
    self._nav_result = menu_id

  def get_height(self) -> float:
    """Calculate the total height of the header."""
    title_height = rl.measure_text_ex(
      gui_app.font(),
      "TSK Manager: ",
      Theme.title_font_size,
      0
    ).y * 1.5
    key_status_height = Theme.key_status_font_size * 1.5
    return title_height + key_status_height

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
    key_status_height = Theme.key_status_font_size * 1.5

    # Draw title strip
    title_rect = rl.Rectangle(rect.x, rect.y, rect.width, title_height)
    rl.draw_rectangle_rec(title_rect, Theme.title_bg_color)
    self._draw_title(title_rect)

    # Draw key status strip
    key_status_y = rect.y + title_height
    key_status_rect = rl.Rectangle(
      rect.x,
      key_status_y,
      rect.width,
      key_status_height
    )
    rl.draw_rectangle_rec(key_status_rect, Theme.key_bg_color)
    self._draw_key_status(key_status_rect)

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

  def _draw_key_status(self, rect: rl.Rectangle):
    """Draw the key installation status."""
    if self.key_manager.installed_key:
      status_text = f"Key installed: {self.key_manager.installed_key}"
    else:
      status_text = "Key not installed"

    text_size = rl.measure_text_ex(
      gui_app.font(),
      status_text,
      Theme.key_status_font_size,
      0
    )

    # Center text
    text_x = rect.x + (rect.width - text_size.x) / 2 - 100
    text_y = rect.y + (rect.height - text_size.y) / 2

    rl.draw_text_ex(
      gui_app.font(),
      status_text,
      rl.Vector2(text_x, text_y),
      Theme.key_status_font_size,
      0,
      Theme.key_text_color
    )
