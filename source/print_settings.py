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
    def __init__(self, _name: str, _F: float, _diam: float, _dz: float, _ndoz: int,_startE:float,_diam_syr:float) -> None:
        self.name: str = _name
        self.F: float = _F
        self.diam: float = _diam
        self.dz: float = _dz
        self.ndoz: int = _ndoz
        self.startE:float = _startE
        self.diam_syr:float = _diam_syr

class TrajectorySettings(object):
    nx: int = 2
    ny: int = 2
    d: float = 0.6
    dz: float = 0.3
    nz: int = 2
    start_xyz:Point3D
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
