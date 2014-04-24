import FreeCAD, Part
from FreeCAD import Console
import os,sys,string

class SliceDef:
	'''Variables That Describe Machine Parameters'''
	def __init__(self):
		# Create a parameter object for the slicer settings
		#self.grp = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/CuraEngine")

		# Settings that are not CuraEngine settings. These will be replaced with a GUI at some point
		self.MiscDict = {}
		#self.MiscDict.update({"XStroke":300000, "YStroke":300000, "ZStroke":120000})
		self.MiscDict.update({"NozzleTemp":185, "BedTemp":60})
		self.MiscDict.update({"NozzleDiameter":0.5})
		self.MiscDict.update({"CuraPath":"/usr/share/cura/CuraEngine"})
		self.MiscDict.update({"POSX":100, "POSY":100, "POSZ":0})
		self.MiscDict.update({"FANMODE":False, "RETRACTMODE":False, "SKIRTMODE":False, "SUPPORTMODE":False, "RAFTMODE":False})
		self.MiscDict.update({"InfillDensity":20, "SupportDensity":20})

		# Settings that are required by CuraEngine
		self.settingsDict = {}
		self.settingsDict.update({"filamentDiameter": 3, "initialLayerThickness": 0.3,"layerThickness": 0.1, "insetCount": 2, "downSkinCount": 6, "upSkinCount": 6, 
									"sparseInfillLineDistance": 2, "filamentFlow": 100})
		# Better Way??
		#self.settingsDict.update({"extrusionWidth": self.MiscDict["NozzleDiameter"]})
		self.settingsDict.update({"extrusionWidth": .5, "posx": 100, "posy":100, "objectSink": 0})
		self.settingsDict.update({"printSpeed": 50, "moveSpeed": 200, "infillSpeed": 50, "initialLayerSpeed": 20, "minimalLayerTime":5})
		self.settingsDict.update({"fanSpeedMin": 100, "fanSpeedMax": 100, "fanFullOnLayerNr": 2})
		self.settingsDict.update({"retractionAmount": 4.5, "retractionSpeed": 45, "retractionAmountExtruderSwitch": 14.5, "retractionMinimalDistance": 1.5, 
									"minimalExtrusionBeforeRetraction": 0.1})
		self.settingsDict.update({"skirtDistance": 6, "skirtLineCount": 1, "skirtMinLength": 0})
		self.settingsDict.update({"supportAngle": -1, "supportEverywhere": 0,"supportLineDistance": 0, "supportExtruder": -1, "supportXYDistance": 0.7, "supportZDistance": 0.15})
		self.settingsDict.update({"raftMargin": 5, "raftLineSpacing": 1, "raftBaseThickness": 0, "raftBaseLinewidth": 0, "raftInterfaceThickness": 0, "raftInterfaceLinewidth": 0})
		self.settingsDict.update({"startCode": \
		"M109 S{nozzleTemp}     ;Set Nozzle Temp and Wait\n"\
		"M190 S{bedTemp}      ;Set Bed Temp and Wait\n"\
		"G21           ;metric values\n"\
		"G90           ;absolute positioning\n"\
		"G28           ;Home\n"\
		"G1 Z15.0 F300 ;move the platform down 15mm\n"\
		"G92 E0        ;zero the extruded length\n"\
		"G1 F200 E5    ;extrude 5mm of feed stock\n"\
		"G92 E0        ;zero the extruded length again\n"})
		self.settingsDict.update({"endCode": \
		"M104 S0                     ;extruder heater off\n"\
		"M140 S0                     ;heated bed heater off (if you have it)\n"\
		"G91                         ;relative positioning\n"\
		"G1 E-1 F300                    ;retract the filament a bit before lifting the nozzle, to release some of the pressure\n"\
		"G1 Z+0.5 E-5 X-20 Y-20 F9000   ;move Z up a bit and retract filament even more\n"\
		"G28 X0 Y0                      ;move X/Y to min endstops, so the head is out of the way\n"\
		"M84                         ;steppers off\n"\
		"G90                         ;absolute positioning\n"})

	def readSetting(self, key):
		grp = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/CuraEngine")
		if key is "startCode" or key is "endCode":
			val = grp.GetString(key)
		else:
			val = grp.GetFloat(key)
		if not val:
			return self.settingsDict[key]
		else:
			return val

	def writeSetting(self, key, val):
		grp = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/CuraEngine")
		if key is "startCode" or key is "endCode":
			grp.SetString(key, val)
		else:
			grp.SetFloat(key, val)
		Console.PrintMessage("Setting " + key + " to " + str(val) + '\n')

	def readMisc(self, key):
		grp = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/CuraEngine")
		val = grp.GetFloat(key)
		if not val:
			return self.MiscDict[key]
		else:
			return val

	def writeMisc(self, key, val):
		grp = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/CuraEngine")
		grp.SetFloat(key, val)
		Console.PrintMessage("Setting " + key + " to " + str(val) + '\n')

	def exportSettings(self):
		tmpDic = {}
		
		for key in self.settingsDict:
			tmpDic[key] = self.readSetting(key)
		
		return tmpDic
