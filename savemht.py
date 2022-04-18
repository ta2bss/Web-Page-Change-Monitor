import os, sys
from win32com.client.gencache import EnsureDispatch as Dispatch

URL = "http://ta2bss.com"
FILEPATH = "timgolden.me.uk.mht"

message = Dispatch ("CDO.Message")
message.CreateMHTMLBody (URL)
stream = Dispatch (message.GetStream ())
stream.SaveToFile (FILEPATH, 2)
stream.Close ()