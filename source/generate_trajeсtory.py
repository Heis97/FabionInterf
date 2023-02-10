from path_planner.polygon import Point3D
from math import sqrt
from enum import Enum
from print_settings import PrintSettings,TrajectorySettings

class Current_corner(Enum):
    bot_left = 0
    bot_right = 1
    top_left = 2
    top_right = 3


class GCodeFrame(object):
    x:float = 0
    y:float = 0
    z:float = 0
    e:float = 0
    f:float = 0
    com_num:int = 0

    def __init__(self,_com_num,_x,_y,_z,_e,_f):
        self.x = _x
        self.y = _y
        self.z = _z
        self.e = _e
        self.f = _f
        self.com_num = _com_num

def check_corner(x:float,y:float,start_x:float=0,start_y:float=0)-> Current_corner:
    if y==0:
        if x==0:
            return Current_corner.bot_left
        else:
            return Current_corner.bot_right
    else:
        if x==0:
            return Current_corner.top_left
        else:
            return Current_corner.top_right


def convert_to_points3d(tr:list)->"list[Point3D]":
    p3ds = []
    for i in range(len(tr)):
        p3ds.append(Point3D(tr[i][0],tr[i][1],tr[i][2]))
    return p3ds

def convert_to_tr(traj:"list[list[Point3D]]")->"list[Point3D]":
    p3ds = []
    for i in range(len(traj)):
        for j in range((traj[i])):
            p3ds.append([traj[i][j].x,traj[i][j].y,traj[i][j].z])
    return p3ds

