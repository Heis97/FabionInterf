from math import dist
import numpy as np
import random
from Viewer3D_GL import PrimitiveType

from polygon import Mesh3D, Polygon3D,Point3D,Mesh3D,Flat3D


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
    y_min:float = 1000000.
    i_min = 0.
    y_max:float = -1000000.
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
            if (p1-p2).magnitude()>0.1:
                traj.append(p2)
                traj.append(p1)
                flagRL =1
        elif(len(ps)==4) and flagRL == 1:
            p1,p2 = FindCross_for_line(ps,y)
            if (p1-p2).magnitude()>0.1:
                traj.append(p1)
                traj.append(p2)
                flagRL =0
    
        y+=step

    #for i in range(len(traj)):
        #print(str(traj[i].x)+" "+str(traj[i].y)+" "+str(traj[i].z)+" ")
    #добавление точки слева
    return traj


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
        

def set_z_layer(layer: "list[Point3D]",z:float):
    for i in range(len(layer)):
        layer[i].z = z
    return layer


def filResTraj2d(filt:float,traj: "list[list[Point3D]]")->"list[Point3D]":
    traj_f = []
    if len(traj)==0:
        return []

    traj_f.append(traj[0][0])
    for lr in range(len(traj)):
        for i in range(1,len(traj[lr])):
            dist = distance( traj_f[-1],traj[lr][i])
            if dist>filt:
                traj_f.append(traj[lr][i])

    return traj_f

def Generate_multiLayer2d (contour: "list[Point3D]", step: float, alfa: float, amount: int):
    traj:"list[list[Point3D]]" = []
    for i in range (amount):
        alfa2 = alfa
        if i % 2 == 0:
            alfa2 += np.pi/2
        traj.append(GeneratePositionTrajectory_angle (contour, step, alfa2)) 

    return filResTraj2d(step/2,Trajectory.optimize_tranzitions_2_layer(traj) ) 

def Generate_multiLayer2d_mesh (contour: "list[list[Point3D]]",z:"list[float]", step: float, alfa: float):
    traj:"list[list[Point3D]]" = []
    for i in range (len(contour)):
        alfa2 = alfa
        if i % 2 == 0:
            alfa2 += np.pi/2
        layer = set_z_layer(GeneratePositionTrajectory_angle (contour[i], step, alfa2),z[i])
       
        traj.append(layer) 

    traj= Trajectory.optimize_tranzitions_2_layer(traj)
    for i in range (len(traj)):
        if i!=len(traj)-1:
            if len(traj[i])>0:
                last_pos= traj [i][-1].Clone()
                last_pos.z = z[i+1]
                traj[i].append(last_pos)

    return filResTraj2d(step/2,traj) 

def slice_mesh(mesh:Mesh3D,dz:float,step: float, alfa: float):
    contours = []
    zs = []
    len_ps = 1
    z = dz
    while len_ps>0:
        cont = mesh.find_intersect_triangles(Flat3D(Point3D(0,0, 1),-z))
        
        len_ps = len(cont)
        if len_ps>0:
            print(len_ps)
            contours.append(cont)
            zs.append(z)
            z+=dz

    return Generate_multiLayer2d_mesh(contours, zs, step, alfa)




