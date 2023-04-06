import numpy as np
import random
from path_planner.Viewer3D_GL import PrimitiveType
from enum import  Enum
from path_planner.polygon import Mesh3D, Polygon3D,Point3D,Mesh3D,Flat3D


class Filling_type(Enum):
    Rectangle_def = 1
    Rectangle_discr = 2
    Rectangle_ecv_cont = 3




def distance(p1: Point3D, p2: Point3D):
    dist3 = (p1.x-p2.x)**2+(p1.y-p2.y)**2+(p1.z-p2.z)**2
    return np.sqrt(dist3)

def rotate_point(x: float, y: float, alfa: float):
    
    x_r = x * np.cos(alfa) - y * np.sin(alfa)
    y_r = x * np.sin(alfa) + y * np.cos(alfa)
    return x_r, y_r

def translate_list_points(points: "list[Point3D]", p:Point3D):
    translated_points = []
    for i in range(len(points)):       
        translated_points.append(points[i]+p)
    return translated_points

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
        if((y >= contour[i].y and y <contour[i-1].y) 
        or (y >= contour[i-1].y and y <contour[i].y)):
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
            
def GeneratePositionTrajectory_angle(contour: "list[Point3D]", step: float, alfa: float,fil_type:Filling_type):
    contour_rotate = rotate_list_points(contour, alfa)
    trans = Point3D(0., 0., 0.)
    contour_translate = translate_list_points(contour_rotate,trans)
    traj,ps_cells = GeneratePositionTrajectory(contour_translate, step,fil_type)

    traj_translate  = translate_list_points(traj, -trans)
    ps_cells_translate  = translate_list_points(ps_cells, -trans)

    traj_rotate = rotate_list_points(traj_translate, -alfa)
    ps_cells_rotate = rotate_list_points(ps_cells_translate, -alfa)

    
    return traj_rotate ,ps_cells_rotate 

def GeneratePositionTrajectory(contour: "list[Point3D]", step: float,fil_type:Filling_type):
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
    y = round(p_min.y/step)*step
    ps_cells:"list[Point3D]" = []
    flagRL = 0
    #print("++++++++++++++++++++++")
    while y<=p_max.y:

        ps = FindPoints_for_line(contour,y)
        if(len(ps)==4):
            p1,p2 = FindCross_for_line(ps,y)
            if fil_type==Filling_type.Rectangle_discr:
                p1 = discr_xy(p1, step)
                p2 = discr_xy(p2, step)
            ps_cells+=line_cells(p1, p2, step)
            if (p1-p2).magnitude()>0.1:
                if flagRL == 0:
                    lam = p1.Clone()
                    p1 = p2.Clone()
                    p2 = lam.Clone()                    
                    flagRL =1
                else:                   
                    flagRL =0

                #if len(traj)>0:
                    #p1.x =min(p1.x,traj[-1].x)
                    #traj[-1].x = p1.x
                traj.append(p1)
                traj.append(p2)
    
        y+=step

    return traj,filtr_cells_in_layer_xy(ps_cells,step)

def discr_xy(p:Point3D,step:float):
    p.x = round(p.x/step)*step
    p.y = round(p.y/step)*step
    return p

def repeat_contour_2d(ps:"list[Point3D]",delt:float)->"list[Point3D]":
    lines = comp_eval_lines(ps)
    lines_off= offset_lines(lines, delt)
    ps_f = intersec_lines(lines_off)
    return ps_f 

def repeat_contour_2d_step(ps:"list[Point3D]",delt:float)->"list[Point3D]":
    step = 0.1
    if delt < 0: step = -0.1
    
    step_i = abs(int(delt/step))
    #print(step_i)
    arr = repeat_contour_2d(ps,step)
    
    for i in range(step_i):
        arr = repeat_contour_2d(arr,step)

    return arr

def comp_eval_lines(ps:"list[Point3D]")->list:
    lines=[]
    for i in range(len(ps)):
        lines.append([ps[i-1].x,ps[i-1].y,ps[i].x-ps[i-1].x,ps[i].y-ps[i-1].y])
    return lines 

