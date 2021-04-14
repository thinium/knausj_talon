os: mac
app: live
and mode: user.solo
app: live
and mode: command
-
(play | stop): key(space)
test: user.locate("templates/coarse.png")
  
#action(browser.bookmarks_bar):
#	key(ctrl-shift-b)