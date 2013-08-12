# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import get_template
from django import forms
from django.shortcuts import render_to_response
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
import sys
import os
from django.views.decorators.csrf import csrf_exempt 
from django.core.mail import send_mail 
import time
from scipy.stats.stats import pearsonr

def find_map(variable, value, dem_wins):
	infile_variance=open("../data/all_raw_norm.csv").read().split('\n')

	min_dist=10000000000
	
	map_id=0
	dem=0
	minority=0
	index=0
	final_vals=[]
	print 'value'
	print value
	if len(value)==1:
			print '1 value'
	else:
		print '>1 value'

	for token in infile_variance[1:5000]:
		token=token.split('\t')
		if len(value)==1:
			y=    float(token[  int(variable[0])   ]) - float(value[0] )
			flag=True
			if dem_wins>0 and dem_wins!=int(token[11]):
				flag=False

			if abs(y) < min_dist and flag:
				min_dist=abs(y)
				map_id=index
				final_vals=[]
				for token2 in [3,8,7,4,5,6,9]:
					final_vals.append(token[token2])
				dem=int(token[11])
				minority=int(token[10])

	
		elif len(value)==0:
			if dem_wins>0 and dem_wins==int(token[11]):
				map_id=index
				dem=int(token[11])
				minority=int(token[10])
				final_vals=[]
				for token2 in [3,8,7,4,5,6,9]:
					final_vals.append(token[token2])
		else:
			x=0
			print value
			temp_vals=[]
			for itr in range(0,len(variable)):
				temp_vals.append(token[ variable[int(itr)]]  )
			
			for itr in range(0,len(variable)):
				x+= (float( token[ variable[int(itr)]]  )-value[int(itr)])*(float( token[ variable[int(itr)]]      )-value[int(itr)])
			flag=True

			if dem_wins>0 and dem_wins!=int(token[11]):
				flag=False

			if x<min_dist and flag:
				min_dist=x
				map_id=index
				dem=int(token[11])
				minority=int(token[10])
				final_vals=[]
				for token2 in [3,8,7,4,5,6,9]:
					final_vals.append(token[token2])
				print final_vals

			else:
				print 'too bad'

			print 'done'
		index+=1
	print 'map_id from function =',map_id
	print final_vals
	print 'selected dem=',str(dem_wins),' found ',str(dem)
	return map_id,final_vals,dem,minority

class datamandering_filter(forms.Form):

    repub_choices = ( ("1", "not important"), ("2", " high cracking "), ("3", " medium cracking "), ("4", "neutral "), ("5", " medium packing "), ("6", " high packing "))
    repub_choices_list = forms.ChoiceField(choices=repub_choices, widget=forms.Select(), label='Republican distribution')

    college_choices = ( ("1", "not important"), ("2", " high cracking "), ("3", " medium cracking "), ("4", "neutral "), ("5", " medium packing "), ("6", " high packing "))
    college_choices_list = forms.ChoiceField(choices=college_choices, widget=forms.Select(), label='College distribution')

    dem_choices = ( ("1", "not important"), ("2", " high cracking "), ("3", " medium cracking "), ("4", "neutral "), ("5", " medium packing "), ("6", " high packing "))
    dem_choices_list = forms.ChoiceField(choices=dem_choices, widget=forms.Select(), label='Democrat distribution')

    income_choices = ( ("1", "not important"), ("2", " high cracking "), ("3", " medium cracking "), ("4", "neutral "), ("5", " medium packing "), ("6", " high packing "))
    income_choices_list = forms.ChoiceField(choices=income_choices, widget=forms.Select(), label='income distribution')

    poverty_choices = ( ("1", "not important"), ("2", " high cracking "), ("3", " medium cracking "), ("4", "neutral "), ("5", " medium packing "), ("6", " high packing "))
    poverty_choices_list = forms.ChoiceField(choices=poverty_choices, widget=forms.Select(), label='poverty distribution')

    minority_choices = ( ("1", "not important"), ("2", " high cracking "), ("3", " medium cracking "), ("4", "neutral "), ("5", " medium packing "), ("6", " high packing "))
    minority_choices_list = forms.ChoiceField(choices=minority_choices, widget=forms.Select(), label='minority distribution')

    compactness_choices = ( ("1", "not important"), ("2", " very low compaction "), ("3", " low compaction "), ("4", "average compaction "), ("5", " high compaction "), ("6", " very high compaction "))
    compactness_choices_list = forms.ChoiceField(choices=compactness_choices, widget=forms.Select(), label='compactness', initial=" very high compaction ")
 
    dem_wins_choices = ( ("1", "not important"), ("2", " 36 Dem - 23 Repub "), ("3", " 37 Dem - 22 Repub "), ("4", "38 Dem - 21 Repub"), ("5", " 39 Dem - 20 Repub "), ("6", " 40 Dem - 19 Repub "),("7", " 41 Dem - 18 Repub "),("8", " 42 Dem - 17 Repub "),("9", " 43 Dem - 16 Repub "))
    dem_wins_choices_list = forms.ChoiceField(choices=dem_wins_choices, widget=forms.Select(), label='Democrat districts')

    minority_wins_choices = ( ("1", "not important"), ("2", " high cracking "), ("3", " medium cracking "), ("4", "neutral "), ("5", " medium packing "), ("6", " high packing "))
    minority_wins_choices_list = forms.ChoiceField(choices=minority_wins_choices, widget=forms.Select(), label='Minority districts')

