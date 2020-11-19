'''
Authors:    Yongyang Liu <liuyongyang@gatech.edu>
            
Date:       3 Oct 2020
'''

import pygame

def Display(Obst, Start, Goal, tree, path, size):
    
    # color
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 200, 0)
    RED = (255, 0, 0)
    PURPLE = (128,0,128)
    
    # initialize pygame screen
    pygame.init()
    screen = pygame.display.set_mode([size*10, size*10])
    pygame.display.set_caption("Path Following")
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    clock.tick(100)
    screen.fill(WHITE)
    for i in range(5):
        pygame.draw.circle(screen, BLACK, (Obst[i,0]*10,Obst[i,1]*10), Obst[i,2]*10)
    pygame.draw.circle(screen, GREEN, (Start[0,0]*10,Start[0,1]*10), 1*10)
    pygame.draw.circle(screen, BLUE, (Goal[0,0]*10,Goal[0,1]*10), 5*10)
    pygame.display.update()
    
    # draw rrt graph
    for node in tree.nodes:
        for neighbour in node.neighbours:
            pygame.draw.line(screen, PURPLE, [node.pos.x, node.pos.y], [neighbour.pos.x, neighbour.pos.y])
        pygame.display.update()
    
    # draw optimal path
    pygame.draw.lines(screen, RED, False, path, 2)
    pygame.display.update()
    pygame.image.save(screen,'RRT_50Hz.jpeg')
	
    input("Press Enter to quit")
    pygame.quit()

    
