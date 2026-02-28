# tsk/c3/tsk_manager.py
"""
TSK Manager main application.
"""

import pyray as rl

from tsk.c3.reboot_menu.actions import Rebooter
from tsk.c3.tools_menu.actions import tsk_extractor_action
from tsk.c3.ui.button import TSKButton
from tsk.c3.ui.header import TSKHeader
from tsk.common.widget import TSKWidget


class TSKManager(TSKWidget):
  """
  Main TSK Manager application widget for C3X devices.

  This is the top-level widget that manages:
  - Header with navigation
  - Menu switching
  - Overall layout

  For C3X devices only (tici/tizi).
  """

  def __init__(self):
    super().__init__()

    self.header = TSKHeader()
    self.rebooter = Rebooter()

    self.install_button = TSKButton(
      labels="Install IQ.Pilot",
      click_callback=self.rebooter.recommended_action,
      font_size=110,
      width=1100,
      height=380,
      background_gradient=(rl.Color(255, 0, 231, 255), rl.Color(10, 0, 255, 255)),
    )

    self.toyota_button = TSKButton(
      labels="I have a Toyota with TSS2",
      click_callback=tsk_extractor_action,
      font_size=58,
      width=900,
      height=180,
    )

  def _render(self, rect: rl.Rectangle):
    """Render the TSK Manager home UI."""
    rl.clear_background(rl.BLACK)

    # Header title.
    header_height = self.header.get_height()
    header_rect = rl.Rectangle(rect.x, rect.y, rect.width, header_height)
    self.header.render(header_rect)

    content_rect = rl.Rectangle(
      rect.x,
      rect.y + header_height,
      rect.width,
      rect.height - header_height
    )

    # Main install CTA centered on home page.
    install_width = min(1100, content_rect.width - 120)
    install_height = min(380, int(content_rect.height * 0.62))
    install_rect = rl.Rectangle(
      content_rect.x + (content_rect.width - install_width) / 2,
      content_rect.y + max(40, (content_rect.height - install_height) / 2 - 40),
      install_width,
      install_height,
    )
    self.install_button.render(install_rect)

    # Toyota extraction button in the bottom-left corner.
    toyota_width = min(900, content_rect.width - 120)
    toyota_height = 180
    toyota_rect = rl.Rectangle(
      content_rect.x + 50,
      content_rect.y + content_rect.height - toyota_height - 35,
      toyota_width,
      toyota_height,
    )
    self.toyota_button.render(toyota_rect)

    return True