def offset_line(x:float,y:float,vx:float,vy:float, delt:float)->list:
    vx_r,vy_r = rotate_point(vx, vy, -np.pi/2)
    vlen = (vx_r**2+vy_r**2)**0.5
    vx_r = vx_r*delt/vlen
    vy_r = vy_r*delt/vlen
    return [x+vx_r,y+vy_r,vx,vy]

def offset_lines(lines:list, delt:float)->list:
    lines_off = []
    for line in lines:
        lines_off.append(offset_line(line[0],line[1],line[2],line[3], delt))
    return lines_off

"""
y = ax+b

x = x1+k*xa1
y = y1+k*ya1

x = x2+j*xa2
y = y2+j*ya2

x1+k*xa1 = x2+j*xa2
y1+k*ya1 = y2+j*ya2

k = (x2+j*xa2-x1)/xa1

y1+ya1*(x2+j*xa2-x1)/xa1 = y2+j*ya2

y1*xa1 + ya1*x2 + ya1*j*xa2 - ya1*x1 = y2*xa1 + j*ya2*xa1

ya1*j*xa2 - j*ya2*xa1 = y2*xa1  - y1*xa1 - ya1*x2 + ya1*x1

(ya1*xa2-ya2*xa1) j = y2*xa1 - y1*xa1 - ya1*x2 + ya1*x1
j = (y2*xa1 - y1*xa1 - ya1*x2 + ya1*x1)/(ya1*xa2 - ya2*xa1)
"""

def intersec_2line(line1:list,line2:list):
    x1 = line1[0]
    y1 = line1[1]
    xa1 = line1[2]
    ya1 = line1[3]

    x2 = line2[0]
    y2 = line2[1]
    xa2 = line2[2]
    ya2 = line2[3]

    if ya1*xa2 - ya2*xa1==0:
        return 0,0

    j = (y2*xa1 - y1*xa1 - ya1*x2 + ya1*x1)/(ya1*xa2 - ya2*xa1)
    x = x2+j*xa2
    y = y2+j*ya2

    return x,y

def intersec_3line(line1:list,line2:list,line3:list):
    x1,y1= intersec_2line(line1,line2)
    p1 = Point3D(x1,y1,0)
    x2,y2= intersec_2line(line2,line3)
    p2 = Point3D(x2,y2,0)
    ang = Point3D.ang(p2-p1,Point3D(line2[2], line2[3], 0))
    return x1,y1,ang



def intersec_lines(lines:list)->"list[Point3D]":
    ps = []
    k= 0
    for i in range(len(lines)):

        #x,y  = intersec_2line(lines[i-1], lines[i])
        x,y,ang=intersec_3line(lines[i-2],lines[i-1], lines[i])
        if ang<0.1:

            ps.append(Point3D(x,y,0))
        else:
            k+=1

    #print(k,len(lines),len(ps))
    return ps



def line_cells(p1: Point3D,p2: Point3D,step: float)->"list[Point3D]":
    x = []
    start_x = round(min(p1.x,p2.x)/step)*step 
    for i in range(round(abs(p1.x-p2.x)/step)):
        x.append(Point3D((start_x+i*step)+step/2,p1.y+step/2,0))
        x.append(Point3D((start_x+i*step)+step/2,p1.y-step/2,0))
    return x

def filtr_cells_in_layer_xy(ps:"list[Point3D]",step:float)->"list[Point3D]":
    ps_f = []
    inds = []
    for i in range(len(ps)):
        for j in range(i,len(ps)):
            if((ps[j]-ps[i]).magnitude_xy()<0.001):
                if not inds.__contains__(j) and i!=j:
                    ps_f.append(ps[j])
                    inds.append(j)
    return ps_f

