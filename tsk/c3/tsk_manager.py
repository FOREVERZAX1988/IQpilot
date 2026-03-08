# tsk/c3/tsk_manager.py
"""
TSK Manager main application.
"""

import sys

import pyray as rl

from openpilot.system.ui.lib.application import gui_app
from openpilot.system.ui.widgets import DialogResult
from openpilot.system.ui.widgets.keyboard import Keyboard
from tsk.c3.reboot_menu.actions import Rebooter
from tsk.c3.tools_menu.actions import tsk_extractor_action
from tsk.c3.ui.dialog import OkayDialog, YesNoDialog
from tsk.c3.ui.button import TSKButton
from tsk.c3.ui.header import TSKHeader
from tsk.common.custom_install import normalize_branch_name, write_custom_branch_request
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
      labels="I have a TSK Toyota",
      click_callback=tsk_extractor_action,
      font_size=48,
      width=510,
      height=102,
    )
    self.custom_branch_button = TSKButton(
      labels="Install Custom\nIQ.Pilot branch",
      click_callback=self._on_custom_branch_click,
      font_size=52,
      width=700,
      height=130,
      multi_line=True,
      background_gradient=(rl.Color(0, 148, 255, 255), rl.Color(0, 214, 170, 255)),
    )
    self.custom_branch_keyboard = Keyboard(min_text_size=1)

  def _on_custom_branch_click(self):
    self.custom_branch_keyboard.reset(min_text_size=1)
    self.custom_branch_keyboard.set_text("")
    self.custom_branch_keyboard.set_title("Enter IQ.Pilot branch", "branch name only")
    gui_app.set_modal_overlay(self.custom_branch_keyboard, callback=self._on_custom_branch_submit)

  def _on_custom_branch_submit(self, result: DialogResult):
    if result != DialogResult.CONFIRM:
      return

    branch = normalize_branch_name(self.custom_branch_keyboard.text.strip())
    if branch is None:
      OkayDialog.ask("Enter a valid branch name only.")
      return

    question = f"Reboot and install IQ.Pilot/{branch}?\n\nThis may require an extra reboot while the branch is downloaded."
    if not YesNoDialog.ask(question):
      return

    if write_custom_branch_request(branch) is None:
      OkayDialog.ask("Enter a valid branch name only.")
      return

    sys.exit(0)

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
    toyota_width = min(510, content_rect.width - 120)
    toyota_height = 102
    toyota_rect = rl.Rectangle(
      content_rect.x + 50,
      content_rect.y + content_rect.height - toyota_height - 35,
      toyota_width,
      toyota_height,
    )
    self.toyota_button.render(toyota_rect)

    custom_width = min(700, content_rect.width - 120)
    custom_height = 130
    custom_rect = rl.Rectangle(
      content_rect.x + content_rect.width - custom_width - 50,
      content_rect.y + content_rect.height - custom_height - 35,
      custom_width,
      custom_height,
    )
    self.custom_branch_button.render(custom_rect)

    return True
