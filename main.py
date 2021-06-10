import pygame
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
RED, GREEN, BLUE, PURPLE = (255, 0, 0), (0, 255, 0), (0, 0, 128), (153, 0, 153)
HEIGHT, WIDTH, SIZE = 600, 600, 15
start, end = None, None
impassable = set()
ready = True

class Node():
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.parent = None
        self.h = 0
        self.g = 0
        self.f = 0
    
    def setG(self, g):
        self.g = g
        self.f = self.g + self.h
    
    def setH(self, h):
        self.h = h
        self.f = self.g + self.h
  
def createPath(node):    
    l = [node]
    current = node
    while current.parent != None:
        fillSquare(current.x, current.y, PURPLE)
        l.append(current.parent)
        current = current.parent
    fillSquare(current.x, current.y, PURPLE)
    l.reverse()
    return l
        
def search(graph, a, b):
    openSet = [a]
    closedSet = []
    neighbours = {(-1, 0), (0, 1), (0, -1), (1, 0), (-1, -1), (1, 1), (1, -1), (-1, 1)}
    while openSet:
        node = min(openSet, key = lambda k: k.f)        
        openSet.remove(node)
        closedSet.append(node)
        fillSquare(node.x, node.y, RED)
        pygame.time.wait(5)
        if node.x == b.x and node.y == b.y:
            return createPath(node)
        for x, y in neighbours:
            num = 14 if x and y else 10              
            x2, y2 = node.x + x, node.y + y
            if 0 <= x2 < len(graph) and 0 <= y2 < len(graph[0]):                
                n = graph[x2][y2]
                if n.value == 0 or n in closedSet:
                    continue
                elif n in openSet:
                    newG = node.g + num
                    if newG < n.g:
                        n.setG(newG)
                        n.parent = node
                else:
                    n.parent = node
                    n.setG(n.parent.g + num)
                    xdiff, ydiff = abs(b.x - x2), abs(b.y - y2)
                    diagonal, straight = min(xdiff, ydiff), abs(xdiff - ydiff)
                    n.setH(diagonal * 14 + straight * 10)                
                    openSet.append(n)
                    fillSquare(n.x, n.y, GREEN)
                    pygame.time.wait(5)
    
    print("NO PATH FOUND")                    
    return []

def findPath():
    x1, y1 = start
    x2, y2 = end
    grid = []
    
    for x in range(WIDTH//SIZE):
        grid.append([])
        for y in range(HEIGHT//SIZE):
            num = 0 if (x, y) in impassable else 1                
            grid[x].append(Node(num, x, y))
    
    path = search(grid, grid[x1][y1], grid[x2][y2])   
    print("SHORTEST PATH:", len(path))

def initialize():
    global ready, start, end, impassable
    start, end, impassable = None, None, set()
    screen.fill(WHITE)    
    for i in range(0, WIDTH, SIZE):
        for j in range(0, HEIGHT, SIZE):
            rect = pygame.Rect(i, j, SIZE, SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
    pygame.display.flip()        
    ready = True    
     
def fillSquare(col, row, color):
    rect = pygame.Rect(col * SIZE, row * SIZE, SIZE, SIZE)
    screen.fill(color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    pygame.display.flip()

def onClick():
    mpos_x, mpos_y = event.pos 
    col, row = mpos_x // SIZE, mpos_y // SIZE   
    global start, end, impassable 
    
    if start == (col, row) or end == (col, row):
        return     
    
    if not start:
        color = BLUE
        start = (col, row) 
    elif not end:
        color = BLUE
        end = (col, row)   
    else:
        color = BLACK
        impassable.add((col, row))   
        
    fillSquare(col, row, color)
    
  
            
if __name__ == "__main__":
    
    pygame.init() 
    # Set up the drawing window
    screen = pygame.display.set_mode([HEIGHT, WIDTH])
    initialize()
    # Run until the user asks to quit
    running = True
    while running:
    
        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if pygame.mouse.get_pressed()[0] and ready:
                onClick()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and start and end and ready: 
                    ready = False
                    findPath()                    
                elif event.key == pygame.K_ESCAPE:
                    initialize()                   
                
    pygame.quit()
