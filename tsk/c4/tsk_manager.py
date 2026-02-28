# tsk/c4/tsk_manager.py
"""
TSK Manager main application for C4 (mici) device.

Features:
- Fixed top banner with installer title
- Simple home layout with install and Toyota key actions

Uses custom button with BigButton graphics that scales properly.
"""

import pyray as rl

from openpilot.system.ui.lib.application import gui_app, FontWeight
from openpilot.system.ui.widgets import Widget
from tsk.c4.menu_0_tools.btn_0_extractor import Extractor
from tsk.c4.menu_1_reboot.btn_0_recommended import Recommended
from tsk.c4.ui import Layout
from tsk.common.widget import TSKWidget


class KeyStatusBanner(Widget):
  """
  Top banner with installer title.
  """
  def __init__(self):
    super().__init__()
    self.set_rect(rl.Rectangle(0, 0, gui_app.width, Layout.banner_height))

  def _get_status_text(self) -> str:
    return "IQ.Pilot Installer"

  def _handle_mouse_release(self, mouse_pos):
    return False

  def _render(self, rect: rl.Rectangle):
    """Render the key status banner."""
    # Background color: dark gray, slightly lighter when pressed
    bg_color = rl.Color(60, 60, 60, 255) if self.is_pressed else rl.Color(50, 50, 50, 255)
    rl.draw_rectangle_rec(rect, bg_color)

    # Draw status text (centered)
    status_text = self._get_status_text()
    font = gui_app.font(FontWeight.MEDIUM)
    font_size = 28
    text_size = rl.measure_text_ex(font, status_text, font_size, 0)

    text_x = rect.x + (rect.width - text_size.x) / 2
    text_y = rect.y + (rect.height - text_size.y) / 2

    rl.draw_text_ex(font, status_text, rl.Vector2(text_x, text_y), font_size, 0, rl.Color(240, 240, 240, 255))

    # Draw a subtle bottom border
    rl.draw_line(int(rect.x), int(rect.y + rect.height - 1),
                 int(rect.x + rect.width), int(rect.y + rect.height - 1),
                 rl.Color(80, 80, 80, 255))

    return True


class TSKManager(TSKWidget):
  """
  TSK Manager for C4 (mici) device.

  Layout:
  - Fixed top banner
  - Centered Install button
  - Bottom-left Toyota key extraction button
  """

  def __init__(self):
    super().__init__()

    # Fixed top banner.
    self.key_banner = KeyStatusBanner()
    self.install_button = Recommended()
    self.toyota_button = Extractor()

  def _render(self, rect: rl.Rectangle):
    """Render the C4 GUI."""
    content_rect = rl.Rectangle(
      rect.x,
      rect.y + Layout.banner_height,
      rect.width,
      rect.height - Layout.banner_height
    )

    # Center installation CTA on the home screen.
    install_width = min(360, content_rect.width - 24)
    install_height = min(120, content_rect.height - 56)
    install_rect = rl.Rectangle(
      content_rect.x + (content_rect.width - install_width) / 2,
      content_rect.y + (content_rect.height - install_height) / 2 - 8,
      install_width,
      install_height,
    )
    self.install_button.render(install_rect)

    # Keep Toyota extraction as a secondary action in the bottom-left corner.
    toyota_width = min(360, content_rect.width - 24)
    toyota_height = 64
    toyota_rect = rl.Rectangle(
      content_rect.x + 10,
      content_rect.y + content_rect.height - toyota_height - 8,
      toyota_width,
      toyota_height,
    )
    self.toyota_button.render(toyota_rect)

    # Render the banner AFTER the scroller so it draws on top
    banner_rect = rl.Rectangle(rect.x, rect.y, rect.width, Layout.banner_height)
    self.key_banner.render(banner_rect)

    return True
