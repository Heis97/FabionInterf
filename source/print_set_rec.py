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
    def __init__(self, name: str, F: float, diam: float, dz: float, ndoz: int,startE:float,diam_syr:float) -> None:
        self.name: str = name
        self.F: float = F
        self.diam: float = diam
        self.dz: float = dz
        self.ndoz: int = self.ndoz_fab_oct(ndoz)
        self.startE:float = startE
        self.diam_syr:float = diam_syr

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
    def __init__(self,nx: int,ny: int,d: float,dz: float,nz: int,start_xyz:Point3D) -> None:
        self.nx: int = nx
        self.ny: int = ny
        self.d: float = d
        self.dz: float = dz
        self.nz: int = nz
        self.start_xyz:Point3D = start_xyz
        
class PrinterType(Enum):
    Fabion = 0
    Regemat = 1
