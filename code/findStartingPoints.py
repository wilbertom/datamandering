import math 

low_res_infile=open('/home/john/datamandering_project/data/IL_house_centroids.csv').read().split('\n')
high_res_infile=open('/home/john/datamandering_project/data/IL_bg_centroids.csv').read().split('\n')

blocks=[]
high_res_infile=high_res_infile[1:]

for token in high_res_infile:
   #print token
   if len(token)>1:
      print token
      token=token.split('\t')
   
      blocks.append([token[0],float(token[1]),float(token[2])])

outfile=open('/home/john/datamandering_project/data/IL_house_starting.csv',"w")
outfile.write(low_res_infile[0]+'\n')
low_res_infile=low_res_infile[1:]

for token in low_res_infile:
   if len(token)>3:
      temp=token
      token=token.split('\t')
      min_value=1000000000
      min_index=0
      for token2 in blocks:
         #print str(token[1]),' ',str(token2[1]),' ',str(token[2]),' ',str(token2[2])
         temp_val=math.sqrt(           (  float(token[1])-token2[1]  )   * ( float(token[1])-token2[1])     +    (float(token[2])-token2[2] )*(  float(token[2])-token2[2] )                )
         if  temp_val < min_value:
              min_value=temp_val
              min_index=token2[0]
      outfile.write(str(temp)+'\t'+str(min_index)+'\n')