def filtr_cells_in_z(ps:"list[Point3D]",step:float,dz:float)->"list[Point3D]":
    ps_f = []
    ps_z = []
    inds = []
    for i in range(len(ps)):
        ps_f.append([])
        for j in range(i,len(ps)):
            if((ps[j]-ps[i]).magnitude_xy()<0.001):
                if not inds.__contains__(j) and i!=j:
                    ps_f[i].append(ps[j])
                    inds.append(j) 
    for i in range(len(ps_f)):
        ps_f[i].sort(key=lambda x: x.z)
        for j in range(1,len(ps_f[i])):
            if abs((ps_f[i][j].z-ps_f[i][j-1].z)-dz) > 0.1:
                ps_f[i] = None
                break
    for i in range(len(ps_f)):
        if ps_f[i]!=None:
            ps_z+=ps_f[i]
    return ps_z

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

        for i in range(len(traj[lr])):
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
        traj.append(GeneratePositionTrajectory_angle (contour, step, alfa2,Filling_type.Rectangle_def)) 

    return filResTraj2d(step/2,Trajectory.optimize_tranzitions_2_layer(traj) ) 

def Generate_multiLayer2d_mesh (contour: "list[list[Point3D]]",z:"list[float]", step: float, alfa: float)->"tuple[list[Point3D],list[Point3D]]":
    traj:"list[list[Point3D]]" = []
    cells_all = []
    for i in range (len(contour)):
        alfa2 = alfa
        if i % 2 == 0:
            alfa2 += np.pi/2
        if i==0:
            step_l = 1.4
            alfa2 = np.pi/4
        else:
            step_l = step
        layer2d,cells2d = GeneratePositionTrajectory_angle (contour[i], step_l, alfa2,Filling_type.Rectangle_def)
        layer = set_z_layer(layer2d,z[i])
        cells = set_z_layer(cells2d,z[i])
        traj.append(layer) 
        cells_all+=cells 

    traj= Trajectory.optimize_tranzitions_2_layer(traj)
    for i in range (len(traj)):
        if i!=len(traj)-1:
            if len(traj[i])>0:
                last_pos= traj [i][-1].Clone()
                last_pos.z = z[i+1]
                traj[i].append(last_pos)
    
    return filResTraj2d(0.01,traj),filtr_cells_in_z(cells_all, step,z[0]) 


#нарезка модели на слои
def slice_mesh(mesh:Mesh3D,dz:float,step: float, alfa: float)->"tuple[list[Point3D],list[Point3D]]":
    contours = []
    zs = []
    len_ps = 1
    z = dz
    #последовательная нарезка модели на контуры, с шагом dz
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

        for i in range(len(traj)-1):
            for layer_1 in range(len(approach[i])):
                for layer_2 in range(len(approach[i+1])): 
                    if traj[i] != None and traj[i+1] != None:              
                        dists[i][layer_1][layer_2] = distance(
                        traj[i][approach[i][layer_1][1]],
                        traj[i+1][approach[i][layer_2][0]])    
        fast_way =[]
        for i in range(len(dists)):
            if i==0:
                low,up = Trajectory.find_best_way_first(dists[i])
                fast_way = [low,up]
            else:
                low,up = Trajectory.find_best_way_cont(dists[i],fast_way[-1])
                fast_way.append(up)

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
        print(all_tr)


    def set_layer_direction(layer:"list[Point3D]",inds:"list[int]")->"list[Point3D]":
        if inds[0] == 0:
            pass
        elif inds[0] == -1:
            layer.reverse()
        elif inds[0] == 1:
            layer = Mesh3D.reverse_line_direct(layer)       
        elif inds[0] == -2:
            layer.reverse()
            layer = Mesh3D.reverse_line_direct(layer)
        return layer



if __name__ == "__main__":

    #cont = [Point3D(-20,20,0),Point3D(20,20,0),Point3D(20,-20,0),Point3D(-20,-20,0)]
    cont = GenerateContour(10,5,3) 
    traj = Generate_multiLayer2d(cont, 1.3, np.pi/2,  10)

