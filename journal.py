import random
import csv

data_j=[['Name','Actual impact factor','Predicted impact factor','Error']]

def training(data_x,data_y):
	n=len(data_x)
	mean_x=0;mean_y=0;
	for i in range(len(data_x)):
		mean_x+=data_x[i]/n
		mean_y+=data_y[i]/n

	cov=0;sd_x=0;sd_y=0;sd_x_inc=0;sd_y_inc=0
	for i in range(len(data_x)):
		cov+=(data_x[i]-mean_x)*(data_y[i]-mean_y)/n
		sd_x_inc+=(data_x[i]-mean_x)**2
		sd_y_inc+=(data_y[i]-mean_y)**2
	sd_x=(sd_x_inc/n)**0.5
	sd_y=(sd_y_inc/n)**0.5
	corr_coef=cov/(sd_x*sd_y)
	a=corr_coef*sd_y/sd_x
	b=mean_y-a*mean_x
	return [corr_coef,a,b]

def testing(test_x):
	m=len(test_x)
	result_y=[]
	ans=training(train_h,train_i)[1:]
	a,b=map(float,ans)
	for i in range(len(test_x)):
		result_y.append(a*test_x[i]+b)
	if len(data_j[1])<3:
		for i in range(len(data_j)-1):
			data_j[i+1].append(result_y[i])
	return result_y

def calc_error(test_y,result_y):
	errors=[]
	er_sq=0;
	m=len(test_y)
	for i in range(len(result_y)):
		errors.append(test_y[i]-result_y[i])
		er_sq+=(test_y[i]-result_y[i])**2
	er_ms=(er_sq/m)
	for i in range(len(data_j)-1):
		data_j[i+1].append(errors[i])
	return er_ms


##### Extracting impact factor and h-index from found.txt ######
file="found.txt"
f=open(file,"r")
lines=f.readlines()
impact_factor=[] 
h_index=[]
names=[]
for x in lines:
    impact_factor.append(float((x.split(';')[2]).split('\n')[0]))
    h_index.append(float((x.split(';')[1])))
    names.append(x.split(';')[0])

f.close()

#h_index=[1,2,3,4,5,6,7,8,9,10]
#impact_factor=[2,4,6,8,10,12,14,16,18,20]

#### Randomizer #####
map_in=list(zip(names,h_index,impact_factor))
random.shuffle(map_in)
names,h_index,impact_factor=zip(*map_in)


#### Dividing dataset into 80% data for training and 20% for testing ####
train_h=h_index[:int(0.8*len(h_index))]         #from 0 to 496 exclusive
train_i=impact_factor[:len(train_h)]
train_n=names[:len(train_h)]
test_y=impact_factor[len(train_i):]
test_x=h_index[len(train_h):]
test_names=names[len(train_h):]

for i in range(len(test_names)):
	entry=[]
	entry.append(test_names[i])
	entry.append(test_y[i])
	data_j.append(entry)

csv.register_dialect('myDialect',delimiter = ';',
quoting=csv.QUOTE_NONE,skipinitialspace=True)

if __name__=="__main__":
	
	#### To see correlation coefficient for complete data ####
	print("Correlation Coefficient: "+str(training(h_index,impact_factor)[0]))

	print("a: "+str(training(train_h,train_i)[1]))
	print("b: "+str(training(train_h,train_i)[2]))

	print("Mean-squared error: "+str(calc_error(test_y,testing(test_x))))

	#### Writing to spreadsheet ####

	#------- Journals -------#
	with open ('Journals_data.csv','w') as jour_w:
		writer=csv.writer(jour_w,dialect='myDialect')
		writer.writerows(data_j)
	jour_w.close()

