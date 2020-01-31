import matplotlib
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import re
import numpy as np
import sys

#Load list of users

users = []
with open(sys.argv[2],"r") as u_ptr:
	for line in u_ptr:
		# print(line)
		users.append(line.rstrip())
		
print(users)
# users = ['Arun Kumar Thangavel',
		 # 'Venkatraman Radhakrishnan',
		 # 'Dineshbabu Vellore Dinakarababu',
		 # 'Harsha Sriramagiri',
		 # 'Suresh Intel',
		 # 'Kaushik K Raghuraman',
		 # 'Vikram Siva Subramanian',
		 # 'Ayyappa Karthikeyan',
		 # 'Balakumar R',
		 # 'Arun Kumar Vikram',
		 # 'Harish Lalithkumar']
#Empty dicts
user_activity = {} ## Users with number of texts sent by each
date_activity = {} ## Dates with number of texts on that date
hour_activity = {} ## Most active time of the day
#Lines to ignore
ignore1 = re.compile(r'image omitted')
ignore2 = re.compile(r'video omitted')
ignore3 = re.compile(r'^(?!\[).*')
ignore4 = re.compile(r'\:\s')
text = ''
num_msgs = 0
#Open chat file
with open(sys.argv[1],"r",encoding="utf8") as f_ptr:
	#Read each line in loop
	for line in f_ptr:
		valid_line = ignore4.search(line)

		if (ignore1.search(line) or ignore2.search(line) or ignore3.search(line) or not(valid_line)):
			# print(line)
			continue
		print(line)
		text += re.split("]",line)[1].split(":")[1]
		# print(m)
		num_msgs+=1
		m = re.search(r'[\d]{1,2}/[\d]{1,2}/[\d]{1,2},\s[\d]{1,2}:[\d]{1,2}:[\d]{1,2}\s..',line)
		if m:
			date_time = datetime.strptime(m.group(),'%m/%d/%y, %I:%M:%S %p')
			
			date = date_time.date()
			time = date_time.time()
			#Load in to dict
			if date in date_activity:
				date_activity[date] += 1
			else:
				date_activity[date] = 1
			hour = ((time.hour)%24) + 1
			if hour in hour_activity:
				hour_activity[hour] += 1
			else:
				hour_activity[hour] = 1
		for name in users:
			m = re.search(name,line)
			if m:
				user = m.group()
				if user in user_activity:
					user_activity[user] += 1
				else:
					user_activity[user] = 1

#User activity Plot
plt.figure(1)
plt.bar(range(len(user_activity)),list(user_activity.values()),align='center',color='green')
plt.xticks(range(len(user_activity)), list(user_activity.keys()),rotation=15,fontsize=7)
plt.ylabel('# of Messages')
plt.xlabel('User')
plt.title("Activity by User")


#Date Acitivity
plt.figure(2)
ordered_date = sorted(date_activity.items(), key = lambda x:x, reverse=False)
x_val = [datetime.strftime(x[0],'%m/%d/%y') for x in ordered_date]
y_val = [x[1] for x in ordered_date]
ax2 = plt.axes()
ax2.set_facecolor("black")
ax2.xaxis.set_major_locator(ticker.MultipleLocator(3))
plt.xticks(rotation=15,fontsize=6)
plt.ylabel("# of Messages")
plt.xlabel("Date")
plt.title("Acitivity by Date")
plt.plot(x_val,y_val)

#Time Acitivy
ordered_date = sorted(hour_activity.items(), key = lambda x:x, reverse=False)
x_val = [(x[0]/24)*2*np.pi for x in ordered_date]
y_val = [x[1] for x in ordered_date]
fig = plt.figure(3)
ax = fig.add_subplot(111,projection='polar')
ax.plot(x_val,y_val,color='red')
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi/2)
ax.set_xticks(np.linspace(0,2*np.pi,24,endpoint=False))
ticks = ['12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', '7 AM','8 AM','9 AM','10 AM','11 AM','12 PM', '1 PM', '2 PM', '3 PM', '4 PM',  '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM', '11 PM']
ax.set_xticklabels(ticks)
plt.setp(ax.get_yticklabels(),visible=False)
plt.title("Activity by Time")
plt.show()