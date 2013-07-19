import numpy as np

class district_info:
	Name="district_info"
	def __init__(self,ID):
		self.ID=int(ID)
		self.repub=0.0;
		self.dem=0.0;
		self.wnh=0.0;
		self.minority=0.0;
		self.income=0.0; #disperse via population in block group
		self.population=0.0;
		self.poverty=0.0;
		self.college_degree=0.0;
		self.urban=0.0;
		self.winning_minority=0.0;
		self.winning_dem=0.0;		
		self.rural=0.0;

repub_index=32
dem_index=31
wnh_index=11
minority_index=[12,13,14,15,16,17,18]
income_index=25
population_index=10
poverty_index=24
college_degree_index=8
urban_index=5
rural_index=6

block_group_infile=open('/home/john/datamandering_project/data/block_neighbor_fixed.csv').read().split('\n')
header=block_group_infile[0].split('\t')
header=header[5:29]

block_group_infile=block_group_infile[1:]
while len(block_group_infile[-1])<2:
	block_group_infile=block_group_infile[:-1]

district=[]
for token in xrange(0,59):
	district.append(district_info(token))

map_infile=open("/home/john/final1/all_maps.txt").read().split('\n')

outfile_raw=open("/home/john/datamandering_project/code/all_raw.txt","w")
outfile_raw.write('map#\turban_packing\trural_packing\tcollege_degree_packing\tincome_packing\tpoverty_packing\tminority_packing\trepub_packing\tdem_packing\tminority_wins\tdem_wins\n')


#while len(map_infile[-1])<2:
#	map_infile=map_infile[:-1]

#go through each map
for x in xrange(0,len(map_infile)):
	map_infile[x]=map_infile[x].split('\t')
	print str(x)+' map '+str(len(map_infile[x]))
	#reset districts
	district=[]
	for token in xrange(0,59):
		district.append(district_info(token))

	temp=map_infile[x]
	while len(temp[-1])<1:
		temp=temp[:-1]
	
	#go through each block and add it to the district
	ok=True
	for y in xrange(0,len(temp)):
		temp2=block_group_infile[y].split('\t')
		for itr in range(0,len(temp2)):
			if temp2[itr]=='' or temp2[itr]==' ':
				temp2[itr]='0'
		if temp[y]=='':
			ok=False
			break
		if int(temp[y])<0 or int(temp[y]) >58:
			ok=False
			break

		#print 'input len=',str(len(temp2)),' repub index=',str(repub_index),' district len=',str(len(district)),' district index=',str(temp[y])
		#print y
		#update that district's data
		if float(temp2[dem_index])==0: 
			district[int(temp[y])].repub+=float(temp2[population_index])
		else:
			district[int(temp[y])].repub+=float(temp2[population_index])*float(temp2[repub_index])/(float(temp2[dem_index])+float(temp2[repub_index]))
		
		if float(temp2[repub_index])==0: 
			district[int(temp[y])].dem+=float(temp2[population_index])
		else:
			district[int(temp[y])].dem+=float(temp2[population_index])*float(temp2[dem_index])/ (float(temp2[repub_index])+float(temp2[dem_index]))
	

		district[int(temp[y])].wnh+=float(temp2[wnh_index])

		minority_sum=0
		for token_minority in minority_index:
			minority_sum+=float(temp2[token_minority])

		district[int(temp[y])].minority+=minority_sum

		district[int(temp[y])].income+=float(temp2[income_index])*float(temp2[population_index])
		district[int(temp[y])].population+=float(temp2[population_index])
		district[int(temp[y])].poverty+=float(temp2[poverty_index])
		district[int(temp[y])].college_degree+=float(temp2[college_degree_index])
		district[int(temp[y])].urban+=float(temp2[urban_index])
		district[int(temp[y])].rural+=float(temp2[rural_index])
		
	if ok:



		#output the data for the map on variability	
		print 'everything passed!'
		outfile_raw.write(str(x)+'\t')

		temp=[]
		for y in range(0,59):
			temp.append(district[y].urban/district[y].population)
		outfile_raw.write(str(np.std(temp)/np.mean(temp))+'\t')

		temp=[]
		for y in range(0,59):
			temp.append(district[y].rural/district[y].population)
		outfile_raw.write(str(np.std(temp)/np.mean(temp))+'\t')

		temp=[]
		for y in range(0,59):
			temp.append(district[y].college_degree/district[y].population)
		outfile_raw.write(str(np.std(temp)/np.mean(temp))+'\t')

		temp=[]
		for y in range(0,59):
			temp.append(district[y].income/district[y].population)
		outfile_raw.write(str(np.std(temp)/np.mean(temp))+'\t')

		temp=[]
		for y in range(0,59):
			temp.append(district[y].poverty/district[y].population)
		outfile_raw.write(str(np.std(temp)/np.mean(temp))+'\t')

		temp=[]
		for y in range(0,59):
			temp.append(district[y].minority/district[y].population)
		outfile_raw.write(str(np.std(temp)/np.mean(temp))+'\t')

		temp=[]
		for y in range(0,59):
			temp.append(district[y].repub/district[y].population)
		outfile_raw.write(str(np.std(temp)/np.mean(temp))+'\t')

		temp=[]
		for y in range(0,59):
			temp.append(district[y].dem/district[y].population)
		outfile_raw.write(str(np.std(temp)/np.mean(temp))+'\t')

		temp=0
		for y in range(0,59):
			if (district[y].wnh<district[y].minority ):
				temp+=1
		outfile_raw.write(str(temp)+'\t')

		temp=0
		for y in range(0,59):
			print "dem=",str(district[y].dem)," rep=",str(district[y].repub)," %rep=",str(district[y].repub/(district[y].dem+district[y].repub)*100.0)
			if (district[y].repub<0.755*district[y].dem ):
				temp+=1
		outfile_raw.write(str(temp)+'\n')	

	else:
		print 'something failed...'



