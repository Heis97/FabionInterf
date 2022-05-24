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




class BufferFrame:
    def __init__(self, x:float,y:float,z:float,f:float,v:float,g:int,d:int):
        self.x = x
        self.y = y
        self.z = z
        self.f = f
        self.v = v
        self.g = g
        self.d = d
    
    def toString(self,n:int)->str:
        if self.g==11:
            return 'N'+str(n)+' G11 X'+str(round(self.x,4))+' Y'+str(round(self.y,4))+' Z'+str(round(self.z,4))+  ' D'+str(self.d)+'\n'
        if self.g==87:
            return 'N'+str(n)+' G87 P'+str(round(self.x,4))+' P'+str(round(self.d,4))+' P'+str(round(self.v,4))+'\n'
        if self.g==88:
            return 'N'+str(n)+' G88 X'+str(round(self.x,4))+' Y'+str(round(self.y,4))+' Z'+str(round(self.z,4))+' F'+str(round(self.f,4))+ ' V'+str(round(self.v,4))+  ' D'+str(self.d)+' Q0 T1 I0 J0 \n'
        if self.g==89:
            return 'N'+str(n)+' G89 P'+str(round(self.x,4))+' P'+str(round(self.d,4))+' P'+str(round(self.v,4))+'\n'

class BufferCreator:
    def G11(x:float,y:float,z:float,d:int)->BufferFrame:
        return BufferFrame(x=x,y=y,z=z,d=d,g=11)
    def G87(x:float,d:int,v:float)->BufferFrame:
        return BufferFrame(x=x,d=d,v=v,g=87)
    def G89(x:float,d:int,v:float)->BufferFrame:
        return BufferFrame(x=x,d=d,v=v,g=89)
    def G88(x:float,y:float,z:float,f:float,v:float,d:int)->BufferFrame:
        return BufferFrame(x,y,z,f,v,g=88,d=d)

class G11(BufferFrame):
    def __init__(self, x:float,y:float,z:float,d:int):
        self.x = x
        self.y = y
        self.z = z
        self.d = d
    def generateFrame(self,n:int)->str:
        return 'N'+str(n)+' G11 X'+str(round(self.x,4))+' Y'+str(round(self.y,4))+' Z'+str(round(self.z,4))+  ' D'+str(self.d)+'\n'

class G87(BufferFrame):
    def __init__(self, x:float,d:float,v:float):
        self.x = x
        self.d = d
        self.v = v
    def generateFrame(self,n:int)->str:
        return 'N'+str(n)+' G87 P'+str(round(self.x,4))+' P'+str(round(self.d,4))+' P'+str(round(self.v,4))+'\n'

class G89(BufferFrame):
    def __init__(self, x:float,d:float,v:float):
        self.x = x
        self.d = d
        self.v = v
    def generateFrame(self,n:int)->str:
        return 'N'+str(n)+' G89 P'+str(round(self.x,4))+' P'+str(round(self.d,4))+' P'+str(round(self.v,4))+'\n'

class G88(BufferFrame):
    def __init__(self, x:float,y:float,z:float,f:float,v:float,d:float):
        self.x = x
        self.y = y
        self.z = z
        self.f = f
        self.v = v
        self.d = d
    def generateFrame(self,n:int)->str:
        return 'N'+str(n)+' G88 X'+str(round(self.x,4))+' Y'+str(round(self.y,4))+' Z'+str(round(self.z,4))+' F'+str(round(self.f,4))+ ' V'+str(round(self.v,4))+  ' D'+str(self.d)+' Q0 T1 I0 J0 \n'


