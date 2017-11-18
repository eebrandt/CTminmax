#!/usr/bin/python

"""
Erin Brandt, 11/16/2017
This program is used to calculate CT min and max for Habronattus. It takes in 2 different files: (1) .tsv files based on BORIS-based voice recorder analysis, (2) .csv files containing temperature information
"""

# for importing .tsv files
import pandas as pd
# for doing numerical calcuations and for making numpy arrays
import numpy as np
# for getting current date and time for timestamp
import datetime
# used to root through folders on computer
import os
# for opening, writing, and manipulating .csv (also .tsv) files
import csv
# for user dialog and message boxes
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox

# gets timestamp for adding to the filename (keeps files from getting overwritten
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

# change this string if you want to change where the gui folder chooser is defaulted to.
trialinfo_folder = "/home/eebrandt/projects/dissertation/uncategorized/physiology/CTminmax/data"

# opens a dialog to choose the trial information file, and throws error if you don't choose one
infofile = tkFileDialog.askopenfilename(initialdir = trialinfo_folder, title = "Choose the file that contains overall information")    
if infofile == "":
	tkMessageBox.showerror(
       	    "Open file",
       	    "You need to choose a file with overall information.")
	raise SystemExit

# get folder that contains .tsv files for trials
# change this string if you want the folder chooser to default to opening a different place
timedata_folder = "/home/eebrandt/projects/dissertation/uncategorized/physiology/CTminmax/data/recordings/tsvs/"
trial_folder = tkFileDialog.askdirectory(initialdir= timedata_folder, title = "Choose the folder that contains trial time files.")

# array to hold list of .tsv files in folder
tsvs = []
for file in os.listdir(trial_folder):
	if file.endswith(".tsv"):
		tsvs.append(file)
#print tsvs
# get folder that contains .csv files for trials (temperature data)
# change this string if you want the folder chooser to default to opening a different place
tempdata_folder = "/home/eebrandt/projects/dissertation/uncategorized/physiology/CTminmax/data/temp_data/"
temp_folder = tkFileDialog.askdirectory(initialdir= tempdata_folder, title = "Choose the folder that contains trial temp files.")

#makes a .csv file that will compile all of the data
fl = open(trialinfo_folder + "/CTminmax_processed" + "_" + timestamp + '.csv', 'w')
writer = csv.writer(fl)

writearray = []

#header row for csv file
headers = ["page", "trial", "chamber", "ID", "sex", "species", "mass", "treatment", "date", "date_fed", "start_time", "down_initial", "down_20sec", "down_final"]
# writes header row
writer.writerow(headers)

#read in trial info file
trialinfo = pd.read_csv(infofile, sep=',', header =1, usecols=[0,1,2,3,4,5,6,7,8,9,10]) 
#turns trial info into numpy array
trialarray = np.array(trialinfo)

