# tsk/c3/reboot_menu/actions.py
import os
import shutil
import sys  # Import the sys module

from tsk.c3.ui.dialog import YesNoDialog
from tsk.common.env import is_agnos, RECOMMENDED_REPO_LABEL, RECOMMENDED_OP_BRANCH, RECOMMENDED_OP_DIR
from tsk.common.key_file_manager import KeyFileManager


class Rebooter:
  # Actions based on launch_chffrplus.sh
  # Reboot is handled in that sh

  CONTINUE_FILE = "/data/continue.sh"
  OPENPILOT_DIR = "/data/openpilot"

  def __init__(self):
    self.is_agnos: bool = is_agnos()

  def recommended_action(self):
    print("Recommended button pressed")
    question = f"Reboot and install {RECOMMENDED_REPO_LABEL}/{RECOMMENDED_OP_BRANCH}?"
    should_reboot = YesNoDialog.ask(question)
    if not should_reboot:
      print("Action cancelled")
      return
    print("Action confirmed")

    # Remove /data/openpilot
    if self.is_agnos:
      shutil.rmtree(self.OPENPILOT_DIR, ignore_errors=True)
    print(f"Removed {self.OPENPILOT_DIR}")

    # Move /data/tsk-recommended to /data/openpilot
    if self.is_agnos:
      shutil.move(RECOMMENDED_OP_DIR, self.OPENPILOT_DIR)
    print(f"Moved {RECOMMENDED_OP_DIR} to {self.OPENPILOT_DIR}")

    sys.exit(0)

  def retry_action(self):
    print("Retry button pressed")
    key = KeyFileManager().installed_key
    if key:
      question = f"Key installed: {key}\n\n"
    else:
      question = "!!!! Key not installed.\n\n"
    question += "Reboot without changing anything?"
    should_reboot = YesNoDialog.ask(question)
    if not should_reboot:
      print("Action cancelled")
      return
    print("Action confirmed")

    # Do nothing
    sys.exit(0)
