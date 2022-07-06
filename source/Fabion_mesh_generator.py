from math import sqrt
import socket
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,QTextEdit,
    QInputDialog, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPolygon
from PyQt5.QtCore import (pyqtProperty, pyqtSignal, pyqtSlot, QPoint, QSize,
        Qt, QTime, QTimer)

from path_planner.Viewer3D_GL import GLWidget
from generate_trajeсtory import *
from g_code_parser import *

class Fabion_mesh_app(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, QtCore.Qt.Window)
        self.setWindowTitle("Создание решётки")
        self.resize(1200, 800)   
        print("1")
        self.koord_1 = [[0,0,0,0]]
        self.koord_2p5d = []
        self.koord_sph = [[0,0,0,0]]
        self.prog_code = ""
        self.build()

    def build(self):

        self.viewer3d = GLWidget(self)
        self.viewer3d.setGeometry(QtCore.QRect(400, 10, 600, 600))
        self.viewer3d.draw_start_frame(10.)

        self.but_gen_mesh = QtWidgets.QPushButton('Генерировать решётку', self)
        self.but_gen_mesh.setGeometry(QtCore.QRect(230, 80, 150, 40))
        self.but_gen_mesh.clicked.connect(self.gen_mesh)

        self.but_gen_layer = QtWidgets.QPushButton('Генерировать слой', self)
        self.but_gen_layer.setGeometry(QtCore.QRect(230, 120, 150, 40))
        self.but_gen_layer.clicked.connect(self.gen_layer)

        self.but_clear = QtWidgets.QPushButton('Очистить траекторию', self)
        self.but_clear.setGeometry(QtCore.QRect(230, 250, 150, 40))
        self.but_clear.clicked.connect(self.clear_mesh)

        self.but_gen_sph = QtWidgets.QPushButton('Генерировать внесение', self)
        self.but_gen_sph.setGeometry(QtCore.QRect(230, 160, 150, 40))
        self.but_gen_sph.clicked.connect(self.gen_spher)

        self.but_gen_file = QtWidgets.QPushButton('Генерировать файл', self)
        self.but_gen_file.setGeometry(QtCore.QRect(230, 420, 150, 40))
        self.but_gen_file.clicked.connect(self.gen_file)

        self.lin_nx = QtWidgets.QLineEdit(self)
        self.lin_nx.setGeometry(QtCore.QRect(30, 70, 120, 20))#nx
        self.lin_nx.setText('4')

        self.lin_ny = QtWidgets.QLineEdit(self)
        self.lin_ny.setGeometry(QtCore.QRect(30, 100, 120, 20))#ny
        self.lin_ny.setText('4')

        self.lin_d = QtWidgets.QLineEdit(self)
        self.lin_d.setGeometry(QtCore.QRect(30, 130, 120, 20))#d
        self.lin_d.setText('1.2')

        self.lin_dz = QtWidgets.QLineEdit(self)
        self.lin_dz.setGeometry(QtCore.QRect(30, 160, 120, 20))#dZ
        self.lin_dz.setText('0.3')

        self.lin_diam = QtWidgets.QLineEdit(self)
        self.lin_diam.setGeometry(QtCore.QRect(30, 190, 120, 20))#diam
        self.lin_diam.setText('0.6')

        self.lin_F = QtWidgets.QLineEdit(self)
        self.lin_F.setGeometry(QtCore.QRect(30, 220, 120, 20))#F
        self.lin_F.setText('3')

        self.lin_nz = QtWidgets.QLineEdit(self)
        self.lin_nz.setGeometry(QtCore.QRect(30, 250, 120, 20))#nz
        self.lin_nz.setText('6')

        self.lin_ndoz = QtWidgets.QLineEdit(self)
        self.lin_ndoz.setGeometry(QtCore.QRect(30, 280, 120, 20))#ndoz
        self.lin_ndoz.setText('0')

        self.lin_startz = QtWidgets.QLineEdit(self)
        self.lin_startz.setGeometry(QtCore.QRect(30, 310, 120, 20))#startz
        self.lin_startz.setText('0')

        self.lin_startE = QtWidgets.QLineEdit(self)
        self.lin_startE.setGeometry(QtCore.QRect(30, 340, 120, 20))#startz
        self.lin_startE.setText('0')

        self.lin_name = QtWidgets.QLineEdit(self)
        self.lin_name.setGeometry(QtCore.QRect(30, 400, 300, 20))#name
        self.lin_name.setText('g_new_mesh.txt')
        
        #----------------------------------------------

        self.label_nx = QtWidgets.QLabel('Nx',self)
        self.label_nx.setGeometry(QtCore.QRect(160, 70, 60, 20))

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 100, 60, 20))
        self.label_nx.setText('Ny')

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 130, 60, 20))
        self.label_nx.setText('a')

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 160, 60, 20))
        self.label_nx.setText('dz')

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 190, 60, 20))
        self.label_nx.setText('diam')

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 220, 60, 20))
        self.label_nx.setText('F')

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 250, 60, 20))
        self.label_nx.setText('nz')

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 280, 60, 20))
        self.label_nx.setText('ndoz')

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 310, 60, 20))
        self.label_nx.setText('startz')

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 340, 60, 20))
        self.label_nx.setText('startE')

        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setGeometry(QtCore.QRect(160, 375, 60, 20))
        self.label_name.setText('Name')
    def clear_mesh(self):
        self.prog_code = ""
        self.koord_1 = [[0,0,0,0]]
        self.koord_sph = [[0,0,0,0]]
        self.viewer3d.clear()
        self.viewer3d.draw_start_frame(10.)

    def clear_mesh_2(self):
        #self.prog_code = ""
        self.koord_1 = [[0,0,0,0]]
        self.koord_sph = [[0,0,0,0]]
        self.viewer3d.clear()
        self.viewer3d.draw_start_frame(10.)
    def gen_mesh(self):
        try:
            self.koord_1 = generate_mesh(
                [self.koord_1[-1]],
                int(self.lin_nx.text()),
                int(self.lin_ny.text()),
                float(self.lin_d.text()),
                float(self.lin_dz.text()),
                int(self.lin_nz.text()),
                float(self.lin_startz.text()))
            gcode = generate_fileGcode(
                self.koord_1,
                self.lin_name.text(),
                float(self.lin_F.text()),
                float(self.lin_diam.text()),
                float(self.lin_dz.text()),
                float(self.lin_ndoz.text()),
                float(self.lin_startE.text()))
            
            self.prog_code+=gcode
            #self.clear_mesh_2()
            self.addToViewerTraj(parse_g_code(self.prog_code))            
        except BaseException:
            print("Cannot generate mesh")
        
    def gen_layer(self):
        try:
            self.koord_1 = generate_1layers(
                [self.koord_1[-1]],int(self.lin_nx.text()),
                int(self.lin_ny.text()),
                float(self.lin_d.text()),
                float(self.lin_dz.text()),
                float(self.lin_startz.text())
                )
            gcode = generate_fileGcode(
                self.koord_1,
                self.lin_name.text(),
                float(self.lin_F.text()),
                float(self.lin_diam.text()),
                float(self.lin_dz.text()),
                float(self.lin_ndoz.text()),
                float(self.lin_startE.text()))
            self.prog_code+=gcode
            #self.clear_mesh_2()
            #self.viewer3d.clear()
            self.addToViewerTraj(parse_g_code(self.prog_code)) 
        except BaseException:
            print("Cannot generate layer")
    def gen_spher(self):
        try:
            self.koord_sph = generate_spher(
                int(self.lin_nx.text()),
                int(self.lin_ny.text()),
                float(self.lin_d.text()),
                float(self.lin_startz.text()))
            gcode = generate_file_sph(
                self.koord_sph,
                self.lin_name.text(),
                float(self.lin_F.text()),
                float(self.lin_diam.text()),
                float(self.lin_dz.text()),
                float(self.lin_ndoz.text()),
                float(self.lin_startE.text()))
            self.prog_code+=gcode
            #self.clear_mesh_2()
            self.addToViewerTraj(parse_g_code(self.prog_code))            

        except BaseException:
            pass
    def gen_file(self):
        try:
            f1 = open("g_programs/"+self.lin_name.text(),'w')
            f1.write(self.prog_code)
            f1.close()
        except BaseException:
            print("Cannot generate file")
    def gen_file_1(self):
        #try:
            #self.koord_1 = generate_mesh(int(self.lin_nx.text()),int(self.lin_ny.text()),float(self.lin_d.text()),float(self.lin_dz.text()),int(self.lin_nz.text()))
        generate_file_sph(
            self.koord_sph,
            self.lin_name.text(),
            float(self.lin_F.text()),
            float(self.lin_diam.text()),
            float(self.lin_dz.text()),
            float(self.lin_ndoz.text()),
            float(self.lin_startE.text()))
        #self.update()
        #except BaseException:
            #pass

    def addToViewerTraj(self,traj:"list[Point3D]"):    
        self.viewer3d.addLines(traj, 1.0, 0.5, 0.5, 1.)

    def addToViewer(self):        
        self.viewer3d.addLines(convert_to_points3d(self.koord_1), 1.0, 0.5, 0.5, 1.)


















    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.drawLines(qp)
        self.update()
    def pointTo25D(self,x:float,y:float,z:float)->"tuple[float,float]":
        x2d:float = 1.732*x-1.732*y
        y2d:float = x + y + 2*z
        return x2d,-y2d
    def koords3dTo25D(self,koords:list)->list:
        koords2d = []
        for i in range(len(koords)):
            x,y = self.pointTo25D(koords[i][0],koords[i][1],koords[i][2])
            koords2d.append([x,y])
        return koords2d
    def drawLines(self, qp):
        pen = QPen(Qt.blue, 1, Qt.SolidLine)
        qp.setPen(pen)
        #print(str(self.koord_2))
        paint_koords = self.koords3dTo25D(self.koord_1)
        Xmin=10000
        Ymin=10000
        Xmax=-10000
        Ymax=-10000
        Xq1=500
        Xq2= Xq1+60
        Yq1=20
        Yq2=Yq1+60
        if len(paint_koords)==0:
            return
        for i in range(len(paint_koords)-1):            
            if paint_koords[i][0]>Xmax:
                Xmax=paint_koords[i][0]
            if paint_koords[i][0]<Xmin:
                Xmin=paint_koords[i][0]
            if paint_koords[i][1]>Ymax:
                Ymax=paint_koords[i][1]
            if paint_koords[i][1]<Ymin:
                Ymin=paint_koords[i][1]
        k=abs(Xq1-Xq2)/abs(Xmax-Xmin)  

        offX=Xmin*k-Xq1
        offY=Ymin*k-Yq1
        pen = QPen(Qt.blue, 1, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(int(len(paint_koords))-1):   
            x1=paint_koords[i][0]
            y1=paint_koords[i][1]
            x2=paint_koords[i+1][0]
            y2=paint_koords[i+1][1]
            qp.drawLine(int(x1*k-offX),int(y1*k-offY),int(x2*k-offX),int(y2*k-offY))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Fabion_mesh_app()
    window.show()
    sys.exit(app.exec_())
