import numpy as np
import random
from Viewer3D_GL import PrimitiveType

from polygon import Mesh3D, Polygon3D,Point3D


def distance(p1: Point3D, p2: Point3D):
    dist3 = (p1.x-p2.x)**2+(p1.y-p2.y)**2+(p1.z-p2.z)**2
    return np.sqrt(dist3)

def rotate_point(x: float, y: float, alfa: float):
    x_r = x * np.cos(alfa) - y * np.sin(alfa)
    y_r = x * np.sin(alfa) + y * np.cos(alfa)
    return x_r, y_r

def rotate_list_points(points: "list[Point3D]", alfa: float):
    rotated_points = []
    for i in range(len(points)):
        p_r_x, p_r_y = rotate_point(points[i].x, points[i].y, alfa)
        point_rot = Point3D(p_r_x, p_r_y, points[i].z)
        rotated_points.append(point_rot)
    return rotated_points     
    
def findGab(cont:"list[Point3D]"):
    minX = 100000
    minY = 100000
    maxX = -100000
    maxY = -100000
    for i in range(len(cont)):
        if(cont[i].x>maxX):
            maxX = cont[i].x
        if(cont[i].y>maxY):
            maxY = cont[i].y

        if(cont[i].x<minX):
            minX = cont[i].x
        if(cont[i].y<minY):
            minY = cont[i].y

    return minX, maxX,minY,maxY

def findGabPol(pol:"list[Polygon3D]"):
    minX = 100000
    minY = 100000
    maxX = -100000
    maxY = -100000

    for i in range(len(pol)):
        cont = pol[i].vert_arr[0]
        if(cont.x>maxX):
            maxX = cont.x
        if(cont.y>maxY):
            maxY = cont.y

        if(cont.x<minX):
            minX = cont.x
        if(cont.y<minY):
            minY = cont.y

    return minX, maxX,minY,maxY

def affilPoint(p:Point3D,minX, maxX,minY,maxY)->bool:
    if p.x < minX or p.x > maxX:
        return False
    if p.y < minY or p.y > maxY:
        return False
    return True

def affilPolyg(p:Polygon3D,minX, maxX,minY,maxY)->bool:
    for i in range(len(p.vert_arr)):
        if affilPoint(p.vert_arr[i],minX, maxX,minY,maxY):
            return True
    return False


def GenerateContour(n: int,rad:float,delt:float)->"list[Point3D]":
    step = 2*np.pi/n
    a = 0
    contour = []
    for a in range (n):
        l = random.uniform(rad,rad+delt)
        x = l*np.cos(a*step)
        y = l*np.sin(a*step)
        contour.append(Point3D(x, y, 0))
    return contour

def divideTraj(s: "list[Point3D]", step: float)->"list[Point3D]":
    cont_traj = []
    for i in range(len(s)-1):
        cont_traj.append(s[i])
        dist2 = (s[i+1].x-s[i].x)**2+(s[i+1].y-s[i].y)**2+(s[i+1].z-s[i].z)**2
        dist = np.sqrt(dist2)
        
        if(2*dist>step):
            n = int(dist/step)
            for j in range(n):
                x = s[i].x +(step*j*(s[i+1].x - s[i].x))/dist
                y = s[i].y +(step*j*(s[i+1].y - s[i].y))/dist
                z = s[i].z +(step*j*(s[i+1].z - s[i].z))/dist
                cont_traj.append(Point3D(x,y,z))

    return cont_traj

def filterTraj(s: "list[Point3D]", filt: float)->"list[Point3D]":
    cont_traj = []
    for i in range(len(s)-1):
        dist2 = (s[i+1].x-s[i].x)**2+(s[i+1].y-s[i].y)**2+(s[i+1].z-s[i].z)**2
        dist = np.sqrt(dist2)      
        if(dist>filt):
            cont_traj.append(s[i])
    return cont_traj

def FindPoints_for_line(contour: "list[Point3D]", y: float):
    p1: Point3D
    p2: Point3D
    ps: list[Point3D]
    ps = []
    for i in range(0, len(contour)):
        if((y >= contour[i].y and y <contour[i-1].y or (y >= contour[i-1].y and y <contour[i].y))):
            ps.append(contour[i-1] ) 
            ps.append(contour[i] ) 
    #print(len(ps))
    if(len(ps)>3):
        
        if(ps[0].x<ps[2].x):
            return ps
        else:
            ps2: list[Point3D]
            ps2 = []
            ps2.append(ps[2])
            ps2.append(ps[3])
            ps2.append(ps[0])
            ps2.append(ps[1])
            return ps2
    else:
        return []


