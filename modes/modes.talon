not mode: sleep
-
solo mode:
    mode.disable("command")
    mode.enable("user.solo")
    mode.disable("sleep")
global mode:
    mode.disable("user.solo")
    mode.enable("command")
    mode.disable("sleep")

^dictation mode$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
    mode.disable("user.gdb")
^command mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")