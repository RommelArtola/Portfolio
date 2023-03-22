#!/usr/bin/env python
# coding: utf-8

# In[1]:


import turtle
import math
import random

class Escape():
    def __init__(self, fence=100, step_size = 30):
        '''Sets forth all the variables to be used in the class/methods of the class.'''
        self.fence_radius = fence
        self.step_size = step_size
        self.turtle = turtle.Turtle()

    def fence(self):
        '''Creates the fence perimeter for the walker to visualize the bounds'''
        self.turtle.penup()
        #The middle of the circle will be (0,0) due to the negative radius logic for y below.
        self.turtle.setposition(0, -self.fence_radius)
        self.turtle.pendown()
        #Draws the circle with the given radius.
        self.turtle.circle(self.fence_radius)

    def capture(self):
        '''Setting walker back to origin of the drawing, or (0,0)'''
        self.turtle.penup()
        self.turtle.goto(0,0)

    def escape(self):
        '''Moves walker randomly until walker is 200 meters away from origin (0,0).'''
        #For fun I wanted to see how many steps it takes to complete. And make random line colors based on RGB
        steps_needed = 0
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        #Get ready to draw.
        ##First we set the colormode to RGB values, 255.
        turtle.colormode(255)
        #We change the pencolor to the randomly generated values
        self.turtle.pencolor((r,g,b))
        #We set the pen down
        self.turtle.pendown()
        #Make bigger lines a little bit bigger than than the default.
        self.turtle.pensize(3)
        #Get position of pen. It should be (0,0) at this point.
        x,y = self.turtle.position()
        #While loop to keep the walker walking until they reach the perimeter using Pythagorean Theorem.
        while math.sqrt(x**2 + y**2) < self.fence_radius:
            #degrees in integers.
            self.turtle.right(random.randint(0,360))
            self.turtle.forward(self.step_size)
            x,y = self.turtle.position()
            steps_needed += 1
        print(f'It took the walker {steps_needed} steps to complete')
    
    def animate(self):
        '''The method that implements the previous methods below and brings them all together.'''
        #Draw the circle fence perimeter
        self.fence()
        #Set the walker back in the middle of the drawn circle.
        self.turtle.penup()
        self.turtle.goto(0,0)
        self.escape()
            
            
    
    
        



walker = Escape(200, 50)
walker.animate()

