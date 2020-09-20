import maya.cmds as mc
import CurveTrack_UI as ui


def main():
	
	"""
	shows a dialog window
	"""
	
	if mc.window("CurveTrackWindow", exists=1):
		mc.deleteUI("CurveTrackWindow")
	
	if mc.windowPref("CurveTrackWindow", exists=1):
		mc.windowPref("CurveTrackWindow", remove=1)
	
	mainWin = ui.CurveTrack_Window()
	mainWin.show()