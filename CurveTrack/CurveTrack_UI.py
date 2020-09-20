import maya.cmds as mc
import CurveTrack_Utility as utility
from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin


class CurveTrack_Window(MayaQWidgetBaseMixin, QtWidgets.QDialog):
	
	"""
	creates a dialog window
	"""
	
	def __init__(self):
		
		super(CurveTrack_Window, self).__init__()
		self.createUI()
		
		self.newObjList = []
		
	
	def createUI(self):
		
		"""
		sets the window and its elements settings
		"""
		
		#window----------------------------------
		self.setObjectName("CurveTrackWindow")
		self.setWindowTitle("Create Curve Track")
		self.setMinimumSize(370, 280)
		
		#mainLayout----------------------------------
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.setLayout(self.mainLayout)
		
		#frontGrp----------------------------------
		self.frontGrp = QtWidgets.QGroupBox()
		self.frontGrp.setTitle("Front axis")
		self.frontGrp.setAlignment(QtCore.Qt.AlignHCenter)
		self.mainLayout.addWidget(self.frontGrp)
		
		#frontRadioBtnLayout----------------------------------
		self.frontRadioBtnLayout = QtWidgets.QHBoxLayout()
		#self.frontRadioBtnLayout.setContentsMargins(30, 0, 0, 10)
		self.frontGrp.setLayout(self.frontRadioBtnLayout)
		
		#front radio button----------------------------------
		self.frontBtn_x = QtWidgets.QRadioButton("X")
		self.frontBtn_x.setChecked(True)
		self.frontBtn_y = QtWidgets.QRadioButton("Y")
		self.frontBtn_z = QtWidgets.QRadioButton("Z")
		
		self.frontBtn_x.clicked.connect(self.checkUpAxis)
		self.frontBtn_y.clicked.connect(self.checkUpAxis)
		self.frontBtn_z.clicked.connect(self.checkUpAxis)
		
		self.frontRadioBtnLayout.addWidget(self.frontBtn_x)
		self.frontRadioBtnLayout.addWidget(self.frontBtn_y)
		self.frontRadioBtnLayout.addWidget(self.frontBtn_z)
		
		#frontCheckBox----------------------------------
		self.frontCheckBox = QtWidgets.QCheckBox("Negativ")
		self.frontRadioBtnLayout.addWidget(self.frontCheckBox)
		
		#upGrp----------------------------------
		self.upGrp = QtWidgets.QGroupBox()
		self.upGrp.setTitle("Up axis")
		self.upGrp.setAlignment(QtCore.Qt.AlignHCenter)
		self.mainLayout.addWidget(self.upGrp)
		
		#upRadioBtnLayout----------------------------------
		self.upRadioBtnLayout = QtWidgets.QHBoxLayout()
		#self.upRadioBtnLayout.setContentsMargins(30, 0, 0, 10)
		self.upGrp.setLayout(self.upRadioBtnLayout)
		
		#up radio button----------------------------------
		self.upBtn_x = QtWidgets.QRadioButton("X")
		self.upBtn_y = QtWidgets.QRadioButton("Y")
		self.upBtn_y.setChecked(True)
		self.upBtn_z = QtWidgets.QRadioButton("Z")
		
		self.upBtn_x.clicked.connect(self.checkUpAxis)
		self.upBtn_y.clicked.connect(self.checkUpAxis)
		self.upBtn_z.clicked.connect(self.checkUpAxis)
		
		self.upRadioBtnLayout.addWidget(self.upBtn_x)
		self.upRadioBtnLayout.addWidget(self.upBtn_y)
		self.upRadioBtnLayout.addWidget(self.upBtn_z)
		
		#upCheckBox----------------------------------
		self.upCheckBox = QtWidgets.QCheckBox("Negativ")
		self.upRadioBtnLayout.addWidget(self.upCheckBox)
		
		#calculatedValuesGrp----------------------------------
		self.calculatedValuesGrp = QtWidgets.QGroupBox()
		self.calculatedValuesGrp.setTitle("Calculated values")
		self.calculatedValuesGrp.setAlignment(QtCore.Qt.AlignHCenter)
		self.mainLayout.addWidget(self.calculatedValuesGrp)
		
		#calculatedValuesLayout----------------------------------
		self.calculatedValuesLayout = QtWidgets.QHBoxLayout()
		self.calculatedValuesGrp.setLayout(self.calculatedValuesLayout)
		
		#valuesLayout----------------------------------
		self.valuesLayout = QtWidgets.QVBoxLayout()
		self.calculatedValuesLayout.addLayout(self.valuesLayout)
		
		#numberValueLayout----------------------------------
		self.numberValueLayout = QtWidgets.QHBoxLayout()
		self.valuesLayout.addLayout(self.numberValueLayout)
		
		#number of objects----------------------------------
		self.numberObjLabel = QtWidgets.QLabel("Number of objects: ")
		self.numberValueLayout.addWidget(self.numberObjLabel)
		
		self.numberObj = QtWidgets.QLineEdit()
		self.numberObj.setMaximumSize(60, 30)
		self.numberValueLayout.addWidget(self.numberObj)
		
		numberObjValidator = QtGui.QIntValidator(0, 1000000000)
		self.numberObj.setValidator(numberObjValidator)
		self.numberObj.setText("0")
		
		#stepValueLayout----------------------------------
		self.stepValueLayout = QtWidgets.QHBoxLayout()
		self.valuesLayout.addLayout(self.stepValueLayout)
		
		#step----------------------------------
		self.stepObjLabel = QtWidgets.QLabel("Step: ")
		self.stepValueLayout.addWidget(self.stepObjLabel)
		
		self.stepObj = QtWidgets.QLineEdit()
		self.stepObj.setMaximumSize(60, 30)
		self.stepValueLayout.addWidget(self.stepObj)
		
		stepObjValidator = QtGui.QDoubleValidator()
		stepObjValidator.setNotation(QtGui.QDoubleValidator().StandardNotation) 
		self.stepObj.setValidator(stepObjValidator)
		self.stepObj.setText("0.0")
		
		#calculateBtn----------------------------------
		self.calculateBtn = QtWidgets.QPushButton("Calculate")
		self.calculateBtn.setMinimumSize(150, 50)
		self.calculateBtn.clicked.connect(self.calculate)
		self.calculatedValuesLayout.addWidget(self.calculateBtn)
		
		#finalBtnLayout
		self.finalBtnLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.finalBtnLayout)
		
		#createBtn----------------------------------
		self.createBtn = QtWidgets.QPushButton("Create")
		self.createBtn.setMinimumSize(50, 35)
		self.createBtn.clicked.connect(self.createObj)
		self.finalBtnLayout.addWidget(self.createBtn)
		
		#deleteCreatedBtn----------------------------------
		self.deleteCreatedBtn = QtWidgets.QPushButton("Delete created")
		self.deleteCreatedBtn.setMinimumSize(50, 35)
		self.deleteCreatedBtn.clicked.connect(self.deleteObj)
		self.finalBtnLayout.addWidget(self.deleteCreatedBtn)
		
	
	def checkUpAxis(self):
	
		"""
		Checks the selected vectors, they don't have to be the same
		"""
	
		selFrontAxis = self.getSelAxis("Front")
		selUpAxis = self.getSelAxis("Up")
		
		if selFrontAxis == selUpAxis:
			self.newUpAxis(selUpAxis)
		
	
	def getSelAxis(self, type="Front"):
		
		"""
		returns the selected vector
		
		accepts arguments:
			@type[str] - vector type
		
		return arguments:
			@[str] - vector name
		"""
		
		if type == "Front":
			radioBtnList = [self.frontBtn_x, self.frontBtn_y, self.frontBtn_z]
		
		elif type == "Up":
			radioBtnList = [self.upBtn_x, self.upBtn_y, self.upBtn_z]
			
		for btn in radioBtnList:
			if btn.isChecked():
				return btn.text()
		
	
	def newUpAxis(self, selUpAxis):
		
		"""
		Selects the next vector in the queue
		
		accepts arguments:
			@selUpAxis[str] - current vector
		"""
		
		if selUpAxis == "X":
			self.upBtn_y.setChecked(True)
		
		elif selUpAxis == "Y":
			self.upBtn_z.setChecked(True)
		
		else:
			self.upBtn_x.setChecked(True)
	
	
	def calculate(self):
	
		"""
		Called when the "Calculate" button is pressed
		Displays the number of objects and the step
		"""
		
		selList = utility.getSelList()
		
		if not utility.checkSelList(selList):
			mc.warning("Select curve, UpVector object and object!")
			return
		
		selFrontAxis = self.getSelAxis("Front")
		
		objNumber, iterValue = utility.getValue(selList, selFrontAxis)
		
		self.numberObj.setText(str(objNumber))
		self.stepObj.setText(str(iterValue))


	def createObj(self):
	
		"""
		Called when the "Create" button is pressed
		Calls the function for creating objects
		"""
		
		selList = utility.getSelList()
		
		if not utility.checkSelList(selList):
			mc.warning("Select curve, UpVector object and object!")
			return
		
		numberObj = int(self.numberObj.text())
		stepObj = float(self.stepObj.text())
		selFrontAxis = self.getSelAxis("Front")
		selFrontNegativ = self.frontCheckBox.isChecked()
		selUpAxis = self.getSelAxis("Up")
		selUpNegativ = self.upCheckBox.isChecked()
		
		self.newObjList += utility.putOnCurve(selList, numberObj, stepObj, selFrontAxis, selFrontNegativ, selUpAxis, selUpNegativ)
			
		mc.select(selList[0], selList[1], selList[2])
		
		
	def deleteObj(self):
	
		"""
		Called when the "Delete created" button is pressed
		Removes created objects
		"""
		
		if not len(self.newObjList):
			return
			
		for obj in self.newObjList:
			try:
				mc.delete(obj)
			
			except:
				continue
		
		self.newObjList = []