def generate_file(tr: list, name: str, F: float, diam: float, dz: float, ndoz: int):
    f1=open(name,'w')
    N = 5
    for i in range(len(tr)):
        x = tr[i][0]
        y = tr[i][1]
        z = tr[i][2]
        if(i==0):
            f1.write('N'+str(N)+' G11 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z+3,4))+  ' D'+str(ndoz)+'\n')
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
            f1.write('N'+str(N)+' G11 X'+str(round(x,4))+' Y'+str(round(y,4))+' Z'+str(round(z+3,4))+  ' D'+str(ndoz)+'\n')
            N+=5

    f1.close()  


def generate_traj_collag_1(z1:float,trajectory_settings:TrajectorySettings):
    nx: int = trajectory_settings.nx
    ny: int= trajectory_settings.ny
    d: float= trajectory_settings.d
    dz: float= trajectory_settings.dz
    nz: int= trajectory_settings.nz
    start_xyz:Point3D= trajectory_settings.start_xyz
    a = nx*d
    b = ny*d
    traj = []
    z = z1
    traj.append(Point3D(0,0,z))
    traj.append(Point3D(a,0,z))
    traj.append(Point3D(a,b/2,z))
    traj.append(Point3D(0,b/2,z))
    traj.append(Point3D(0,b,z))
    traj.append(Point3D(a,b,z))
    traj.append(Point3D(0,0,z))
    z+=dz/2
    traj.append(Point3D(0,0,z))
    traj.append(Point3D(0,b,z))
    traj.append(Point3D(a,b,z))
    traj.append(Point3D(a,0,z))
    traj.append(Point3D(0,0,z))
    z+=dz
    traj.append(Point3D(0,0,z))
    traj.append(Point3D(0,b,z))
    traj.append(Point3D(a,b,z))
    traj.append(Point3D(a,0,z))
    traj.append(Point3D(0,0,z))
    z+=dz
    traj.append(Point3D(0,0,z,False))
    traj.append(Point3D(0,b,z,False))
    traj.append(Point3D(a,b,z,False))
    traj.append(Point3D(a,0,z,False))
    traj.append(Point3D(0,0,z,False))
    z+=dz
    return Point3D.add_offs(traj, trajectory_settings.start_xyz)

def generate_traj_collag_2(z1:float,trajectory_settings:TrajectorySettings):
    nx: int = trajectory_settings.nx
    ny: int= trajectory_settings.ny
    d: float= trajectory_settings.d
    dz: float= trajectory_settings.dz
    nz: int= trajectory_settings.nz
    start_xyz:Point3D= trajectory_settings.start_xyz
    a = nx*d
    b = ny*d
    traj = []
    z = z1
    traj.append(Point3D(0,b/2,z,False))
    traj.append(Point3D(0,0,z))
    traj.append(Point3D(a,0,z))
    traj.append(Point3D(a,b,z))
    traj.append(Point3D(0,b,z))
    traj.append(Point3D(0,b/2,z))
    traj.append(Point3D(a,b/2,z))
    traj.append(Point3D(a/2,b,z,False))
    traj.append(Point3D(a/2,0,z))
    traj.append(Point3D(0,b/2,z,False))
    z+=dz
    traj.append(Point3D(0,b/2,z,False))
    traj.append(Point3D(0,0,z))
    traj.append(Point3D(a,0,z))
    traj.append(Point3D(a,b,z))
    traj.append(Point3D(0,b,z))
    traj.append(Point3D(0,b/2,z))
    traj.append(Point3D(a,b/2,z))
    traj.append(Point3D(a/2,b,z,False))
    traj.append(Point3D(a/2,0,z))
    traj.append(Point3D(0,b/2,z,False))
    z+=dz
    traj.append(Point3D(0,b/2,z,False))
    traj.append(Point3D(0,0,z))
    traj.append(Point3D(a,0,z))
    traj.append(Point3D(a,b,z))
    traj.append(Point3D(0,b,z))
    traj.append(Point3D(0,b/2,z))
    traj.append(Point3D(a,b/2,z))
    traj.append(Point3D(a/2,b,z,False))
    traj.append(Point3D(a/2,0,z))
    traj.append(Point3D(0,b/2,z,False))
    z+=dz
    traj.append(Point3D(0,b/2,z,False))
    traj.append(Point3D(0,0,z))
    traj.append(Point3D(a,0,z))
    traj.append(Point3D(a,b,z))
    traj.append(Point3D(0,b,z))
    traj.append(Point3D(0,b/2,z))
    traj.append(Point3D(a,b/2,z))
    traj.append(Point3D(a/2,b,z,False))
    traj.append(Point3D(a/2,0,z))
    traj.append(Point3D(0,b/2,z,False))

    
    return Point3D.add_offs(traj, trajectory_settings.start_xyz)

def generate_traj_collag_3(z1:float,trajectory_settings:TrajectorySettings):
    nx: int = trajectory_settings.nx
    ny: int= trajectory_settings.ny
    d: float= trajectory_settings.d
    dz: float= trajectory_settings.dz
    nz: int= trajectory_settings.nz
    start_xyz:Point3D= trajectory_settings.start_xyz
    a = nx*d
    b = ny*d
    traj = []
    z = z1
    traj.append(Point3D(a/2,b,z,False))
    traj.append(Point3D(0,b,z))
    traj.append(Point3D(0,0,z))
    traj.append(Point3D(a/2,0,z))
    traj.append(Point3D(a/2,b,z))
    traj.append(Point3D(a,b,z))
    traj.append(Point3D(a,0,z))
    traj.append(Point3D(a/2,0,z))
    z+=dz
    traj.append(Point3D(a/2,0,z,False))
    traj.append(Point3D(0,0,z))
    traj.append(Point3D(0,b,z))
    traj.append(Point3D(a/2,b,z))
    traj.append(Point3D(a/2,0,z))
    traj.append(Point3D(a,0,z))
    traj.append(Point3D(a,b,z))
    traj.append(Point3D(a/2,b,z))
    z+=dz

    traj.append(Point3D(a/2,b,z,False))
    traj.append(Point3D(0,b,z))
    traj.append(Point3D(0,0,z))
    traj.append(Point3D(a/2,0,z))
    traj.append(Point3D(a/2,b,z))
    traj.append(Point3D(a,b,z))
    traj.append(Point3D(a,0,z))
    traj.append(Point3D(a/2,0,z))
    z+=dz
    traj.append(Point3D(a/2,0,z,False))
    traj.append(Point3D(0,0,z))
    traj.append(Point3D(0,b,z))
    traj.append(Point3D(a/2,b,z))
    traj.append(Point3D(a/2,0,z))
    traj.append(Point3D(a,0,z))
    traj.append(Point3D(a,b,z))
    traj.append(Point3D(a/2,b,z))
    z+=dz


    

    
    return Point3D.add_offs(traj, trajectory_settings.start_xyz)

def set_z_layer(layer: "list[Point3D]",z:float):
    for i in range(len(layer)):
        layer[i].z = z
    return layer

def generate_traj_collag_4(z1:float,trajectory_settings:TrajectorySettings):
    nx: int = trajectory_settings.nx
    ny: int= trajectory_settings.ny
    d: float= trajectory_settings.d
    dz: float= trajectory_settings.dz
    nz: int= trajectory_settings.nz
    start_xyz:Point3D= trajectory_settings.start_xyz
    a = nx*d
    b = ny*d
    traj_all = []
    traj = []
    z = z1

    ps = [Point3D(0,0,0),
    Point3D(0,0,0),Point3D(0,b/2,0),Point3D(0,b,0),
    Point3D(a/3,0,0),Point3D(0,b/2,0),Point3D(a/3,b,0),
    Point3D(2*a/3,0,0),Point3D(2*a/3,b/2,0),Point3D(2*a/3,b,0),
    Point3D(a,0,0),Point3D(a,b/2,0),Point3D(a,b,0)]

    ps_f = [Point3D(0,0,0),
    Point3D(0,0,0,False),Point3D(0,b/2,0,False),Point3D(0,b,0,False),
    Point3D(a/3,0,0,False),Point3D(0,b/2,0,False),Point3D(a/3,b,0,False),
    Point3D(2*a/3,0,0,False),Point3D(2*a/3,b/2,0,False),Point3D(2*a/3,b,0,False),
    Point3D(a,0,0,False),Point3D(a,b/2,0,False),Point3D(a,b,0,False)]

    traj = []
    traj.append(ps_f[2].Clone())
    traj.append(ps[1].Clone())
    traj.append(ps[10].Clone())
    traj.append(ps[12].Clone())
    traj.append(ps[3].Clone())
    traj.append(ps[2].Clone())
    traj.append(ps[11].Clone())
    traj.append(ps_f[7].Clone())
    traj.append(ps[9].Clone())
    traj.append(ps_f[6].Clone())
    traj.append(ps[4].Clone())
    traj.append(ps_f[2].Clone())

    traj = set_z_layer(traj, z)

    traj_all+=traj   
    z+=dz

    traj = []
    traj.append(ps_f[2].Clone())
    traj.append(ps[1].Clone())
    traj.append(ps[10].Clone())
    traj.append(ps[12].Clone())
    traj.append(ps[3].Clone())
    traj.append(ps[2].Clone())
    traj.append(ps[11].Clone())
    traj.append(ps_f[7].Clone())
    traj.append(ps[9].Clone())
    traj.append(ps_f[6].Clone())
    traj.append(ps[4].Clone())
    traj.append(ps_f[2].Clone())

    traj = set_z_layer(traj, z)

    traj_all+=traj   
    z+=dz

    traj = []
    traj.append(ps_f[2].Clone())
    traj.append(ps[1].Clone())
    traj.append(ps[10].Clone())
    traj.append(ps[12].Clone())
    traj.append(ps[3].Clone())
    traj.append(ps[2].Clone())
    traj.append(ps[11].Clone())
    traj.append(ps_f[7].Clone())
    traj.append(ps[9].Clone())
    traj.append(ps_f[6].Clone())
    traj.append(ps[4].Clone())
    traj.append(ps_f[2].Clone())

    traj = set_z_layer(traj, z)

    traj_all+=traj   
    z+=dz

    traj = []
    traj.append(ps_f[2].Clone())
    traj.append(ps[1].Clone())
    traj.append(ps[10].Clone())
    traj.append(ps[12].Clone())
    traj.append(ps[3].Clone())
    traj.append(ps[2].Clone())
    traj.append(ps[11].Clone())
    traj.append(ps_f[7].Clone())
    traj.append(ps[9].Clone())
    traj.append(ps_f[6].Clone())
    traj.append(ps[4].Clone())
    traj.append(ps_f[2].Clone())

    traj = set_z_layer(traj, z)

    traj_all+=traj   
    z+=dz

    

    return Point3D.add_offs(traj_all, trajectory_settings.start_xyz)

def generate_file_def(tr: "list[GCodeFrame]"):
    f1=open("fab_cod_mesh.cnc",'w')
    N = 5
    f1.write('N'+str(N)+' G90'+'\n')
    N+=5
    ndoz = 3
    k = 0.1
    for i in range(len(tr)):
        com_num = tr[i].com_num
        if com_num == 0:
            f1.write('N'+str(N)+' G11 X'+str(round(k*tr[i].x,4))+' Y'+str(round(k*tr[i].y,4))+' Z'+str(round(k*tr[i].z,4))+  ' D'+str(ndoz)+'\n')
            N+=5
        elif com_num == 1:
            f1.write('N'+str(N)+' G88 X'+str(round(k*tr[i].x,4))+' Y'+str(round(k*tr[i].y,4))+' Z'+str(round(k*tr[i].z,4))+ ' F'+str(round(k*tr[i].f/60,4))+ ' V'+str(round(k*tr[i].e,4))+  ' D'+str(ndoz)+' Q0 T1 I0 J0 \n')
            N+=5
    f1.close()



def generate_traj_Fabion(tr: list, print_settings:PrintSettings)->str:
    code = ";Fabion"
    name: str = print_settings.name
    Flow: float = print_settings.F 
    diam: float = print_settings.diam
    dz: float = print_settings.dz
    ndoz: int = print_settings.ndoz
    startE:float = print_settings.startE
    diam_syr:float = print_settings.diam_syr
    F = Flow*60
    F_tr = 20*60
    cur_z= ' Z'
    safe_z = 50
    if ndoz==1:
        cur_z = ' A'
    elif ndoz==2:
        cur_z = ' B'
    v_all = startE
    code += (';'+name+
    ' F'+str(round(F,4))+
    '\n; diam'+str(round(diam,4))+
    '\n; dz'+str(round(dz,4))+
    '\n; ndoz'+str(round(ndoz,4))+
    '\n; startE'+str(round(startE,4))+'\n')
    code +=('T'+str(int(ndoz))+'\n')
    code +=('G92 E0\n')
    code +=('M302 S0\n')
    code +=('G90\n')
    for i in range(len(tr)):
        x = tr[i].x
        y = tr[i].y
        z = tr[i].z
        if(i==0):
            code +=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z+safe_z,4))+ ' F'+str(round(F_tr,5))+'\n')
            code +=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z,4))+ ' F'+str(round(F_tr,5))+  '\n')
            code +=('G1 E0.05\n')
            code +=('G92 E0\n')
        else:
            x_ = tr[i-1].x
            y_ = tr[i-1].y
            z_ = tr[i-1].z
            rasst = sqrt((x - x_)**2+(y - y_)**2+(z - z_)**2)
            v = diam*dz*rasst/(3.141592*(diam_syr/2)**2)
            v_all+=v
            if tr[i].extrude is True:
                code +=('G1 X'+str(round(x,5))+' Y'+str(round(y,5))+cur_z+str(round(z,5))+ ' F'+str(round(F,5))+ ' E'+str(round(v_all,5))+'\n')
            else:
                code +=('G0 X'+str(round(x,5))+' Y'+str(round(y,5))+cur_z+str(round(z,5))+ ' F'+str(round(F_tr,5))+'\n')
    code +=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z+safe_z,4))+ ' F'+str(round(F_tr,5))+  '\n')

    vol_cm3 = 0.058*(v_all-startE)
    code +=(";Volume: "+str(round(vol_cm3,4))+"cm3"+'\n')    

    f1=open(name,'w')
    f1.write(code)
    f1.close() 
    return code




