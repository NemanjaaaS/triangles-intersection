# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 16:14:13 2021

@author: Nemanja
"""
from __future__ import division 
import pygame
import numpy as np


pygame.init()

#POLJA ZA UNOS KOORDINATA
base_font = pygame.font.Font(None,26)
x1 = ''
input_rect_x1 = pygame.Rect(5,35,20,26)
y1 = ''
input_rect_y1 = pygame.Rect(110,35,20,26)
x2 = ''
input_rect_x2 = pygame.Rect(215,35,20,26)
y2 = ''
input_rect_y2 = pygame.Rect(320,35,20,26)
x3 = ''
input_rect_x3 = pygame.Rect(425,35,20,26)
y3 = ''
input_rect_y3 = pygame.Rect(530,35,20,26)

Font=pygame.font.SysFont('timesnewroman',  30)

#clock
clock=pygame.time.Clock()
black=(0,0,0)
white=(255,255,255)
neka=(0,255,0)
grey=(247,247,247)

Cx1= Font.render('x1',False,neka)
Cy1= Font.render('y1',False,neka)
Cx2= Font.render('x2',False,neka)
Cy2= Font.render('y2',False,neka)
Cx3= Font.render('x3',False,neka)
Cy3= Font.render('y3',False,neka)

pPre= Font.render('Povrsina preseka:',False,black)
pUni= Font.render('Povrsina unije:',False,black)

active1=False
active2=False
active3=False
active4=False
active5=False
active6=False
#KLASA BUTTON
class button:
    def __init__(self, position, size, clr=[100, 100, 100], cngclr=None, func=None, text='', font="Segoe Print", font_size=16, font_clr=[0, 0, 0]):
        self.clr    = clr
        self.size   = size
        self.func   = func
        self.surf   = pygame.Surface(size)
        self.rect   = self.surf.get_rect(center=position)

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr

        if len(clr) == 4:
            self.surf.set_alpha(clr[3])


        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])

    def draw(self, wn):
        self.mouseover()

        self.surf.fill(self.curclr)
        self.surf.blit(self.txt_surf, self.txt_rect)
        wn.blit(self.surf, self.rect)

    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr

    def call_back(self, *args):
        if self.func:
            return self.func(*args)




#FUNKCIJA ZA PRONALAZENJE TACKE PRESEKA DVE PRAVE
def find_intersection( p0, p1, p2, p3 ) :

    s10_x = p1.x - p0.x
    s10_y = p1.y - p0.y
    s32_x = p3.x - p2.x
    s32_y = p3.y - p2.y

    denom = s10_x * s32_y - s32_x * s10_y

    if denom == 0 : return None

    denom_is_positive = denom > 0

    s02_x = p0.x - p2.x
    s02_y = p0.y - p2.y

    s_numer = s10_x * s02_y - s10_y * s02_x

    if (s_numer < 0) == denom_is_positive : return None

    t_numer = s32_x * s02_y - s32_y * s02_x

    if (t_numer < 0) == denom_is_positive : return None

    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None

    t = t_numer / denom

    intersection_point = [ p0.x + (t * s10_x), p0.y + (t * s10_y) ]
    
    return intersection_point

#KLASA POINT
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


#FUNKCIJA ZA DODAVANJE KOORDINATA U NIZ
niz_trouglova=[]
def fn1(ax1,ay1,ax2,ay2,ax3,ay3):
    
    ax1=int(x1); ay1=int(y1); ax2=int(x2); ay2=int(y2); ax3=int(x3); ay3=int(y3)
    tacke=[ax1,ay1,ax2,ay2,ax3,ay3]
    niz_trouglova.append(tacke)
    
    print(niz_trouglova)
    return niz_trouglova



#FUNKCIJA ZA ISCRTAVANJE TROUGLOVA IZ NIZA
def fn2(niz):
    niz2=[]
    niz=niz_trouglova
    for i in niz:
        for j in i:
            niz2.append(j)
            
        pygame.draw.polygon(wn, black, [[niz2[0],niz2[1]],[niz2[2],niz2[3]],[niz2[4],niz2[5]]],3)
        
        niz2=[]


#FUNKCIJA ZA POVRSINU TROUGLA
def area(x1, y1, x2, y2, x3, y3):
 
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)


 
#PROVERA DA LI JE TACKA UNUTAR TROUGLA
def isInside(x1, y1, x2, y2, x3, y3, x, y):
 
    A = area (x1, y1, x2, y2, x3, y3)
 
    A1 = area (x, y, x2, y2, x3, y3)
     
    A2 = area (x1, y1, x, y, x3, y3)
     
    A3 = area (x1, y1, x2, y2, x, y)
     

    if(A == A1 + A2 + A3):
        return True
    else:
        return False
 

#PROVERA DA LI JE TROUGAO DOBRO NACRTAN ZBOG NP
def CheckTriWinding(tri, allowReversed):
	trisq = np.ones((3,3))
	trisq[:,0:2] = np.array(tri)
	detTri = np.linalg.det(trisq)
	if detTri < 0.0:
		if allowReversed:
			a = trisq[2,:].copy()
			trisq[2,:] = trisq[1,:]
			trisq[1,:] = a
		else: raise ValueError("triangle has wrong winding direction")
	return trisq

#PROVERAVA DA LI SE TROUGLOVI PREKLAPAJU
def TriTri2D(t1, t2, eps = 0.0, allowReversed = False, onBoundary = True):

	t1s = CheckTriWinding(t1, allowReversed)
	t2s = CheckTriWinding(t2, allowReversed)
 
	if onBoundary:
		chkEdge = lambda x: np.linalg.det(x) < eps
	else:
		chkEdge = lambda x: np.linalg.det(x) <= eps
 

	for i in range(3):
		edge = np.roll(t1s, i, axis=0)[:2,:]
 
		if (chkEdge(np.vstack((edge, t2s[0]))) and
			chkEdge(np.vstack((edge, t2s[1]))) and  
			chkEdge(np.vstack((edge, t2s[2])))):
			return False
 
	for i in range(3):
		edge = np.roll(t2s, i, axis=0)[:2,:]
 
		if (chkEdge(np.vstack((edge, t1s[0]))) and
			chkEdge(np.vstack((edge, t1s[1]))) and  
			chkEdge(np.vstack((edge, t1s[2])))):
			return False
 
	return True
def polygon_area(x,y):
    correction = x[-1] * y[0] - y[-1]* x[0]
    main_area = np.dot(x[:-1], y[1:]) - np.dot(y[:-1], x[1:])
    return int(0.5*np.abs(main_area + correction))
  
#FUNKCIJA KOJA VRACA POVRSINU UNIJE I PRESEKA
def fn3(niz):
    pUnije=0
    pPreseka=0 
    nizUP=[]
 
    niz=niz_trouglova
    t1=[]
    t2=[]
    tackePreseka=[]
    for i in range(len(niz)):
        
        for j in range(i+1,len(niz)):
            t1=[[niz[i][0],niz[i][1]],[niz[i][2],niz[i][3]],[niz[i][4],niz[i][5]]]
            t2=[[niz[j][0],niz[j][1]],[niz[j][2],niz[j][3]],[niz[j][4],niz[j][5]]]

            t1p0=Point(niz[i][0],niz[i][1])
            t1p1=Point(niz[i][2],niz[i][3])
            t1p2=Point(niz[i][4],niz[i][5])
            
            t2p0=Point(niz[j][0],niz[j][1])
            t2p1=Point(niz[j][2],niz[j][3])
            t2p2=Point(niz[j][4],niz[j][5])
            
            tackeT1=[t1p0,t1p1,t1p2]
            tackeT2=[t2p0,t2p1,t2p2]
            
            #PROVERA DA LI SE TROUGLOVI T1 T2 PREKLAPAJU
            if TriTri2D(t1,t2) == True:

                temp1=[]
                #DA LI T1 IMA TACKE U SEBI KOJE PRIPADAJU T2
                for k in tackeT2:
                    
                    if(isInside(t1[0][0], t1[0][1], t1[1][0], t1[1][1], t1[2][0], t1[2][1], k.x, k.y)):
                        temp1.append(k)
                
                if len(temp1)==1:
                    if find_intersection(t1p0,t1p1,t2p0,t2p1)!=None:
                        R=find_intersection(t1p0,t1p1,t2p0,t2p1)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p1,t2p0,t2p2)!=None:
                        R=find_intersection(t1p0,t1p1,t2p0,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p1,t2p1,t2p2)!=None:
                        R=find_intersection(t1p0,t1p1,t2p1,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p2,t2p0,t2p1)!=None:
                        R=find_intersection(t1p0,t1p2,t2p0,t2p1)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p2,t2p0,t2p2)!=None:
                        R=find_intersection(t1p0,t1p2,t2p0,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p2,t2p1,t2p2)!=None:
                        R=find_intersection(t1p0,t1p2,t2p1,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p1,t1p2,t2p0,t2p1)!=None:
                        R=find_intersection(t1p1,t1p2,t2p0,t2p1)
                        tackePreseka.append(R)
                    if find_intersection(t1p1,t1p2,t2p0,t2p2)!=None:
                        R=find_intersection(t1p1,t1p2,t2p0,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p1,t1p2,t2p1,t2p2)!=None:
                        R=find_intersection(t1p1,t1p2,t2p1,t2p2)
                        tackePreseka.append(R)
                    
                    pPreseka+=area(tackePreseka[0][0],tackePreseka[0][1],tackePreseka[1][0],tackePreseka[1][1],temp1[0].x,temp1[0].y)
                    pUnije+=area(t1[0][0], t1[0][1], t1[1][0], t1[1][1], t1[2][0], t1[2][1])+area(t2[0][0], t2[0][1], t2[1][0], t2[1][1], t2[2][0], t2[2][1])-area(tackePreseka[0][0],tackePreseka[0][1],tackePreseka[1][0],tackePreseka[1][1],temp1[0].x,temp1[0].y)
                
                if len(temp1)==2:
                    if find_intersection(t1p0,t1p1,t2p0,t2p1)!=None:
                        R=find_intersection(t1p0,t1p1,t2p0,t2p1)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p1,t2p0,t2p2)!=None:
                        R=find_intersection(t1p0,t1p1,t2p0,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p1,t2p1,t2p2)!=None:
                        R=find_intersection(t1p0,t1p1,t2p1,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p2,t2p0,t2p1)!=None:
                        R=find_intersection(t1p0,t1p2,t2p0,t2p1)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p2,t2p0,t2p2)!=None:
                        R=find_intersection(t1p0,t1p2,t2p0,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p2,t2p1,t2p2)!=None:
                        R=find_intersection(t1p0,t1p2,t2p1,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p1,t1p2,t2p0,t2p1)!=None:
                        R=find_intersection(t1p1,t1p2,t2p0,t2p1)
                        tackePreseka.append(R)
                    if find_intersection(t1p1,t1p2,t2p0,t2p2)!=None:
                        R=find_intersection(t1p1,t1p2,t2p0,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p1,t1p2,t2p1,t2p2)!=None:
                        R=find_intersection(t1p1,t1p2,t2p1,t2p2)
                        tackePreseka.append(R)
                    pPreseka+=2*area(tackePreseka[0][0],tackePreseka[0][1],tackePreseka[1][0],tackePreseka[1][1],temp1[0].x,temp1[0].y)
                    pUnije+=area(t1[0][0], t1[0][1], t1[1][0], t1[1][1], t1[2][0], t1[2][1])+area(t2[0][0], t2[0][1], t2[1][0], t2[1][1], t2[2][0], t2[2][1])-2*area(tackePreseka[0][0],tackePreseka[0][1],tackePreseka[1][0],tackePreseka[1][1],temp1[0].x,temp1[0].y)
                if len(temp1)==3:
                    pPreseka+=area(temp1[0].x,temp1[0].y,temp1[1].x,temp1[1].y,temp1[2].x,temp1[2].y)
                    pUnije+=area(t1[0][0], t1[0][1], t1[1][0], t1[1][1], t1[2][0], t1[2][1])+area(t2[0][0], t2[0][1], t2[1][0], t2[1][1], t2[2][0], t2[2][1])-area(temp1[0].x,temp1[0].y,temp1[1].x,temp1[1].y,temp1[2].x,temp1[2].y)
                if len(temp1)==0:
                    if find_intersection(t1p0,t1p1,t2p0,t2p1)!=None:
                        R=find_intersection(t1p0,t1p1,t2p0,t2p1)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p1,t2p0,t2p2)!=None:
                        R=find_intersection(t1p0,t1p1,t2p0,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p1,t2p1,t2p2)!=None:
                        R=find_intersection(t1p0,t1p1,t2p1,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p2,t2p0,t2p1)!=None:
                        R=find_intersection(t1p0,t1p2,t2p0,t2p1)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p2,t2p0,t2p2)!=None:
                        R=find_intersection(t1p0,t1p2,t2p0,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p0,t1p2,t2p1,t2p2)!=None:
                        R=find_intersection(t1p0,t1p2,t2p1,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p1,t1p2,t2p0,t2p1)!=None:
                        R=find_intersection(t1p1,t1p2,t2p0,t2p1)
                        tackePreseka.append(R)
                    if find_intersection(t1p1,t1p2,t2p0,t2p2)!=None:
                        R=find_intersection(t1p1,t1p2,t2p0,t2p2)
                        tackePreseka.append(R)
                    if find_intersection(t1p1,t1p2,t2p1,t2p2)!=None:
                        R=find_intersection(t1p1,t1p2,t2p1,t2p2)
                        tackePreseka.append(R)
                    
                    if len(tackePreseka)==4:
                        pPreseka+=area(tackePreseka[0][0],tackePreseka[0][1],tackePreseka[1][0],tackePreseka[1][1],tackePreseka[2][0],tackePreseka[2][1])
                        pUnije+=area(t1[0][0], t1[0][1], t1[1][0], t1[1][1], t1[2][0], t1[2][1])+area(t2[0][0], t2[0][1], t2[1][0], t2[1][1], t2[2][0], t2[2][1])-2*area(tackePreseka[0][0],tackePreseka[0][1],tackePreseka[1][0],tackePreseka[1][1],tackePreseka[2][0],tackePreseka[2][1])
                    if len(tackePreseka)==6:
                        pPreseka+=polygon_area(tackePreseka[0][0],tackePreseka[0][1])
                        pUnije+=area(t1[0][0], t1[0][1], t1[1][0], t1[1][1], t1[2][0], t1[2][1])+area(t2[0][0], t2[0][1], t2[1][0], t2[1][1], t2[2][0], t2[2][1])-polygon_area(tackePreseka[0][0],[0][1])
                    
                        
                        

                print("Povrsina unije:" ,pUnije)
                print("Povrsina preseka:",pPreseka)

            else:
                print("Nema preklapanje trouglova")
                

                
   



wn_width=1200
wn_height=950
wn=pygame.display.set_mode((wn_width,wn_height))
pygame.display.set_caption("Drawing triagnels")

font = pygame.font.Font('freesansbold.ttf',2)
 
button1 = button(position=(80, 100), size=(150, 50), clr=(181, 181, 181), cngclr=(255, 0, 0), func=fn1, text='Dodaj')


button_list = [button1]

state=True
const = 0
unija=0
presek=0
nizUPa=[0,0]

#MAIN FUNKCIJA
while state:
    
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            state=False
        #DA LI JE KLIKNUTO DUGME I DA LI JE BACKSPACE
        if event.type == pygame.KEYDOWN:
            if active1==True:
                if event.key == pygame.K_BACKSPACE:
                    x1 = x1[:-1]
                else:
                    x1+=event.unicode

            if active2==True:    
                if event.key == pygame.K_BACKSPACE:
                    y1 = y1[:-1]
                else:
                    y1+=event.unicode
            if active3==True:
                if event.key == pygame.K_BACKSPACE:
                    x2 = x2[:-1]
                else:
                    x2+=event.unicode

            if active4==True:    
                if event.key == pygame.K_BACKSPACE:
                    y2 = y2[:-1]
                else:
                    y2+=event.unicode
            if active5==True:
                if event.key == pygame.K_BACKSPACE:
                    x3 = x3[:-1]
                else:
                    x3+=event.unicode

            if active6==True:    
                if event.key == pygame.K_BACKSPACE:
                    y3 = y3[:-1]
                else:
                    y3+=event.unicode
        #DA LI JE KLIKNUT MIS
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect_x1.collidepoint(event.pos):
                active1=True
            else:
                active1=False
            
            if input_rect_y1.collidepoint(event.pos):
                active2=True
            else:
                 active2=False
                 
            if input_rect_x2.collidepoint(event.pos):
                active3=True
            else:
                active3=False
            
            if input_rect_y2.collidepoint(event.pos):
                active4=True
            else:
                 active4=False
            if input_rect_x3.collidepoint(event.pos):
                active5=True
            else:
                active5=False
            
            if input_rect_y3.collidepoint(event.pos):
                active6=True
            else:
                 active6=False
            #POZIVANJE FUNKCIJA AKO JE KLIKNUTO DUGME   
            for b in button_list:
                if b.rect.collidepoint(event.pos):
                    b.call_back(x1,y1,x2,y2,x3,y3)
                    fn2(niz_trouglova)
                    fn3(niz_trouglova)
                    nizUPa=fn3(niz_trouglova)
    wn.fill(grey)
    #ISCRTAVANJE POLJA ZA PITANJE      
    #x1
    pygame.draw.rect(wn,black,input_rect_x1,2)
    
    text_surfice = base_font.render(x1,True,(black))
    wn.blit(text_surfice,(input_rect_x1.x+5,input_rect_x1.y+5))
    
    input_rect_x1.w = max(100,text_surfice.get_width()+10)
    
    #y1
    pygame.draw.rect(wn,black,input_rect_y1,2)
    
    text_surfice = base_font.render(y1,True,(black))
    wn.blit(text_surfice,(input_rect_y1.x+5,input_rect_y1.y+5))
    
    input_rect_y1.w = max(100,text_surfice.get_width()+10)
    
    #x2
    pygame.draw.rect(wn,black,input_rect_x2,2)
    
    text_surfice = base_font.render(x2,True,(black))
    wn.blit(text_surfice,(input_rect_x2.x+5,input_rect_x2.y+5))
    
    input_rect_x2.w = max(100,text_surfice.get_width()+10)
    
    #y2
    pygame.draw.rect(wn,black,input_rect_y2,2)
    
    text_surfice = base_font.render(y2,True,(black))
    wn.blit(text_surfice,(input_rect_y2.x+5,input_rect_y2.y+5))
    
    input_rect_y2.w = max(100,text_surfice.get_width()+10)
    
    #x3
    pygame.draw.rect(wn,black,input_rect_x3,2)
    
    text_surfice = base_font.render(x3,True,(black))
    wn.blit(text_surfice,(input_rect_x3.x+5,input_rect_x3.y+5))
    
    input_rect_x3.w = max(100,text_surfice.get_width()+10)
    
    #y3
    pygame.draw.rect(wn,black,input_rect_y3,2)
    
    text_surfice = base_font.render(y3,True,(black))
    wn.blit(text_surfice,(input_rect_y3.x+5,input_rect_y3.y+5))
    
    input_rect_y3.w = max(100,text_surfice.get_width()+10)

    #ISPISIVANJE X1,Y1...UNIJA PRESEK
    wn.blit(Cx1,(45,2))
    wn.blit(Cy1,(145,1))
    wn.blit(Cx2,(245,2))
    wn.blit(Cy2,(345,1))
    wn.blit(Cx3,(445,2))
    wn.blit(Cy3,(545,1))
    wn.blit(pPre,(20,820))
    wn.blit(pUni,(20,850))


    
    
    
    
    #ISCRTAVANJE DUGMICA
    for b in button_list:
        b.draw(wn)
        fn2(niz_trouglova)
            

    pygame.display.update()
   
    clock.tick(30)
    




pygame.quit()
quit()
