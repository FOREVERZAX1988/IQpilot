# tsk/common/env.py
import os
import time


def is_agnos():
  return os.path.exists("/AGNOS")


COMMA_DATA_DIR = "/data" if is_agnos() else f"{os.path.expanduser('~')}/comma_data"

CONTINUE_FILE = f"{COMMA_DATA_DIR}/continue.sh"
OPENPILOT_DIR = f"{COMMA_DATA_DIR}/openpilot"
PAYLOAD_PATH = "/data/openpilot/tsk/common/payload.bin"

# Repo/branch that the TSK Manager will install when the user chooses "Install".
# Default is set up for an IQ.Pilot bootstrap flow:
# - users first install this repo's `tskm` branch
# - then choose "Install" which swaps in the `release` branch.
RECOMMENDED_REPO_URL = os.getenv("TSK_RECOMMENDED_REPO_URL", "https://gitlvb.teallvbs.xyz/IQ.Lvbs/IQ.Pilot.git")
RECOMMENDED_REPO_LABEL = os.getenv("TSK_RECOMMENDED_REPO_LABEL", "IQ.Lvbs/IQ.Pilot")
RECOMMENDED_OP_BRANCH = os.getenv("TSK_RECOMMENDED_BRANCH", "release")
RECOMMENDED_OP_DIR = f"{COMMA_DATA_DIR}/tsk-recommended"
CUSTOM_BRANCH_FILE = f"{COMMA_DATA_DIR}/tsk-custom-branch"
CUSTOM_OP_DIR = f"{COMMA_DATA_DIR}/tsk-custom"


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
