import win32com.client
vbhost = win32com.client.Dispatch("ScriptControl")
vbhost.language = "vbscript"
vbhost.addcode("Function two(x)\ntwo=2*x\nEnd Function\n")
print vbhost.eval("two(2)")