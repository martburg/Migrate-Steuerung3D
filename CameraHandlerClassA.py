from direct.showbase import DirectObject
from panda3d.core import Vec3,Vec2
import math

# Last modified: 10/2/2009 -27/5/2013
# This class takes over control of the camera and sets up a Real Time Strategy game type camera control system. The user can move the camera three
# ways. If the mouse cursor is moved to the edge of the screen, the camera will pan in that direction. If the right mouse button is held down, the
# camera will orbit around it's target point in accordance with the mouse movement, maintaining a fixed distance. The mouse wheel will move the
# camera closer to or further from it's target point.

# This code was originally developed by Ninth from the Panda3D forums, and has been modified by piratePanda to achieve a few effects.
   # First mod: Comments. I've gone through the code and added comments to explain what is doing what, and the reason for each line of code.
   # Second mod: Name changes. I changed some names of variables and functions to make the code a bit more readable (in my opinion).
   # Third mod: Variable pan rate. I have changed the camera panning when the mouse is moved to the edge of the screen so that the panning
      # rate is dependant on the distance the camera has been zoomed out. This prevents the panning from appearing faster when
      # zoomed in than when zoomed out. I have also added a pan rate variable, which could be modified by an options menu, so it is
      # easier to give the player control over how fast the camera pans.
   # Fourth mod: Variable pan zones. I added a variable to control the size of the zones at the edge of the screen where the camera starts
      # panning.
   # Fifth mod: Orbit limits: I put in a system to limit how far the camera can move along it's Y orbit to prevent it from moving below the ground
      # plane or so high that you get a fast rotation glitch.
   # Sixth mod: Pan limits: I put in variables to use for limiting how far the camera can pan, so the camera can't pan away from the map. These
      # values will need to be customized to the map, so I added a function for setting them.
      
# Starting Point Hard coded; Limits Hard Coded To Kampfbahn; ZMovement Added q toggles between y movement or z movement MBU
   