class Trajectory(object):
    def __init__(self,contour: "list[Point3D]", step: float, alfa: float, amount: int) -> None:
        traj = Generate_multiLayer2d (contour, step, alfa, amount)

    def optimize_tranzitions( traj:"list[list[Point3D]]"):
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

    def optimize_tranzitions_2_layer(traj:"list[list[Point3D]]"):
        approach = []
        for i in range(len(traj)):
            s1 = 0
            s2 = 1

            e1 = -1
            e2 = -2
            approach.append([[s1,e1],[s2,e2],[e1,s1],[e2,s2]])
        
        dists = []
        
        
        for i in range(len(approach)): 
            b = []
            for j in range(len(approach[i])):
                c = [1000000000.]*len(approach[i])
                b.append(c) 
            dists.append(b) 
            #print(dists[i])
            #print("dists[i]_____________")
        #print(approach[0])
        
        for i in range(len(traj)-1):
            for layer_1 in range(len(approach[i])):
                for layer_2 in range(len(approach[i+1])): 
                    #print(str(i)+" "+str(layer_1)+" "+str(layer_2)+" ")  
                    if traj[i] != None and traj[i+1] != None:              
                        dists[i][layer_1][layer_2] = distance(
                        traj[i][approach[i][layer_1][1]],
                        traj[i+1][approach[i][layer_2][0]])    
                    #print(str(i)+": "+traj[i][approach[i][layer_1][1]].ToString()+"; "+traj[i+1][approach[i][layer_2][0]].ToString()+" "+str(dists[i][layer_1][layer_2]) )

            #print("__________________")
        
        fast_way =[]
        for i in range(len(dists)):
            if i==0:
                low,up = Trajectory.find_best_way_first(dists[i])
                fast_way = [low,up]
            else:
                low,up = Trajectory.find_best_way_cont(dists[i],fast_way[-1])
                fast_way.append(up)
            #print(dists[i])
            #print("dists[i]_____________")

        #print(fast_way)
        print("traj before_____________")
        Trajectory.comp_trans(traj)

        print("traj after_____________")
        Trajectory.comp_trans(Trajectory.optimize_trans(traj,approach,fast_way) )



        return traj

    

    def find_best_way_first(trans_map:"list[list[float]]"):
        low:int = 0
        up:int =0
        min_dist:float = 100000
        for i in range(len(trans_map)): 
            for j in range(len(trans_map[i])):
                if(trans_map[i][j]<min_dist):
                    min_dist = trans_map[i][j]
                    low = i
                    up = j
        return low,up

    def find_best_way_cont(trans_map:"list[list[float]]",prev_l:int):
        low:int = prev_l
        up:int =0
        min_dist:float = 100000
        for j in range(len(trans_map[prev_l])):
            if(trans_map[prev_l][j]<min_dist):
                min_dist = trans_map[prev_l][j]
                up = j
        return low,up

    def optimize_trans(traj:"list[list[Point3D]]",approach:"list[list[int]]",fast_way:"list[int]"):
        opt_traj = []
        for i in range(len(traj)):

            opt_traj.append(Trajectory.set_layer_direction(traj[i],approach[i][fast_way[i]]))

        return opt_traj



    def comp_trans(traj:"list[list[Point3D]]"):
        trans = []
        all_tr = 0.
        for i in range(len(traj)-1):
            if traj[i] != None and traj[i+1] != None:    
                dist = distance(traj[i][-1],traj[i+1][0])
                trans.append(dist)
                all_tr+=dist
        #print(trans )
        print(all_tr)


    def set_layer_direction(layer:"list[Point3D]",inds:"list[int]")->"list[Point3D]":
        #print(layer[0].ToString()+" "+layer[1].ToString()+" "+layer[-2].ToString()+" "+layer[-1].ToString()+" ")
        #print(">>>>>>>>>   "+str(inds[0])+"   <<<<<<<<<<<              |||||||||||||||||||||||||||||||")
        if inds[0] == 0:
            pass
        elif inds[0] == -1:
            layer.reverse()

        elif inds[0] == 1:
            layer = Mesh3D.reverse_line_direct(layer)

            
        
        elif inds[0] == -2:
            layer.reverse()
            layer = Mesh3D.reverse_line_direct(layer)

        #print(layer[0].ToString()+" "+layer[1].ToString()+" "+layer[-2].ToString()+" "+layer[-1].ToString()+" ")
        #print("________________________________")
        #print(inds[0])
        return layer

    

  




if __name__ == "__main__":

    #cont = [Point3D(-20,20,0),Point3D(20,20,0),Point3D(20,-20,0),Point3D(-20,-20,0)]
    cont = GenerateContour(10,5,3) 
    traj = Generate_multiLayer2d(cont, 1.3, np.pi/2,  10)

