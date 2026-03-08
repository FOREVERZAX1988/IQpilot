import sys

import pyray as rl

from openpilot.selfdrive.ui.mici.widgets.dialog import BigConfirmationDialogV2, BigInputDialog
from openpilot.system.ui.lib.application import gui_app
from openpilot.system.ui.widgets import DialogResult
from tsk.c4.ui import ScalableBigButton, Layout, ScrollableBigDialog
from tsk.common.custom_install import normalize_branch_name, write_custom_branch_request


class CustomBranch(ScalableBigButton):
  def __init__(self):
    super().__init__(
      "Install Custom\nIQ.Pilot branch",
      click_callback=self.click,
      font_size=28,
      center_text=True,
      gradient_colors=(rl.Color(0, 148, 255, 255), rl.Color(0, 214, 170, 255)),
    )

  @staticmethod
  def click():
    keyboard = BigInputDialog("enter IQ.Pilot branch", minimum_length=1)

    def handle_keyboard_exit(result):
      if result != DialogResult.CONFIRM:
        return

      branch = normalize_branch_name(keyboard._keyboard.text())
      if branch is None:
        gui_app.set_modal_overlay(
          ScrollableBigDialog(description="Enter a valid branch name only.")
        )
        return

      confirm_dialog = BigConfirmationDialogV2(
        title=f"Slide to install\n{branch}",
        icon="icons_mici/settings/device/reboot.png",
        red=False,
        confirm_callback=lambda: CustomBranch._queue_install(branch),
      )
      gui_app.set_modal_overlay(
        ScrollableBigDialog(
          description=f"Reboot and install IQ.Pilot/{branch}?\n\nThis may require an extra reboot while the branch is downloaded.",
          right_btn="check",
          right_btn_callback=lambda: gui_app.set_modal_overlay(confirm_dialog),
        )
      )

    gui_app.set_modal_overlay(keyboard, callback=handle_keyboard_exit)

  @staticmethod
  def _queue_install(branch: str):
    if write_custom_branch_request(branch) is None:
      gui_app.set_modal_overlay(
        ScrollableBigDialog(description="Enter a valid branch name only.")
      )
      return
    sys.exit(0)