def generate_file_sph(tr: list, name: str, F: float, diam: float, dz: float, ndoz: int,startE:float)->str:

    
    code =""
    F = F*60
    Diam_syr = 10.5
    cur_z= ' Z'
    safe_z = 50
    safe_z_intern = 5
    if ndoz==1:
        cur_z = ' A'
    elif ndoz==2:
        cur_z = ' B'

    code+=(';'+name+
    ' F'+str(round(F,4))+
    '\n; diam'+str(round(diam,4))+
    '\n; dz'+str(round(dz,4))+
    '\n; ndoz'+str(round(ndoz,4))+
    '\n; startE'+str(round(startE,4))+'\n')
    code+=('T'+str(int(ndoz))+'\n')
    code+=('G92 E0\n')
    code+=('M302 S0\n')
    code+=('G90\n')
    v_all = startE
    for i in range(len(tr)):
        x = tr[i][0]
        y = tr[i][1]
        z = tr[i][2]
        if i == 0:
            code+=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z+safe_z,4))+' F600.0\n')
            code+=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z+safe_z_intern,4))+  '\n')
        
            
        code+=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z+safe_z_intern,4))+'\n')
        code+=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z,4))+'\n')

        rasst = dz
        v = diam*diam*rasst/(3.141592*(Diam_syr/2)**2)
        v_all+=v

        code+=('G1' +' E'+str(round(v_all,4))+ ' \n')
        code+=('G0' +cur_z +str(round(z+dz,4))+ ' F50.0 \n')
        code+=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z+safe_z_intern,4))+  ' F'+str(round(F,4))+'\n')

    code+=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z+safe_z,4))+ '\n')

    f1=open(name,'w')
    f1.write(code)
    f1.close() 
    return code


