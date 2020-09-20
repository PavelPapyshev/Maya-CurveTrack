import maya.cmds as mc


def getSelList():
	
	"""
	Returns a list of objects selected in the scene
	"""
	
	return mc.ls(sl=1, l=1)


def checkSelList(selList):
	
	"""
	Checks a list of objects
	
	return arguments:
		@[bool] - result of checking
	"""
	
	if len(selList) < 3:
		return False
	
	shape =  mc.listRelatives(selList[0], s=1)[0]
	
	if mc.objectType(shape) != "nurbsCurve":
		return False
	
	return True
		

def getValue(selList, selFrontAxis):
	
	"""
	Calculates the number of objects and step
	
	accepts arguments:
		@selList[list] - list of objects
		@selFrontAxis[str] - selected front axis
	
	return arguments:
		@objNumber[int] - number of objects
		@iterValue[float] - step
	"""
	
	#length curve
	cvLen = mc.arclen(selList[0])
	
	#length of the object along the selected axis
	objLen = getLengthObj(obj=selList[2], vector=selFrontAxis)
	
	#number of objects to create
	objNumber = int(cvLen // objLen)
	
	#step between objects
	iterValue = round(((objLen * 100) / cvLen) / 100, 4)
	
	return objNumber, iterValue


def getLengthObj(obj, vector):
	
	"""
	Calculates the length of an object
	
	accepts arguments:
		@obj[str] - object
		@vector[str] - selected axis
	
	return arguments:
		@[float] - length object
	"""
	
	boundingBox = mc.xform(obj, q=1, bb=1) #[xmin, ymin, zmin, xmax, ymax, zmax]
	
	if vector == "X":
		return boundingBox[3] - boundingBox[0]
	
	elif vector == "Y":
		return boundingBox[4] - boundingBox[1]
	
	elif vector == "Z":
		return boundingBox[5] - boundingBox[2]
		
		
def putOnCurve(selList, numberObj, stepObj, selFrontAxis, selFrontNegativ, selUpAxis, selUpNegativ):
	
	"""
	Creates objects and links them to the selected curve
	
	accepts arguments:
		@selList[list] - list of selected objects
		@numberObj[int] - number of objects
		@stepObj[float] - step
		@selFrontAxis[string] - selected front axis
		@selFrontNegativ[bool] - positive or negative front axis
		@selUpAxis[string] - selected up axis
		@selUpNegativ[bool] - positive or negative up axis
	
	return arguments:
		@newObjList[list] - list of created objects
	"""
	
	newObjList = []
	value = 0
	
	while numberObj > 0:
		
		obj = mc.duplicate(selList[2], rr=1)
		mpNode = mc.pathAnimation(selList[0], obj,
									follow=1,
									followAxis=selFrontAxis.lower(),
									upAxis=selUpAxis.lower(),
									worldUpType="object",
									worldUpObject=selList[1],
									inverseFront=selFrontNegativ,
									inverseUp=selUpNegativ,
									bank=0,
									startTimeU=0,
									endTimeU=1)
									
		conList = mc.listConnections("{}.u".format(mpNode), s=1)
		mc.delete(conList[0])
		mc.setAttr("{}.u".format(mpNode), value)

		value += stepObj
		numberObj -= 1
		newObjList.append(obj)
	
	return newObjList