from pyglet.gl import *
from pyglet.window import key
import sys
import os
import math
import random
import numpy as np

max_y=42.64801601
min_y=36.79879616
max_x=-87.35520766
min_x=-91.794212596

maps=[]
block_group=[]
color=[]
members=[]
random.seed(4)
for x in range(0,59):
	a=random.random()+0.1
	b=random.random()+0.1
	c=random.random()+0.1
	color.append([b,a,c])
	members.append([])
		

max_pop=220000
min_pop=210000

class group:
	Name="group"
	def __init__(self,ID,neighbors,pop,lat,lng,shape):

		self.ID=int(ID)-1
		self.neighbor=[]
		neighbors=neighbors.split(':')
		for token in neighbors:
			if len(token)>0:
				self.neighbor.append(int(token)-1)
				if int(token) == 0:
					print 'wft'
		self.district=-1
		self.pop=int(pop)
		self.y=float(lat)
		self.x=float(lng)
		shape=shape.split(' ')
		if len(shape[-1])<2:
			shape=shape[:-1]
		self.shape=shape
		self.reserved=False

class common:
	Name="common"
	def __init__(self):
		self.ID=[]

# Direct OpenGL commands to this window.
window = pyglet.window.Window(700,1000,resizable=True)
win_h=700
win_w=1000
taken=[]
taken_start=[]

temp_district_map=[]
def add_block( district,  block_id):
	global temp_district_map
	temp_district_map.append(block_id)
	for token in block_group[block_id].neighbor:
		if district==block_group[token].district and token not in temp_district_map:
			add_block(district,token)	

def check_contig(district):
	global temp_district_map
	temp_district_map=[]

	add_block(district,members[district][0])
	if len(members[district])==len(temp_district_map):
		return True
	else:
		#for token in members:
		#	if token not in temp_district_map:
		#		print str(token)+' ',
		#print '\n'
		return False