def FindCross_for_line(p: "list[Point3D]" ,y: float):

    x = p[0].x+(p[1].x-p[0].x)*(y-p[0].y)/(p[1].y-p[0].y)
    p1 = Point3D(x,y,0)

    x = p[2].x+(p[3].x-p[2].x)*(y-p[2].y)/(p[3].y-p[2].y)
    p2 = Point3D(x,y,0)
    return p1,p2
            
def GeneratePositionTrajectory_angle(contour: "list[Point3D]", step: float, alfa: float):
    contour_rotate = rotate_list_points(contour, alfa)
    traj = GeneratePositionTrajectory(contour_rotate, step)
    traJ_rotate = rotate_list_points(traj, -alfa)
    return traJ_rotate

def GeneratePositionTrajectory(contour: "list[Point3D]", step: float):
    # нахождение нижней точки
    y_min:float = 10000.
    i_min = 0.
    y_max:float = -10000.
    i_max = 0.
    for i in range(len(contour)):
        if(contour[i].y < y_min):
            y_min = contour[i].y
            i_min = i
        if(contour[i].y>y_max):
            y_max = contour[i].y
            i_max = i
    p_min = contour[i_min]
    p_max = contour[i_max]
    traj = []
    #добавление линии
    y = p_min.y
    flagRL = 0
    while y<p_max.y:
        ps = FindPoints_for_line(contour,y)
        if(len(ps)==4) and flagRL == 0:
            p1,p2 = FindCross_for_line(ps,y)
            traj.append(p2)
            traj.append(p1)
            flagRL =1
        elif(len(ps)==4) and flagRL == 1:
            p1,p2 = FindCross_for_line(ps,y)
            traj.append(p1)
            traj.append(p2)
            flagRL =0
    
        y+=step

    #for i in range(len(traj)):
        #print(str(traj[i].x)+" "+str(traj[i].y)+" "+str(traj[i].z)+" ")
    #добавление точки слева
    return traj

def Generate_one_layer_traj (contour: "list[Point3D]", step: float, alfa: float):
    traj = GeneratePositionTrajectory_angle(contour, step, alfa)
    return  traj 


def filResTraj(filt:float,proj_traj: "list[Point3D]",normal_arr,matrs):
    proj_traj_f = []
    normal_arr_f = []
    matrs_f = []
    proj_traj_f.append(proj_traj[0])
    normal_arr_f.append(normal_arr[0])
    matrs_f.append(matrs[0])
    for i in range(1,len(proj_traj)):
        dist = distance( proj_traj_f[-1],proj_traj[i])
        if dist>filt:
            proj_traj_f.append(proj_traj[i])
            normal_arr_f.append(normal_arr[i])
            matrs_f.append(matrs[i])

    return proj_traj_f,normal_arr_f, matrs_f
        




def filResTraj2d(filt:float,traj: "list[Point3D]"):
    traj_f = []
    traj_f.append(traj[0])

    for i in range(1,len(traj)):
        dist = distance( traj_f[-1],traj[i])
        if dist>filt:
            traj_f.append(traj[i])

    return traj_f

def Generate_multiLayer2d (contour: "list[Point3D]", step: float, alfa: float, amount: int):
    traj:"list[list[Point3D]]" = []
    for i in range (amount):
        alfa2 = alfa
        if i % 2 == 0:
            alfa2 += np.pi/2
        traj.append(Generate_one_layer_traj (contour, step, alfa2)) 

    return filResTraj2d(step/2,traj)


class Trajectory(object):
    def __init__(self,contour: "list[Point3D]", step: float, alfa: float, amount: int) -> None:
        traj = Generate_multiLayer2d (contour, step, alfa, amount)

    def optimize_tranzitions(self, traj:"list[list[Point3D]]"):
        approach = []
        for i in range(len(traj)):
            s1 = 0
            s2 = 1

            e1 = -1
            e2 = -2
            approach.append([[s1,e1],[s2,e2],[e1,s1],[e2,s2]])

        dists = []

        for i in range(len(traj)-1):
            dists_between = []
            for layer_1 in range(len(approach[i])):
                dists_layer = []
                for layer_2 in range(len(approach[i+1])):      
                    dists_layer.append(distance(traj[i][approach[i][layer_1][layer_2]],traj[i+1][approach[i][layer_1][layer_2]]))             
                dists_between.append(dists_layer)
            dists.append(dists_between)
        
        return traj

    def set_layer_direction(self,layer:"list[Point3D]",inds:"list[int]"):


        return layer
