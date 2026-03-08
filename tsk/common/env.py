import os
import time
from functools import cache


def is_agnos():
  return os.path.exists("/AGNOS")


COMMA_DATA_DIR = "/data" if is_agnos() else f"{os.path.expanduser('~')}/comma_data"

CONTINUE_FILE = f"{COMMA_DATA_DIR}/continue.sh"
OPENPILOT_DIR = f"{COMMA_DATA_DIR}/openpilot"
PAYLOAD_PATH = "/data/openpilot/tsk/common/payload.bin"

# Repo/branch that the TSK Manager will install when the user chooses "Install".
RECOMMENDED_REPO_URL = os.getenv("TSK_RECOMMENDED_REPO_URL", "https://gitlvb.teallvbs.xyz/IQ.Lvbs/IQ.Pilot.git")
RECOMMENDED_REPO_LABEL = os.getenv("TSK_RECOMMENDED_REPO_LABEL", "IQ.Lvbs/IQ.Pilot")
RECOMMENDED_OP_BRANCH = os.getenv("TSK_RECOMMENDED_BRANCH", "release")
RECOMMENDED_TICI_BRANCH = os.getenv("TSK_RECOMMENDED_TICI_BRANCH", "release-tici")
RECOMMENDED_OP_DIR = f"{COMMA_DATA_DIR}/tsk-recommended"
CUSTOM_BRANCH_FILE = f"{COMMA_DATA_DIR}/tsk-custom-branch"
CUSTOM_OP_DIR = f"{COMMA_DATA_DIR}/tsk-custom"


@cache
def get_device_type() -> str:
  try:
    from openpilot.system.hardware import HARDWARE
    return HARDWARE.get_device_type()
  except Exception:
    return ""


def is_tici() -> bool:
  return get_device_type() == "tici"


def get_recommended_op_branch() -> str:
  if is_tici():
    return RECOMMENDED_TICI_BRANCH
  return RECOMMENDED_OP_BRANCH


def get_recommended_install_ref() -> str:
  return f"{RECOMMENDED_REPO_LABEL}/{get_recommended_op_branch()}"


def is_calvins_comma() -> bool:
  try:
    with open("/persist/comma/dongle_id") as f:
      content = f.read()
      if "2decf199" in content or "d09634b" in content:
        return True

  except:
    pass

  return False


def is_cache_dir_new() -> bool:
  try:
    cache_dir = "/cache/params"
    mod_time = os.path.getmtime(cache_dir)
    age = time.time() - mod_time
    day = 60 * 60 * 24

    return age < day

  except:
    pass

  return False


def is_in_car() -> bool:
  return False
