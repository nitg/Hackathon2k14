#oggpnosn
#hkhr
# Problem Set 11: Simulating robots
# Name:Tanay
# Collaborators:
# Time:
import ps11_visualize as viz
import math
import random
import pylab
# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width=width
        self.height=height
        tile_position=[(x,y) for x in range(0,width) for y in range(0,height)]
        self.tiles={}
        for pos in tile_position:
            self.tiles[pos]=False
                                
        # TODO: Your code goes here
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x=int(pos.getX())
        y=int(pos.getY())
        self.tiles[(x,y)]=True
                    
        # TODO: Your code goes here
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[(m,n)]

        # TODO: Your code goes here
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width*self.height
        # TODO: Your code goes here
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        count=0        
        for pos in self.tiles:
            if self.tiles[pos]==True:
                count+=1
        return count
        # TODO: Your code goes here
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.randrange(0,width),random.randrange(0,heigth))
        # TODO: Your code goes here
    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        return 0<=pos.getX()<=self.width and 0<=pos.getY()<=self.height        
        # TODO: Your code goes here


class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """

        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        
        self.speed=speed
        self.d=random.randrange(0,360)
        self.position=Position(random.randrange(0,room.width),random.randrange(0,room.height))
        self.room=room
        # TODO: Your code goes here
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
        # TODO: Your code goes here
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.d
        # TODO: Your code goes here
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position=position
        # TODO: Your code goes here
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        # TODO: Your code goes here

        self.d=direction

class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # TODO: Your code goes here
        newPos=self.getRobotPosition().getNewPosition(self.d,self.speed)
        if self.room.isPositionInRoom(newPos):
            self.setRobotPosition(newPos)        
        else:
            self.setRobotDirection(random.randrange(0,360))
        self.room.cleanTileAtPosition(self.position)
        
        
# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    lol=[]
    
    for i in range(num_trials):
        lol.append([])#;print lol
        room=RectangularRoom(width,height)
        bots=[robot_type(room,speed) for k in range(num_robots)]
        percentage_cleaned=0
        if visualize==True:anim=viz.RobotVisualization(num_robots,width,height)
        while(percentage_cleaned<min_coverage):
            for j in range(num_robots):
                bots[j].updatePositionAndClean()
            percentage_cleaned=float(room.getNumCleanedTiles())/room.getNumTiles()  
            lol[i].append(percentage_cleaned)
            if visualize==True:anim.update(room,bots)
    if visualize==True:anim.done()
    return lol    

    # TODO: Your code goes here

# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means
def mean(l):
    mn=0
    for i in l:
        mn+=i
    return mn/float(len(l))

def conv(lol):
    lol=[len(l) for l in lol]
    return mean(lol)
        
        
# === Problem 4
def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    times=[]
    area=[]
    for i in range(5,30,5):
        area.append(i*i)
        lol=runSimulation(1,1.0,i,i,.75,60,Robot,False)    
        lol=[len(l) for l in lol]
        times.append(mean(lol))
    print times,area
    pylab.plot(area,times)
    pylab.title("Time Vs Area")
    pylab.xlabel("Area")
    pylab.ylabel("Time Taken")
    pylab.show()
    

    
    # TODO: Your code goes here
#showPlot1()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    # TODO: Your code goes here
    times=[]
    bots=[]
    for i in range(1,11,1):
        bots.append(i)
        lol=runSimulation(i,1,25,25,.75,10,Robot,False)
        lol=[len(l) for l in lol]
        times.append(mean(lol))
#    print times,bots
    pylab.title("Time Vs No of bots")
    pylab.xlabel("No of Bots")
    pylab.ylabel("Time Taken")
    pylab.plot(bots,times)
    pylab.show()

#showPlot2()

def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    # TODO: Your code goes here
    ratio=[1,25.0/16,4,25.0/4,25]
    times=[]
    times.append(conv(runSimulation(1,1,20,20,.75,10,Robot,False)))
    times.append(conv(runSimulation(1,1,25,16,.75,10,Robot,False)))
    times.append(conv(runSimulation(1,1,40,10,.75,10,Robot,False)))
    times.append(conv(runSimulation(1,1,50,8,.75,10    ,Robot,False)))
    times.append(conv(runSimulation(1,1,80,5,.75,10,Robot,False)))
    pylab.title("Time Vs Ratio")
    pylab.xlabel("Ratio")
    pylab.ylabel("Time Taken")
    pylab.plot(ratio,times)
    pylab.show()
#showPlot3()    
def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    # TODO: Your code goes here
    times=[]
    for i in  range(1,6):
        cents=[]
        times=[]
        for cent in range(80,101,30):
            print "Running Simulation for",i,"robots and",cent,"percent cleaning"
            lol=runSimulation(i,1,25,25,cent,10,Robot,False)
            times.append(conv(lol))
            cents.append(cent)
        pylab.plot(cents,times)
    pylab.xlabel("Percentage Cleaned")
    pylab.ylabel("Time Taken")
    pylab.title("Cleaning Time vs Percentage Cleaned")
    pylab.show()

#showPlot4()
# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    def updatePositionAndClean(self):
        self.setRobotDirection(random.randrange(0,360))
        newPos=self.getRobotPosition().getNewPosition(self.d,self.speed)
        if self.room.isPositionInRoom(newPos):
            self.setRobotPosition(newPos)        
        else:
            self.setRobotDirection(random.randrange(0,360))
        self.room.cleanTileAtPosition(self.position)

# === Problem 6
import matplotlib.pyplot as plt 

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    # TODO: Your code goes here
    typs=[Robot,RandomWalkRobot]
    p=[]
    TRIALS=20
    for typ in typs:
        times=[]
        area=[]
        plt.xlabel("Area")
        plt.ylabel("Times")
        plt.title("Times vs Area")
        for i in range(1,20,1):
            lol=runSimulation(i,1,25,25,.75,TRIALS,typ,False)
            times.append(conv(lol))
            area.append(i)
        p,=plt.plot(area,times)
    plt.legend([p],["RandomWalkRobot"])    
    plt.show()
showPlot5()
