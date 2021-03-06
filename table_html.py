#! /usr/bin/python
from api_func.api_func import *
import pandas
import json
import sys
from io import StringIO
import argparse

#########################
# CLI ARGUMENT HANDLING #
#########################

parser=argparse.ArgumentParser()

parser.add_argument('-file', help='Path to file containing API credentials')
parser.add_argument('-cpu', help='ID of a CPU Device Metric Trends Report')
parser.add_argument('-mem', help='ID of a MEM Device Metric Trends Report')
parser.add_argument('-inv', help='ID of a Device Inventory Report')
parser.add_argument('-widget', help='ID of a text widget to post HTML table into')

args = parser.parse_args()

###################
# PARSE API CREDS #
###################

key_file_path = args.file
file = open(key_file_path, 'r')
file_text = file.read()

key_file_json = json.loads(file_text)
AccessId = key_file_json['id']
AccessKey = key_file_json['key']
Company = key_file_json['company']

##############
# CPU REPORT #
##############

#Request Info
resourcePath = '/functions'
queryParams =''

cp_report_id = args.cpu

data_dict = {'type':'generateReport',
			 'reportId':cp_report_id}

data = json.dumps(data_dict)

thing = LM_POST(AccessId, AccessKey, Company, resourcePath, queryParams, data)

lm_response = json.loads(thing['body'])
result_url = lm_response['data']['resulturl'].strip()

response = requests.head(result_url, allow_redirects=True)
response_url = response.url

final = requests.get(response_url)

if(final.status_code == 200):

	# Trim the first few nonsense characters
	csv = final.content.decode()
	csv = "\n".join(csv.split("\n", 1)[1:])

	TESTDATA = StringIO(csv)
	cpu_df = pandas.read_csv(TESTDATA, sep=',')

	# Remove unused columns
	cpu_df = cpu_df.drop(['Change(Delta)','Change(%)','Start','End','Datapoint'], axis=1)
	cpu_df = cpu_df.rename(index=str, columns={"Min":"CPU_Min_30_Days",
											   "Max":"CPU_Max_30_Days",
											   "Average":"CPU_Average_30_Days",
											   "Instance":"CPU_Instance"})
else:
	print('ERROR! CODE: '+(final.status_code))

#################
# MEMORY REPORT #
#################

mem_report_id = args.mem

data_dict = {'type':'generateReport',
			 'reportId':mem_report_id}

data = json.dumps(data_dict)

thing = LM_POST(AccessId, AccessKey, Company, resourcePath, queryParams, data)

lm_response = json.loads(thing['body'])
result_url = lm_response['data']['resulturl'].strip()

response = requests.head(result_url, allow_redirects=True)
response_url = response.url

final = requests.get(response_url)

if(final.status_code == 200):

	# Trim the first few nonsense characters
	csv = final.content.decode()
	csv = "\n".join(csv.split("\n", 1)[1:])

	TESTDATA = StringIO(csv)
	mem_df = pandas.read_csv(TESTDATA, sep=',')

	# Remove unused columns
	mem_df = mem_df.drop(['Change(Delta)','Change(%)','Start','End','Datapoint'], axis=1)
	mem_df = mem_df.rename(index=str, columns={"Min":"MEM_Min_30_Days",
											   "Max":"MEM_Max_30_Days",
											   "Average":"MEM_Average_30_Days",
											   "Instance":"MEM_Instance"})
else:
	print('ERROR! CODE: '+(final.status_code))

joined_df = cpu_df.merge(mem_df, on='Device')
row_count = joined_df.shape[0]

for i in range(row_count):
	original = joined_df.at[i,'Device']
	new = original.split(' (')[0]
	joined_df.at[i,'Device'] = new

####################
# DEVICE INVENTORY #
####################

inv_report_id = args.inv

data_dict = {'type':'generateReport',
			 'reportId':inv_report_id}

data = json.dumps(data_dict)

thing = LM_POST(AccessId, AccessKey, Company, resourcePath, queryParams, data)

lm_response = json.loads(thing['body'])
result_url = lm_response['data']['resulturl'].strip()

response = requests.head(result_url, allow_redirects=True)
response_url = response.url

final = requests.get(response_url)
csv = final.content.decode()

if(final.status_code == 200):

	# Trim the first few nonsense characters
	csv = final.content.decode()
	csv = "\n".join(csv.split("\n", 4)[4:])

	TESTDATA = StringIO(csv)
	inv_df = pandas.read_csv(TESTDATA, sep=',')

	last_df = joined_df.merge(inv_df, on='Device', how='outer')
else:
	print('ERROR! CODE: '+(final.status_code))

######################################
# Uncomment the below to write a CSV #
######################################

last_df.to_csv('inventory_report.csv', encoding='utf-8')

#############################################################################################
# Uncomment the below to update a text widget with an html table corresponding to your data #
#############################################################################################

html_header = '''
<html>
<head>
	<style>
	table {
		width: 100%;
		height: 100%;
	}
	tr, td, th {
	    font-family: Avenir, Helvetica, Arial, sans-serif;
	    border-collapse: collapse;
	}

	td, th {
	    border: 1px solid #ddd;
	    padding: 2px;
	}

	tr:nth-child(even) {background-color: #f2f2f2;}

	tr:hover {background-color: #ddd;}

	th {
	    padding-top: 12px;
	    padding-bottom: 12px;
	    text-align: center;
	    background-color: #037DF8;
	    color: white;
	}
	</style>
</head>
<body>
'''

html = last_df.to_html(index=False)

html_footer = '''
</body>
</html>
'''

html_file = html_header + html + html_footer

file_ = open('html.html', 'w')
file_.write(html_file)
file_.close()

#########################
# UPDATE LM TEXT WIDGET #
#########################

# First GET widget info

widgetID = args.widget

resourcePath = '/dashboard/widgets/' + str(widgetID)
queryParams = ''
data = ''

get_result = LM_GET(AccessId, AccessKey, Company, resourcePath, queryParams, data)
get_result_json = json.loads(get_result['body'])
widget = get_result_json['data']

widget['content'] = html_file
put_payload = json.dumps(widget)

update_result = LM_PUT(AccessId, AccessKey, Company, resourcePath, queryParams, put_payload)

if(update_result['code'] == 200):
	print('Success!')

