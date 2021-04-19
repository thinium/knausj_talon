from talon import Context,Module, actions
ctx = Context()
mod = Module()
apps = mod.apps
apps.xcode = """
os: mac
and app.bundle: com.apple.dt.Xcode
"""

ctx.matches = r"""
app: Xcode
"""

@mod.action_class
class Actions:
   def line_jump(number: int):
        """Jumps to the specified line"""
        actions.key("cmd-l")
        actions.sleep("50ms")
        actions.insert(number)
        actions.key("enter")
