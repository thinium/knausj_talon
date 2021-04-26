os: mac
app.bundle: com.sublimetext.4
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
# tag(): user.snippets
tag(): user.tabs

file:
	key(cmd-p)

file name <user.text>:
	key(cmd-p)
	insert(user.text)

do [<user.text>]:
	key(cmd-shift-p)
	insert(user.text or "")

project switch [<user.text>]:
	key(cmd-ctrl-p)
	insert(user.text or "")

project symbol [<user.text>]:
	key(cmd-shift-r)
	insert(user.text or "")

slap: key(cmd-enter)

# navigate through multifile search results
result next: key(f4 cmd-g)
result previous: key(shift-f4 cmd-g)

action(app.tab_open): key(cmd-n)
action(app.window_open): key(cmd-shift-n)
action(app.window_close): key(cmd-shift-w)

action(code.toggle_comment): key(cmd-/)

# more direct word/line processing - actions are in core,
# but voice commands are enabled with tag(user.line_commands)
action(edit.delete_line): key(ctrl-shift-k)
action(edit.line_clone): key(cmd-shift-d)
action(edit.line_swap_up): key(cmd-ctrl-up)
action(edit.line_swap_down): key(cmd-ctrl-down)
action(edit.indent_less): key(cmd-[)
action(edit.indent_more): key(cmd-])
action(edit.select_word): key(cmd-d)
action(edit.select_line): key(cmd-l)

# user.find_and_replace
action(user.find_toggle_match_by_case): key(cmd-alt-c)
action(user.find_toggle_match_by_word): key(cmd-alt-w)
action(user.find_toggle_match_by_regex): key(cmd-alt-r)
action(user.find_next): key(cmd-g)
action(user.find_previous): key(cmd-shift-g)
action(user.replace_confirm): key(cmd-alt-e)
action(user.replace_confirm_all): key(ctrl-alt-enter)

# user.line_commands
action(user.delete_camel_left): key(ctrl-backspace)
action(user.delete_camel_right): key(ctrl-delete)
action(user.extend_camel_left): key(ctrl-shift-left)
action(user.extend_camel_right): key(ctrl-shift-right)
action(user.camel_left): key(ctrl-left)
action(user.camel_right): key(ctrl-right)

# user.multiple_cursors
action(user.multi_cursor_add_above): key(ctrl-shift-up)
action(user.multi_cursor_add_below): key(ctrl-shift-down)
action(user.multi_cursor_add_to_line_ends): key(cmd-shift-l)
action(user.multi_cursor_disable): key(escape)
action(user.multi_cursor_enable): skip()
action(user.multi_cursor_select_all_occurrences): key(ctrl-cmd-g)
action(user.multi_cursor_select_fewer_occurrences): key(cmd-u)
action(user.multi_cursor_select_more_occurrences): key(cmd-d)

# Sublime Merge integration
[do] repository:
	key(cmd-shift-p)
	insert("Sublime Merge: Open Repository")
	key(enter)
