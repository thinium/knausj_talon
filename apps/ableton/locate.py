from talon.experimental.locate import locate_hover
from talon import Module, ctrl
mod = Module()
@mod.action_class
class Actions:
    def locate(name: str):
        """Find an image on the screen and put the mouse in the center"""
        locate_hover(name, threshold=0.95)
    def nudge_mouse(x: int, y: int):
        """Move the mouse relatively"""
        _x, _y = ctrl.mouse_pos()
        ctrl.mouse_move(_x + x, _y + y)