def even_out_map_high():

	global block_group
	global senate_start
	global senate_size
	global total_members
	global members

	itr2=0

	edge=[]
	for z in xrange(0,59):
		senate_size[z]=0;

	for token in block_group:
		senate_size[token.district]+=token.pop
	#-----init variables
	for x2 in xrange(0,59):
		edge.append(common())

	#-----find all the nodes that are on the boarder (have a neighbor with a different district)
	for block_num in xrange(0,len(block_group)): 
		
		for y2 in xrange(0,len(block_group[block_num].neighbor)):
			#-----if my neighbor has a different district then it is a possibility for a swap if a smaller district size
			if block_group[block_num].district!=block_group[block_group[block_num].neighbor[y2]].district and senate_size[block_group[block_num].district]>senate_size[block_group[block_group[block_num].neighbor[y2]].district]:
				#-----add that neigbor to the list of possible swap candidates for that district
				if block_group[block_num].neighbor[y2] not in edge[block_group[block_num].district].ID:
					edge[block_group[block_num].district].ID.append(block_group[block_num].neighbor[y2])

	wtf_itr=0
	uneven_high=True
	total_itr=0
	while uneven_high:
		#print itr2
		#go through each district
		total_itr+=1
		for x in xrange(0,59):

			#-----if the district population is too small than steal another districts
			if (senate_size[x]>max_pop and len(edge[x].ID)>0):

				#-----Let us pick a block to give at random
				temp_spot=0
				if len(edge[x].ID)==0:
					temp_spot=edge[x][0]
				else:
					temp_spot=edge[x].ID[random.randint(0, len(edge[x].ID)-1) ]

				receiving_district=block_group[temp_spot].district

				contiguous_tag=True
				#ok so we picked a neighbor so know let's give that neighbor one of me
				choices=[]
				for token in block_group[temp_spot].neighbor:
					if block_group[token].district==x:
						choices.append(token)

				if total_itr>10000:
					return False		

				if len(choices)==0:
					#print 'wtf...'
					#print 'neighbos '+str(len(block_group[temp_spot].neighbor))+ ' '+str(temp_spot)
					wtf_itr+=1
					if wtf_itr >1000:
						print 'wtd\'ed'
						return False

					edge=[]
					for x2 in xrange(0,59):
						edge.append(common())

					for x2 in xrange(0,len(block_group)):
						for y2 in xrange(0,len(block_group[x2].neighbor)):
							#-----if my neighbor has a different district then it is a possibility for a swap with a small size
							if block_group[x2].district!=block_group[block_group[x2].neighbor[y2]].district and senate_size[block_group[x2].district]>senate_size[block_group[block_group[x2].neighbor[y2]].district]:
								#-----add that neigbor to the list of possible swap candidates for that district
								if block_group[x2].neighbor[y2] not in edge[block_group[x2].district].ID:
									edge[block_group[x2].district].ID.append(block_group[x2].neighbor[y2])

					break

				else:
					temp_spot=choices[random.randint(0, len(choices)-1) ]

				block_group[temp_spot].district=receiving_district
				members[receiving_district].append(temp_spot)
				del members[x][members[x].index(temp_spot)]
				if (check_contig(x)):

					#-----I got smaller
					senate_size[x]-=block_group[temp_spot].pop

					#-----You got bigger
					senate_size[receiving_district]+=block_group[temp_spot].pop


					edge=[]
					for x2 in xrange(0,59):
						edge.append(common())

					for x2 in xrange(0,len(block_group)):
						for y2 in xrange(0,len(block_group[x2].neighbor)):
							#-----if my neighbor has a different district then it is a possibility for a swap with a small size
							if block_group[x2].district!=block_group[block_group[x2].neighbor[y2]].district and senate_size[block_group[x2].district]>senate_size[block_group[block_group[x2].neighbor[y2]].district]:
								#-----add that neigbor to the list of possible swap candidates for that district
								if block_group[x2].neighbor[y2] not in edge[block_group[x2].district].ID:
									edge[block_group[x2].district].ID.append(block_group[x2].neighbor[y2])

				else:
					#print 'broke district '+str(receiving_district)
					members[x].append(temp_spot)
					del members[receiving_district][members[receiving_district].index(temp_spot)]
					block_group[temp_spot].district=x

					

		uneven_high=False
		for x in xrange(0,59):
			if senate_size[x]>max_pop:
				uneven_high=True;
		
	return True


def even_out_map_low():

	global block_group
	global senate_start
	global senate_size
	global taken
	global taken_start
	
	itr2=0

	edge=[]

	for z in xrange(0,59):
		senate_size[z]=0;

	for token in block_group:
		senate_size[token.district]+=token.pop
	#-----init variables
	taken=[]
	for x2 in xrange(0,59):
		edge.append(common())
		taken.append(0)
		taken_start.append(0)

	#-----find all the nodes that are on the boarder (have a neighbor with a different district)
	for block_num in xrange(0,len(block_group)): 
		taken_start[block_group[block_num].district]+=1
		taken[block_group[block_num].district]+=1
		for y2 in xrange(0,len(block_group[block_num].neighbor)):
			#-----if my neighbor has a different district then it is a possibility for a swap if a smaller district size
			if block_group[block_num].district!=block_group[block_group[block_num].neighbor[y2]].district and senate_size[block_group[block_num].district]<senate_size[block_group[block_group[block_num].neighbor[y2]].district]:
				#-----add that neigbor to the list of possible swap candidates for that district
				if block_group[block_num].neighbor[y2] not in edge[block_group[block_num].district].ID:
					edge[block_group[block_num].district].ID.append(block_group[block_num].neighbor[y2])

	uneven_low=True
	while uneven_low:

		#go through each district
		for x in xrange(0,59):

			#-----if the district population is too small than steal another districts
			if (senate_size[x]<min_pop and len(edge[x].ID)>0):

				max_district=0
				value=0

				#-----Let us find what blocks we can steal
				temp_spot=0
				if len(edge[x].ID)==0:
					temp_spot=edge[x][0]
				else:

					temp_spot=edge[x].ID[random.randint(0, len(edge[x].ID)-1) ]
					
		
				contiguous_tag=True
				previous_district=block_group[temp_spot].district
				block_group[temp_spot].district=x
				members[x].append(temp_spot)
				del members[previous_district][members[previous_district].index(temp_spot)]

				#print 'working on '+str(previous_district)+' with size '+str(senate_size[previous_district]) + ' current district size '+str(senate_size[x])

				if (check_contig(previous_district)):

					#-----You got smaller
					senate_size[previous_district]-=block_group[temp_spot].pop

					#-----I got bigger
					senate_size[x]+=block_group[temp_spot].pop

					edge=[]
					for x2 in xrange(0,59):
						edge.append(common())

					for x2 in xrange(0,len(block_group)):
						for y2 in xrange(0,len(block_group[x2].neighbor)):
							#-----if my neighbor has a different district then it is a possibility for a swap with a small size
							if block_group[x2].district!=block_group[block_group[x2].neighbor[y2]].district and senate_size[block_group[x2].district]<senate_size[block_group[block_group[x2].neighbor[y2]].district]:
								#-----add that neigbor to the list of possible swap candidates for that district
								if block_group[x2].neighbor[y2] not in edge[block_group[x2].district].ID:
									edge[block_group[x2].district].ID.append(block_group[x2].neighbor[y2])

				else:
					#print 'broke district '+str(previous_district)
					block_group[temp_spot].district=previous_district
					members[previous_district].append(temp_spot)
					del members[x][members[x].index(temp_spot)]
					

		uneven_low=False
		for x in xrange(0,59):
			if senate_size[x]<min_pop:
				uneven_low=True;

	return True
				
				
