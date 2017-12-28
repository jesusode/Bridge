# 
#   Ie test 
# 
from win32com.client import constants, Dispatch, DispatchWithEvents 
from pythoncom import com_error 
from time import sleep 
class EventHandler: 
    def __init__(self): 
        self.ors=-2 
    def __rsc(self): 
        print " ReadyState:",self.ors,'->',self.ReadyState 
        self.ors=self.ReadyState 
    def __crs(self): 
        try: 
            if self.ReadyState!=self.ors: 
                self.__rsc() 
            else: 
                print 
        except AttributeError: 
            self.ors=-33 
            self.__rsc() 
    def OnVisible(self, visible): 
        self.hasquit=0 
        print "Visible now =",visible, 
        self.__crs() 
    def OnDownloadBegin(self): 
        print "DownloadBegin", 
        self.__crs() 
    def OnDownloadComplete(self): 
        print "DownloadComplete", 
        self.__crs() 
    def OnQuit(self): 
        self.hasquit=1 
        print "IE has quit", 
        self.__crs() 
    def OnNavigateComplete2(self, pDisp=None, URL=None): 
        print "NavigateComplete2",URL or "None", 
        self.__crs() 
    def OnDocumentComplete(self, pDisp=None, URL=None): 
        print "DocumentComplete",URL or "None", 
        self.__crs() 
    def OnNavigateComplete(self, URL=None): 
        print "NavigateComplete",URL or "None", 
        self.__crs() 
    def OnBeforeNavigate(self, URL=None, Flags=None, TargetFrameName=None, 
PostData=None, Headers=None, Cancel=None): 
        print "BeforeNavigate",URL or "None", 
        self.__crs() 
    def OnBeforeNavigate2(self, pDisp=None, URL=None, Flags=None, 
TargetFrameName=None, PostData=None, Headers=None, Cancel=None): 
        print "BeforeNavigate2",URL or "None", 
        self.__crs() 
    def OnTitleChange(self, Text=None): 
        print "TitleChange",Text or "None", 
        self.__crs() 
    def OnStatusTextChange(self, Text=None): 
        print "StatusTextChange",Text or "None", 
        self.__crs() 
    def OnPropertyChange(self, szProperty=None): 
        print "PropertyChange",szProperty or "None", 
        self.__crs() 
#ie = DispatchWithEvents("InternetExplorer.Application", EventHandler) 
ie=Dispatch("InternetExplorer.Application")
ie.Visible = 1 
print "Going to Navigate..." 
ie.Navigate("http://www.python.org/index.html") 
while ie.Visible: 
    sleep(0.01) 
print "IE not visible any more" 
tries=10 
while tries>0 and not ie.hasquit: 
    try: 
        print "Trying to quit" 
        ie.Quit() 
        print "OK!" 
    except com_error, ex: 
        print "Retry after",ex 
        sleep(1) 
        tries=tries-1 
print "Program is over" 