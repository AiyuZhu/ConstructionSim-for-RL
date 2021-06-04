# IMPORT PYGAME AND OPENGL
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# IMPORT PYGAME MENU
import PygameMenus
# from pygameMenu.locals import *n

# IMPORT CLASSES
import BIMClass.Site.siteOnly_multi_tar as Site

# IMPORT GUI

import sys
import time

def main():
    # INIT PYGAME
    pygame.init()
    display = (1200, 800)

    # INIT PYGAME DISPLAY AND OPENGL
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(25, display[0] / display[1], 0.1, 50.0)
    glClearColor(1, 1, 1, 1)
    glTranslate(1, 0, -5)
    glRotatef(35, 1, 0, 0)
    glOrtho(0, 1000, 0, 1000, 0, 1000)
    glEnable(GL_DEPTH_TEST)

    # RENDER POSITION
    rotate_x = 0
    rotate_y = 0
    translate_x = 0
    translate_y = 0
    z_position = 0

    # MOUSE INPUTS
    mouse_rotate = False
    mouse_move = False

    # CREATE 3D ENV
    siteEnv = Site.site(15,15,8)

    # MAIN GAME LOOP
    pygame.key.set_repeat(16, 100)
    in_game = True
    open_map = False
    show_steps = True

    while in_game:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_rotate = True
                elif event.button == 3:
                    mouse_move = True
                elif event.button == 5:
                    translate_y -= 50
                elif event.button == 4:
                    translate_y += 50
            elif event.type == MOUSEBUTTONUP:
                mouse_rotate = False
                mouse_move = False
            elif event.type == MOUSEMOTION:
                i, j = event.rel
                if mouse_move:
                    translate_x += i
                    translate_y += j
                elif mouse_rotate:
                    rotate_x += i
                    rotate_y += j
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    z_position -= 50
                elif event.key == K_DOWN:
                    z_position += 50
                elif event.key == K_LEFT:
                    translate_x -= 50
                elif event.key == K_RIGHT:
                    translate_x += 50
                elif event.key == 113:
                    rotate_x -= 50
                elif event.key == 101:
                    rotate_x += 50
                if event.key == K_w:
                    siteEnv.sco_action("forward")
                elif event.key == K_a:
                    siteEnv.sco_action("left")
                elif event.key == K_s:
                    siteEnv.sco_action("back")
                elif event.key == K_d:
                    siteEnv.sco_action("right")
                elif event.key == K_u:
                    siteEnv.sco_action("up")
                elif event.key == K_n:  # 115
                    siteEnv.sco_action("down")
                # elif event.key == K_i:  #
                #     siteEnv.sco_action("change_dir")
                # elif event.key == K_o:  #
                #     siteEnv.sco_action("erect2")
                # elif event.key == K_y:  #
                #     siteEnv.sco_action("layf")
                # elif event.key == K_h:  #
                #     siteEnv.sco_action("layb")
                # elif event.key == K_g:  #
                #     siteEnv.sco_action("layl")
                # elif event.key == K_j:  #
                #     siteEnv.sco_action("layr")
                # elif event.key == K_1:
                #     siteEnv.sco_action("rotate1")
                # elif event.key == K_2:
                #     siteEnv.sco_action("rotate2")
                # elif event.key == K_3:
                #     siteEnv.sco_action("rotate3")
                # elif event.key == K_4:
                #     siteEnv.sco_action("rotate4")
                # elif event.key == K_5:
                #     siteEnv.sco_action("assembly_node1")
                # elif event.key == K_6:
                #     siteEnv.sco_action("assembly_node2")
                if event.key == K_SPACE:
                    # if siteEnv.sco.working == True and siteEnv.sco.arrived == False:
                    #     siteEnv = Site.site(15, 15, 8)

                    siteEnv.switch_sco("switch")




                if open_map == True:
                    print(siteEnv.print_map())

                if show_steps == True:
                    if siteEnv.sco.type == 'beam':
                        print("SCO id: {}, step is {}, component crash is {}, component arrive is {}, component node 1 assembly is {}, component node 2 assembly is {}, componenet working is {}, component wrong work is {}, check arrive is  {}, check lock is {}".format(siteEnv.sco.id, siteEnv.sco.steps, siteEnv.sco.crash, siteEnv.sco.arrived, siteEnv.sco.node1_assembly, siteEnv.sco.node2_assembly, siteEnv.sco.working, siteEnv.sco.wrong_work, siteEnv.sco.check_arrive, siteEnv.sco.lock))
                    elif siteEnv.sco.type == 'column':
                        print("SCO id: {}, step is {}, component crash is {}, component arrive is {}, component node 1 assembly is {}, component node 2 assembly is {}, componenet working is {}, component wrong work is {}, check lock is {}".format(siteEnv.sco.id, siteEnv.sco.steps, siteEnv.sco.crash, siteEnv.sco.arrived, siteEnv.sco.node1_assembly, siteEnv.sco.node2_assembly, siteEnv.sco.working, siteEnv.sco.wrong_work, siteEnv.sco.lock))
                    # print('node1 is {}, node2 is {}'.format(siteEnv.sco.node1, siteEnv.sco.node2,))


        if siteEnv.sco.crash:

            # print("erect coll", siteEnv.sco.collision_e)
            siteEnv = Site.site(15, 15, 8)

        arrived_count = 0
        for _ in siteEnv.scos:
            if _.arrived == True:
                arrived_count += 1
                if arrived_count == 3:
                    siteEnv = Site.site(15, 15, 8)
                    print("Great job! You build it")
            # time.sleep(5)
            # siteEnv = Site.site(15, 15, 6)


        if in_game:

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            if siteEnv.sco.steps == 0:
                siteEnv.sco.working = False
            elif siteEnv.sco.steps != 0:
                siteEnv.sco.working = True
            draw_site(siteEnv)

            # TRANSLATE OBJECT IF MOUSE MOVED
            glTranslatef(translate_x, translate_y, -z_position)
            glRotatef(rotate_y / 20., 1, 0, 0)
            glRotatef(rotate_x / 20., 0, 1, 0)

            # RESET ROTATE
            rotate_x = 0
            rotate_y = 0
            translate_x = 0
            translate_y = 0
            z_position = 0
            pygame.display.flip()
        else:
            pygame.quit()