#integer to increment through .tsvs
fileint = 0
#loops through each .tsv (trial)
while fileint < len(tsvs):
	tsvname = tsvs[fileint][:-4]
	name = tsvname.split('-')
	print tsvname
	#subsets the current trial records from the trial info array, first by page, then by trial number
	infotrialsubset = trialarray[trialarray[:,0] == int(name[0])]
	infotrialsubset = infotrialsubset[infotrialsubset[:,1] == int(name[1])]

	#reads in .tsv file (tab-delimited), skips first 15 rows which is header garbage
	timesread = pd.read_csv(timedata_folder +"/" + tsvs[fileint], sep='\t', skiprows = 15,dtype={'time': float, 'subject': str, 'behavior': str, 'status': str}, usecols=[0,4,5,8]) 

	#read in temperature file
	tempsread = pd.read_csv(tempdata_folder + "/" + tsvname + ".csv" , sep=',',dtype={'time': float, 'channel1':float, 'channel2': float, 'channel3': float, 'channel4':float}, skiprows =0) 
	tempsarray=np.array(tempsread)

	#puts the input data into a numpy array
	masterarray = np.array(timesread)

	#make array of flips, which is independent of any individual
	fliparray = masterarray[masterarray[:,1] == "none"]
	
	#integer to increment individuals
	indint = 1
	#figures out the number of individuals from subset array
	inds = infotrialsubset.shape[0]
	
	#loops through each individual of trial
	while indint < inds+1:

		print indint
		#pulls all of the time information for our individual of interest
		ind_array = masterarray[masterarray[:,1] == str(indint)]
		#makes array to hold "down" information, plus duration
		downsarray = np.zeros((len(ind_array)/2,3))

		#makes array to hold final information about time and temp
		times_array = np.zeros((3,5))

		#makes array that only holds info. for down starts
		startarray = ind_array[ind_array[:,3] == "START"]
		#makes array that only holds info. for down stops
		stoparray = ind_array[ind_array[:,3] == "STOP"]

		downint = 0
		#calculates start, stop, and duration info for each of the downs
		while downint < len(startarray):
			downsarray[downint][0] = startarray[downint][0]
			downsarray[downint][1] = stoparray[downint][0]
			downsarray[downint][2] = stoparray[downint][0] - startarray[downint][0]
			downint = downint +1

		#find first down
		times_array[0][1] = downsarray[0][0]
	
		#find 20 sec down. Makes array of all downs longer than 20 seconds
		twentysec = downsarray[downsarray[:,2] > 20]
		#If there is no down that lasts 20 seconds, we use the ending one

		if twentysec.size == 0:
			times_array[1][1] = downsarray[-1][0]
		else:
			times_array[1][1] = twentysec[0][0]	
	
		#find final down
		times_array[2][1] = downsarray[-1][0]
	
		#find initial times; this is usually the last previous flip before the animal went down. If there were no previous flips, take a time 60 secons before the down begins.
		flipinitial = fliparray[fliparray[:,0] < (times_array[0][1] - 5)]
		if flipinitial.size == 0:
			times_array[0][0] = (times_array[0][1] - 60)
		else:
			times_array[0][0] = flipinitial[-1][0]

		#find 20 sec. down time; usually the last previous flip before the animal went down
		fliptwenty = fliparray[fliparray[:,0] < (times_array[1][1] - 5)]
		#finds all stops that occur before the 20 second down 
		stops20 = downsarray[downsarray[:,1] < (times_array[1][1] -5)]

		if fliptwenty.size == 0:
			times_array[1][0] = (times_array[1][1] - 60)
		elif stops20.size == 0:
			times_array[1][0] = fliptwenty[-1][0]
		elif stops20[-1][1] > fliptwenty[-1][0]:
			#print "yup"
			times_array[1][0] = stops20[-1][1]
		else:
			times_array[1][0] = fliptwenty[-1][0]

		#find last down time; usually the last previous flip before the animal went down, but also might be the last time the animal was up
		flipfinal = fliparray[fliparray[:,0] < (times_array[2][1] - 5)]
		#print flipfinal
		stopsfinal = downsarray[downsarray[:,1] < (times_array[2][1] -5)]
	
		if flipfinal.size == 0:
			#print "flipfinal zero"
			times_array[2][0] = (times_array[2][1] - 60)
		elif stopsfinal.size == 0:
			#print "stopsfinal zero"
			times_array[2][0] = flipfinal[-1][0]
		elif stopsfinal[-1][1] > flipfinal[-1][0]:
			#print "stopsfinal better"
			times_array[2][0] = stopsfinal[-1][1]
		else:
			times_array[2][0] = flipfinal[-1][0]

		tempint = 0
		#match temps to times, for each of the three "downs" that we care about
		while tempint < 3:

			tempindex = int(round(times_array[tempint][0]))
			times_array[tempint][2]= tempsarray[tempindex][indint]
		
			tempindex = int(round(times_array[tempint][1]))
			times_array[tempint][3]= tempsarray[tempindex][indint]
	
			times_array[tempint][4] = (times_array[tempint][2] + times_array[tempint][3])/2
			tempint += 1

		#write temp. info to array for writing
		towrite = [infotrialsubset[indint-1][0], infotrialsubset[indint-1][1], infotrialsubset[indint-1][2], infotrialsubset[indint-1][3], infotrialsubset[indint-1][4], infotrialsubset[indint-1][5], infotrialsubset[indint-1][6], infotrialsubset[indint-1][7], infotrialsubset[indint-1][8], infotrialsubset[indint-1][9], infotrialsubset[indint-1][10], times_array[0][4], times_array[1][4], times_array[2][4]]
		writearray.append(towrite)		
		
		indint +=1
	fileint += 1

#writes the array to the .csv
writer.writerows(writearray)
fl.close()

#This section makes a second .csv file that adds the temperature range for each individual (if the individual had cold and hot)

#converts the previous list to a numpy array of all data previously compiled
allarray = np.asarray(writearray)

