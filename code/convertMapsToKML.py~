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
import random 
import zipfile
import os
import sys

groups=[]
districts=[]
rand_style=['PolyStyle00','PolyStyle01','PolyStyle02','PolyStyle03','PolyStyle04','PolyStyle05','PolyStyle06','PolyStyle07']
infile=open('/home/john/gerry/block_neighbor_fixed.csv').read().split('\n')

infile=infile[1:]

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

for x in xrange(0,10000):
	name="../outdir/map_"+str(x)
	outfile_kml=open(name+".kml","w")
	outfile_kml.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document id="%s">\n  <name>%s</name>\n  <Snippet></Snippet>\n  <Folder id="FeatureLayer0">\n    <name>%s</name>\n  <Snippet></Snippet>\n'%("map_"+str(x),"map_"+str(x),"map_"+str(x)))

	print x
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
	
	for x in xrange(0,59):
		m = MultiPolygon(district[int(x)])
		n = cascaded_union(m)
		coords=''	
		for token in list(n.exterior.coords):
			#print token[0]
			outfile.write(str(token[0])+','+str(token[1])+' ')
			coords+=str(token[0])+','+str(token[1])+' '
		outfile.write(':')
		kml_buffer="<Placemark>\n\t<name>%s</name>\n\t<styleUrl>#%s</styleUrl>\n\t<Snippet></Snippet>\n\t<description>\n\t</description>\n\t<MultiGeometry>\n\t<Polygon>\n\t\t<outerBoundaryIs><LinearRing><coordinates> %s \n\t\t</coordinates></LinearRing></outerBoundaryIs>\n\t</Polygon>\n\t</MultiGeometry>\n</Placemark>\n"% (str(x+1),rand_style[random.randint(0,7)],coords)
		outfile_kml.write(kml_buffer)
	outfile_kml.write('</Folder>\n  <Style id="PolyStyle00">\n    <LabelStyle>\n      <color>00000000</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.500000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1eA0A0A0</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle01">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.500000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e1400AA</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle02">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e1478A0</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle03">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e78A000</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle04">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e785A00</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle05">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e784678</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle06">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1eC87878</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle07">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e003C14</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle08">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.500000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e1400AA</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle09">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e1478A0</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle10">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e78A000</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle11">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e785A00</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle12">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e784678</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle13">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1eC87878</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle14">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e003C14</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n')	
	outfile_kml.write('<Style id="PolyStyle15">\n    <LabelStyle>\n      <color>640A0A0A</color>\n      <scale>0.000000</scale>\n    </LabelStyle>\n    <LineStyle>\n      <color>640A0A0A</color>\n      <width>1.5000000</width>\n    </LineStyle>\n    <PolyStyle>\n      <color>1e003C14</color>\n      <outline>1</outline>\n    <fill>1</fill>\n	</PolyStyle>\n  </Style>\n</Document>\n</kml>\n')	
	outfile.write('\n')
	outfile_kml.close()
	# open the zip file for writing, and write stuff to it

	zipit = zipfile.ZipFile(name+".kmz", "w")
	zipit.write(name+".kml", os.path.basename(name+".kml"), zipfile.ZIP_DEFLATED)
	os.system('rm '+name+".kml")