class CameraHandlerPers(DirectObject.DirectObject):
   def __init__(self,cam,mouseWatcherNode):
   
      base.disableMouse()
      # This disables the default mouse based camera control used by panda. This default control is awkward, and won't be used.
      self.cam = cam
      self.mouseWatcherNode = mouseWatcherNode
      
      self.lens=self.cam.node().getLens()
      
      self.cam.setPos(100,-250,150)
      self.camPos_g = (100,-250,150)
      self.cam.lookAt(0,0,0)
      self.camTarget_g_x = 0
      self.camTarget_g_y = 0
      self.camTarget_g_z = 0
      self.camDist_g = 377
      # Gives the camera an initial position and rotation.
      
      self.mx,self.my=0,0
      # Sets up variables for storing the mouse coordinates
      self.panning = False
      self.orbiting=False
      self.mouseleft = '0' 
      self.mouseright = '0' 
      self.mousemod = '0'
      self.control = '0'
      self.PanA = False
      self.mouseposPanStartX = 0
      self.mouseposPanStartY = 0
      self.camposPanStartX = 0
      self.camposPanStartY = 0   
      
      
      
      # A boolean variable for specifying whether the camera is in orbiting mode. Orbiting mode refers to when the camera is being moved
      # because the user is holding down the right mouse button.
      
      self.target=Vec3()
      # sets up a vector variable for the camera's target. The target will be the coordinates that the camera is currently focusing on.
      
      self.camDist = 377
      # A variable that will determine how far the camera is from it's target focus
      
      self.panRateDivisor = 20
      # This variable is used as a divisor when calculating how far to move the camera when panning. Higher numbers will yield slower panning
      # and lower numbers will yield faster panning. This must not be set to 0.
      
      self.panZoneSize = .15
      # This variable controls how close the mouse cursor needs to be to the edge of the screen to start panning the camera. It must be less than 1,
      # and I recommend keeping it less than .2
      
      self.panLimitsX = Vec2(-100, 100)
      self.panLimitsY = Vec2(-100, 100)
      self.panLimitsZ = Vec2(-100, 100)
      # These three variables will serve as limits for how far the camera can pan, so you don't scroll away from the map.

      self.setTarget(0,0,0)
      # calls the setTarget function to set the current target position to the origin.
      
      self.turnCameraAroundPoint(0,0)
      # calls the turnCameraAroundPoint function with a turn amount of 0 to set the camera position based on the target and camera distance
      self.accept("mouse2",self.startAPan)
      self.accept("mouse2-up",self.stopAPan)
      self.accept("mouse3",self.startOrbit)
      # sets up the camrea handler to accept a right mouse click and start the "drag" mode.
      
      self.accept("mouse3-up",self.stopOrbit)
      # sets up the camrea handler to understand when the right mouse button has been released, and ends the "drag" mode when
      # the release is detected.
      self.accept("wheel_up",self.On_wheel_up)
      # sets up the camera handler to detect when the mouse wheel is rolled upwards and uses a lambda function to call the
      # adjustCamDist function  with the argument 0.9
      
      self.accept("wheel_down",self.On_wheel_down)
      # sets up the camera handler to detect when the mouse wheel is rolled upwards and uses a lambda function to call the
      # adjustCamDist function  with the argument 1.1
      
   #++++Added to implement left mouse button to start pan movement
      #
      self.accept("mouse1",self.startPan)
      # sets up thew camera handler to accept  a left mouse click and act as second reason to start pan mode
      # (first is mouse near the sides of the window)
      self.accept("mouse1-up",self.stopPan)
      # sets up the camera handler to understand when the left mouse button has been released, and ends the "pan" mode when
      # the release is detected.
      # 
      self.accept('h', self.On_h )
      # resets the camera Position to StartPoint
      self.ToggleZ = False
      self.accept('q', self.On_q )
      # toggles Z movement of camera
      self.accept('d',self.On_d)
      self.accept('d-up',self.On_D_up)
      self.accept('control-g',self.On_Control_g)
      self.accept('g',self.On_g)
   #++++End Addition
      taskMgr.add(self.camMoveTask,'camMoveTask')
      # sets the camMoveTask to be run every frame
   def startAPan(self):
      #print "middleButton down"
      self.camposPanStartX = self.cam.getPos()[0]
      self.camposPanStartY = self.cam.getPos()[1]
      if self.mouseWatcherNode.hasMouse():
         self.mouseposPanStartX = self.mouseWatcherNode.getMouse()[0]
         self.mouseposPanStartY = self.mouseWatcherNode.getMouse()[1] 
      self.targetStartX = self.target.getX()
      self.targetStartY = self.target.getY()
      self.PanA = True
   def stopAPan(self):
      #print "middleButton up" 
      self.PanA = False
   def On_wheel_up(self):
      if self.mouseWatcherNode.hasMouse():
         self.adjustCamDist(0.9) 
   def On_wheel_down(self):
      if self.mouseWatcherNode.hasMouse():
         self.adjustCamDist(1.1)       
   def On_d(self):
      self.mousemod = '1'
   def On_D_up(self):
      self.mousemod = '0'

   def turnCameraAroundPoint(self,deltaX,deltaY):
      # This function performs two important tasks. First, it is used for the camera orbital movement that occurs when the
      # right mouse button is held down. It is also called with 0s for the rotation inputs to reposition the camera during the
      # panning and zooming movements.
      # The delta inputs represent the change in rotation of the camera, which is also used to determine how far the camera
         # actually moves along the orbit.
      
         newCamHpr = Vec3()
         newCamPos = Vec3()
         # Creates temporary containers for the new rotation and position values of the camera.
         
         camHpr=self.cam.getHpr()
         # Creates a container for the current HPR of the camera and stores those values.
         
         newCamHpr.setX(camHpr.getX()+deltaX)
         newCamHpr.setY(self.clamp(camHpr.getY()-deltaY, -89, -0))
         newCamHpr.setZ(camHpr.getZ())
         # Adjusts the newCamHpr values according to the inputs given to the function. The Y value is clamped to prevent
         # the camera from orbiting beneath the ground plane and to prevent it from reaching the apex of the orbit, which
         # can cause a disturbing fast-rotation glitch.
         
         self.cam.setHpr(newCamHpr)
         # Sets the camera's rotation to the new values.
         
         angleradiansX = newCamHpr.getX() * (math.pi / 180.0)
         angleradiansY = newCamHpr.getY() * (math.pi / 180.0)
         # Generates values to be used in the math that will calculate the new position of the camera.         
         newCamPos.setX(self.camDist*math.sin(angleradiansX)*math.cos(angleradiansY)+self.target.getX())
         newCamPos.setY(-self.camDist*math.cos(angleradiansX)*math.cos(angleradiansY)+self.target.getY())
         newCamPos.setZ(-self.camDist*math.sin(angleradiansY)+self.target.getZ())
         self.cam.setPos(newCamPos.getX(),newCamPos.getY(),newCamPos.getZ())
         # Performs the actual math to calculate the camera's new position and sets the camera to that position.
         #Unfortunately, this math is over my head, so I can't fully explain it.
                     
         self.cam.lookAt(self.target.getX(),self.target.getY(),self.target.getZ() )
         # Points the camera at the target location.
         
   def setTarget(self,x,y,z):
      #This function is used to give the camera a new target position.
      x = self.clamp(x, self.panLimitsX.getX(), self.panLimitsX.getY())
      self.target.setX(x)
      y = self.clamp(y, self.panLimitsY.getX(), self.panLimitsY.getY())
      self.target.setY(y)
      self.target.setZ(z)
      # Stores the new target position values in the target variable. The x and y values are clamped to the pan limits.
      
   def setPanLimits(self,xMin, xMax, yMin, yMax):
      # This function is used to set the limitations of the panning movement.
      
      self.panLimitsX = (xMin, xMax)
      self.panLimitsY = (yMin, yMax)
      # Sets the inputs into the limit variables.
      
   def clamp(self, val, minVal, maxVal):
      # This function constrains a value such that it is always within or equal to the minimum and maximum bounds.
      
      val = min( max(val, minVal), maxVal)
      # This line first finds the larger of the val or the minVal, and then compares that to the maxVal, taking the smaller. This ensures
      # that the result you get will be the maxVal if val is higher than it, the minVal if val is lower than it, or the val itself if it's
      # between the two.
      
      return val
      # returns the clamped value
      
   def startOrbit(self):
      # This function puts the camera into orbiting mode.
      
      self.orbiting=True
      # Sets the orbiting variable to true to designate orbiting mode as on.
      self.mouseright = '1' 
   def stopOrbit(self):

      # This function takes the camera out of orbiting mode.
      
      self.orbiting=False
      # Sets the orbiting variable to false to designate orbiting mode as off.
      self.mouseright = '0'
   def startPan(self):
      # This function puts the camera into panning mode.      
      self.panning=True
      # Sets the panning variable to true to designate second panning condition as on.
      self.mouseleft = '1'
   def stopPan(self):
      # This function puts the camera into panning mode.      
      self.panning=False
      # Sets the panning variable to false to designate second panning condition as off.
      self.mouseleft = '0'             
            
   def adjustCamDist(self,distFactor):
      # This function increases or decreases the distance between the camera and the target position to simulate zooming in and out.
      # The distFactor input controls the amount of camera movement.
         # For example, inputing 0.9 will set the camera to 90% of it's previous distance.
      
      self.camDist=self.camDist*distFactor
      # Sets the new distance into self.camDist.
      
      self.turnCameraAroundPoint(0,0)
      # Calls turnCameraAroundPoint with 0s for the rotation to reset the camera to the new position.
      
   def camMoveTask(self,task):
      # This task is the camera handler's work house. It's set to be called every frame and will control both orbiting and panning the camera.
      if self.mouseWatcherNode.hasMouse():
         # We're going to use the mouse, so we have to maqke sure it's in the game window. If it's not and we try to use it, we'll get
         # a crash error.
         
         mpos = self.mouseWatcherNode.getMouse()
         # Gets the mouse position
         #++++Brauch maus pos auch fuer picken der Baelle
         self.mousepos=self.mouseWatcherNode.getMouse()
         angleradians1 = self.cam.getH() * (math.pi / 180.0)
         if self.orbiting:
         # Checks to see if the camera is in orbiting mode. Orbiting mode overrides panning, because it would be problematic if, while
         # orbiting the camera the mouse came close to the screen edge and started panning the camera at the same time.
         
            self.turnCameraAroundPoint((self.mx-mpos.getX())*100,(self.my-mpos.getY())*100)       
            # calculates new values for camera rotation based on the change in mouse position. mx and my are used here as the old
            # mouse position.
            
         else:
         # If the camera isn't in orbiting mode, we check to see if the mouse is close enough to the edge of the screen to start panning
         
            moveY=False
            moveX=False
            moveZ=False

            # these two booleans are used to denote if the camera needs to pan. X and Y refer to the mouse position that causes the
            # panning. X is the left or right edge of the screen, Y is the top or bottom.
            
            if self.my > (1 - self.panZoneSize):
               angleradiansX1 = self.cam.getH() * (math.pi / 180.0)
               panRate1 = (1 - self.my - self.panZoneSize) * (self.camDist / self.panRateDivisor)
               if self.ToggleZ == False:
                  moveY = True
                  moveZ = False
               else:
                  moveY = False
                  moveZ = True               
            if self.my < (-1 + self.panZoneSize):
               angleradiansX1 = self.cam.getH() * (math.pi / 180.0)+math.pi
               panRate1 = (1 + self.my - self.panZoneSize)*(self.camDist / self.panRateDivisor)
               if self.ToggleZ == False:
                  moveY = True
                  moveZ = False
               else:
                  moveY = False
                  moveZ = True 
            if self.mx > (1 - self.panZoneSize):
               angleradiansX2 = self.cam.getH() * (math.pi / 180.0)+math.pi*0.5
               panRate2 = (1 - self.mx - self.panZoneSize) * (self.camDist / self.panRateDivisor)
               moveX = True
            if self.mx < (-1 + self.panZoneSize):
               angleradiansX2 = self.cam.getH() * (math.pi / 180.0)-math.pi*0.5
               panRate2 = (1 + self.mx - self.panZoneSize) * (self.camDist / self.panRateDivisor)
               moveX = True
            # These four blocks check to see if the mouse cursor is close enough to the edge of the screen to start panning and then
            # perform part of the math necessary to find the new camera position. Once again, the math is a bit above my head, so
            # I can't properly explain it. These blocks also set the move booleans to true so that the next lines will move the camera.           
            if moveY and self.panning:
               tempX = self.target.getX()+math.sin(angleradiansX1)*panRate1
               tempX = self.clamp(tempX, self.panLimitsX.getX(), self.panLimitsX.getY())
               self.target.setX(tempX)
               tempY = self.target.getY()-math.cos(angleradiansX1)*panRate1
               tempY = self.clamp(tempY, self.panLimitsY.getX(), self.panLimitsY.getY())
               self.target.setY(tempY)
               self.turnCameraAroundPoint(0,0)
            if moveX and self.panning:
               tempX = self.target.getX()-math.sin(angleradiansX2)*panRate2
               tempX = self.clamp(tempX, self.panLimitsX.getX(), self.panLimitsX.getY())
               self.target.setX(tempX)
               tempY = self.target.getY()+math.cos(angleradiansX2)*panRate2
               tempY = self.clamp(tempY, self.panLimitsY.getX(), self.panLimitsY.getY())
               self.target.setY(tempY)
               self.turnCameraAroundPoint(0,0)
            if moveZ and self.panning:
               tempZ = self.target.getZ()-math.cos(angleradiansX1)*panRate1

               tempZ = self.clamp(tempZ, self.panLimitsZ.getX(), self.panLimitsZ.getY())
               self.target.setZ(tempZ)
               self.turnCameraAroundPoint(0,0)
            if self.PanA:
               #print self.cam.getHpr()
               angleradiansH = self.cam.getH() * (math.pi / 180.0)
               angleradiansP = self.cam.getP() * (math.pi / 180.0)
               DeltaX=self.mouseposPanStartX-mpos.getX()
               DeltaY=self.mouseposPanStartY-mpos.getY()
               #filmsize = self.lens.getFilmSize()
               CamPosZ = self.cam.getPos()[2]
               self.cam.setPos(self.camposPanStartX+math.cos(angleradiansH)*DeltaX/2*100
                               ,self.camposPanStartY+math.cos(angleradiansP)*DeltaY/2*100,CamPosZ)

         self.mx=mpos.getX()
         self.my=mpos.getY()
         # The old mouse positions are updated to the current mouse position as the final step.
      return task.cont
   def On_h(self):
      """ Reset Cam Pos"""
      self.cam.setPos(0,-250,66)
      self.cam.lookAt(0,0,0)  
      self.camDist = 258
      self.setTarget(0,0,0)
      self.turnCameraAroundPoint(0,0)
      
   def On_q(self):
      """ Toggles Y-Movement to Z-Movement"""
      if self.ToggleZ == False:
         self.ToggleZ = True
      else:
         self.ToggleZ = False
         
   def On_Control_g(self):
      self.camPos_g = self.cam.getPos()  
      self.camDist_g = self.camDist
      self.camTarget_g_x = self.target.getX()
      self.camTarget_g_y = self.target.getY()
      self.camTarget_g_z = self.target.getZ()
               

   def On_g(self):
      self.cam.setPos(self.camPos_g)  
      self.camDist = self.camDist_g
      self.cam.lookAt(self.camTarget_g_x,self.camTarget_g_y,self.camTarget_g_z)
      self.setTarget(self.camTarget_g_x,self.camTarget_g_y,self.camTarget_g_z)
      
