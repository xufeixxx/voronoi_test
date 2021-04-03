from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import matplotlib.pyplot as plt
import random
from overall.settings import Settings
from overall.list import point_list, voronoiCell_list, vertex_list, ridge_list
from entity.point import Point
from entity.vertex import Vertex
from entity.edge import Ridge
from entity.voronoiCell import VoronoiCell

setts = Settings()


class Function:

    def __init__(self, vor):
        self.vor = vor

    def make_vertices(self):
        i = 1
        for vertex in self.vor.vertices:
            vertex_list.append(Vertex(i, vertex[0], vertex[1]))
            i += 1

    def make_ridges(self):
        for ridge in self.vor.ridge_vertices:
            if ridge[0] != -1 and ridge[1] != -1:
                ridge_list.append(Ridge(ridge[0] + 1, ridge[1] + 1))

    def make_voronoiCells(self):
        k = 1
        for region in self.vor.regions:
            if len(region) != 0 and exist_negative_one(region) is False:
                voronoiCell = VoronoiCell(k)
                num = 0
                for i in range(len(region)):
                    voronoiCell.ridge_list.append([region[i] + 1, region[(i + 1) % len(region)] + 1])
                    vertex = from_vId_find_vertex(region[i] + 1)
                    voronoiCell.polyX.append(vertex.v_x)
                    voronoiCell.polyY.append(vertex.v_y)
                    if i == 0:
                        voronoiCell.maxX = vertex.v_x
                        voronoiCell.maxY = vertex.v_y
                        voronoiCell.minX = vertex.v_x
                        voronoiCell.minY = vertex.v_y
                    else:
                        if voronoiCell.maxX < vertex.v_x:
                            voronoiCell.maxX = vertex.v_x
                        if voronoiCell.maxY < vertex.v_y:
                            voronoiCell.maxY = vertex.v_y
                        if voronoiCell.minX > vertex.v_x:
                            voronoiCell.minX = vertex.v_x
                        if voronoiCell.minY > vertex.v_y:
                            voronoiCell.minY = vertex.v_y
                    num += 1
                voronoiCell.polySides = num
                k += 1
                voronoiCell_list.append(voronoiCell)

    def show(self):
        voronoi_plot_2d(self.vor)
        plt.show()


def make_points():
    for i in range(setts.point_num):
        x = random.randint(setts.map_width[0], setts.map_width[1])
        y = random.randint(setts.map_length[0], setts.map_length[1])
        point = Point(i + 1, x, y)
        point_list.append(point)


def make_voronoi():
    xy_list = np.empty((0, 2))
    for point in point_list:
        xy_list = np.append(xy_list, [[point.p_x, point.p_y]], axis=0)
    return Voronoi(xy_list)


def exist_negative_one(list):
    for i in list:
        if i == -1:
            return True
    return False


def from_vId_find_vertex(v_id):
    for v in vertex_list:
        if v.v_id == v_id:
            return v


def point_in_notIn_polygon(x, y, voronoiCell):  # 此算法从网上获得https://blog.csdn.net/hjh2005/article/details/9246967，经实验当点位于v图的边的时候一定程度上，位于左侧边上判定为在v图之内，右侧边判定之外
    j = voronoiCell.polySides - 1
    oddNodes = False
    for i in range(voronoiCell.polySides):
        if voronoiCell.polyY[i] < y <= voronoiCell.polyY[j] or voronoiCell.polyY[i] >= y > voronoiCell.polyY[j]:
            if voronoiCell.polyX[i] + (y - voronoiCell.polyY[i]) / (voronoiCell.polyY[j] - voronoiCell.polyY[i]) * (
                    voronoiCell.polyX[j] - voronoiCell.polyX[i]) <= x:
                oddNodes = not oddNodes

        j = i

    return oddNodes


def point_in_which_VCell(x, y):  # 返回维诺格的id
    for voronoiCell in voronoiCell_list:
        if point_in_notIn_polygon(x, y, voronoiCell):
            return voronoiCell.vc_id
    return 0
# 返回0代表不在任何一个维诺格中，此点在实验中应该被舍弃，形参x， y是用户的位置数据


def make_randNum_in_vCell(voronoiCell):
    x = random.uniform(voronoiCell.minX, voronoiCell.maxX)
    y = random.uniform(voronoiCell.minY, voronoiCell.maxY)
    if point_in_notIn_polygon(x, y, voronoiCell):
        return x, y
    else:
        make_randNum_in_vCell(voronoiCell)