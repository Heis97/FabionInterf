from enum import Enum
from path_planner.polygon import Point3D

class PrintSettings(object):
    name: str = ""
    F: float = 5
    diam: float = 0.4
    dz: float = 0.3
    ndoz: int = 0
    startE:float = 0
    diam_syr:float = 1.75
    v_vn:float = 1

    def __init__(self, name: str, F: float, diam: float, dz: float, ndoz: int,startE:float,diam_syr:float,v_vn:float) -> None:
        self.name: str = name
        self.F: float = F
        self.diam: float = diam
        self.dz: float = dz
        self.ndoz: int = ndoz# self.ndoz_fab_oct(ndoz)
        self.startE:float = startE
        self.diam_syr:float = diam_syr
        self.v_vn:float = v_vn

    def ndoz_fab_oct(self,doz:int):
        if doz==1:
             return 2
        elif doz==2:
             return 0
        else:
             return 1

class TrajectorySettings(object):
    nx: int = 2
    ny: int = 2
    d: float = 0.6
    dz: float = 0.3
    nz: int = 2
    start_xyz:Point3D

    perims:int = 0

    r_int: float = 0.6
    r_int_decr: float = 0.6
    k_e_ext: float = 0.6
    lin_retr: float = 0.6
    ang_int_r: float = 0.6
    
    def __init__(self,nx: int,ny: int,d: float,dz: float,nz: int,start_xyz:Point3D,r_int: float,r_int_decr,k_e_ext: float, lin_retr,ang_int_r: float ) -> None:
        self.nx: int = nx
        self.ny: int = ny
        self.d: float = d
        self.dz: float = dz
        self.nz: int = nz
        self.start_xyz:Point3D = start_xyz
        self.r_int: float = r_int
        self.r_int_decr: float = r_int_decr
        self.k_e_ext: float = k_e_ext
        self.lin_retr: float = lin_retr
        self.ang_int_r: float = ang_int_r 
            
class PrinterType(Enum):
    Fabion = 0
    Regemat = 1