def generate_fileGcode_regemat(tr: list, print_settings:PrintSettings)->str:
    name: str = print_settings.name
    Flow: float = print_settings.F 
    diam: float = print_settings.diam
    dz: float = print_settings.dz
    ndoz: int = print_settings.ndoz
    startE:float = print_settings.startE
    diam_syr:float = print_settings.diam_syr
    code = ""
    
    F = Flow
    Diam_syr = diam_syr
    
    cur_z= ' Z'
    safe_z = 20

    v_all = startE

    code +=(
        'M109 S60 H6; set temperature H6 \n'+
        'M109 S240 H4; set temperature H4 \n'+     
        'G28 W3; homing\n'+
        'G28 XYZ; homing\n'+
        'T'+str(int(ndoz))+ '\n'+
        'G0 Z20 F5 ; initial movement for warming\n'+
        'T'+str(int(ndoz))+ '; use tool\n')
    for i in range(len(tr)):
        x = tr[i][0]
        y = tr[i][1]
        z = tr[i][2]
        if(i==0):
            code +=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z+safe_z,4))+' F20\n'+
        'G92 E0 \n'+
        'G1 E10 F6  ; pre-compensate \n'+
        'G92 E0 \n')
            code +=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z,4))+  ' F10\n')
            code +=('T'+str(int(ndoz))+ ' S0 \n')

        else:
            x_ = tr[i-1][0]
            y_ = tr[i-1][1]
            z_ = tr[i-1][2] 
            rasst = sqrt((x - x_)**2+(y - y_)**2+(z - z_)**2)
            v = diam*dz*rasst/(3.141592*(Diam_syr/2)**2)
            v_all+=v
            code +=('G1 X'+str(round(x,5))+' Y'+str(round(y,5))+cur_z+str(round(z,5))+ ' F'+str(round(F,5))+ ' E'+str(round(v_all,5))+'\n')

    code +=('G0 X'+str(round(x,4))+' Y'+str(round(y,4))+cur_z+str(round(z+safe_z,4))+ '\n')

    code +=(";Volume: "+str(0.058*(v_all-startE))+"cm2"+'\n')    

    f1=open(name,'w')
    f1.write(code)
    f1.close() 
    return code

