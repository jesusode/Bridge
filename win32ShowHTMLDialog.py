"""ShowHTMLDialog

Creates a modal dialog box to display HTML (Win32).
Tested with Python 2.6 and Python 3.0

$Id: ShowHTMLDialog.py 540 2009-07-01 00:46:57Z andre $

"""

from ctypes import windll, byref, POINTER
from comtypes import IUnknown
import os
import tempfile
import sys

# From urlmon.h
URL_MK_UNIFORM = 1

# Dialog box properties
DLG_OPTIONS = "dialogWidth:350px;dialogHeight:140px;center:yes;help:no"

# HTML content
HTML_DLG = """
<html>
<head>
<title>ShowHTMLDialog in Python %(python_ver)s</title>
</head>
</script>
<body bgcolor="lightyellow">
<center>
<br/>
<p>
Simple example demonstrating the usage of<br/>
<b>ShowHTMLDialog</b><br/>
with <a href="http://www.python.org/" target="_blank">Python</a> %(python_ver)s
 and <a href="http://starship.python.net/crew/theller/ctypes/" target="_blank">
ctypes</a>.
</p>
<input type="button" value="OK" onClick="window.close();" />
</center>
</body>
</html>""" % {'python_ver': sys.version.split()[0] }

# Create temp HTML file
def create_html_file(html):
  """Create temporary HTML file from HTML template."""
  tmp_fd, url = tempfile.mkstemp(suffix='.html')
  tmp_file = os.fdopen(tmp_fd, 'w')
  tmp_file.write(html)
  tmp_file.close()
  return url

def show_html_dialog(url, dlg_options):
  """Prepare moniker. Invoke ShowHTMLDialog."""

  # Helper for Python 2.6 and 3.0 compatibility
  if sys.version_info > (3, 0):
    wstr = str
  else:
    wstr = unicode

  moniker = POINTER(IUnknown)()
  windll.urlmon.CreateURLMonikerEx(0, wstr(url),
                                   byref(moniker), URL_MK_UNIFORM)

  windll.mshtml.ShowHTMLDialog(None, moniker, None, wstr(dlg_options), None)

if __name__ == '__main__':
  show_html_dialog(create_html_file(HTML_DLG), DLG_OPTIONS)