samples=0		
				
def advance():

	global temp_block_group
	global temp_senate_start
	global temp_senate_size
	global all_neighbors
	global block_group
	global senate_start
	global senate_size
	global samples
	global members
	start_pop=100000
	neighbor_same=[]

	block_group=temp_block_group[:]
	senate_start=temp_senate_start[:]
	senate_last_start=senate_start[:]
	senate_size=temp_senate_size[:]
	for x2 in range(0,len(all_neighbors)):
			all_neighbors[x2].ID=[]
			#neighbor_same[x2].ID=[]

	for x2 in range(0,len(block_group)):
			block_group[x2].district=-1

	go=True

	while (go):
		
		random.seed()
		for x in range(0,59):
			if (senate_start[x]>-1):

			   #erase neighboring node that were taken by other districts
				z=0
				len_neighbors=len(all_neighbors[x].ID)
				while z<len_neighbors:
					if block_group[all_neighbors[x].ID[z]].district > -1:
						del all_neighbors[x].ID[z]
						len_neighbors-=1
					else:
						z+=1

				#add new neighbors of active node to district
				for token_neighbor in block_group[senate_start[x]].neighbor:
					#add neigbor if free and not previously in current list
					if (block_group[token_neighbor].district==-1):
						if token_neighbor not in all_neighbors[x].ID:
							all_neighbors[x].ID.append(token_neighbor)

				#if there's at least one neighbor then expand district to a random neighbor
				if (len(all_neighbors[x].ID)>0):

						index =  random.randint(0, len(all_neighbors[x].ID)-1)
						block_group[all_neighbors[x].ID[index]].district=x;
					
						# set that neighbor to focus then delete from neighbor list
						senate_start[x]=all_neighbors[x].ID[index];
						senate_last_start[x]=all_neighbors[x].ID[index];
						senate_size[x]+=block_group[all_neighbors[x].ID[index]].pop;
						del all_neighbors[x].ID[index]
		            
						#if district too big then stop
						if (senate_size[x]>start_pop):
							senate_start[x]=-1
				else:
						#if district has no neighbors then stop
						senate_start[x]=-2

		#check if all district are exhausted
		check=True
		for x2 in range(0,59):
			if (senate_start[x2]>-1):
				check=False;

		all_used=True;		
		if (check):
			num_neg=0;
			for x2 in xrange(0,len(block_group)):
				if (block_group[x2].district==-1):
					all_used=False;
					num_neg+=1
				else:
					pass
				
			ooops=0
			if (all_used):
				check_neighbors=True
				for x in range(0,len(block_group)):
					members[block_group[x].district].append(x)
		
				for x in xrange(0,59):
					if check_contig(x)==False:
						check_neighbors=False
						break

				if check_neighbors:
					size=True
					go=False

					for z in range(0,59):
						if senate_size[z]<100000:
							size=False
				
					if (size):
						if even_out_map_high()==False:
							return False
						even_out_map_low()
						for z in range(0,59):
							outfile.write(str(senate_size[z])+'\t'+str(senate_start[z])+'\n')
						tremp_itr=0
						temp_str=''
						for token in block_group:
							tremp_itr+=1
							temp_str+=str(token.district)+'\t'
						outfile2.write(temp_str[:-1]+'\n')

						samples+=1
						reset=True
						return False
					else:
						pass

				else:

					block_group=temp_block_group[:]
					for x in range(0,len(block_group)):
						block_group[x].district=-1
					senate_start=temp_senate_start[:]
					senate_last_start=senate_start[:]
					senate_size=temp_senate_size[:]
					members=[]
					for x in range(0,59):
						members.append([])
				
			else:
				start_pop+=500
				for x in range(0,59):
					if senate_start[x]<0 and senate_size[x]<start_pop:
						senate_start[x]=senate_last_start[x]


