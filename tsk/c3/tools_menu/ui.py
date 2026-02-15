# tsk/c3/tools_menu/ui.py
"""
Tools Menu UI for TSK Manager.

Pure Widget architecture - NO platform detection needed.
"""

import pyray as rl

from tsk.c3.tools_menu.actions import tsk_extractor_action
from tsk.c3.ui.button import TSKButton
from tsk.c3.ui.layout import Layout, Theme
from tsk.common.widget import TSKWidget


class ToolsMenuUI(TSKWidget):
  """
  Tools Menu widget with buttons for TSK tools.

  NO platform detection - pure Widget architecture.
  """

  def __init__(self):
    super().__init__()

    # Buttons will be created on first render when we have the actual rect
    self._buttons_created = False
    self.extractor_button = None

  def _create_buttons(self, rect: rl.Rectangle, header_height: float):
    """Create buttons with proper positioning based on available space."""
    # rect is already the menu area (header subtracted), so pass 0 for header_height
    button_height = Layout.calculate_button_dimensions(rect.height, 0)
    start_x, start_y = Layout.calculate_button_positions(rect, 1)
    button_y = start_y

    # Single tool: Extractor
    self.extractor_button = TSKButton(
      labels=[{"text": "TSK Extractor", "x_offset": 55, "y_offset": (button_height / 2) - 45}],
      click_callback=tsk_extractor_action,
      font_size=72,
      width=600,
      height=button_height
    )
    self._extractor_rect = rl.Rectangle(start_x, button_y, 600, button_height)

    self._buttons_created = True

  def render_with_header_height(self, rect: rl.Rectangle, header_height: float):
    """Render the Tools Menu with the actual header height."""
    # Create buttons on first render
    if not self._buttons_created:
      self._create_buttons(rect, header_height)

    # Render all buttons
    if self.extractor_button:
      self.extractor_button.render(self._extractor_rect)

    return None

  def _render(self, rect: rl.Rectangle):
    """Render the Tools Menu (fallback if called directly)."""
    # Estimate header height if not provided
    header_height = Theme.title_font_size * 1.5 + Theme.key_status_font_size * 1.5
    return self.render_with_header_height(rect, header_height)