def draw_site(site):
    # Get Center Point Of The Map
    # For good view position
    center_x = len(site.site_3D[0][0]) / 2
    center_y = len(site.site_3D[0]) / 2
    # print("Center X: {}\nCenter Y: {}\nCenter Z:{}".format(center_x,center_y,center_z))

    # Set Cube Size
    Cube_Size = 100
    all_space = False

    # Draw site
    for k in range(len(site.site_3D)):
        # draw ground
        if k == 0:
            for i in range(len(site.site_3D[0])):
                for j in range(len(site.site_3D[0][0])):
                    if site.site_3D[0][i][j] != 50 and site.site_3D[0][i][j] != 'foundation':
                        draw_cube((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 10)
                        draw_plane((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 10)
                    elif site.site_3D[0][i][j] == 50:
                        draw_cube((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 50)
                        draw_plane((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 10)
                    elif site.site_3D[0][i][j] == 'foundation':
                        draw_cube((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 'foundation')
                        draw_plane((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 10)
        # draw component and other
        if k != 0:
            #draw target
            for sco in site.scos:
                draw_plane((sco.y_tar_1 - center_x) * Cube_Size, (sco.z_tar_1 - 1) * Cube_Size,
                           (sco.x_tar_1 - center_y) * -Cube_Size,
                           Cube_Size, 5)
                draw_plane((sco.y_tar_2 - center_x) * Cube_Size, (sco.z_tar_2 - 1) * Cube_Size,
                           (sco.x_tar_2 - center_y) * -Cube_Size,
                           Cube_Size, 5)
                if sco.length > 2:
                    if sco.x_tar_1 > sco.x_tar_2:
                        for x_len in range(abs(sco.x_tar_1 - sco.x_tar_2) - 1):
                            draw_plane((sco.y_tar_2 - center_x) * Cube_Size, (sco.z_tar_2 - 1) * Cube_Size,
                                       (sco.x_tar_2 + x_len + 1 - center_y) * -Cube_Size,
                                       Cube_Size, 5)
                    elif sco.x_tar_2 > sco.x_tar_1:
                        for x_len in range(abs(sco.x_tar_2 - sco.x_tar_1) - 1):
                            draw_plane((sco.y_tar_1 - center_x) * Cube_Size, (sco.z_tar_1 - 1) * Cube_Size,
                                       (sco.x_tar_1 + x_len + 1 - center_y) * -Cube_Size,
                                       Cube_Size, 5)
                    elif sco.y_tar_1 > sco.y_tar_2:
                        for x_len in range(abs(sco.y_tar_1 - sco.y_tar_2) - 1):
                            draw_plane((sco.y_tar_2 + x_len + 1 - center_x) * Cube_Size, (sco.z_tar_2 - 1) * Cube_Size,
                                       (sco.x_tar_2 - center_y) * -Cube_Size,
                                       Cube_Size, 5)
                    elif sco.y_tar_2 > sco.y_tar_1:
                        for x_len in range(abs(sco.y_tar_2 - sco.y_tar_1) - 1):
                            draw_plane((sco.y_tar_1 + x_len + 1 - center_x) * Cube_Size, (sco.z_tar_1 - 1) * Cube_Size,
                                       (sco.x_tar_1 - center_y) * -Cube_Size,
                                       Cube_Size, 5)
                    elif sco.z_tar_1 > sco.z_tar_2:
                        for z_len in range(sco.length - 2):
                            draw_plane((sco.y_tar_1 - center_x) * Cube_Size, (sco.z_tar_2 + z_len) * Cube_Size,
                                       (sco.x_tar_1 - center_y) * -Cube_Size,
                                       Cube_Size, 5)
                    elif sco.z_tar_2 > sco.z_tar_1:
                        for z_len in range(sco.length - 2):
                            draw_plane((sco.y_tar_1 - center_x) * Cube_Size, (sco.z_tar_1 + z_len) * Cube_Size,
                                       (sco.x_tar_1 - center_y) * -Cube_Size,
                                       Cube_Size, 5)

            # draw component
            for i in range(len(site.site_3D[0])):
                for j in range(len(site.site_3D[0][0])):
                    if site.site_3D[k][i][j] == 0:
                        if all_space is True:
                            draw_plane((j - center_x) * Cube_Size, (k-1) * Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 1)
                    if site.site_3D[k][i][j] == 1:
                        draw_cube((j - center_x) * Cube_Size,  (k-1)*Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 1)
                        draw_plane((j - center_x) * Cube_Size, (k - 1) * Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 1)
                    if site.site_3D[k][i][j] == 2:
                        draw_cube((j - center_x) * Cube_Size,  (k-1)*Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 2)
                        draw_plane((j - center_x) * Cube_Size, (k - 1) * Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 2)
                    if site.site_3D[k][i][j] == 100:
                        draw_cube((j - center_x) * Cube_Size,  (k-1)*Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 100)
                        draw_plane((j - center_x) * Cube_Size, (k - 1) * Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 1)
                    if site.site_3D[k][i][j] == 200:
                        draw_cube((j - center_x) * Cube_Size,  (k-1)*Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 200)
                        draw_plane((j - center_x) * Cube_Size, (k - 1) * Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 1)

                    # draw fid
                    if site.site_3D[k][i][j] == 'fid':
                        draw_cube((j - center_x) * Cube_Size,  (k-1)*Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 'fid')

                    # draw init place
                    if site.site_3D[k][i][j] == 3:
                        draw_plane((j - center_x) * Cube_Size, (k - 1) * Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 3)




def draw_cube(centerPosX, centerPosY, centerPosZ, edgeLength,type):
    halfSideLength = edgeLength * 0.5
    vertices = (
        # front face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # back face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom left

        # left face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # right face
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # top face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # top face
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength  # bottom left
    )

    # OLD RENDER (POLYGONS)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # NEW RENDER (GL_QUADS)
    glBegin(GL_QUADS)

    if type == 10:
        glColor3f(0.75, 0.75, 0.75)
    elif type == 50:
        glColor3f(0, 0.7, 0.7)
    elif type == 1:
        glColor3f(1, 0.65, 0)
    elif type == 100:
        glColor3f(0, 1, 0)
    elif type == 200:
        glColor3f(1, 0.1, 1)
    elif type == 2:
        glColor3f(0, 0, 1)
    elif type == 'foundation':
        glColor3f(1, 0.5, 1)
    elif type == 'fid':
        glColor3f(0, 0, 0)


    # FOR EVERY VERTICES
    for x in range(24):
        glVertex3f(vertices[x * 3], vertices[x * 3 + 1], vertices[x * 3 + 2])
    glColor3f(0.5, 0.5, 0.5)
    glEnd()



def draw_plane(centerPosX, centerPosY, centerPosZ, edgeLength, type):
    halfSideLength = edgeLength * 0.5
    vertices = (
        # front face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # back face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom left

        # left face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # right face
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # top face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # top face
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength  # bottom left
    )

    # OLD RENDER (POLYGONS)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    if type == 10:
        glLineWidth(2)
        glColor3f(0, 0, 0)
    elif type == 1:
        glLineWidth(0.1)
        glColor3f(0.9, 0.9, 0.9)
        # glLineStipple(10, 0x5555)
    elif type == 3:
        glColor3f(1, 0.65, 0)
    elif type == 5:
        glLineWidth(2)
        glColor3f(1, 0.1, 1)
    elif type == 100:
        glColor3f(0, 1, 0)


    glEnableClientState(GL_VERTEX_ARRAY)
    # glEnable(GL_LINE_STIPPLE)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glDrawArrays(GL_QUADS, 0, 24)
    glDisableClientState(GL_VERTEX_ARRAY)


if __name__ =="__main__":
    main()