class CameraHandlerTop(DirectObject.DirectObject):
   
   def __init__(self,cam,mouseWatcherNode):
   
      base.disableMouse()
      # This disables the default mouse based camera control used by panda. This default control is awkward, and won't be used.
      self.cam = cam
      self.mouseWatcherNode = mouseWatcherNode

      self.lens=self.cam.node().getLens()      
    
      self.mx,self.my=0,0
      self.mousepos =(0,0)
      self.mouseposPanStartX = 0
      self.mouseposPanStartY = 0
      self.camposPanStartX = 0
      self.camposPanStartY = 0     
      # Sets up variables for storing the mouse coordinates
      self.panning = False
      self.mouseleft = '0' 
      self.mouseright = '0' 
      self.mousemod = '0'
      self.control = '0'  

      self.accept("wheel_up",self.On_wheel_up)
      self.accept("wheel_down",self.On_wheel_down)
      self.accept("mouse1",self.startPan)
      self.accept("mouse1-up",self.stopPan)
     
  
      taskMgr.add(self.camMoveTask,'camMoveTaskTop')
   def On_wheel_up(self):
      if self.mouseWatcherNode.hasMouse():
         fs=self.lens.getFilmSize()
         self.lens.setFilmSize(fs*0.9)
   def On_wheel_down(self):
      if self.mouseWatcherNode.hasMouse():
         fs=self.lens.getFilmSize()
         self.lens.setFilmSize(fs*1.1)

   def startPan(self):
      # This function puts the camera into panning mode. 
      if (self.mouseWatcherNode.hasMouse()):
         self.mouseposPanStartX = self.mouseWatcherNode.getMouse()[0]
         self.mouseposPanStartY = self.mouseWatcherNode.getMouse()[1]
         self.camposPanStartX = self.cam.getPos()[0]
         self.camposPanStartY = self.cam.getPos()[1]
         self.panning=True
      # Sets the panning variable to true to designate second panning condition as on.
      self.mouseleft = '1'
   def stopPan(self):
      # This function puts the camera into panning mode.      
      self.panning=False
      # Sets the panning variable to false to designate second panning condition as off.
      self.mouseleft = '0'                         
   def camMoveTask(self,task):
      # This task is the camera handler's work house. It's set to be called every frame and will control both orbiting and panning the camera.
      if self.mouseWatcherNode.hasMouse():
         if self.panning:
            mpos = self.mouseWatcherNode.getMouse()
            self.mousepos=self.mouseWatcherNode.getMouse()
            DeltaX=self.mouseposPanStartX-mpos.getX()
            DeltaY=self.mouseposPanStartY-mpos.getY()
            filmsize = self.lens.getFilmSize()
            CamPosZ = self.cam.getPos()[2]
            self.cam.setPos(self.camposPanStartX+DeltaX/2*filmsize[0]
                            ,self.camposPanStartY+DeltaY/2*filmsize[1],CamPosZ)
            self.cam.lookAt(self.camposPanStartX+DeltaX/2*filmsize[0]
                            ,self.camposPanStartY+DeltaY/2*filmsize[1],0) 
            

      return task.cont

