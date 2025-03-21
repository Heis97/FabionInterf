import numpy as np
import PathPlanner
import gc
from polygon import Mesh3D, Point3D, Polygon3D,Flat3D, PrimitiveType
import Viewer3D_GL
from Viewer3D_GL import GLWidget
from trajectory2d import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton,QSlider, QLineEdit, QOpenGLWidget,QTextEdit,
    QInputDialog, QApplication,QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPolygon
from PyQt5.QtCore import (pyqtProperty, pyqtSignal, pyqtSlot, QPoint, QSize,
        Qt, QTime, QTimer,QThread)
import os

class PathPlannerWidg(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.setWindowTitle("PathPlanner")
        self.resize(1400, 1000)  
        self.cont:"list[Point3D]" = None
        self.surf:Mesh3D = None      
        self.build()
        self.test_cut()
        #extruder_m = GLWidget.extract_coords_from_stl_bin("cube_1_bin.stl")
        
        #PathPlanner.initWind(self.ppw)
    def build(self):
        
        self.ppw = Viewer3D_GL.GLWidget(self)
        self.ppw.setGeometry(QtCore.QRect(200, 0, 1000, 1000))
        self.ppw.draw_start_frame(10.)

        self.but_compPlan = QtWidgets.QPushButton('Рассчитать', self)
        self.but_compPlan.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.but_compPlan.clicked.connect(self.compPlan)

        self.but_loadSurf = QtWidgets.QPushButton('Загрузить', self)
        self.but_loadSurf.setGeometry(QtCore.QRect(0, 30, 100, 30))
        self.but_loadSurf.clicked.connect(self.loadSurf)

        self.but_selectCont = QtWidgets.QPushButton('Выделить', self)
        self.but_selectCont.setGeometry(QtCore.QRect(0, 60, 100, 30))
        self.but_selectCont.clicked.connect(self.selectCont)

        self.but_saveCont = QtWidgets.QPushButton('Сохранить контур', self)
        self.but_saveCont.setGeometry(QtCore.QRect(0, 90, 100, 30))
        self.but_saveCont.clicked.connect(self.saveCont)

        self.but_setXY = QtWidgets.QPushButton('XY', self)
        self.but_setXY.setGeometry(QtCore.QRect(0, 120, 100, 30))
        self.but_setXY.clicked.connect(self.setXY)

        self.but_genSurf = QtWidgets.QPushButton('Генерировать', self)
        self.but_genSurf.setGeometry(QtCore.QRect(0, 210, 100, 30))
        self.but_genSurf.clicked.connect(self.genSurf)

        self.but_gl_rot = QtWidgets.QPushButton('Выкл поворот', self)
        self.but_gl_rot.setGeometry(QtCore.QRect(0, 400, 100, 30))
        self.but_gl_rot.clicked.connect(self.gl_rot)

        self.but_gl_trans = QtWidgets.QPushButton('Выкл перемещ', self)
        self.but_gl_trans.setGeometry(QtCore.QRect(0, 430, 100, 30))
        self.but_gl_trans.clicked.connect(self.gl_trans)

        self.lin_mod = QtWidgets.QLineEdit(self)
        self.lin_mod.setGeometry(QtCore.QRect(0, 150, 200, 30))
        self.lin_mod.setText("path_planner/extruder.stl")

        self.lin_traj = QtWidgets.QLineEdit(self)
        self.lin_traj.setGeometry(QtCore.QRect(0, 180, 200, 30))
        self.lin_traj.setText("traj_test_1")
        #self.but1.clicked.connect()

    def test_cut(self):
        #extruder_m = self.ppw.extract_coords_from_stl("cube_1_ascii.stl")
        extruder_m = GLWidget.extract_coords_from_stl_bin("cyl_2_bin.stl")
        #extruder_m = self.ppw.extract_coords_from_stl("source/path_planner/cube30.stl")
        extruder_mesh = Mesh3D( extruder_m,PrimitiveType.triangles)
        #extruder_mesh.scaleMesh(0.5)
        extruder_mesh= extruder_mesh.setTransform([[1,0,0,0],[0,1,0,0],[0,0,1,-2],[0,0,0,1]])
        glObjExtr =Viewer3D_GL.Paint_in_GL(0.2,0.2,0.2,1,PrimitiveType.triangles,extruder_mesh)
        #self.ppw.paint_objs.append(glObjExtr)
        ps_intersec,ps_cells = slice_mesh(extruder_mesh, 0.3, 4, 0)
        mesh_intersec = Mesh3D(ps_intersec,PrimitiveType.lines)
        self.ppw.paint_objs.append(Viewer3D_GL.Paint_in_GL(1,0,0,0.3,PrimitiveType.lines,mesh_intersec))
        mesh_cells = Mesh3D(ps_cells,PrimitiveType.points)
        self.ppw.paint_objs.append(Viewer3D_GL.Paint_in_GL(1,0,0,0.3,PrimitiveType.points,mesh_cells ))
        



    def loadSurf(self):
        m = self.ppw.extract_coords_from_stl("source\\"+self.lin_mod.text())
        mesh = Mesh3D( m,PrimitiveType.triangles)
        self.surf = mesh
        self.ppw.paint_objs = []
        self.ppw.paint_objs.append(Viewer3D_GL.Paint_in_GL(0.5,0.5,0,1,PrimitiveType.triangles,mesh))
        gc.collect()

    def compPlan(self):
        if self.cont!=None and self.surf!=None:
            proj_traj,normal_arr, matrs = PathPlanner.Generate_multiLayer(self.cont, 1.6, np.pi/2, self.surf, 1.3, 0.3, 3, 5)
            mesh3d_traj = Mesh3D(proj_traj,PrimitiveType.lines)
            self.ppw.paint_objs.append(Viewer3D_GL.Paint_in_GL(0.5,1,0.5,1,PrimitiveType.lines,mesh3d_traj))

            PathPlanner.saveTrajTxt(proj_traj,matrs,self.lin_traj.text())

            extruder_m = self.ppw.extract_coords_from_stl("source/path_planner/extruder.stl")
            extruder_mesh = Mesh3D( extruder_m,PrimitiveType.triangles)
            extruder_mesh.scaleMesh(0.1)
            extruder_mesh.invertNormals()
            extruder_mesh.setTransform(matrs[0])
            glObjExtr = Viewer3D_GL.Paint_in_GL(0.2,0.2,0.2,1,PrimitiveType.triangles,extruder_mesh)
            glObjExtr.matrs = matrs
            self.ppw.paint_objs.append(glObjExtr)
    
    
    def gl_rot(self):
        if self.ppw.rot:
            self.ppw.rot = False
            self.but_gl_rot.setText("Вкл поворот")
        else:
            self.ppw.rot = True
            self.but_gl_rot.setText("Выкл поворот")


    def gl_trans(self):
        if self.ppw.trans:
            self.ppw.trans= False
            self.but_gl_trans.setText("Вкл перемещ")
        else:
            self.ppw.trans = True
            self.but_gl_trans.setText("Выкл перемещ")

    def saveCont(self):
        if self.ppw.cont!=None:
            self.cont = self.ppw.cont.copy()
            print(PathPlanner.ToStringList(self.cont))
            self.ppw.cont = None
            self.ppw.cont_select = False

    def selectCont(self):
        self.ppw.cont = []
        self.ppw.cont_select = True

    def setXY(self):
        self.ppw.setXY()

    def genSurf(self):
        orig,smooth2 = PathPlanner.surface()
        koords3 = PathPlanner.arrayViewer_GL_2d(smooth2[0],smooth2[1],smooth2[2], 0)
        mesh3 =  self.ppw.gridToTriangleMesh(koords3)
        self.surf = Mesh3D(mesh3,PrimitiveType.triangles)
        self.ppw.paint_objs = []
        self.ppw.paint_objs.append(Viewer3D_GL.Paint_in_GL(0.5,0.5,0,1,PrimitiveType.triangles,self.surf))
        

if __name__ == "__main__":
    app =QtWidgets.QApplication(sys.argv)
    path_planner = PathPlannerWidg() 
    path_planner.show()
    sys.exit(app.exec_())
