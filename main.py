from func.function import make_points, make_voronoi
from overall.list import point_list, vertex_list, voronoiCell_list, ridge_list
from func.function import Function, from_vId_find_vertex, point_in_which_VCell, make_randNum_in_vCell

make_points()
vor = make_voronoi()
func = Function(vor)
func.make_vertices()
func.make_ridges()
func.make_voronoiCells()
x, y = make_randNum_in_vCell(voronoiCell_list[1])
func.show()
print("hello world")

# i = 0
# for reg in vor.regions:
#     for k in reg:
#         if k == -1:
#             i += 1
# print(i/(len(vor.regions)-1))
# sdpoobpsdbsd