class CameraHandlerFront(DirectObject.DirectObject):
   def __init__(self,cam,mouseWatcherNode):
   
      base.disableMouse()
      # This disables the default mouse based camera control used by panda. This default control is awkward, and won't be used.
      self.cam = cam
      self.mouseWatcherNode = mouseWatcherNode

      self.lens=self.cam.node().getLens()      
    
      self.mx,self.my=0,0
      self.mousepos =(0,0)
      self.mouseposPanStartX = 0
      self.mouseposPanStartY = 0
      self.camposPanStartX = 0
      self.camposPanStartZ = 0     
      # Sets up variables for storing the mouse coordinates
      self.panning = False
      self.mouseleft = '0' 
      self.mouseright = '0' 
      self.mousemod = '0'
      self.control = '0'  

      self.accept("wheel_up",self.On_wheel_up)
      self.accept("wheel_down",self.On_wheel_down)
      self.accept("mouse1",self.startPan)
      self.accept("mouse1-up",self.stopPan)
     
  
      taskMgr.add(self.camMoveTask,'camMoveTaskFront')
   def On_wheel_up(self):
      if self.mouseWatcherNode.hasMouse():
         fs=self.lens.getFilmSize()
         self.lens.setFilmSize(fs*0.9)
   def On_wheel_down(self):
      if self.mouseWatcherNode.hasMouse():
         fs=self.lens.getFilmSize()
         self.lens.setFilmSize(fs*1.1)

   def startPan(self):
      # This function puts the camera into panning mode. 
      if (self.mouseWatcherNode.hasMouse()):
         self.mouseposPanStartX = self.mouseWatcherNode.getMouse()[0]
         self.mouseposPanStartY = self.mouseWatcherNode.getMouse()[1]
         self.camposPanStartX = self.cam.getPos()[0]
         self.camposPanStartZ = self.cam.getPos()[2]
         self.panning=True
      # Sets the panning variable to true to designate second panning condition as on.
      self.mouseleft = '1'
   def stopPan(self):
      # This function puts the camera into panning mode.      
      self.panning=False
      # Sets the panning variable to false to designate second panning condition as off.
      self.mouseleft = '0'                         
   def camMoveTask(self,task):
      # This task is the camera handler's work house. It's set to be called every frame and will control both orbiting and panning the camera.
      if self.mouseWatcherNode.hasMouse():
         if self.panning:
            
            mpos = self.mouseWatcherNode.getMouse()
            self.mousepos=self.mouseWatcherNode.getMouse()
            DeltaX=self.mouseposPanStartX-mpos.getX()
            DeltaY=self.mouseposPanStartY-mpos.getY()
            filmsize = self.lens.getFilmSize()
            CamPosY = self.cam.getPos()[1]
            self.cam.setPos(self.camposPanStartX+DeltaX/2*filmsize[0],CamPosY
                            ,self.camposPanStartZ+DeltaY/2*filmsize[1])

      return task.cont
