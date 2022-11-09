from math import sqrt
import socket
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,QTextEdit,QSlider,
    QInputDialog, QApplication,QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPolygon
from PyQt5.QtCore import (pyqtProperty, pyqtSignal, pyqtSlot, QPoint, QSize,
        Qt, QTime, QTimer)

from path_planner.Viewer3D_GL import GLWidget,Paint_in_GL
from generate_trajeсtory import *
from g_code_parser import *
from path_planner.trajectory2d import *
from print_settings import PrintSettings,TrajectorySettings
from path_planner.polygon import Mesh3D, Point3D, Polygon3D,Flat3D, PrimitiveType

class Fabion_mesh_app(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, QtCore.Qt.Window)
        self.setWindowTitle("Создание решётки")
        self.resize(1360, 800)   
        self.koord_1 = [[0,0,0,0]]
        self.koord_2p5d = []
        self.koord_sph = [[0,0,0,0]]
        self.prog_code = ""
        self.build()
        #cont = GenerateContour(40, 20, 3)
        #self.viewer3d.addLines(cont, 1, 0, 0, 0.3)

        #cont_r = repeat_contour_2d(cont, 3)

        #self.viewer3d.addLinesDef(cont_r, 0, 1, 0, 1.3)


    def build(self):
        self.slider_l_x = QSlider(Qt.Horizontal,self)
        self.slider_l_x.setGeometry(QtCore.QRect(10, 500, 150, 20))
        self.slider_l_x.valueChanged.connect(self.update_l_x)

        self.slider_l_y = QSlider(Qt.Horizontal,self)
        self.slider_l_y.setGeometry(QtCore.QRect(10, 540, 150, 20))
        self.slider_l_y.valueChanged.connect(self.update_l_y)

        self.slider_l_z = QSlider(Qt.Horizontal,self)
        self.slider_l_z.setGeometry(QtCore.QRect(10, 580, 150, 20))
        self.slider_l_z.valueChanged.connect(self.update_l_z)

        self.slider_l_p = QSlider(Qt.Horizontal,self)
        self.slider_l_p.setGeometry(QtCore.QRect(10, 620, 150, 20))
        self.slider_l_p.valueChanged.connect(self.update_l_p)

        self.viewer3d = GLWidget(self)
        self.viewer3d.setGeometry(QtCore.QRect(350, 10, 600, 600))
        self.viewer3d.draw_start_frame(10.)

        self.but_gen_mesh = QtWidgets.QPushButton('Генерировать решётку', self)
        self.but_gen_mesh.setGeometry(QtCore.QRect(230, 80, 150, 40))
        self.but_gen_mesh.clicked.connect(self.gen_mesh)

        self.but_gen_mesh = QtWidgets.QPushButton('Генерировать решётку\n Regemat', self)
        self.but_gen_mesh.setGeometry(QtCore.QRect(230+150, 80, 150, 40))
        self.but_gen_mesh.clicked.connect(self.gen_mesh_regemat)

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
        self.but_gen_file.setGeometry(QtCore.QRect(230, 320, 150, 40))
        self.but_gen_file.clicked.connect(self.gen_file)

        self.but_open_stl = QtWidgets.QPushButton('Открыть модель', self)
        self.but_open_stl.setGeometry(QtCore.QRect(230, 520, 150, 40))
        self.but_open_stl.clicked.connect(self.openFileNameDialog)

        self.but_open_stl = QtWidgets.QPushButton('Генерировать траекторию', self)
        self.but_open_stl.setGeometry(QtCore.QRect(230, 560, 150, 40))
        self.but_open_stl.clicked.connect(self.gen_traj_from_obj)

        self.but_convert_code = QtWidgets.QPushButton('Конверитровать для Fab', self)
        self.but_convert_code.setGeometry(QtCore.QRect(920, 620, 150, 40))
        self.but_convert_code.clicked.connect(self.conv_g_code)



        self.lin_nx = QtWidgets.QLineEdit(self)
        self.lin_nx.setGeometry(QtCore.QRect(30, 70, 120, 20))#nx
        self.lin_nx.setText('10')

        self.lin_ny = QtWidgets.QLineEdit(self)
        self.lin_ny.setGeometry(QtCore.QRect(30, 100, 120, 20))#ny
        self.lin_ny.setText('10')

        self.lin_d = QtWidgets.QLineEdit(self)
        self.lin_d.setGeometry(QtCore.QRect(30, 130, 120, 20))#d
        self.lin_d.setText('4.0')

        self.lin_dz = QtWidgets.QLineEdit(self)
        self.lin_dz.setGeometry(QtCore.QRect(30, 160, 120, 20))#dZ
        self.lin_dz.setText('0.8')

        self.lin_diam = QtWidgets.QLineEdit(self)
        self.lin_diam.setGeometry(QtCore.QRect(30, 190, 120, 20))#diam
        self.lin_diam.setText('1.0')

        self.lin_F = QtWidgets.QLineEdit(self)
        self.lin_F.setGeometry(QtCore.QRect(30, 220, 120, 20))#F
        self.lin_F.setText('5')

        self.lin_nz = QtWidgets.QLineEdit(self)
        self.lin_nz.setGeometry(QtCore.QRect(30, 250, 120, 20))#nz
        self.lin_nz.setText('6')

        self.lin_ndoz = QtWidgets.QLineEdit(self)
        self.lin_ndoz.setGeometry(QtCore.QRect(30, 280, 120, 20))#ndoz
        self.lin_ndoz.setText('3')

        self.lin_startx = QtWidgets.QLineEdit(self)
        self.lin_startx.setGeometry(QtCore.QRect(30, 310, 40, 20))#startz
        self.lin_startx.setText('160')

        self.lin_starty = QtWidgets.QLineEdit(self)
        self.lin_starty.setGeometry(QtCore.QRect(70, 310, 40, 20))#starty
        self.lin_starty.setText('50')

        self.lin_startz = QtWidgets.QLineEdit(self)
        self.lin_startz.setGeometry(QtCore.QRect(110, 310, 40, 20))#startz
        self.lin_startz.setText('0')

        self.lin_startE = QtWidgets.QLineEdit(self)
        self.lin_startE.setGeometry(QtCore.QRect(30, 340, 120, 20))#startz
        self.lin_startE.setText('0')

        self.lin_diam_syr = QtWidgets.QLineEdit(self)
        self.lin_diam_syr.setGeometry(QtCore.QRect(30, 370, 120, 20))#diam_syr
        self.lin_diam_syr.setText('9.1')

        self.lin_name = QtWidgets.QLineEdit(self)
        self.lin_name.setGeometry(QtCore.QRect(30, 430, 300, 20))#name
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
        self.label_nx.setText('startxyz')

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 340, 60, 20))
        self.label_nx.setText('startE')

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 370, 60, 20))
        self.label_nx.setText('Diam_syr')

        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setGeometry(QtCore.QRect(160, 405, 60, 20))
        self.label_name.setText('Name')

        self.box_g_code = QtWidgets.QTextEdit(self)
        self.box_g_code.setGeometry(QtCore.QRect(850, 10, 500, 600))
        self.box_g_code.setText('')

    def conv_g_code(self):
        g_code = self.box_g_code.toPlainText()
        generate_file_def(parse_g_code_def(g_code))
    
    def clear_mesh(self):
        self.prog_code = ""
        self.koord_1 = [[0,0,0,0]]
        self.koord_sph = [[0,0,0,0]]
        self.viewer3d.clear_traj()
        #self.viewer3d.draw_start_frame(10.)

    def clear_mesh_2(self):
        #self.prog_code = ""
        self.koord_1 = [[0,0,0,0]]
        self.koord_sph = [[0,0,0,0]]
        self.viewer3d.clear()
        self.viewer3d.draw_start_frame(10.)
    def gen_mesh(self):
        try:
            print_settings, trajectory_settings = self.setSettings()
            self.koord_1 = generate_mesh([self.koord_1[-1]],trajectory_settings)

            gcode = generate_traj_Fabion(self.koord_1, print_settings)
                
            self.prog_code+=gcode
            #self.clear_mesh_2()
            self.addToViewerTraj(parse_g_code(self.prog_code))            
        except BaseException:
            print("Cannot generate mesh")

    def setSettings(self)->"tuple[PrintSettings,TrajectorySettings]":
        print_settings = PrintSettings(
            self.lin_name.text(),
                float(self.lin_F.text()),
                float(self.lin_diam.text()),
                float(self.lin_dz.text()),
                float(self.lin_ndoz.text()),
                float(self.lin_startE.text()),
                float(self.lin_diam_syr.text()))
        trajectory_settings = TrajectorySettings(
                int(self.lin_nx.text()),
                int(self.lin_ny.text()),
                float(self.lin_d.text()),
                float(self.lin_dz.text()),
                int(self.lin_nz.text()),
                Point3D(
                    float(self.lin_startx.text()),
                    float(self.lin_starty.text()),
                    float(self.lin_startz.text())
                    ))
        
        return print_settings, trajectory_settings    

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Открыть модель", "","STL (*.stl);;All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            model = GLWidget.extract_coords_from_stl_bin(fileName)
            mesh = Mesh3D( model,PrimitiveType.triangles)
            #mesh.setTransform(matr)
            glObj = Paint_in_GL(0.2,0.2,0.2,1,PrimitiveType.triangles,mesh)
            self.viewer3d.paint_objs.append(glObj)

    def gen_traj_from_obj(self):
        if len(self.viewer3d.paint_objs)>0:
            print_settings, trajectory_settings = self.setSettings()
            ps_intersec,ps_cells = slice_mesh(self.viewer3d.paint_objs[-1].mesh_obj, trajectory_settings.dz , trajectory_settings.d, 0)
            self.viewer3d.paint_objs[-1].visible = False
            #mesh_intersec = Mesh3D(ps_intersec,PrimitiveType.lines)
            gcode = generate_traj_Fabion(ps_intersec,print_settings)          
            self.prog_code+=gcode
            self.addToViewerTraj(parse_g_code(self.prog_code))
            #self.addToViewerTraj(ps_intersec)
        
    def gen_mesh_regemat(self):
        print_settings, trajectory_settings = self.setSettings()
        self.koord_1 = generate_mesh_regemat([self.koord_1[-1]],trajectory_settings)
        gcode = generate_fileGcode_regemat(self.koord_1,print_settings)          
        self.prog_code+=gcode
        self.addToViewerTraj(parse_g_code(self.prog_code))
        self.gen_file()
        
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
        self.box_g_code.setText(self.prog_code)
        self.viewer3d.addLines(traj, 1.0, 0.5, 0.5, 1.)

    def addToViewerCont(self,traj:"list[Point3D]"):    
        self.viewer3d.addLinesDef(traj, 1.0, 0.5, 0.5, 1.)


    def addToViewer(self):        
        self.viewer3d.addLines(convert_to_points3d(self.koord_1), 1.0, 0.5, 0.5, 1.)

    def update_l_x(self,value):
        self.viewer3d.setLight(0,float(value))

    def update_l_y(self,value):
        self.viewer3d.setLight(1,float(value))

    def update_l_z(self,value):
        self.viewer3d.setLight(2,float(value))

    def update_l_p(self,value):
        self.viewer3d.setLight(3,float(value))
















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
