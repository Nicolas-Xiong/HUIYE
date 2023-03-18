# -*- coding: utf-8 -*-
"""
Created on Thu May 14 04:59:16 2020

@author: Nicolas Xiong
"""

import re
from copy import deepcopy
import numpy as np
import turtle as tl

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']  #用于正常显示中文标签
plt.rcParams['axes.unicode_minus']=  False  #用于正常显示正负号


def Bezier_curve(t): #三阶贝塞尔曲线的系数,t为时间
    return [(1-t)*(1-t)*(1-t),3*t*(1-t)*(1-t),3*t*t*(1-t),t*t*t]

def Bezier_dispersed(N,P0,P1,P2,P3):  #三阶贝塞尔曲线离散，N为离散点个数
    Dt=1/N
    Pn=[]
    for n in range(N):
        re=P0[0]*Bezier_curve(Dt*n)[0]+P1[0]*Bezier_curve(Dt*n)[1]+P2[0]*Bezier_curve(Dt*n)[2]+P3[0]*Bezier_curve(Dt*n)[3]
        im=P0[1]*Bezier_curve(Dt*n)[0]+P1[1]*Bezier_curve(Dt*n)[1]+P2[1]*Bezier_curve(Dt*n)[2]+P3[1]*Bezier_curve(Dt*n)[3]
        Pn.append([re,im])
    return Pn  

def line(x,y,dx,dy):
    return [[x+1/3*dx,y+1/3*dy],[x+2/3*dx,y+2/3*dy],[x+dx,y+dy]]
    

