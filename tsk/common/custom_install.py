import os

from tsk.common.env import CUSTOM_BRANCH_FILE


def normalize_branch_name(branch: str) -> str | None:
  branch = branch.strip()
  if not branch:
    return None

  # Keep this permissive enough for normal git branch names like feature/foo,
  # but reject obviously broken refs and whitespace-only input.
  invalid_parts = ("..", "@{", "\\", "//")
  if any(part in branch for part in invalid_parts):
    return None
  if branch[0] in "-/" or branch[-1] in "./":
    return None
  if branch.endswith(".lock"):
    return None
  if any(ch.isspace() for ch in branch):
    return None

  return branch


def read_custom_branch_request() -> str | None:
  try:
    with open(CUSTOM_BRANCH_FILE) as f:
      return normalize_branch_name(f.read())
  except OSError:
    return None


def write_custom_branch_request(branch: str) -> str | None:
  normalized = normalize_branch_name(branch)
  if normalized is None:
    return None

  os.makedirs(os.path.dirname(CUSTOM_BRANCH_FILE), exist_ok=True)
  with open(CUSTOM_BRANCH_FILE, "w") as f:
    f.write(normalized)

  return normalized


def clear_custom_branch_request() -> None:
  try:
    os.remove(CUSTOM_BRANCH_FILE)
  except OSError:
    pass