class BufferProgramm:
    frames :"list[BufferFrame]"
    current_layer:int
    corner:int #0 - rightup, 1 - leftdown
    axis:int

    def __init__(self, frames:"list[BufferFrame]"):
        self.frames = frames

    def addFrames(self,prog2:"list[BufferFrame]"):
        self.frames.extend(prog2)

    def generate_mesh(self,nx: int,ny: int,d: float,dz: float,nz: int,start_z:float):
        tr = []
        tr1 = []
        for i_z in range(int(nz/2)):
            tr1 = self.generate_2layers(tr,nx,ny,d,dz,start_z)   
            tr = tr1.copy()
        return tr
    
    def generate_spher(self,nx: int,ny: int,d: float,dz: float):
        tr = []
        z = dz
        x_st = d/2
        y_st = d/2
        for i in range(nx):
            for j in range(ny):
                x = x_st+d*i
                y = y_st+d*j
                tr.append([x,y,z,1])
        return tr


    #d - расстояние между линиями| dz - толщина линии |nx,ny - количество линий по каждой оси
   
    def generate_2layers(self,tr: list,nx: int,ny: int,d: float,dz: float,start_z:float):
        Lx = d*nx
        Ly = d*ny
        x = 0
        y = 0
        z = start_z
        layer = 0
        if len(tr)==0:
            pass
        else:
            x = tr[-1][0]
            y = tr[-1][1]
            z = tr[-1][2]
            layer =tr[-1][3]+1
        
        z+=dz
        tr.append([x,y,z,layer])
        if(ny%2==0):
            for i in range(0,int(ny/2)):

                x += Lx
                tr.append([x,y,z,layer])

                y+=d
                tr.append([x,y,z,layer])
            
                x -= Lx
                tr.append([x,y,z,layer])

                y+=d
                tr.append([x,y,z,layer])
            x += Lx
            tr.append([x,y,z,layer])

            z+=dz
            layer +=1
            if(nx%2==0):
                for i in range(0,int(nx/2)):

                    y -= Ly
                    tr.append([x,y,z,layer])

                    x-=d
                    tr.append([x,y,z,layer])
                
                    y += Ly
                    tr.append([x,y,z,layer])

                    x-=d
                    tr.append([x,y,z,layer])

                y -= Ly
                tr.append([x,y,z,layer]) 
                
                return tr
            else:
                for i in range(0,int((nx-1)/2)):

                    y -= Ly
                    tr.append([x,y,z,layer])

                    x-=d
                    tr.append([x,y,z,layer])
                
                    y += Ly
                    tr.append([x,y,z,layer])

                    x-=d
                    tr.append([x,y,z,layer])

                y -= Ly
                tr.append([x,y,z,layer])   

                x-=d
                tr.append([x,y,z,layer])
                
                y += Ly
                tr.append([x,y,z,layer]) 
                return tr
        else:
            for i in range(0,int((ny-1)/2)):

                x += Lx
                tr.append([x,y,z,layer])

                y+=d
                tr.append([x,y,z,layer])
            
                x -= Lx
                tr.append([x,y,z,layer])

                y+=d
                tr.append([x,y,z,layer])
            x += Lx
            tr.append([x,y,z,layer])

            y+=d
            tr.append([x,y,z,layer])
        
            x -= Lx
            tr.append([x,y,z,layer])

            z+=dz
            layer +=1
            if(nx%2==0):
                for i in range(0,int(nx/2)):

                    y -= Ly
                    tr.append([x,y,z,layer])

                    x+=d
                    tr.append([x,y,z,layer])
                
                    y += Ly
                    tr.append([x,y,z,layer])

                    x+=d
                    tr.append([x,y,z,layer])

                y -= Ly
                tr.append([x,y,z,layer])    
                return tr
            else:
                for i in range(0,int((nx-1)/2)):

                    y -= Ly
                    tr.append([x,y,z,layer])

                    x+=d
                    tr.append([x,y,z,layer])
                
                    y += Ly
                    tr.append([x,y,z,layer])

                    x+=d
                    tr.append([x,y,z,layer])

                y -= Ly
                tr.append([x,y,z,layer])   

                x+=d
                tr.append([x,y,z,layer])
                
                y += Ly
                tr.append([x,y,z,layer]) 
                return tr   
    
    
    def generate_1layersX(self,tr: list,nx: int,ny: int,d: float,dz: float):
        Lx = d*nx
        Ly = d*ny
        x = 0
        y = 0
        z = 0
        layer = 0
        if len(tr)==0:
            print("len0")
            pass
        else:
            x = tr[-1][0]
            y = tr[-1][1]
            z = tr[-1][2]
            print(x)
            print(y)
            print(z)
            layer =tr[-1][3]+1        
        z+=dz
        tr.append([x,y,z,layer])
        if(ny%2==0):
            for i in range(0,int(ny/2)):
                x += Lx
                tr.append([x,y,z,layer])
                y+=d
                tr.append([x,y,z,layer])            
                x -= Lx
                tr.append([x,y,z,layer])
                y+=d
                tr.append([x,y,z,layer])
            x += Lx
            tr.append([x,y,z,layer])
            if self.corner == 0:
                self.corner = 1
            elif self.corner == 1:
                self.corner = 0
            return tr           
        else:
            for i in range(0,int((ny-1)/2)):
                x += Lx
                tr.append([x,y,z,layer])
                y+=d
                tr.append([x,y,z,layer])            
                x -= Lx
                tr.append([x,y,z,layer])
                y+=d
                tr.append([x,y,z,layer])
            x += Lx
            tr.append([x,y,z,layer])
            y+=d
            tr.append([x,y,z,layer])        
            x -= Lx
            tr.append([x,y,z,layer])
            if self.corner == 0:
                self.corner = 1
            elif self.corner == 1:
                self.corner = 0
            return tr 

    def generate_1layersY(self,tr: list,nx: int,ny: int,d: float,dz: float):
        Lx = d*nx
        Ly = d*ny
        x = 0
        y = 0
        z = 0
        layer = 0
        if len(tr)==0:
            print("len0")
            pass
        else:
            x = tr[-1][0]
            y = tr[-1][1]
            z = tr[-1][2]
            print(x)
            print(y)
            print(z)
            layer =tr[-1][3]+1        
        z+=dz
        tr.append([x,y,z,layer])
        if(nx%2==0):
            for i in range(0,int(nx/2)):
                y += Ly
                tr.append([x,y,z,layer])
                x+=d
                tr.append([x,y,z,layer])            
                y -= Ly
                tr.append([x,y,z,layer])
                x+=d
                tr.append([x,y,z,layer])
            y += Lx
            tr.append([x,y,z,layer])
            if self.corner == 0:
                self.corner = 1
            elif self.corner == 1:
                self.corner = 0
            return tr           
        else:
            for i in range(0,int((nx-1)/2)):
                y += Ly
                tr.append([x,y,z,layer])
                x+=d
                tr.append([x,y,z,layer])            
                y -= Ly
                tr.append([x,y,z,layer])
                x+=d
                tr.append([x,y,z,layer])
            y += Ly
            tr.append([x,y,z,layer])
            x+=d
            tr.append([x,y,z,layer])        
            y -= Ly
            tr.append([x,y,z,layer])
            if self.corner == 0:
                self.corner = 1
            elif self.corner == 1:
                self.corner = 0
            return tr 

    def generate_file(self,tr: list, name: str, F: float, diam: float, dz: float, ndoz: int):
        f1=open(name,'w')
        n = 5
        for i in range(len(self.frames)):
            x = self.frames[i].x
            y = self.frames[i].y
            z = self.frames[i].z
            if(i==0):
                f1.write('N'+str(n)+' G11 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z+10,4))+  ' D'+str(ndoz)+'\n')
                n+=5
                f1.write('N'+str(n)+' G11 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z,4))+  ' D'+str(ndoz)+'\n')
                n+=5
                #f1.write('N'+str(n)+' G87 P2 P3 P0\n')
                f1.write('N'+str(n)+' G87 P0 P'+str(ndoz)+' P0.1\n')
                n+=5
            else:
                x_ = tr[i-1][0]
                y_ = tr[i-1][1]
                z_ = tr[i-1][2] 
                rasst = sqrt((x - x_)**2+(y - y_)**2+(z - z_)**2)
                v = diam*dz*rasst
                f1.write('N'+str(n)+' G88 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z,4))+ ' F'+str(round(F,4))+ ' V'+str(round(v,4))+  ' D'+str(ndoz)+' Q0 T1 I0 J0 \n')
                n+=5
            if(i==len(tr)-1):
                f1.write('N'+str(n)+' G11 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z+10,4))+  ' D'+str(ndoz)+'\n')
                n+=5

        f1.close()                     


def generate_file(tr: list, name: str, F: float, diam: float, dz: float, ndoz: int):
    f1=open(name,'w')
    N = 5
    for i in range(len(tr)):
        x = tr[i][0]
        y = tr[i][1]
        z = tr[i][2]
        if(i==0):
            f1.write('N'+str(N)+' G11 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z+10,4))+  ' D'+str(ndoz)+'\n')
            N+=5
            f1.write('N'+str(N)+' G11 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z,4))+  ' D'+str(ndoz)+'\n')
            N+=5
            #f1.write('N'+str(N)+' G87 P2 P3 P0\n')
            f1.write('N'+str(N)+' G87 P0 P'+str(ndoz)+' P0.1\n')
            N+=5
        else:
            x_ = tr[i-1][0]
            y_ = tr[i-1][1]
            z_ = tr[i-1][2] 
            rasst = sqrt((x - x_)**2+(y - y_)**2+(z - z_)**2)
            v = diam*dz*rasst
            f1.write('N'+str(N)+' G88 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z,4))+ ' F'+str(round(F,4))+ ' V'+str(round(v,4))+  ' D'+str(ndoz)+' Q0 T1 I0 J0 \n')
            N+=5
        if(i==len(tr)-1):
            f1.write('N'+str(N)+' G11 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z+10,4))+  ' D'+str(ndoz)+'\n')
            N+=5

    f1.close()  

def generate_fileGcode(tr: list, name: str, F: float, diam: float, dz: float, ndoz: int):
    f1=open(name,'w')
    F = F*60
    v_all = 0.05
    
    for i in range(len(tr)):
        x = tr[i][0]
        y = tr[i][1]
        z = tr[i][2]
        if(i==0):
            f1.write('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z+10,4))+'\n')
            f1.write('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z,4))+  '\n')
            f1.write('G1 E0.05\n')
            #f1.write('N'+str(N)+' G87 P2 P3 P0\n')
            #f1.write('N'+str(N)+' G87 P0 P'+str(ndoz)+' P0.1\n')
        else:
            x_ = tr[i-1][0]
            y_ = tr[i-1][1]
            z_ = tr[i-1][2] 
            rasst = sqrt((x - x_)**2+(y - y_)**2+(z - z_)**2)
            k = 0.00513152
            v = diam*dz*rasst
            v= k*rasst
            v_all+=v
            f1.write('G1 X'+str(round(x,5))+' Y'+str(round(y,5))+' Z'+str(round(z,5))+ ' F'+str(round(F,5))+ ' E'+str(round(v_all,5))+'\n')
        if(i==len(tr)-1):

            f1.write('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z+10,4))+ '\n')

    f1.write(";Volume: "+str(0.058*v_all)+'\n')    
    f1.close()  


def generate_file_sph(tr: list, name: str, F: float, diam: float, dz: float, ndoz: int):
    f1=open(name,'w')
    N = 5
    for i in range(len(tr)):
        x = tr[i][0]
        y = tr[i][1]
        z = tr[i][2]
        f1.write('N'+str(N)+' G11 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z+4,4))+  ' D'+str(ndoz)+'\n')
        N+=5
        f1.write('N'+str(N)+' G11 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z,4))+  ' D'+str(ndoz)+'\n')
        N+=5
        #f1.write('N'+str(N)+' G87 P2 P'+str(ndoz)+' P0\n')
        #N+=5
        rasst=1
        v = diam*diam*rasst
        f1.write('N'+str(N)+' G88 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z+2,4))+ ' F'+str(round(F,4))+ ' V'+str(round(v,4))+  ' D'+str(ndoz)+' Q0 T1 I0 J0 \n')
        N+=5
        f1.write('N'+str(N)+' G11 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z+4,4))+  ' D'+str(ndoz)+'\n')
        N+=5
        
    f1.close() 


#d - расстояние между линиями| dz - толщина линии |nx,ny - количество линий по каждой оси
def generate_mesh(nx: int,ny: int,d: float,dz: float,nz: int,start_z:float):
    tr = []
    tr1 = []
    for i_z in range(int(nz/2)):
        tr1 = generate_2layers(tr,nx,ny,d,dz,start_z)   
        tr = tr1.copy()
    return tr
    
def generate_spher(nx: int,ny: int,d: float,dz: float):
    tr = []
    z = dz
    x_st = d/2
    y_st = d/2
    for i in range(nx):
        for j in range(ny):
            x = x_st+d*i
            y = y_st+d*j
            tr.append([x,y,z,1])
    return tr


#d - расстояние между линиями| dz - толщина линии |nx,ny - количество линий по каждой оси
def generate_2layers(tr: list,nx: int,ny: int,d: float,dz: float,start_z:float):
    Lx = d*nx
    Ly = d*ny
    x = 0
    y = 0
    z = start_z
    layer = 0
    if len(tr)==0:
        pass
    else:
        x = tr[-1][0]
        y = tr[-1][1]
        z = tr[-1][2]
        layer =tr[-1][3]+1
    
    z+=dz
    tr.append([x,y,z,layer])
    if(ny%2==0):
        for i in range(0,int(ny/2)):

            x += Lx
            tr.append([x,y,z,layer])

            y+=d
            tr.append([x,y,z,layer])
        
            x -= Lx
            tr.append([x,y,z,layer])

            y+=d
            tr.append([x,y,z,layer])
        x += Lx
        tr.append([x,y,z,layer])

        z+=dz
        layer +=1
        if(nx%2==0):
            for i in range(0,int(nx/2)):

                y -= Ly
                tr.append([x,y,z,layer])

                x-=d
                tr.append([x,y,z,layer])
            
                y += Ly
                tr.append([x,y,z,layer])

                x-=d
                tr.append([x,y,z,layer])

            y -= Ly
            tr.append([x,y,z,layer]) 
             
            return tr
        else:
            for i in range(0,int((nx-1)/2)):

                y -= Ly
                tr.append([x,y,z,layer])

                x-=d
                tr.append([x,y,z,layer])
            
                y += Ly
                tr.append([x,y,z,layer])

                x-=d
                tr.append([x,y,z,layer])

            y -= Ly
            tr.append([x,y,z,layer])   

            x-=d
            tr.append([x,y,z,layer])
            
            y += Ly
            tr.append([x,y,z,layer]) 
            return tr
    else:
        for i in range(0,int((ny-1)/2)):

            x += Lx
            tr.append([x,y,z,layer])

            y+=d
            tr.append([x,y,z,layer])
        
            x -= Lx
            tr.append([x,y,z,layer])

            y+=d
            tr.append([x,y,z,layer])
        x += Lx
        tr.append([x,y,z,layer])

        y+=d
        tr.append([x,y,z,layer])
    
        x -= Lx
        tr.append([x,y,z,layer])

        z+=dz
        layer +=1
        if(nx%2==0):
            for i in range(0,int(nx/2)):

                y -= Ly
                tr.append([x,y,z,layer])

                x+=d
                tr.append([x,y,z,layer])
            
                y += Ly
                tr.append([x,y,z,layer])

                x+=d
                tr.append([x,y,z,layer])

            y -= Ly
            tr.append([x,y,z,layer])    
            return tr
        else:
            for i in range(0,int((nx-1)/2)):

                y -= Ly
                tr.append([x,y,z,layer])

                x+=d
                tr.append([x,y,z,layer])
            
                y += Ly
                tr.append([x,y,z,layer])

                x+=d
                tr.append([x,y,z,layer])

            y -= Ly
            tr.append([x,y,z,layer])   

            x+=d
            tr.append([x,y,z,layer])
            
            y += Ly
            tr.append([x,y,z,layer]) 
            return tr   

def generate_1layers(tr: list,nx: int,ny: int,d: float,dz: float,start_z:float):
    
    Lx = d*nx
    Ly = d*ny
    x = 0
    y = 0
    z = start_z
    layer = 0
    if len(tr)==0:
        print("len0")
        pass
    else:
        x = tr[-1][0]
        y = tr[-1][1]
        z = tr[-1][2]
        print(x)
        print(y)
        print(z)
        layer =tr[-1][3]+1
    
    z+=dz
    tr.append([x,y,z,layer])
    if(ny%2==0):
        for i in range(0,int(ny/2)):

            x += Lx
            tr.append([x,y,z,layer])

            y+=d
            tr.append([x,y,z,layer])
        
            x -= Lx
            tr.append([x,y,z,layer])

            y+=d
            tr.append([x,y,z,layer])
        x += Lx
        tr.append([x,y,z,layer])
        return tr
        
    else:
        for i in range(0,int((ny-1)/2)):

            x += Lx
            tr.append([x,y,z,layer])

            y+=d
            tr.append([x,y,z,layer])
        
            x -= Lx
            tr.append([x,y,z,layer])

            y+=d
            tr.append([x,y,z,layer])
        x += Lx
        tr.append([x,y,z,layer])

        y+=d
        tr.append([x,y,z,layer])
    
        x -= Lx
        tr.append([x,y,z,layer])
        return tr 

def generate_begin(tr:list,Lx:float, Ly:float, delt:float):
    x = -delt
    y = -delt
    z = 0
    tr.append([x,y,z])#0
    x = Lx+delt
    tr.append([x,y,z])#1
    y = Ly+delt
    tr.append([x,y,z])#2
    x = -delt
    tr.append([x,y,z])#3
    y = -delt
    tr.append([x,y,z])#0
    return tr

class ex11(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, QtCore.Qt.Window)
        self.setWindowTitle("Создание решётки")
        self.resize(1200, 700)   
        print("1")
        self.koord_1 = []

        self.koord_2p5d = []
        self.koord_sph = []
        
        self.build()

    def build(self):
        self.but_gen_mesh = QtWidgets.QPushButton('Генерировать решётку', self)
        self.but_gen_mesh.setGeometry(QtCore.QRect(30, 20, 150, 40))
        self.but_gen_mesh.clicked.connect(self.gen_mesh)

        self.but_gen_layer = QtWidgets.QPushButton('Генерировать слой', self)
        self.but_gen_layer.setGeometry(QtCore.QRect(230, 120, 150, 40))
        self.but_gen_layer.clicked.connect(self.gen_layer)

        self.but_gen_sph = QtWidgets.QPushButton('Генерировать внесение', self)
        self.but_gen_sph.setGeometry(QtCore.QRect(230, 160, 150, 40))
        self.but_gen_sph.clicked.connect(self.gen_spher)

        self.but_gen_file_sph = QtWidgets.QPushButton('Генерировать файл внесение', self)
        self.but_gen_file_sph.setGeometry(QtCore.QRect(230, 200, 150, 40))
        self.but_gen_file_sph.clicked.connect(self.gen_file_1)

        self.but_file = QtWidgets.QPushButton('Генерировать файл', self)
        self.but_file.setGeometry(QtCore.QRect(180, 20, 150, 40))
        self.but_file.clicked.connect(self.gen_file)

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
        self.lin_ndoz.setText('3')

        self.lin_startz = QtWidgets.QLineEdit(self)
        self.lin_startz.setGeometry(QtCore.QRect(30, 310, 120, 20))#startz
        self.lin_startz.setText('0')

        self.lin_name = QtWidgets.QLineEdit(self)
        self.lin_name.setGeometry(QtCore.QRect(30, 370, 300, 20))#name
        self.lin_name.setText('g_new_mesh.txt')

        #----------------------------------------------

        self.label_nx = QtWidgets.QLabel(self)
        self.label_nx.setGeometry(QtCore.QRect(160, 70, 60, 20))
        self.label_nx.setText('Nx')

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

        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setGeometry(QtCore.QRect(160, 400, 60, 20))
        self.label_name.setText('Name')

    def gen_mesh(self):
        try:
            self.koord_1 = generate_mesh(int(self.lin_nx.text()),int(self.lin_ny.text()),float(self.lin_d.text()),float(self.lin_dz.text()),int(self.lin_nz.text()),float(self.lin_startz.text()))
            self.update()
        except BaseException:
            pass
    def gen_layer(self):
        try:
            tr =  []
            self.koord_1 = generate_1layers(
                tr,int(self.lin_nx.text()),
                int(self.lin_ny.text()),
                float(self.lin_d.text()),
                float(self.lin_dz.text()),
                float(self.lin_startz.text())
                )
            self.update()
        except BaseException:
            pass
    def gen_spher(self):
        try:
            tr =  []
            self.koord_sph = generate_spher(int(self.lin_nx.text()),int(self.lin_ny.text()),float(self.lin_d.text()),float(self.lin_dz.text()))
            self.update()
        except BaseException:
            pass
    def gen_file(self):
        try:
            #self.koord_1 = generate_mesh(int(self.lin_nx.text()),int(self.lin_ny.text()),float(self.lin_d.text()),float(self.lin_dz.text()),int(self.lin_nz.text()))
            #generate_file(self.koord_1,self.lin_name.text(),float(self.lin_F.text()),float(self.lin_diam.text()),float(self.lin_dz.text()),float(self.lin_ndoz.text()))
            generate_fileGcode(self.koord_1,self.lin_name.text(),float(self.lin_F.text()),float(self.lin_diam.text()),float(self.lin_dz.text()),float(self.lin_ndoz.text()))
            self.update()
        except BaseException:
            pass
    def gen_file_1(self):
        try:
            #self.koord_1 = generate_mesh(int(self.lin_nx.text()),int(self.lin_ny.text()),float(self.lin_d.text()),float(self.lin_dz.text()),int(self.lin_nz.text()))
            generate_file_sph(self.koord_sph,self.lin_name.text(),float(self.lin_F.text()),float(self.lin_diam.text()),float(self.lin_dz.text()),float(self.lin_ndoz.text()))
            self.update()
        except BaseException:
            pass

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.drawLines(qp)

    def pointTo25D(self,x:float,y:float,z:float)->"tuple[float,float]":
        x2d:float = 1.732*x-1.732*y
        y2d:float = x + y + 2*z
        return x2d,y2d

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
        Xq1=400
        Xq2= Xq1+600
        Yq1=20
        Yq2=Yq1+600
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
    window = ex11()
    window.show()
    sys.exit(app.exec_())