#d - расстояние между линиями| dz - толщина линии |nx,ny - количество линий по каждой оси
def generate_mesh(tr:list,trajectory_settings:TrajectorySettings):
    nx: int = trajectory_settings.nx
    ny: int= trajectory_settings.ny
    d: float= trajectory_settings.d
    dz: float= trajectory_settings.dz
    nz: int= trajectory_settings.nz
    start_xyz:Point3D= trajectory_settings.start_xyz
    tr1 = []
    for i_z in range(int(nz/2)):
        tr1 = generate_2layers(tr,nx,ny,d,dz,start_xyz)   
        tr = tr1.copy()
    return tr

def generate_mesh_regemat(tr:list,trajectory_settings:TrajectorySettings):
    nx: int = trajectory_settings.nx
    ny: int= trajectory_settings.ny
    d: float= trajectory_settings.d
    dz: float= trajectory_settings.dz
    nz: int= trajectory_settings.nz
    start_xyz:Point3D= trajectory_settings.start_xyz
    tr1 = []
    for i_z in range(int(nz/2)):
        tr1 = generate_2layers(tr,nx,ny,d,dz,start_xyz) 
        print(tr1)  
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


# a - расстояние между линиями| dz - толщина линии(для сфероидов - высота первого слоя) |nx,ny - количество линий по каждой оси
# diam - толщина дорожки // F - скорость подачи в мм/с // nz - количество слоёв // ndoz- номер дозатора
# startz - высота первого слоя при генерации слоя или решётки
def generate_2layers(tr: list[Point3D],nx: int,ny: int,d: float,dz: float,start_xyz:Point3D):
    Lx = d*nx
    Ly = d*ny
    x = start_xyz.x
    y = start_xyz.y
    z = start_xyz.z
    z+=dz
    if len(tr)==0 or (tr[-1].x ==0 and tr[-1].y==0 and tr[-1].z==0):
        tr = [Point3D(x,y,z)]
        pass
    else:
        x = tr[-1].x
        y = tr[-1].y
        z = tr[-1].z
    
    tr.append(Point3D(x,y,z))
    if(ny%2==0):
        for i in range(0,int(ny/2)):

            x += Lx
            tr.append(Point3D(x,y,z))

            y+=d
            tr.append(Point3D(x,y,z))
        
            x -= Lx
            tr.append(Point3D(x,y,z))

            y+=d
            tr.append(Point3D(x,y,z))
        x += Lx
        tr.append(Point3D(x,y,z))

        z+=dz
        tr.append(Point3D(x,y,z))

        if(nx%2==0):
            for i in range(0,int(nx/2)):

                y -= Ly
                tr.append(Point3D(x,y,z))

                x-=d
                tr.append(Point3D(x,y,z))
            
                y += Ly
                tr.append(Point3D(x,y,z))

                x-=d
                tr.append(Point3D(x,y,z))

            y -= Ly
            tr.append(Point3D(x,y,z))
             
            return tr
        else:
            for i in range(0,int((nx-1)/2)):

                y -= Ly
                tr.append(Point3D(x,y,z))

                x-=d
                tr.append(Point3D(x,y,z))
            
                y += Ly
                tr.append(Point3D(x,y,z))

                x-=d
                tr.append(Point3D(x,y,z))

            y -= Ly
            tr.append(Point3D(x,y,z))   

            x-=d
            tr.append(Point3D(x,y,z))
            
            y += Ly
            tr.append(Point3D(x,y,z)) 
            return tr
    else:
        for i in range(0,int((ny-1)/2)):

            x += Lx
            tr.append(Point3D(x,y,z))

            y+=d
            tr.append(Point3D(x,y,z))
        
            x -= Lx
            tr.append(Point3D(x,y,z))

            y+=d
            tr.append(Point3D(x,y,z))
        x += Lx
        tr.append(Point3D(x,y,z))

        y+=d
        tr.append(Point3D(x,y,z))
    
        x -= Lx
        tr.append(Point3D(x,y,z))

        z+=dz

        tr.append(Point3D(x,y,z))
        if(nx%2==0):
            for i in range(0,int(nx/2)):

                y -= Ly
                tr.append(Point3D(x,y,z))

                x+=d
                tr.append(Point3D(x,y,z))
            
                y += Ly
                tr.append(Point3D(x,y,z))

                x+=d
                tr.append(Point3D(x,y,z))

            y -= Ly
            tr.append(Point3D(x,y,z))  
            return tr
        else:
            for i in range(0,int((nx-1)/2)):

                y -= Ly
                tr.append(Point3D(x,y,z))

                x+=d
                tr.append(Point3D(x,y,z))
            
                y += Ly
                tr.append(Point3D(x,y,z))

                x+=d
                tr.append(Point3D(x,y,z))

            y -= Ly
            tr.append(Point3D(x,y,z))  

            x+=d
            tr.append(Point3D(x,y,z))
            
            y += Ly
            tr.append(Point3D(x,y,z)) 
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

def generate_lines_x(n: int):
    ps = []
    for i in range(n+1):
        ps.append(Point3D(0, i / n, 0))
        ps.append(Point3D(1, i / n, 0))

    return ps

def parse_g_code_def(code:str)->"list[GCodeFrame]":
    p3ds = []
    lines = code.split("\n")

    x = 0 
    y = 0
    z = 0
    e = 0
    f = 0
    com_num = 3

    for line in lines:        
        print(line)
        com_num = 3
        coords = line.split()
        if len(coords)>0:
            if coords[0][0]=="G":
                com_num = int(coords[0][1:])
                
            if com_num ==0 or com_num == 1:   
                for coord in coords:
                    if coord[0]=="X":
                        x = float(coord[1:])
                    if coord[0]=="Y":
                        y = float(coord[1:])
                    if coord[0]=="Z":
                        z = float(coord[1:])
                    if coord[0]=="E":
                        e = float(coord[1:])
                    if coord[0]=="F":
                        f = float(coord[1:])
            
            if coords[0][0]=="G":    
                if com_num==0 or com_num==1:
                    #print(com_num)
                    p3ds.append(GCodeFrame(com_num,x,y,z,e,f))

    return p3ds

