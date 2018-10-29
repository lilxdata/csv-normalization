import sys
import pandas 
import datetime
from pytz import timezone

#store input file 
file_to_normalize = sys.argv[1]

#read file 
sample_data = pandas.read_csv(file_to_normalize)

#helper function to convert timestamps to eastern time
date_format = "%m/%d/%y %I:%M:%S %p"
def pst_to_est(time):
  pst_time = datetime.datetime.strptime(time, date_format)
  convert_to_est = pst_time.astimezone(timezone('US/Eastern'))
  est_time = convert_to_est.strftime(date_format)
  return est_time

#initialize empty list of timestamps 
output_timestamps = []

#get list of timestamps from csv
timestamps = sample_data["Timestamp"]

#loop over timestamps and convert to est 
for timestamp in timestamps:
  est = pst_to_est(timestamp)
  output_timestamps.append(est)

#initialize empty dict to output into csv
output_data = {}

#add timestamps to output_data dict
output_data["Timestamp"] = output_timestamps

#address unicode validation
#basically same but accounting for utf-8 in csv export 
output_data["Address"] = sample_data["Address"]

#check that zip code is 5 digits long
#if not, prefix zeroes 

#note: when csv is opened in numbers or excel, their formatting gets rid of 
#leading zeros so it looks like this doesn't work, but if you print output_zips
#all of the zips are transformed 
output_zips = []
zipcodes = sample_data["ZIP"]

def zero_zips(zipcode):
  new_zip = str(zipcode).zfill(5)
  return new_zip

for zipcode in zipcodes:
  zero_zip=zero_zips(zipcode)
  output_zips.append(zero_zip)

output_data["ZIP"] = output_zips

#make all names uppercase 

output_names = []
names = sample_data["FullName"]

for name in names: 
  output_names.append(name.upper())
output_data["FullName"] = output_names

# output_foo = []
# output_bar = []
# output_total = []
# totals = sample_data["TotalDuration"]
# for total in totals:
#   new_total = 

#need to replace broken character w default unicode
output_data["Notes"] = sample_data["Notes"]

#convert dict to dataframe
output_dataframe=pandas.DataFrame.from_dict(output_data)
#print("output df", output_dataframe)
#export to file
output_dataframe.to_csv('notes123.csv', encoding='utf-8')