class DisplayRegionSizer(DirectObject.DirectObject):
   def __init__(self,cam1,cam2,cam3,DisplayRegion1,DisplayRegion2,DisplayRegion3,mouseWatcherNode,
                mouseWatcherNode1,mouseWatcherNode2,mouseWatcherNode3):
      
      self.lens1=cam1.node().getLens()
      self.lens2=cam2.node().getLens()
      self.lens3=cam3.node().getLens()

      self.DisplayRegion1 = DisplayRegion1
      self.DisplayRegion2 = DisplayRegion2
      self.DisplayRegion3 = DisplayRegion3 
      
      self.mouseWatcherNode = mouseWatcherNode
      self.mouseWatcherNode1 = mouseWatcherNode1 
      self.mouseWatcherNode2 = mouseWatcherNode2
      self.mouseWatcherNode3 = mouseWatcherNode3
      
      self.Left1 = DisplayRegion1.getLeft()
      self.Right1 = DisplayRegion1.getRight()
      self.Top1 = DisplayRegion1.getTop()
      self.Bottom1 = DisplayRegion1.getBottom()
      
      self.Left2 = DisplayRegion2.getLeft()
      self.Right2 = DisplayRegion2.getRight()
      self.Top2 = DisplayRegion2.getTop()
      self.Bottom2 = DisplayRegion2.getBottom()
      
      self.Left3 = DisplayRegion3.getLeft()
      self.Right3 = DisplayRegion3.getRight()
      self.Top3 = DisplayRegion3.getTop()
      self.Bottom3 = DisplayRegion3.getBottom()      
      
      self.sizing=False
      
      self.mx,self.my=0,0
      self.mousepos =(0,0)
      self.mouseposSizingStartX = 0
      self.mouseposSizingStartY = 0

      self.accept("mouse1",self.startSize)
      self.accept("mouse1-up",self.stopSize) 
                  
      taskMgr.add(self.DisplayRegionSizeTask,'DisplayRegionSizeTask')
      
   def startSize(self):
      # This function puts the camera into panning mode. 
      if (self.mouseWatcherNode.hasMouse()):
         self.mouseposSizingStartX = self.mouseWatcherNode.getMouse()[0]
         self.mouseposSizingStartY = self.mouseWatcherNode.getMouse()[1]
         
         self.Left1 = self.DisplayRegion1.getLeft()
         self.Right1 = self.DisplayRegion1.getRight()
         self.Top1 = self.DisplayRegion1.getTop()
         self.Bottom1 = self.DisplayRegion1.getBottom()
         
         self.Left2 = self.DisplayRegion2.getLeft()
         self.Right2 = self.DisplayRegion2.getRight()
         self.Top2 = self.DisplayRegion2.getTop()
         self.Bottom2 = self.DisplayRegion2.getBottom()
         
         self.Left3 = self.DisplayRegion3.getLeft()
         self.Right3 = self.DisplayRegion3.getRight()
         self.Top3 = self.DisplayRegion3.getTop()
         self.Bottom3 = self.DisplayRegion3.getBottom()
         
         self.sizing=True
   def stopSize(self):
      # This function puts the camera into panning mode.      
      self.sizing=False
      # Sets the panning variable to false to designate second panning condition as off.
   
   def DisplayRegionSizeTask(self,task):
      if (self.mouseWatcherNode.hasMouse()and 
          (not(self.mouseWatcherNode1.hasMouse()or
               self.mouseWatcherNode2.hasMouse() or
               self.mouseWatcherNode3.hasMouse()))):
         if self.sizing:        
            mpos = self.mouseWatcherNode.getMouse()
            self.mousepos=self.mouseWatcherNode.getMouse()
            DeltaX=self.mouseposSizingStartX-mpos.getX()
            DeltaY=self.mouseposSizingStartY-mpos.getY()
            dr1r = self.Right1-DeltaX/2
            dr2l = self.Left2-DeltaX/2
            dr2b = self.Bottom2-DeltaY/2
            dr3l = self.Left3-DeltaX/2
            dr3t = self.Top3-DeltaY/2
            if dr1r <=0 : dr1r = 0.0001
            if dr2l <=0 : dr2l = 0.0001
            if dr2b <=0 : dr2b = 0.0001
            if dr3t <=0 : dr3t = 0.0001
            if dr1r >=0.999 : dr1r = 0.99
            if dr2l >=0.999 : dr2l = 0.99
            if dr3l >=0.999 : dr3l = 0.99
            if dr2b >=1 : dr2b = 0.9999
            if dr3t >=1 : dr3t = 0.9999            
            self.DisplayRegion1.setDimensions(self.Left1,dr1r,self.Bottom1,self.Top1)
            self.DisplayRegion2.setDimensions(dr2l,self.Right2,dr2b,self.Top2)
            self.DisplayRegion3.setDimensions(dr3l,self.Right3,self.Bottom3,dr3t)
            dr1h = float(self.DisplayRegion1.getPixelHeight())
            dr2h = float(self.DisplayRegion2.getPixelHeight())
            dr3h = float(self.DisplayRegion3.getPixelHeight())
            if dr1h <= 0 : dr1h = 0.01
            if dr2h <= 0 : dr2h = 0.01
            if dr3h <= 0 : dr3h = 0.01            
            AspectRatio1 = (self.DisplayRegion1.getPixelWidth()/dr1h)
            AspectRatio2 = (self.DisplayRegion2.getPixelWidth()/dr2h)
            AspectRatio3 = (self.DisplayRegion3.getPixelWidth()/dr3h)
            self.lens1.setAspectRatio(AspectRatio1)
            self.lens2.setAspectRatio(AspectRatio2)
            self.lens3.setAspectRatio(AspectRatio3)
      return task.cont
      
      