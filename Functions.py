import numpy as np
import datetime
from tqdm import tqdm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_3d_walk(Cx,Cy,Cz, target_window):
    """
    Plots the 3D walk using matplotlib.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(Cx)):
        ax.plot(Cx[i], Cy[i], Cz[i], 'b-o', linewidth=1, markersize=4)
        ax.plot(Cx[i][0], Cy[i][0], Cz[i][0], 'go', markersize=4, label='Start') # Start point
        ax.plot(Cx[i][-1], Cy[i][-1], Cz[i][-1], 'ro', markersize=4, label='End') # End point
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    #ax.legend()
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=target_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def Pivot_Chain(xx,yy,zz,pivot_point,pp,length):
    x={};y={};z={}
    for i in range(1,48):
        x[i]=np.copy(xx);y[i]=np.copy(yy);z[i]=np.copy(zz)
    #reflection on axis y
    x[1][pp:length]=pivot_point[0]-(np.copy(xx)[pp:length]-pivot_point[0])
    #reflection on axis x
    y[2][pp:length]=pivot_point[1]-(np.copy(yy)[pp:length]-pivot_point[1])
    # reflection on axis z
    z[3][pp:length]=pivot_point[2]-(np.copy(zz)[pp:length]-pivot_point[2])
    #reflection on plane y=x
    x[4][pp:length]=pivot_point[0]+(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[4][pp:length]=pivot_point[1]+(np.copy(xx)[pp:length]-pivot_point[0]) 
    #reflection on plane y=-x
    x[5][pp:length]=pivot_point[0]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[5][pp:length]=pivot_point[1]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    #reflection on plane y=z
    y[6][pp:length]=pivot_point[1]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[6][pp:length]=pivot_point[2]+(np.copy(yy)[pp:length]-pivot_point[1])
    #reflection on plane y=-z
    y[7][pp:length]=pivot_point[1]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[7][pp:length]=pivot_point[2]-(np.copy(yy)[pp:length]-pivot_point[1])
    #reflection on plane x=z
    x[8][pp:length]=pivot_point[0]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[8][pp:length]=pivot_point[2]+(np.copy(xx)[pp:length]-pivot_point[0])
    #reflection on plane x=-z
    x[9][pp:length]=pivot_point[0]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[9][pp:length]=pivot_point[2]-(np.copy(xx)[pp:length]-pivot_point[0])
    # rotation 90 arround axis z
    x[10][pp:length]=pivot_point[0]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[10][pp:length]=pivot_point[1]+(np.copy(xx)[pp:length]-pivot_point[0]) 
    # rotation 180 arround axis z
    x[11][pp:length]=pivot_point[0]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    y[11][pp:length]=pivot_point[1]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    # rotation 270 arround axis z
    x[12][pp:length]=pivot_point[0]+(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[12][pp:length]=pivot_point[1]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    # rotation 90 arround axis x
    y[13][pp:length]=pivot_point[1]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[13][pp:length]=pivot_point[2]-(np.copy(yy)[pp:length]-pivot_point[1])    
    #rotation 180 arround axis x
    y[14][pp:length]=pivot_point[1]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    z[14][pp:length]=pivot_point[2]-(np.copy(zz)[pp:length]-pivot_point[2])    
    #rotation 270 arround axis x
    y[15][pp:length]=pivot_point[1]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[15][pp:length]=pivot_point[2]+(np.copy(yy)[pp:length]-pivot_point[1])   
    #rotation 90 arround axis y
    x[16][pp:length]=pivot_point[0]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[16][pp:length]=pivot_point[2]-(np.copy(xx)[pp:length]-pivot_point[0])   
    #rotation 180 arround axis y
    x[17][pp:length]=pivot_point[0]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[17][pp:length]=pivot_point[2]-(np.copy(zz)[pp:length]-pivot_point[2])    
    #/rotation 270 arround axis y
    x[18][pp:length]=pivot_point[0]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[18][pp:length]=pivot_point[2]+(np.copy(xx)[pp:length]-pivot_point[0])
    #rotation 120 arround diagonals
    x[19][pp:length]=pivot_point[0]+(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[19][pp:length]=pivot_point[1]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[19][pp:length]=pivot_point[2]+(np.copy(xx)[pp:length]-pivot_point[0])    

    x[20][pp:length]=pivot_point[0]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[20][pp:length]=pivot_point[1]+(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[20][pp:length]=pivot_point[2]-(np.copy(yy)[pp:length]-pivot_point[1])   

    x[21][pp:length]=pivot_point[0]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[21][pp:length]=pivot_point[1]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[21][pp:length]=pivot_point[2]+(np.copy(yy)[pp:length]-pivot_point[1])   

    x[22][pp:length]=pivot_point[0]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[22][pp:length]=pivot_point[1]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[22][pp:length]=pivot_point[2]-(np.copy(yy)[pp:length]-pivot_point[1])    

    #rotation 240 arround diagonals
    x[23][pp:length]=pivot_point[0]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[23][pp:length]=pivot_point[1]+(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[23][pp:length]=pivot_point[2]+(np.copy(yy)[pp:length]-pivot_point[1])   

    x[24][pp:length]=pivot_point[0]+(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[24][pp:length]=pivot_point[1]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[24][pp:length]=pivot_point[2]-(np.copy(xx)[pp:length]-pivot_point[0]) 

    x[25][pp:length]=pivot_point[0]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[25][pp:length]=pivot_point[1]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[25][pp:length]=pivot_point[2]-(np.copy(xx)[pp:length]-pivot_point[0])   

    x[26][pp:length]=pivot_point[0]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[26][pp:length]=pivot_point[1]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[26][pp:length]=pivot_point[2]+(np.copy(xx)[pp:length]-pivot_point[0])
    #ratation 180 arround axises that connect the centers of opposite planes
    x[27][pp:length]=pivot_point[0]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[27][pp:length]=pivot_point[1]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    z[27][pp:length]=pivot_point[2]+(np.copy(xx)[pp:length]-pivot_point[0])   

    x[28][pp:length]=pivot_point[0]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[28][pp:length]=pivot_point[1]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    z[28][pp:length]=pivot_point[2]-(np.copy(xx)[pp:length]-pivot_point[0])   

    x[29][pp:length]=pivot_point[0]+(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[29][pp:length]=pivot_point[1]+(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[29][pp:length]=pivot_point[2]-(np.copy(zz)[pp:length]-pivot_point[2])   

    x[30][pp:length]=pivot_point[0]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    y[30][pp:length]=pivot_point[1]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[30][pp:length]=pivot_point[2]+(np.copy(yy)[pp:length]-pivot_point[1])   

    x[31][pp:length]=pivot_point[0]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    y[31][pp:length]=pivot_point[1]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[31][pp:length]=pivot_point[2]-(np.copy(yy)[pp:length]-pivot_point[1])   

    x[32][pp:length]=pivot_point[0]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[32][pp:length]=pivot_point[1]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[32][pp:length]=pivot_point[2]-(np.copy(zz)[pp:length]-pivot_point[2])  
    # rotation 120 arround diagonals + invertion
    x[33][pp:length]=pivot_point[0]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[33][pp:length]=pivot_point[1]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[33][pp:length]=pivot_point[2]-(np.copy(xx)[pp:length]-pivot_point[0])  

    x[34][pp:length]=pivot_point[0]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[34][pp:length]=pivot_point[1]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[34][pp:length]=pivot_point[2]+(np.copy(yy)[pp:length]-pivot_point[1])   

    x[35][pp:length]=pivot_point[0]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[35][pp:length]=pivot_point[1]+(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[35][pp:length]=pivot_point[2]-(np.copy(yy)[pp:length]-pivot_point[1])   

    x[36][pp:length]=pivot_point[0]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[36][pp:length]=pivot_point[1]+(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[36][pp:length]=pivot_point[2]+(np.copy(yy)[pp:length]-pivot_point[1])   

    # rotation 240 arround diagonals + invertion
    x[37][pp:length]=pivot_point[0]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[37][pp:length]=pivot_point[1]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[37][pp:length]=pivot_point[2]-(np.copy(yy)[pp:length]-pivot_point[1])    

    x[38][pp:length]=pivot_point[0]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[38][pp:length]=pivot_point[1]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[38][pp:length]=pivot_point[2]+(np.copy(xx)[pp:length]-pivot_point[0])   

    x[39][pp:length]=pivot_point[0]+(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[39][pp:length]=pivot_point[1]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[39][pp:length]=pivot_point[2]+(np.copy(xx)[pp:length]-pivot_point[0])   

    x[40][pp:length]=pivot_point[0]+(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[40][pp:length]=pivot_point[1]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[40][pp:length]=pivot_point[2]-(np.copy(xx)[pp:length]-pivot_point[0])   
    # rotation 90 arround axis z + invertion
    x[41][pp:length]=pivot_point[0]+(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[41][pp:length]=pivot_point[1]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[41][pp:length]=pivot_point[2]-(z[41][pp:length]-pivot_point[2])   
    # rotation 270 arround axis z + invertion
    x[42][pp:length]=pivot_point[0]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    y[42][pp:length]=pivot_point[1]+(np.copy(xx)[pp:length]-pivot_point[0]) 
    z[42][pp:length]=pivot_point[2]-(np.copy(zz)[pp:length]-pivot_point[2])  
    # rotation 90 arround axis x + invertion
    x[43][pp:length]=pivot_point[0]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    y[43][pp:length]=pivot_point[1]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[43][pp:length]=pivot_point[2]+(np.copy(yy)[pp:length]-pivot_point[1])    
    # rotation 270 arround axis x + invertion
    x[44][pp:length]=pivot_point[0]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    y[44][pp:length]=pivot_point[1]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    z[44][pp:length]=pivot_point[2]-(np.copy(yy)[pp:length]-pivot_point[1])  
    # rotation 90 arround axis  y   + invertion                                                                                            
    x[45][pp:length]=pivot_point[0]+(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[45][pp:length]=pivot_point[1]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    z[45][pp:length]=pivot_point[2]+(np.copy(xx)[pp:length]-pivot_point[0])  
    # rotation 270 arround axis y  + invertion
    x[46][pp:length]=pivot_point[0]-(np.copy(zz)[pp:length]-pivot_point[2]) 
    y[46][pp:length]=pivot_point[1]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    z[46][pp:length]=pivot_point[2]-(np.copy(xx)[pp:length]-pivot_point[0])   
    # reflection on the invertion center
    x[47][pp:length]=pivot_point[0]-(np.copy(xx)[pp:length]-pivot_point[0]) 
    y[47][pp:length]=pivot_point[1]-(np.copy(yy)[pp:length]-pivot_point[1]) 
    z[47][pp:length]=pivot_point[2]-(np.copy(zz)[pp:length]-pivot_point[2]) 

    return (x,y,z)

def Pivot_Ring(xx,yy,zz,pivot_point,pp,N, pivot_point2):
    x={};y={};z={}
    for i in range(1,48):
        x[i]=np.copy(xx);y[i]=np.copy(yy);z[i]=np.copy(zz)
    #reflection on axis y
    for i in range(N):
        if xx[i]==pivot_point[0]:
            pivot_point2[1]=i
            if i != pp:
                break
    if pivot_point2[1]>pp:
        x[1][pp:pivot_point2[1]+1]=pivot_point[0]-(np.copy(xx)[pp:pivot_point2[1]+1]-pivot_point[0])
    else:
        x[1][pivot_point2[1]:pp+1]=pivot_point[0]-(np.copy(xx)[pivot_point2[1]:pp+1]-pivot_point[0])
    #reflection on axis x
    for i in range(N):
        if yy[i]==pivot_point[1]:
            pivot_point2[2]=i
            if i != pp:
                break
    if pivot_point2[2]>pp:
        y[2][pp:pivot_point2[1]+1]=pivot_point[1]-(np.copy(yy)[pp:pivot_point2[2]+1]-pivot_point[1])
    else:
        y[2][pivot_point2[1]:pp+1]=pivot_point[1]-(np.copy(yy)[pivot_point2[2]:pp+1]-pivot_point[1])
    # reflection on axis z
    for i in range(N):
        if zz[i]==pivot_point[2]:
            pivot_point2[3]=i
            if i != pp:
                break
    if pivot_point2[3]>pp:
        z[3][pp:pivot_point2[3]+1]=pivot_point[2]-(np.copy(zz)[pp:pivot_point2[3]+1]-pivot_point[2])
    else:
        z[3][pivot_point2[3]:pp+1]=pivot_point[2]-(np.copy(zz)[pivot_point2[3]:pp+1]-pivot_point[2])
    #reflection on plane y=x
    for i in range(N):
        if yy[i]==xx[i]+pivot_point[1]-pivot_point[0]:
            pivot_point2[4]=i
            if i != pp:
                break
    if pivot_point2[4]>pp:
        x[4][pp:pivot_point2[4]+1]=pivot_point[0]+(np.copy(yy)[pp:pivot_point2[4]+1]-pivot_point[1]) 
        y[4][pp:pivot_point2[4]+1]=pivot_point[1]+(np.copy(xx)[pp:pivot_point2[4]+1]-pivot_point[0]) 
    else:
        x[4][pivot_point2[4]:pp+1]=pivot_point[0]+(np.copy(yy)[pivot_point2[4]:pp+1]-pivot_point[1]) 
        y[4][pivot_point2[4]:pp+1]=pivot_point[1]+(np.copy(xx)[pivot_point2[4]:pp+1]-pivot_point[0]) 
    #reflection on plane y=-x
    for i in range(N):
        if yy[i]==pivot_point[1]+pivot_point[0]-xx[i]:
            pivot_point2[5]=i
            if i != pp:
                break
    if pivot_point2[5]>pp:
        x[5][pp:pivot_point2[5]+1]=pivot_point[0]-(np.copy(yy)[pp:pivot_point2[5]+1]-pivot_point[1]) 
        y[5][pp:pivot_point2[5]+1]=pivot_point[1]-(np.copy(xx)[pp:pivot_point2[5]+1]-pivot_point[0]) 
    else:
        x[5][pivot_point2[5]:pp+1]=pivot_point[0]-(np.copy(yy)[pivot_point2[5]:pp+1]-pivot_point[1]) 
        y[5][pivot_point2[5]:pp+1]=pivot_point[1]-(np.copy(xx)[pivot_point2[5]:pp+1]-pivot_point[0]) 
    #reflection on plane y=z
    for i in range(N):
        if yy[i]==zz[i]+pivot_point[1]-pivot_point[2]:
            pivot_point2[6]=i
            if i != pp:
                break
    if pivot_point2[6]>pp:
        y[6][pp:pivot_point2[6]+1]=pivot_point[1]+(np.copy(zz)[pp:pivot_point2[6]+1]-pivot_point[2]) 
        z[6][pp:pivot_point2[6]+1]=pivot_point[2]+(np.copy(yy)[pp:pivot_point2[6]+1]-pivot_point[1])
    else:
        y[6][pivot_point2[6]:pp+1]=pivot_point[1]+(np.copy(zz)[pivot_point2[6]:pp+1]-pivot_point[2]) 
        z[6][pivot_point2[6]:pp+1]=pivot_point[2]+(np.copy(yy)[pivot_point2[6]:pp+1]-pivot_point[1])
    #reflection on plane y=-z
    for i in range(N):
        if yy[i]==+pivot_point[1]+pivot_point[2]-zz[i]:
            pivot_point2[7]=i
            if i != pp:
                break
    if pivot_point2[7]>pp:
        y[7][pp:pivot_point2[7]+1]=pivot_point[1]-(np.copy(zz)[pp:pivot_point2[7]+1]-pivot_point[2]) 
        z[7][pp:pivot_point2[7]+1]=pivot_point[2]-(np.copy(yy)[pp:pivot_point2[7]+1]-pivot_point[1])
    else:
        y[7][pivot_point2[7]:pp+1]=pivot_point[1]-(np.copy(zz)[pivot_point2[7]:pp+1]-pivot_point[2]) 
        z[7][pivot_point2[7]:pp+1]=pivot_point[2]-(np.copy(yy)[pivot_point2[7]:pp+1]-pivot_point[1])
    #reflection on plane x=z
    for i in range(N):
        if xx[i]==zz[i]+pivot_point[0]-pivot_point[2]:
            pivot_point2[8]=i
            if i != pp:
                break
    if pivot_point2[8]>pp:
        x[8][pp:pivot_point2[8]+1]=pivot_point[0]+(np.copy(zz)[pp:pivot_point2[8]+1]-pivot_point[2]) 
        z[8][pp:pivot_point2[8]+1]=pivot_point[2]+(np.copy(xx)[pp:pivot_point2[8]+1]-pivot_point[0])
    else:
        x[8][pivot_point2[8]:pp+1]=pivot_point[0]+(np.copy(zz)[pivot_point2[8]:pp+1]-pivot_point[2]) 
        z[8][pivot_point2[8]:pp+1]=pivot_point[2]+(np.copy(xx)[pivot_point2[8]:pp+1]-pivot_point[0])
    #reflection on plane x=-z
    for i in range(N):
        if xx[i]==pivot_point[0]+pivot_point[2]-zz[i]:
            pivot_point2[9]=i
            if i != pp:
                break
    if pivot_point2[9]>pp:
        x[9][pp:pivot_point2[9]+1]=pivot_point[0]-(np.copy(zz)[pp:pivot_point2[9]+1]-pivot_point[2]) 
        z[9][pp:pivot_point2[9]+1]=pivot_point[2]-(np.copy(xx)[pp:pivot_point2[9]+1]-pivot_point[0])
    else:
        x[9][pivot_point2[9]:pp+1]=pivot_point[0]-(np.copy(zz)[pivot_point2[9]:pp+1]-pivot_point[2]) 
        z[9][pivot_point2[9]:pp+1]=pivot_point[2]-(np.copy(xx)[pivot_point2[9]:pp+1]-pivot_point[0])
    # rotation 90 arround axis z
    for i in range(N):
        if xx[i]==pivot_point[0] and yy[i]==pivot_point[1]:
            pivot_point2[10]=i
            if i != pp:
                break
    if pivot_point2[10]>pp:
        x[10][pp:pivot_point2[10]+1]=pivot_point[0]-(np.copy(yy)[pp:pivot_point2[10]+1]-pivot_point[1]) 
        y[10][pp:pivot_point2[10]+1]=pivot_point[1]+(np.copy(xx)[pp:pivot_point2[10]+1]-pivot_point[0]) 
    else:
        x[10][pivot_point2[10]:pp+1]=pivot_point[0]-(np.copy(yy)[pivot_point2[10]:pp+1]-pivot_point[1]) 
        y[10][pivot_point2[10]:pp+1]=pivot_point[1]+(np.copy(xx)[pivot_point2[10]:pp+1]-pivot_point[0]) 
    # rotation 180 arround axis z
    for i in range(N):
        if xx[i]==pivot_point[0] and yy[i]==pivot_point[1]:
            pivot_point2[11]=i
            if i != pp:
                break
    if pivot_point2[11]>pp:
        x[11][pp:pivot_point2[11]+1]=pivot_point[0]-(np.copy(xx)[pp:pivot_point2[11]+1]-pivot_point[0]) 
        y[11][pp:pivot_point2[11]+1]=pivot_point[1]-(np.copy(yy)[pp:pivot_point2[11]+1]-pivot_point[1]) 
    else:
        x[11][pp:pivot_point2[11]+1]=pivot_point[0]-(np.copy(xx)[pp:pivot_point2[11]+1]-pivot_point[0]) 
        y[11][pp:pivot_point2[11]+1]=pivot_point[1]-(np.copy(yy)[pp:pivot_point2[11]+1]-pivot_point[1])
    # rotation 270 arround axis z
    for i in range(N):
        if xx[i]==pivot_point[0] and yy[i]==pivot_point[1]:
            pivot_point2[12]=i
            if i != pp:
                break
    if pivot_point2[12]>pp:
        x[12][pp:pivot_point2[12]+1]=pivot_point[0]+(np.copy(yy)[pp:pivot_point2[12]+1]-pivot_point[1]) 
        y[12][pp:pivot_point2[12]+1]=pivot_point[1]-(np.copy(xx)[pp:pivot_point2[12]+1]-pivot_point[0]) 
    else:
        x[12][pivot_point2[12]:pp+1]=pivot_point[0]+(np.copy(yy)[pivot_point2[12]:pp+1]-pivot_point[1]) 
        y[12][pivot_point2[12]:pp+1]=pivot_point[1]-(np.copy(xx)[pivot_point2[12]:pp+1]-pivot_point[0]) 
    # rotation 90 arround axis x
    for i in range(N):
        if zz[i]==pivot_point[2] and yy[i]==pivot_point[1]:
            pivot_point2[13]=i
            if i != pp:
                break
    if pivot_point2[13]>pp:
        y[13][pp:pivot_point2[13]+1]=pivot_point[1]+(np.copy(zz)[pp:pivot_point2[13]+1]-pivot_point[2]) 
        z[13][pp:pivot_point2[13]+1]=pivot_point[2]-(np.copy(yy)[pp:pivot_point2[13]+1]-pivot_point[1])
    else:
        y[13][pivot_point2[13]:pp+1]=pivot_point[1]+(np.copy(zz)[pivot_point2[13]:pp+1]-pivot_point[2]) 
        z[13][pivot_point2[13]:pp+1]=pivot_point[2]-(np.copy(yy)[pivot_point2[13]:pp+1]-pivot_point[1])
    #rotation 180 arround axis x
    for i in range(N):
        if zz[i]==pivot_point[2] and yy[i]==pivot_point[1]:
            pivot_point2[14]=i
            if i != pp:
                break
    if pivot_point2[14]>pp:
        y[14][pp:pivot_point2[14]+1]=pivot_point[1]-(np.copy(yy)[pp:pivot_point2[14]+1]-pivot_point[1]) 
        z[14][pp:pivot_point2[14]+1]=pivot_point[2]-(np.copy(zz)[pp:pivot_point2[14]+1]-pivot_point[2])    
    else:
        y[14][pivot_point2[14]:pp+1]=pivot_point[1]-(np.copy(yy)[pivot_point2[14]:pp+1]-pivot_point[1]) 
        z[14][pivot_point2[14]:pp+1]=pivot_point[2]-(np.copy(zz)[pivot_point2[14]:pp+1]-pivot_point[2])
    #rotation 270 arround axis x
    for i in range(N):
        if zz[i]==pivot_point[2] and yy[i]==pivot_point[1]:
            pivot_point2[15]=i
            if i != pp:
                break
    if pivot_point2[15]>pp:
        y[15][pp:pivot_point2[15]+1]=pivot_point[1]-(np.copy(zz)[pp:pivot_point2[15]+1]-pivot_point[2]) 
        z[15][pp:pivot_point2[15]+1]=pivot_point[2]+(np.copy(yy)[pp:pivot_point2[15]+1]-pivot_point[1])   
    else:
        y[15][pivot_point2[15]:pp+1]=pivot_point[1]-(np.copy(zz)[pivot_point2[15]:pp+1]-pivot_point[2]) 
        z[15][pivot_point2[15]:pp+1]=pivot_point[2]+(np.copy(yy)[pivot_point2[15]:pp+1]-pivot_point[1])
    #rotation 90 arround axis y
    for i in range(N):
        if zz[i]==pivot_point[2] and xx[i]==pivot_point[0]:
            pivot_point2[16]=i
            if i != pp:
                break
    if pivot_point2[16]>pp:
        x[16][pp:pivot_point2[16]+1]=pivot_point[0]-(np.copy(zz)[pp:pivot_point2[16]+1]-pivot_point[2]) 
        z[16][pp:pivot_point2[16]+1]=pivot_point[2]-(np.copy(xx)[pp:pivot_point2[16]+1]-pivot_point[0])   
    else:
        x[16][pivot_point2[16]:pp+1]=pivot_point[0]-(np.copy(zz)[pivot_point2[16]:pp+1]-pivot_point[2]) 
        z[16][pivot_point2[16]:pp+1]=pivot_point[2]-(np.copy(xx)[pivot_point2[16]:pp+1]-pivot_point[0])  
    #rotation 180 arround axis y
    for i in range(N):
        if zz[i]==pivot_point[2] and xx[i]==pivot_point[0]:
            pivot_point2[17]=i
            if i != pp:
                break
    if pivot_point2[17]>pp:
        x[17][pp:pivot_point2[17]+1]=pivot_point[0]-(np.copy(xx)[pp:pivot_point2[17]+1]-pivot_point[0]) 
        z[17][pp:pivot_point2[17]+1]=pivot_point[2]-(np.copy(zz)[pp:pivot_point2[17]+1]-pivot_point[2])    
    else:
        x[17][pivot_point2[17]:pp+1]=pivot_point[0]-(np.copy(xx)[pivot_point2[17]:pp+1]-pivot_point[0]) 
        z[17][pivot_point2[17]:pp+1]=pivot_point[2]-(np.copy(zz)[pivot_point2[17]:pp+1]-pivot_point[2])
    #/rotation 270 arround axis y
    for i in range(N):
        if zz[i]==pivot_point[2] and xx[i]==pivot_point[0]:
            pivot_point2[18]=i
            if i != pp:
                break
    if pivot_point2[18]>pp:
        x[18][pp:pivot_point2[18]+1]=pivot_point[0]+(np.copy(zz)[pp:pivot_point2[18]+1]-pivot_point[2]) 
        z[18][pp:pivot_point2[18]+1]=pivot_point[2]+(np.copy(xx)[pp:pivot_point2[18]+1]-pivot_point[0])
    else:
        x[18][pivot_point2[18]:pp+1]=pivot_point[0]+(np.copy(zz)[pivot_point2[18]:pp+1]-pivot_point[2]) 
        z[18][pivot_point2[18]:pp+1]=pivot_point[2]+(np.copy(xx)[pivot_point2[18]:pp+1]-pivot_point[0])
    #rotation 120 arround diagonals
    for i in range(N):
        if 2*zz[i]==2*pivot_point[2]+(yy[i]-pivot_point[1]+xx[i]-pivot_point[0]) and  yy[i]==pivot_point[1]+xx[i]-pivot_point[0]:
            pivot_point2[19]=i
            if i != pp:
                break
    if pivot_point2[19]>pp:
        x[19][pp:pivot_point2[19]+1]=pivot_point[0]+(np.copy(yy)[pp:pivot_point2[19]+1]-pivot_point[1]) 
        y[19][pp:pivot_point2[19]+1]=pivot_point[1]+(np.copy(zz)[pp:pivot_point2[19]+1]-pivot_point[2]) 
        z[19][pp:pivot_point2[19]+1]=pivot_point[2]+(np.copy(xx)[pp:pivot_point2[19]+1]-pivot_point[0])    
    else:
        x[19][pivot_point2[19]:pp+1]=pivot_point[0]+(np.copy(yy)[pivot_point2[19]:pp+1]-pivot_point[1]) 
        y[19][pivot_point2[19]:pp+1]=pivot_point[1]+(np.copy(zz)[pivot_point2[19]:pp+1]-pivot_point[2]) 
        z[19][pivot_point2[19]:pp+1]=pivot_point[2]+(np.copy(xx)[pivot_point2[19]:pp+1]-pivot_point[0])
    for i in range(N):
        if 2*zz[i]==2*pivot_point[2]-(yy[i]-pivot_point[1]+xx[i]-pivot_point[0]) and  yy[i]==pivot_point[1]+xx[i]-pivot_point[0]:
            pivot_point2[20]=i
            if i != pp:
                break
    if pivot_point2[20]>pp:
        x[20][pp:pivot_point2[20]+1]=pivot_point[0]-(np.copy(zz)[pp:pivot_point2[20]+1]-pivot_point[2]) 
        y[20][pp:pivot_point2[20]+1]=pivot_point[1]+(np.copy(xx)[pp:pivot_point2[20]+1]-pivot_point[0]) 
        z[20][pp:pivot_point2[20]+1]=pivot_point[2]-(np.copy(yy)[pp:pivot_point2[20]+1]-pivot_point[1])   
    else:
        x[20][pivot_point2[20]:pp+1]=pivot_point[0]-(np.copy(zz)[pivot_point2[20]:pp+1]-pivot_point[2]) 
        y[20][pivot_point2[20]:pp+1]=pivot_point[1]+(np.copy(xx)[pivot_point2[20]:pp+1]-pivot_point[0]) 
        z[20][pivot_point2[20]:pp+1]=pivot_point[2]-(np.copy(yy)[pivot_point2[20]:pp+1]-pivot_point[1])
    for i in range(N):
        if 2*zz[i]==2*pivot_point[2]+(yy[i]-pivot_point[1]-xx[i]+pivot_point[0]) and  yy[i]==pivot_point[1]-xx[i]+pivot_point[0]:
            pivot_point2[21]=i
            if i != pp:
                break
    if pivot_point2[21]>pp:
        x[21][pp:pivot_point2[21]+1]=pivot_point[0]-(np.copy(zz)[pp:pivot_point2[21]+1]-pivot_point[2]) 
        y[21][pp:pivot_point2[21]+1]=pivot_point[1]-(np.copy(xx)[pp:pivot_point2[21]+1]-pivot_point[0]) 
        z[21][pp:pivot_point2[21]+1]=pivot_point[2]+(np.copy(yy)[pp:pivot_point2[21]+1]-pivot_point[1])
    else:
        x[21][pivot_point2[21]:pp+1]=pivot_point[0]-(np.copy(zz)[pivot_point2[21]:pp+1]-pivot_point[2]) 
        y[21][pivot_point2[21]:pp+1]=pivot_point[1]-(np.copy(xx)[pivot_point2[21]:pp+1]-pivot_point[0]) 
        z[21][pivot_point2[21]:pp+1]=pivot_point[2]+(np.copy(yy)[pivot_point2[21]:pp+1]-pivot_point[1])
    for i in range(N):
        if 2*zz[i]==2*pivot_point[2]+(-yy[i]+pivot_point[1]+xx[i]-pivot_point[0]) and  yy[i]==pivot_point[1]-xx[i]+pivot_point[0]:
            pivot_point2[22]=i
            if i != pp:
                break
    if pivot_point2[22]>pp:
        x[22][pp:pivot_point2[22]+1]=pivot_point[0]+(np.copy(zz)[pp:pivot_point2[22]+1]-pivot_point[2]) 
        y[22][pp:pivot_point2[22]+1]=pivot_point[1]-(np.copy(xx)[pp:pivot_point2[22]+1]-pivot_point[0]) 
        z[22][pp:pivot_point2[22]+1]=pivot_point[2]-(np.copy(yy)[pp:pivot_point2[22]+1]-pivot_point[1])    
    else:
        x[22][pivot_point2[22]:pp+1]=pivot_point[0]+(np.copy(zz)[pivot_point2[22]:pp+1]-pivot_point[2]) 
        y[22][pivot_point2[22]:pp+1]=pivot_point[1]-(np.copy(xx)[pivot_point2[22]:pp+1]-pivot_point[0]) 
        z[22][pivot_point2[22]:pp+1]=pivot_point[2]-(np.copy(yy)[pivot_point2[22]:pp+1]-pivot_point[1])
    #rotation 240 arround diagonals
    for i in range(N):
        if 2*zz[i]==2*pivot_point[2]+(yy[i]-pivot_point[1]+xx[i]-pivot_point[0]) and  yy[i]==pivot_point[1]+xx[i]-pivot_point[0]:
            pivot_point2[23]=i
            if i != pp:
                break
    if pivot_point2[23]>pp:
        x[23][pp:pivot_point2[23]+1]=pivot_point[0]+(np.copy(zz)[pp:pivot_point2[23]+1]-pivot_point[2]) 
        y[23][pp:pivot_point2[23]+1]=pivot_point[1]+(np.copy(xx)[pp:pivot_point2[23]+1]-pivot_point[0]) 
        z[23][pp:pivot_point2[23]+1]=pivot_point[2]+(np.copy(yy)[pp:pivot_point2[23]+1]-pivot_point[1])
    else:
        x[23][pivot_point2[23]:pp+1]=pivot_point[0]+(np.copy(zz)[pivot_point2[23]:pp+1]-pivot_point[2]) 
        y[23][pivot_point2[23]:pp+1]=pivot_point[1]+(np.copy(xx)[pivot_point2[23]:pp+1]-pivot_point[0]) 
        z[23][pivot_point2[23]:pp+1]=pivot_point[2]+(np.copy(yy)[pivot_point2[23]:pp+1]-pivot_point[1])
    for i in range(N):
        if 2*zz[i]==2*pivot_point[2]-(yy[i]-pivot_point[1]+xx[i]-pivot_point[0]) and  yy[i]==pivot_point[1]+xx[i]-pivot_point[0]:
            pivot_point2[24]=i
            if i != pp:
                break
    if pivot_point2[24]>pp:  
        x[24][pp:pivot_point2[24]+1]=pivot_point[0]+(np.copy(yy)[pp:pivot_point2[24]+1]-pivot_point[1]) 
        y[24][pp:pivot_point2[24]+1]=pivot_point[1]-(np.copy(zz)[pp:pivot_point2[24]+1]-pivot_point[2]) 
        z[24][pp:pivot_point2[24]+1]=pivot_point[2]-(np.copy(xx)[pp:pivot_point2[24]+1]-pivot_point[0])
    else:
        x[24][pivot_point2[24]:pp+1]=pivot_point[0]+(np.copy(yy)[pivot_point2[24]:pp+1]-pivot_point[1]) 
        y[24][pivot_point2[24]:pp+1]=pivot_point[1]-(np.copy(zz)[pivot_point2[24]:pp+1]-pivot_point[2]) 
        z[24][pivot_point2[24]:pp+1]=pivot_point[2]-(np.copy(xx)[pivot_point2[24]:pp+1]-pivot_point[0])
    for i in range(N):
        if 2*zz[i]==2*pivot_point[2]+(yy[i]-pivot_point[1]-xx[i]+pivot_point[0]) and  yy[i]==pivot_point[1]-xx[i]+pivot_point[0]:
            pivot_point2[25]=i
            if i != pp:
                break
    if pivot_point2[25]>pp:
        x[25][pp:pivot_point2[25]+1]=pivot_point[0]-(np.copy(yy)[pp:pivot_point2[25]+1]-pivot_point[1]) 
        y[25][pp:pivot_point2[25]+1]=pivot_point[1]+(np.copy(zz)[pp:pivot_point2[25]+1]-pivot_point[2]) 
        z[25][pp:pivot_point2[25]+1]=pivot_point[2]-(np.copy(xx)[pp:pivot_point2[25]+1]-pivot_point[0])   
    else:
        x[25][pivot_point2[25]:pp+1]=pivot_point[0]-(np.copy(yy)[pivot_point2[25]:pp+1]-pivot_point[1]) 
        y[25][pivot_point2[25]:pp+1]=pivot_point[1]+(np.copy(zz)[pivot_point2[25]:pp+1]-pivot_point[2]) 
        z[25][pivot_point2[25]:pp+1]=pivot_point[2]-(np.copy(xx)[pivot_point2[25]:pp+1]-pivot_point[0])
    for i in range(N):
        if 2*zz[i]==2*pivot_point[2]+(-yy[i]+pivot_point[1]+xx[i]-pivot_point[0]) and  yy[i]==pivot_point[1]-xx[i]+pivot_point[0]:
            pivot_point2[26]=i
            if i != pp:
                break
    if pivot_point2[26]>pp:
        x[26][pp:pivot_point2[26]+1]=pivot_point[0]-(np.copy(yy)[pp:pivot_point2[26]+1]-pivot_point[1]) 
        y[26][pp:pivot_point2[26]+1]=pivot_point[1]-(np.copy(zz)[pp:pivot_point2[26]+1]-pivot_point[2]) 
        z[26][pp:pivot_point2[26]+1]=pivot_point[2]+(np.copy(xx)[pp:pivot_point2[26]+1]-pivot_point[0])  
    else:
        x[26][pivot_point2[26]:pp+1]=pivot_point[0]-(np.copy(yy)[pivot_point2[26]:pp+1]-pivot_point[1]) 
        y[26][pivot_point2[26]:pp+1]=pivot_point[1]-(np.copy(zz)[pivot_point2[26]:pp+1]-pivot_point[2]) 
        z[26][pivot_point2[26]:pp+1]=pivot_point[2]+(np.copy(xx)[pivot_point2[26]:pp+1]-pivot_point[0]) 
    #ratation 180 arround axises that connect the centers of opposite planes
    for i in range(N):
        if xx[i]==zz[i]+pivot_point[0]-pivot_point[2] and yy[i]==pivot_point[1]:
            pivot_point2[27]=i
            if i != pp:
                break
    if pivot_point2[27]>pp:
        x[27][pp:pivot_point2[27]+1]=pivot_point[0]-(np.copy(zz)[pp:pivot_point2[27]+1]-pivot_point[2]) 
        y[27][pp:pivot_point2[27]+1]=pivot_point[1]-(np.copy(yy)[pp:pivot_point2[27]+1]-pivot_point[1]) 
        z[27][pp:pivot_point2[27]+1]=pivot_point[2]+(np.copy(xx)[pp:pivot_point2[27]+1]-pivot_point[0])   
    else:
        x[27][pivot_point2[27]:pp+1]=pivot_point[0]-(np.copy(zz)[pivot_point2[27]:pp+1]-pivot_point[2]) 
        y[27][pivot_point2[27]:pp+1]=pivot_point[1]-(np.copy(yy)[pivot_point2[27]:pp+1]-pivot_point[1]) 
        z[27][pivot_point2[27]:pp+1]=pivot_point[2]+(np.copy(xx)[pivot_point2[27]:pp+1]-pivot_point[0])
    for i in range(N):
        if xx[i]==+pivot_point[0]+pivot_point[2]-zz[i] and yy[i]==pivot_point[1]:
            pivot_point2[28]=i
            if i != pp:
                break
    if pivot_point2[28]>pp: 
        x[28][pp:pivot_point2[28]+1]=pivot_point[0]-(np.copy(zz)[pp:pivot_point2[28]+1]-pivot_point[2]) 
        y[28][pp:pivot_point2[28]+1]=pivot_point[1]-(np.copy(yy)[pp:pivot_point2[28]+1]-pivot_point[1]) 
        z[28][pp:pivot_point2[28]+1]=pivot_point[2]-(np.copy(xx)[pp:pivot_point2[28]+1]-pivot_point[0])   
    else:
        x[28][pivot_point2[28]:pp+1]=pivot_point[0]-(np.copy(zz)[pivot_point2[28]:pp+1]-pivot_point[2]) 
        y[28][pivot_point2[28]:pp+1]=pivot_point[1]-(np.copy(yy)[pivot_point2[28]:pp+1]-pivot_point[1]) 
        z[28][pivot_point2[28]:pp+1]=pivot_point[2]-(np.copy(xx)[pivot_point2[28]:pp+1]-pivot_point[0])
    for i in range(N):
        if yy[i]==xx[i]+pivot_point[1]-pivot_point[0] and zz[i]==pivot_point[2]:
            pivot_point2[29]=i
            if i != pp:
                break
    if pivot_point2[29]>pp: 
        x[29][pp:pivot_point2[29]+1]=pivot_point[0]+(np.copy(yy)[pp:pivot_point2[29]+1]-pivot_point[1]) 
        y[29][pp:pivot_point2[29]+1]=pivot_point[1]+(np.copy(xx)[pp:pivot_point2[29]+1]-pivot_point[0]) 
        z[29][pp:pivot_point2[29]+1]=pivot_point[2]-(np.copy(zz)[pp:pivot_point2[29]+1]-pivot_point[2])  
    else:
        x[29][pivot_point2[29]:pp+1]=pivot_point[0]+(np.copy(yy)[pivot_point2[29]:pp+1]-pivot_point[1]) 
        y[29][pivot_point2[29]:pp+1]=pivot_point[1]+(np.copy(xx)[pivot_point2[29]:pp+1]-pivot_point[0]) 
        z[29][pivot_point2[29]:pp+1]=pivot_point[2]-(np.copy(zz)[pivot_point2[29]:pp+1]-pivot_point[2]) 
    for i in range(N):
        if yy[i]==zz[i]+pivot_point[1]-pivot_point[2] and xx[i]==pivot_point[0]:
            pivot_point2[30]=i
            if i != pp:
                break
    if pivot_point2[30]>pp:   
        x[30][pp:pivot_point2[30]+1]=pivot_point[0]-(np.copy(xx)[pp:pivot_point2[30]+1]-pivot_point[0]) 
        y[30][pp:pivot_point2[30]+1]=pivot_point[1]+(np.copy(zz)[pp:pivot_point2[30]+1]-pivot_point[2]) 
        z[30][pp:pivot_point2[30]+1]=pivot_point[2]+(np.copy(yy)[pp:pivot_point2[30]+1]-pivot_point[1])
    else:
        x[30][pivot_point2[30]:pp+1]=pivot_point[0]-(np.copy(xx)[pivot_point2[30]:pp+1]-pivot_point[0]) 
        y[30][pivot_point2[30]:pp+1]=pivot_point[1]+(np.copy(zz)[pivot_point2[30]:pp+1]-pivot_point[2]) 
        z[30][pivot_point2[30]:pp+1]=pivot_point[2]+(np.copy(yy)[pivot_point2[30]:pp+1]-pivot_point[1])
    for i in range(N):
        if yy[i]==pivot_point[1]+pivot_point[2]-zz[i] and xx[i]==pivot_point[0]:
            pivot_point2[31]=i
            if i != pp:
                break
    if pivot_point2[31]>pp:  
        x[31][pp:pivot_point2[31]+1]=pivot_point[0]-(np.copy(xx)[pp:pivot_point2[31]+1]-pivot_point[0]) 
        y[31][pp:pivot_point2[31]+1]=pivot_point[1]-(np.copy(zz)[pp:pivot_point2[31]+1]-pivot_point[2]) 
        z[31][pp:pivot_point2[31]+1]=pivot_point[2]-(np.copy(yy)[pp:pivot_point2[31]+1]-pivot_point[1])   
    else:
        x[31][pivot_point2[31]:pp+1]=pivot_point[0]-(np.copy(xx)[pivot_point2[31]:pp+1]-pivot_point[0]) 
        y[31][pivot_point2[31]:pp+1]=pivot_point[1]-(np.copy(zz)[pivot_point2[31]:pp+1]-pivot_point[2]) 
        z[31][pivot_point2[31]:pp+1]=pivot_point[2]-(np.copy(yy)[pivot_point2[31]:pp+1]-pivot_point[1])
    for i in range(N):
        if yy[i]==pivot_point[1]+pivot_point[0]-xx[i] and zz[i]==pivot_point[2]:
            pivot_point2[32]=i
            if i != pp:
                break
    if pivot_point2[32]>pp: 
        x[32][pp:pivot_point2[32]+1]=pivot_point[0]-(np.copy(yy)[pp:pivot_point2[32]+1]-pivot_point[1]) 
        y[32][pp:pivot_point2[32]+1]=pivot_point[1]-(np.copy(xx)[pp:pivot_point2[32]+1]-pivot_point[0]) 
        z[32][pp:pivot_point2[32]+1]=pivot_point[2]-(np.copy(zz)[pp:pivot_point2[32]+1]-pivot_point[2]) 
    else:
        x[32][pivot_point2[32]:pp+1]=pivot_point[0]-(np.copy(yy)[pivot_point2[32]:pp+1]-pivot_point[1]) 
        y[32][pivot_point2[32]:pp+1]=pivot_point[1]-(np.copy(xx)[pivot_point2[32]:pp+1]-pivot_point[0]) 
        z[32][pivot_point2[32]:pp+1]=pivot_point[2]-(np.copy(zz)[pivot_point2[32]:pp+1]-pivot_point[2]) 

    return (x,y,z,pivot_point2)

def Chain(Cx,Cy,Cz,N):
    pivot=np.random.randint(1,N-1)
    pv=[Cx[pivot],Cy[pivot],Cz[pivot]]
    Chain=Pivot_Chain(Cx,Cy,Cz,pv,pivot,N)
    marker=[1 for i in range(1,35)]
    for i in range(1,33):
        for j in range(pivot,N):
            for k in range(pivot):
                if Chain[0][i][j]==Cx[k] and Chain[1][i][j]==Cy[k] and Chain[2][i][j]==Cz[k]: marker[i]=0
    choice=np.random.randint(1,32)
    if marker[choice]==1:
        Cx=Chain[0][choice];Cy=Chain[1][choice];Cz=Chain[2][choice]
        return (Cx,Cy,Cz)
    else:
        return (Cx,Cy,Cz)
 
def x_plus(N,start):
    return(np.array([i+start[0] for i in range(N)]), np.array([0+start[1] for i in range(N)]), np.array([0+start[2] for i in range(N)]))
def x_minus(N,start):
    return(np.array([-i+start[0] for i in range(N)]), np.array([0+start[1] for i in range(N)]), np.array([0+start[2] for i in range(N)]))
def y_plus(N,start):
    return(np.array([0+start[0] for i in range(N)]), np.array([i+start[1] for i in range(N)]), np.array([0+start[2] for i in range(N)]))
def y_minus(N,start):
    return(np.array([0+start[0] for i in range(N)]), np.array([-i+start[1] for i in range(N)]), np.array([0+start[2] for i in range(N)]))
def z_plus(N,start):
    return(np.array([0+start[0] for i in range(N)]), np.array([0+start[1] for i in range(N)]), np.array([i+start[2] for i in range(N)]))
def z_minus(N,start):
    return(np.array([0+start[0] for i in range(N)]), np.array([0+start[1] for i in range(N)]), np.array([-i+start[2] for i in range(N)]))
arms_generators_6=[x_plus,x_minus,y_plus,y_minus,z_plus,z_minus]
arms_generators_16=[[x_minus,y_minus,z_plus,z_minus],
                    [x_plus,y_minus,z_plus,z_minus],
                    [x_plus,y_plus,z_plus,z_minus],
                    [x_minus,y_plus,z_plus,z_minus]]
arms_generators_24=[[x_minus,y_minus,z_minus],
                    [x_plus,y_minus,z_minus],
                    [x_plus,y_plus,z_minus],
                    [x_minus,y_plus,z_minus],
                    [x_minus,y_minus,z_plus],
                    [x_plus,y_minus,z_plus],
                    [x_plus,y_plus,z_plus],
                    [x_minus,y_plus,z_plus]]

def Star_initiator(arms,arms_generators):
    ## a list of arms lengths
    Cx={};Cy={};Cz={}
    if len(arms)<=6:
        n=0
        start=(0,0,0)
        while n<len(arms):
           (Cx[n],Cy[n],Cz[n])=arms_generators[n](arms[n],start)
           n+=1
    elif  len(arms)<=16:
        n=0;m=0
        start=[(0,0,0),(1,0,0),(1,1,0),(0,1,0)]
        while n<len(arms):
            for i in range(4):
                (Cx[n],Cy[n],Cz[n])=arms_generators[i][m](arms[n],start[i])
                n+=1
                if n%4==0:m+=1
                if n>=len(arms)-1: break
    elif  len(arms)<=16:
        n=0;m=0
        start=[(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
        while n<len(arms):
            for i in range(4):
                (Cx[n],Cy[n],Cz[n])=arms_generators[i][m](arms[n],start[i])
                n+=1
                if n%3==0:m+=1
                if n>=len(arms)-1: break
    else:
        return "too many arms"
    return (Cx,Cy,Cz) 

def Star_initiator(arms,arms_generators):
    ## a list of arms lengths
    Cx={};Cy={};Cz={}
    if len(arms)<=6:
        n=0
        start=(0,0,0)
        while n<len(arms):
           (Cx[n],Cy[n],Cz[n])=arms_generators[n](arms[n],start)
           n+=1
    elif  len(arms)<=16:
        n=0;m=0
        start=[(0,0,0),(1,0,0),(1,1,0),(0,1,0)]
        while n<len(arms):
            for i in range(4):
                (Cx[n],Cy[n],Cz[n])=arms_generators[i][m](arms[n],start[i])
                n+=1
                if n%4==0:m+=1
                if n>=len(arms)-1: break
    else:
        return "too many arms"
    return (Cx,Cy,Cz) 


def Star_pivot(arms,Cx,Cy,Cz):
    arm=np.random.randint(len(arms))
    pivot=np.random.randint(1,arms[arm]-1)
    pv=[Cx[arm][pivot],Cy[arm][pivot],Cz[arm][pivot]]
    Chain=Pivot_Chain(Cx[arm],Cy[arm],Cz[arm],pv,pivot,arms[arm])
    marker=[1 for i in range(1,35)]
    for i in range(1,33):
        for branch in range(len(arms)):
            for j in range(pivot,arms[arm]):
                if branch==arm: 
                    for k in range(pivot):
                        if Chain[0][i][j]==Cx[branch][k] and Chain[1][i][j]==Cy[branch][k] and Chain[2][i][j]==Cz[branch][k]: marker[i]=0
                else:
                    for k in range(arms[branch]):
                        if Chain[0][i][j]==Cx[branch][k] and Chain[1][i][j]==Cy[branch][k] and Chain[2][i][j]==Cz[branch][k]: marker[i]=0
    choice=np.random.randint(1,32)
    if marker[choice]==1:
        Cx[arm]=Chain[0][choice];Cy[arm]=Chain[1][choice];Cz[arm]=Chain[2][choice]
        return (Cx,Cy,Cz)
    else:
        return (Cx,Cy,Cz)
    
def param_calc(traj):
    CM=np.sum(traj,axis=0)/np.size(traj,axis=0)
    sq=(traj[0][:]-CM[0])**2+(traj[1][:]-CM[1])**2+(traj[2][:]-CM[2])**2
    GT=np.zeros((3,3))
    for n in range(traj.shape[0]):
        GT+=np.outer(traj[n]-CM,traj[n]-CM)
    GT=GT/traj.shape[0]
    L=(GT[0][0]+GT[1][1]+GT[2][2])/3
    Ad=((3.0/2)*((GT[0][0]-L)**2+(GT[1][1]-L)**2+(GT[2][2]-L)**2+2*(GT[0][1]**2+GT[0][2]**2+GT[1][2]**2))/((3*L)**2))
    Sd=(27*((GT[0][0]-L)*(GT[1][1]-L)*(GT[2][2]-L)-(GT[0][0]-L)*GT[1][2]**2
                    -(GT[1][1]-L)*GT[0][2]**2-(GT[2][2]-L)*GT[0][1]**2
                    +2*GT[0][1]*GT[1][2]*GT[0][2])/((3*L)**3))

    return np.mean(sq),Ad,Sd
    
def Zimm_Schultz(N_average,k,number):
    theta=N_average/k
    while True:
        N_samples = np.random.gamma(
        shape=k, 
        scale=theta, 
        size=number).astype(int)
        if any(N_samples<3): continue
        else: break
    return N_samples

def get_cube_surface_points(low, high):
    # range() is exclusive at the stop, so we add 1
    side_range = range(low, high + 1)
    
    # Generate all points (x, y, z)
    # Filter: Keep the point if any coordinate is at the boundary
    surface_points = [
        (x, y, z) 
        for x, y, z in itertools.product(side_range, repeat=3)
        if x in (low, high) or y in (low, high) or z in (low, high)
    ]
    
    return surface_points
def Polymer_adsorb_initiator(arms,side):
    ## a list of arms lengths
    arms_generators=[x_plus,x_minus,y_plus,y_minus,z_plus,z_minus]
    Cx={};Cy={};Cz={}
    start=get_cube_surface_points(-side,side)
    rng = np.random.default_rng()
    random_ints = rng.choice(np.arange(1, len(start)), size=len(arms), replace=False)
    n=0
    for i in random_ints:
        if start[i][0]==side:
            (Cx[n],Cy[n],Cz[n])=arms_generators[0](arms[n],start[i])
        elif start[i][0]==-side:
            (Cx[n],Cy[n],Cz[n])=arms_generators[1](arms[n],start[i])
        elif start[i][1]==side:
            (Cx[n],Cy[n],Cz[n])=arms_generators[2](arms[n],start[i])
        elif start[i][1]==-side:
            (Cx[n],Cy[n],Cz[n])=arms_generators[3](arms[n],start[i])
        elif start[i][2]==side:
            (Cx[n],Cy[n],Cz[n])=arms_generators[4](arms[n],start[i])
        else:
            (Cx[n],Cy[n],Cz[n])=arms_generators[5](arms[n],start[i])
        n=n+1
    return (Cx,Cy,Cz) 

def Rg_chain_prediction(N):
    '''N -- a float number
        returns Rg,error_Rg'''
    RG=lambda n:(0.26689-0.17305*n**(-0.528))*n**(1.175194)
    return int(np.sqrt(RG(N)))


