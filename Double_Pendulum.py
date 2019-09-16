# -*- coding: utf-8 -*-
"""
CHAOTIC DOUBLE PENDULUM SIMULATOR
Created on Mon Sep 16 02:39:48 2019
By Antiochian 2K17
"""
import pygame
import sys
import math
import numpy as np

def EquationRHS(currentstate,y):
    #find RHS of Lagrangian using angles and velocities as variables
#UNPACK currentstate array to find useful constants        
    L1 = currentstate[2]     #rod lengths
    L2 = currentstate[3]
    m1 = currentstate[6]     #bob masses
    m2 = currentstate[7]
    g = currentstate[8]     #g value
    
    #unpack y array INSTEAD to find the variables
    theta1 = y[0] 
    theta2 = y[1]
    w1 = y[2]
    w2 = y[3]
    
    ### MATHS GOES HERE ###
    a1 = L2*m2*math.cos(theta1-theta2)/(L1*m1+L1*m2)
    a2 = L1*math.cos(theta1-theta2)/L2
    
    f1 = -g*math.sin(theta1)/L1 - L2*m2*(w2**2)*math.sin(theta1-theta2)/(L1*m1+L1*m2)
    f2 = -g*math.sin(theta2)/L2 + L1*(w1**2)*math.sin(theta1-theta2)/L2
    
    g1 = (f1 - a1*f2)/(1-a1*a2)
    g2 = (f2 - a2*f1)/(1-a1*a2)
    
    #output RHS of differential equation
    return np.array([w1,w2,g1,g2])

def advance(currentstate):
    #use Runge-Kutta and Lagrangian to advance by a timestep
    
    #UNPACK currentstate array        
    theta1 = currentstate[0] #bob angles
    theta2 = currentstate[1] 
    L1 = currentstate[2]     #rod lengths
    L2 = currentstate[3]
    w1 = currentstate[4]    #angular velocities
    w2 = currentstate[5]
    m1 = currentstate[6]     #bob masses
    m2 = currentstate[7]
    g = currentstate[8]     #g value
    dt = currentstate[9]    #timestep value
    
    #Runge-Kutta method goes here
    y0 = np.array([theta1,theta2,w1,w2])
    F0 = EquationRHS(currentstate,y0)
    
    y1 = y0 + F0*dt/2
    F1 = EquationRHS(currentstate,y1)
    
    y2 = y0 + F1*dt/2
    F2 = EquationRHS(currentstate,y2)
    
    y3 = y0 + F2*dt
    F3 = EquationRHS(currentstate,y3)
    
    y4 = y0 + (F0 + 2*F1 + 2*F2 + F3)*dt/6
    
    theta1 = y4[0] 
    theta2 = y4[1]
    w1 = y4[2]
    w2 = y4[3]
    
    nextstate = np.array([theta1,theta2,L1,L2,w1,w2,m1,m2,g,dt])
    return nextstate 

def draw(currentstate, Nx, Ny, scale, window):
    #draws current state to pygame window
    
    #UNPACK currentstate array        
    theta1 = currentstate[0] #bob angles
    theta2 = currentstate[1] 
    L1 = currentstate[2]     #rod lengths
    L2 = currentstate[3]
    #w1 = currentstate[4]    #angular velocities
    #w2 = currentstate[5]
    m1 = currentstate[6]     #bob masses
    m2 = currentstate[7]
    #g = currentstate[8]     #g value
    #dt = currentstate[9]   #timestep value
    
    R1 = max(int(3),int((L1+L2)*scale*m1/(20*m1+20*m2)))
    R2 = max(int(3),int((L1+L2)*scale*m2/(20*m1+20*m2)))
    
    
    center = np.array([int(Nx/2), int(Ny/2)]) #center of screen
    x1 = L1*math.sin(theta1)  #x displacement of bob 1
    y1 = L1*math.cos(theta1) #y displacement of bob 1
    pos1 = center + np.array([int(scale*x1),int(scale*y1)]) #DONT FORGET minus sign
    
    x2 = L1*math.sin(theta1) + L2*math.sin(theta2)
    y2 = L1*math.cos(theta1) + L2*math.cos(theta2)
    pos2 = center + np.array([int(scale*x2), int(scale*y2)])
    
    #Use "Solarized" colour scheme by Ethan Schnoover
    rodcolor = (253, 246, 227) #rods colour
    bobcolor1 = (220, 50, 47) #m1 = red
    bobcolor2 = (38, 139, 210) #m2 = blue
     
    window.fill((7,54,66)) #wipe screen with background colour
    
    #DRAW RODS
    pygame.draw.line(window, rodcolor, center, pos1) #L1
    pygame.draw.line(window, rodcolor, pos1,pos2) #L2
    #DRAW BOBS
    pygame.draw.circle(window, bobcolor1, pos1, R1)
    pygame.draw.circle(window, bobcolor2, pos2, R2)
    
    pygame.display.update() #update screen
    return    
    
def main():
    #initialise window
    pygame.init()
    (Nx, Ny) = (400,400) #initial window size
    window = pygame.display.set_mode((Nx, Ny), pygame.RESIZABLE)
    pygame.display.set_caption('Double Pendulum (Press X to exit)')
    
    #initial values
    theta1 = 0.5 #bob angles
    theta2 = 0.5 
    L1 = 1.0     #rod lengths
    L2 = 1.0
    w1 = 4.0     #angular velocities
    w2 = 5.0
    
    m1 = 1.0     #bob masses
    m2 = 1.0
    g = 9.81     #g value
    dt = 0.01    #time increment

    #pack systemstate into an array (MatLab anyone?)
    currentstate = np.array([theta1,theta2,L1,L2,w1,w2,m1,m2,g,dt])  
    #set default scale
    scale = 0.9*0.5*min(Nx,Ny)/(L1+L2) #make sure pendulum can never go off-screen
    
    clock = pygame.time.Clock()
    while True: #main simulation loop
        clock.tick(40) #set framerate
        
        
        for event in pygame.event.get(): #detect events
            if event.type == pygame.QUIT: #detect attempted exit
                pygame.quit()
                sys.exit()      #these 2 optional lines fix a hangup bug in IDLE  
            elif event.type == pygame.VIDEORESIZE: #detect resize
                (Nx, Ny) = event.size
                window = pygame.display.set_mode((Nx, Ny), pygame.RESIZABLE)
                scale = 0.9*0.5*min(Nx,Ny)/(L1+L2)
            elif event.type == pygame.KEYDOWN:
                if event.unicode == "r":
                    currentstate[0] = theta1 = 1.5*np.random.normal()
                    currentstate[1] = theta2 = 1.5*np.random.normal(theta1) #bias theta2 to be similar to theta1
                    currentstate[4] = w1 = 6*np.random.normal()
                    currentstate[5] = w2 = 6*np.random.normal()
                    currentstate[6] = m1 = min(10,abs(np.random.normal()))
                    currentstate[7] = m2 = min(10*m1,abs(np.random.normal())) #set m2's maximum as 10*m1
                
                
        draw(currentstate, Nx, Ny, scale, window) #draw system onscreen
        currentstate = advance(currentstate) #advance by 1 timestep

#if function is run as script, use default values
if __name__ == '__main__':
    main()