if __name__ == '__main__':
    f = open('HUIYE4.svg','r+')
    
    #match从头开始匹配，不适合大范围查找
    #search匹配整个字符串，返回第一个出现的
    #findall查询所有符合条件的匹配
    result1=re.search('\sd="(.*?)"',f.read())  #括号内的匹配可以单独提取出来
    pathdata=result1.group(1)   #直接取括号内内容
    
    result2=re.findall('[A-Za-z]',pathdata) #匹配所有大小写字母
    pathcmd=result2
    for r in pathcmd:
        if r == 'e':
            pathcmd.remove('e')  #去除所有e，因为e不是命令
    
    cmd_category=list(set(pathcmd))  #获取命令种类
    print(cmd_category)
    re_matchstr='(['
    for c in cmd_category:
        re_matchstr+='^'+c
    re_matchstr=re_matchstr+']*)' #生成re匹配字符串，匹配目标为非命令字符串
    
    path_coordinatestr=[]
    for cmd in pathcmd:
        datastr=re.match(cmd+re_matchstr,pathdata)  #匹配非命令的字符
        path_coordinatestr.append(datastr.group(1)) #将匹配的坐标字符串存入列表
        #pathdata=pathdata.lstrip(datastr.group())   #去除已经匹配过的内容，lstrip会删除datastr.group()里所有的字符，坑
        pathdata=pathdata[len(datastr.group()):len(pathdata)] #字符串精准切片
    
    path_coordinate=[]
    for coordinate in path_coordinatestr:
        coor=re.findall('([^\s]+)',coordinate)  # +匹配前一个字符一次或多次，*匹配前一个字符0次或多次，*会匹配到空值
        coordinatefloat=[]
        if coor :
            for c1 in coor:
                if ',' in c1:
                    coordinatefloat.append([float(c1.split(',')[0]),float(c1.split(',')[1])])  #有数据就化为浮点坐标列表
                else:
                    coordinatefloat.append([float(c1)])
        path_coordinate.append(coordinatefloat)  #获取了命令对应坐标
    
    
    Bezrier=[]  #用于存储坐标集合
    Bezrier_jump=[]  #记录在哪几条曲线发生跳跃
    #Pm,P0,P1,P2,P3=[[0,0]]*5 
    Pm=[0,0]
    P0=[0,0]
    P1=[0,0]
    P2=[0,0]
    P3=[0,0]
    for i in range(len(pathcmd)): 
        if pathcmd[i] == 'm':
            for m in range(len(path_coordinate[i])):  #一个m多坐标，默认第一个为起点，其余为l
                if m == 0:
                    P0[0]=P0[0]+path_coordinate[i][m][0]
                    P0[1]=P0[1]+path_coordinate[i][m][1]
                    Pm=P0[:]   #记录路径起始点
                else:
                    P1,P2,P3 = line(P0[0],P0[1],path_coordinate[i][m][0],path_coordinate[i][m][1])
                    Bezrier.append(deepcopy([P0,P1,P2,P3]))
                    P0=P3[:]
        if pathcmd[i] == 'M':
            for M in range(len(path_coordinate[i])):  #一个M多坐标，默认第一个为起点，其余为L
                if M == 0:
                    P0=path_coordinate[i][M]
                    Pm=P0[:]  #记录路径起始点
                else:
                    P1,P2,P3 = line(P0[0],P0[1],path_coordinate[i][M][0]-P0[0],path_coordinate[i][M][1]-P0[1])
                    Bezrier.append(deepcopy([P0,P1,P2,P3]))
                    P0=P3[:]
        if pathcmd[i] == 'l':
            for l in range(len(path_coordinate[i])):
                P1,P2,P3 = line(P0[0],P0[1],path_coordinate[i][l][0],path_coordinate[i][l][1])
                Bezrier.append(deepcopy([P0,P1,P2,P3]))
                #print([P0,P1,P2,P3])
                P0=P3[:]  
        if  pathcmd[i] == 'L': 
            for L in range(len(path_coordinate[i])):
                P1,P2,P3 = line(P0[0],P0[1],path_coordinate[i][L][0]-P0[0],path_coordinate[i][L][1]-P0[1])
                Bezrier.append(deepcopy([P0,P1,P2,P3]))
                #print([P0,P1,P2,P3])
                P0=P3[:]  
        if pathcmd[i] == 'h':
            for h in range(len(path_coordinate[i])):
                P1,P2,P3 = line(P0[0],P0[1],path_coordinate[i][h][0],0)
                Bezrier.append(deepcopy([P0,P1,P2,P3]))
                #print([P0,P1,P2,P3])
                P0=P3[:]  
        if pathcmd[i] == 'H':
            for H in range(len(path_coordinate[i])):
                P1,P2,P3 = line(P0[0],P0[1],path_coordinate[i][H][0]-P0[0],0)
                Bezrier.append(deepcopy([P0,P1,P2,P3]))
                #print([P0,P1,P2,P3])
                P0=P3[:]  
        if pathcmd[i] == 'v':
            for v in range(len(path_coordinate[i])):
                P1,P2,P3 = line(P0[0],P0[1],0,path_coordinate[i][v][0])
                Bezrier.append(deepcopy([P0,P1,P2,P3]))
                #print([P0,P1,P2,P3])
                P0=P3[:]  
        if pathcmd[i] == 'V':
            for V in range(len(path_coordinate[i])):
                P1,P2,P3 = line(P0[0],P0[1],0,path_coordinate[i][V][0]-P0[1])
                Bezrier.append(deepcopy([P0,P1,P2,P3]))
                #print([P0,P1,P2,P3])
                P0=P3[:]  
        if pathcmd[i] == 'c':    
            for j1 in range(len(path_coordinate[i])):
                if j1%3 == 0:
                    P1[0]=P0[0]+path_coordinate[i][j1][0]
                    P1[1]=P0[1]+path_coordinate[i][j1][1]
                if j1%3 == 1:
                    P2[0]=P0[0]+path_coordinate[i][j1][0]
                    P2[1]=P0[1]+path_coordinate[i][j1][1]
                if j1%3 == 2:
                    P3[0]=P0[0]+path_coordinate[i][j1][0]
                    P3[1]=P0[1]+path_coordinate[i][j1][1]
                    Bezrier.append(deepcopy([P0,P1,P2,P3]))
                    P0=P3[:]  
        if pathcmd[i] == 'C':
            for j2 in range(len(path_coordinate[i])):
                if j2%3 == 0:
                    P1=path_coordinate[i][j2][:] 
                if j2%3 == 1:
                    P2=path_coordinate[i][j2][:]
                if j2%3 == 2:
                    P3=path_coordinate[i][j2][:]
                    Bezrier.append(deepcopy([P0,P1,P2,P3]))
                    P0=P3[:]  #列表复制 
        if pathcmd[i] in ['z','Z']:
            P0=Pm[:]  #回到起始点
            Bezrier_jump.append(len(Bezrier))
    
    function=[]   #获取离散化图像坐标
    BDN=10  #每段曲线获取的离散点数
    for b in range(len(Bezrier)):
        for Bd in Bezier_dispersed(BDN,Bezrier[b][0],Bezrier[b][1],Bezrier[b][2],Bezrier[b][3]):
            function.append(Bd)
    N = len(function)
    
    #用matplotlib散点图表示
    x,y = [[f[0] for f in function],[-f[1] for f in function]]
    plt.scatter(x,y,s=0.1)
    
    #用turtle直接画出来的图形
    tl.setup(2000,1000)
    tl.penup()
    tl.pensize(2) # 画笔粗细
    b = 0.3
    for t in range(N):
        #print(t)
        tl.goto(int(b*function[t][0])-500,-int(b*function[t][1])+500)
        if t in [BDN*bj-1 for bj in Bezrier_jump]:  #精确起笔
            tl.penup()
        else:
            tl.pendown()
    tl.done()

    


