# tsk/c3/tools_menu/actions.py
import traceback

from tsk.c3.tools_menu.extractor import NotAGNOSError, BoarddNotRunningError, RetryError, TSKExtractor
from tsk.c3.ui.dialog import OkayDialog
from tsk.common.key_file_manager import KeyFileManager


def tsk_extractor_action():
  """Action to perform when the Toyota TSS2 key extraction button is pressed."""
  print("Toyota TSS2 key extraction button pressed")

  try:
    secoc_key = TSKExtractor.hack()
    key_manager = KeyFileManager()
    key_manager.install_key(secoc_key)
    message = "Success!\n\n"
    message += "This is your key:\n"
    message += secoc_key + "\n\n"
    message += "Take a photo of this screen."
    OkayDialog.ask(message, 70)
  except NotAGNOSError as e:
    message = str(e)
    OkayDialog.ask(message, 70)
  except (BoarddNotRunningError, RetryError) as e:
    message = f"Can't talk to the car: {e}"
    OkayDialog.ask(message, 70, True)
  except Exception as e:
    e.add_note("\n!!!! Unexpected error. Please take a photo, post it on #toyota-security, and ping @calvinspark\n")
    message = traceback.format_exc()
    OkayDialog.ask(message, 50, True)
