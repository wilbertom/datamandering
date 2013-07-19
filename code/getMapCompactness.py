from PyQt4.QtCore import *
from shapely.wkb import loads
from shapely import *
from shapely.geometry import MultiLineString
from shapely.geometry import MultiPoint
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.geometry import MultiPoint
from shapely.ops import cascaded_union
from shapely.geometry.polygon import LinearRing
import math 

groups=[]
districts=[]

infile=open('../data/block_neighbor_fixed.csv').read().split('\n')

infile=infile[1:]
pi4=math.pi*4

while len(infile[-1])<2:
	infile=infile[:-1]

for token in infile:
	token=token.split('\t')
	print token[0]
	if token[0]!='7296' and token[0]!='9670':
		shape_list=token[-1].split(' ')
		points=[]
		for point_token in shape_list:
			point_token=point_token.split(',')
			points.append( ( float(point_token[0]),float(point_token[1]) ) )
		# points is a list of (x, y) tuples
		#print points
		groups.append(Polygon(points))
	else:
		groups.append(0)


map_infile=open("../data/all_maps.txt").read().split('\n')
outfile_compact=open("compact.txt","w")

for x in xrange(0,10000):

	district=[]
	for token in xrange(0,59):
		district.append([])

	temp=map_infile[x].split('\t')
	while ''==temp[-1]:
		temp=temp[:-1]
	
	#go through each block and add it to the district
	for y in xrange(0,len(temp)):
		#print str(y),str(temp[y]),len(temp)
		if y!=7295 and y!=9669:
			district[int(temp[y])].append(groups[y])

	#merge all polygons in the district
	compact=0

	for x2 in xrange(0,59):
		m = MultiPolygon(district[int(x2)])
		n = cascaded_union(m)
		compact+=n.area/n.length**2/pi4
		
	outfile_compact.write(str(x)+'\t'+str(compact/59.0)+'\n')	
	