@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.A:
		for x in range(0,10000):
			print x
			aaa=advance()

	if symbol == key.E:
		even_out_map_low()

	if symbol == key.R:
		even_out_map_high()
	
@window.event()
def on_resize(width, height):
    global win_h, win_w
    win_w=width
    win_h=height

    #print win_w
    
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(gl.GL_MODELVIEW)

@window.event
def on_draw():

	global block_group
	global samples
	global reset
	
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()
	glPointSize(2)
	trans_x=win_w/(max_x-min_x)
	trans_y=win_h/(max_y-min_y)
	for token in block_group:
		#draw node
		if token.district>-1:
			points=token.shape
			[r,g,b]=color[token.district]
			glColor3f(r,g,b)
		
			glBegin(GL_POLYGON)
			for token2 in points:
				if len(token2)>3:
					token2=token2.split(',')
					x1=(float(token2[0])-min_x)*trans_x
					y1=(float(token2[1])-min_y)*trans_y
					#print str(x1),' ',str(y1)
					glVertex2f(x1, y1)
			glEnd()  
		 
		     #draw node
			glColor3f(0.0,0.0,0.0)
			x1=(token.x-min_x)*trans_x
			y1=(token.y-min_y)*trans_y


			glBegin(GL_POINTS)
			glVertex2f(x1, y1)
			glEnd()
	if reset:
		reset=False


#infile=open('/home/john/gerry/tracts_all.csv').read().split('\n')
infile=open('/home/john/gerry/block_neighbor_fixed.csv').read().split('\n')
infile=infile[1:]
for token in infile:
	if len(token)>3:
		token=token.split('\t')
		#print 'ok',token[0]
		if len(token[0])>0:
#	def __init__(self,ID,neighbors,pop,lat,lng,shape):

			block_group.append(group(token[0],token[-8], token[10] , 1 , 1 ,token[-1]))
#			block_group.append(group(token[0],token[-2], token[5] , 1 , 1 ,token[-1]))
reset=False
#init starting points
senate_start=[]
#senate_file=open('/home/john/gerry/senate_geo_track.csv').read().split('\n')
senate_file=open('/home/john/gerry/senate_geo_group.csv').read().split('\n')
senate_file=senate_file[1:]
senate_size=[]
all_neighbors=[]
for token in senate_file:
	if len(token)>3:
		token=token.split('\t')
		senate_start.append(int(token[3])-1)
		senate_size.append(block_group[int(token[3])].pop)
		block_group[int(token[3])-1].district=int(token[0])-1
		all_neighbors.append(common())


temp_block_group=block_group[:]
temp_senate_start=senate_start[:]
temp_senate_size=senate_size[:]

pyglet.app.run()