@csrf_exempt                                                                                
def main_page(request):
    template = get_template('index.html')
    
    if request.method == 'POST': # If the form has been submitted...
        print 'trying'
        form = datamandering_filter(request.POST) # A form bound to the POST data
        #if form.is_valid(): # All validation rules pass
        if 1==1: # All validation rules pass
            #get user input
				print "yeah!"
				label=[]
				value=[]
				variable=[]

				variable.append(3)
				label.append('College Degree')
				if form['college_choices_list'].value()=='2':
					value.append(0.0)
				elif form['college_choices_list'].value()=='3':
					value.append(0.25)
				elif form['college_choices_list'].value()=='4':
					value.append(0.5)
				elif form['college_choices_list'].value()=='5':
					value.append(0.75)
				elif form['college_choices_list'].value()=='6':
					value.append(1.0)
				elif form['college_choices_list'].value()=='1':
					variable=variable[:-1]
					label=label[:-1]

				variable.append(8)
				label.append('Democratic Voters')		
				if form['dem_choices_list'].value()=='2':
					value.append(0.0)
				elif form['dem_choices_list'].value()=='3':
					value.append(0.25)
				elif form['dem_choices_list'].value()=='4':
					value.append(0.5)
				elif form['dem_choices_list'].value()=='5':
					value.append(0.75)
				elif form['dem_choices_list'].value()=='6':
					value.append(1.0)
				elif form['dem_choices_list'].value()=='1':
					variable=variable[:-1]
					label=label[:-1]

				variable.append(7)
				label.append('Republican Voters')
				if form['repub_choices_list'].value()=='2':
					value.append(0.0)
				elif form['repub_choices_list'].value()=='3':
					value.append(0.25)
				elif form['repub_choices_list'].value()=='4':
					value.append(0.5)
				elif form['repub_choices_list'].value()=='5':
					value.append(0.75)
				elif form['repub_choices_list'].value()=='6':
					value.append(1.0)
				elif form['repub_choices_list'].value()=='1':
					variable=variable[:-1]
					label=label[:-1]

				variable.append(4)
				label.append('Average Household Income')
				if form['income_choices_list'].value()=='2':
					value.append(0.0)
				elif form['income_choices_list'].value()=='3':
					value.append(0.25)
				elif form['income_choices_list'].value()=='4':
					value.append(0.5)
				elif form['income_choices_list'].value()=='5':
					value.append(0.75)
				elif form['income_choices_list'].value()=='6':
					value.append(1.0)
				elif form['income_choices_list'].value()=='1':
					variable=variable[:-1]
					label=label[:-1]
				
				variable.append(5)
				label.append('Poverty')
				if form['poverty_choices_list'].value()=='2':
					value.append(0.0)
				elif form['poverty_choices_list'].value()=='3':
					value.append(0.25)
				elif form['poverty_choices_list'].value()=='4':
					value.append(0.5)
				elif form['poverty_choices_list'].value()=='5':
					value.append(0.75)
				elif form['poverty_choices_list'].value()=='6':
					value.append(1.0)
				elif form['poverty_choices_list'].value()=='1':
					variable=variable[:-1]
					label=label[:-1]

				variable.append(6)
				label.append('Minority')
				if form['minority_choices_list'].value()=='2':
					value.append(0.0)
				elif form['minority_choices_list'].value()=='3':
					value.append(0.25)
				elif form['minority_choices_list'].value()=='4':
					value.append(0.5)
				elif form['minority_choices_list'].value()=='5':
					value.append(0.75)
				elif form['minority_choices_list'].value()=='6':
					value.append(1.0)
				elif form['minority_choices_list'].value()=='1':
					variable=variable[:-1]
					label=label[:-1]

				variable.append(9)
				label.append('Compactness')
				if form['compactness_choices_list'].value()=='2':
					value.append(0.0)
				elif form['compactness_choices_list'].value()=='3':
					value.append(0.25)
				elif form['compactness_choices_list'].value()=='4':
					value.append(0.5)
				elif form['compactness_choices_list'].value()=='5':
					value.append(0.75)
				elif form['compactness_choices_list'].value()=='6':
					value.append(1.0)
				elif form['compactness_choices_list'].value()=='1':
					variable=variable[:-1]
					label=label[:-1]
				
				dem_wins=-1
				if form['dem_wins_choices_list'].value()=='2':
					dem_wins=36
				elif form['dem_wins_choices_list'].value()=='3':
					dem_wins=37
				elif form['dem_wins_choices_list'].value()=='4':
					dem_wins=38
				elif form['dem_wins_choices_list'].value()=='5':
					dem_wins=39
				elif form['dem_wins_choices_list'].value()=='6':
					dem_wins=40
				elif form['dem_wins_choices_list'].value()=='7':
					dem_wins=41
				elif form['dem_wins_choices_list'].value()=='8':
					dem_wins=42
				elif form['dem_wins_choices_list'].value()=='9':
					dem_wins=43

				print 'finding closet map...'

				print value
				print variable
				print label
				map_id=0
				final_vals=[]
				winning_dem=0
				winning_minority=0
				if len(variable)>0 or dem_wins>0:
					map_id,final_vals,winning_dem,winning_minority=find_map(variable,value,dem_wins)

				print str(map_id),'map id'
				print 'done...'
				print final_vals
				print "dems=",str(winning_dem)
				map_file='https://googledrive.com/host/0B2Jo0VTLiqp3eXI5d3o5bTU3Szg/map_'+str(map_id)+'.kmz'
				Response_template=get_template('submitted.html')
				plots=[]
				bins=[]
				histo_data=open('../data/all_raw_norm_histo.csv').read().split('\n')

				for x in range(0,20):
					bins.append(x*0.05)

				current_values=['spacer',0.6837510328,0.7515777284,0.5624658969,0.5748987142,0.6552159729,0.7525620723,0.7931337494,0.8565550323,0.99999,12,40]
				
					
					
				#plots=[]
				#for plot_itr in range(0,len(variable)):
				#	data=get_histo(variable[plot_itr])
				delta_party='Democratic'
				delta_gains=winning_dem-40
				if delta_gains < 0:
					delta_party='Republicans'
					delta_gains*=-1
				sign_minority='+'
				delta_minority=winning_minority-12
				if delta_minority<0:
					delta_minority*=-1
					sign_minority='-'

				winning_white=59-winning_minority
				winning_repub=59-winning_dem

				if len(final_vals)>0:
					variable=[3,8,7,4,5,6,9]
					label=['College Degree','Democratic Voters','Republican Voters','Average Household Income','Poverty','Minority','Compactness']
					for tokenx in range(0,len(label)):
						current_value=current_values[variable[tokenx]]
						selected_value=float(final_vals[tokenx])
				
						histo_data_x=histo_data[variable[tokenx]-1].split('\t')
						data=[]

						for x in range(0,19):
							data.append( (bins[x],histo_data_x[x]) )
						plots.append((data,label[tokenx],current_value,selected_value))

				else:
					delta_gains=0
					delta_minority=0
					winning_minority=13
					winning_white=46
					winning_dem=40
					winning_repub=19


				variables = Context({
               'map_file': map_file,
					'plots': plots,
					'delta_gains':delta_gains,
					'delta_party':delta_party,
					'delta_minority':delta_minority,
					'winning_minority':winning_minority,
					'sign_minority': sign_minority,
					'winning_white':winning_white,
					'winning_dem':winning_dem,
					'winning_repub':winning_repub,

				})
				output = Response_template.render(variables)
				return HttpResponse(output) # Redirect after POST
    else:

        form = datamandering_filter() # An unbound form
        
    return render_to_response('index.html', {
        'form': form,
    })

