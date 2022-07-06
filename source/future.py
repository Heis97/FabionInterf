
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