#subsets the array into hot trials and cold trials
hots = allarray[allarray[:,7] == "hot"]
colds = allarray[allarray[:,7] == "cold"]

#list of the names of individuals that have hot trials
hotkey = hots[:,3]
#list of the names of individuals that have cold trials
coldkey = colds[:,3]

#finds the names of individuals that have hot and cold trials
both = np.intersect1d(hotkey, coldkey)
#finds the names of individuals that have only hot trials
hotsonly = np.setdiff1d(hotkey, both)
#finds the names of individuals that have only cold trials
coldsonly = np.setdiff1d(coldkey, both)

#first, we're going to go through the individuals with both hot and cold trials, calculate range, and write that data to a list that will turn into a row later
#loop through boths
bothint = 0
#makes array that will hold all of the data for the output .csv. Notice that it will have lines for all individuals, not just the ones with hot and cold
combined_line = np.zeros((allarray.shape[0], 14), dtype = "S25")

#loops through each individual that has both trials, calculates range, and writes appropriate data
while bothint < len(both):
	#finds info for hot data
	#find index
	indexhot = np.where(hots==both[bothint])
	hotsline = hots[indexhot[0]]

	#write pertinent data
	combined_line[bothint][0] = hotsline[0][3]
	combined_line[bothint][1] = hotsline[0][4]
	combined_line[bothint][2] = hotsline[0][5]
	combined_line[bothint][3] = hotsline[0][6]
	combined_line[bothint][4] = hotsline[0][11]
	combined_line[bothint][5] = hotsline[0][12]
	combined_line[bothint][6] = hotsline[0][13]
	
	#does the same for cold trials
	#find index
	indexcold = np.where(colds==both[bothint])
	coldsline = colds[indexcold[0]]
	
	#write pertinent data
	combined_line[bothint][7] = coldsline[0][6]
	combined_line[bothint][8] = coldsline[0][11]
	combined_line[bothint][9] = coldsline[0][12]
	combined_line[bothint][10] = coldsline[0][13]
	
	#figures out the temperature ranges
	combined_line[bothint][11] = float(hotsline[0][11]) - float(coldsline[0][11])
	combined_line[bothint][12] = float(hotsline[0][12]) - float(coldsline[0][12])
	combined_line[bothint][13] = float(hotsline[0][13]) - float(coldsline[0][13])

	bothint = bothint + 1

#now we're going to add info for the individuals with only hot trials. Since we're adding to an existing array, our counter needs to start where the previous one left off
hotsint = bothint

#loops through individuals with only hot trial, writes pertinent data
while hotsint < bothint + len(hotsonly):
	indexhot = np.where(hots==hotsonly[hotsint-bothint])
	hotsline = hots[indexhot[0]]

	combined_line[hotsint][0] = hotsline[0][3]
	combined_line[hotsint][1] = hotsline[0][4]
	combined_line[hotsint][2] = hotsline[0][5]
	combined_line[hotsint][3] = hotsline[0][6]
	combined_line[hotsint][4] = hotsline[0][11]
	combined_line[hotsint][5] = hotsline[0][12]
	combined_line[hotsint][6] = hotsline[0][13]

	hotsint = hotsint +1

#now we're going to do the same for colds as we did for hots. We're going to again make the counter start where the previous one left off
coldsint = hotsint

while coldsint < hotsint + len(coldsonly):
	indexcold = np.where(colds==coldsonly[coldsint-hotsint])

	coldsline = colds[indexcold[0]]

	combined_line[coldsint][0] = coldsline[0][3]
	combined_line[coldsint][1] = coldsline[0][4]
	combined_line[coldsint][2] = coldsline[0][5]
	combined_line[coldsint][7] = coldsline[0][6]
	combined_line[coldsint][8] = coldsline[0][11]
	combined_line[coldsint][9] = coldsline[0][12]
	combined_line[coldsint][10] = coldsline[0][13]

	coldsint = coldsint +1
	
#makes a .csv file that will compile all of the range data
fl = open(trialinfo_folder + "/CTminmax_both" + "_" + timestamp + '.csv', 'w')
writer = csv.writer(fl)

#header file for the second .csv file
compiled_header = ["ID", "sex", "species", "mass_hot", "down_initial_hot", "down_20sec_hot", "down_final_hot", "mass_cold", "down_initial_cold", "down_20sec_cold", "down_final_cold", "range_initial", "range_20", "range_final"]

#writes header and array to .csv file
writer.writerow(compiled_header) 
writer.writerows(combined_line)
fl.close()
