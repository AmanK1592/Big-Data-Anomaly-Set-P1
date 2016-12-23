import os, re
import sys , struct, math
import multiprocessing
from Queue import *

PATH = "/home/aman/Desktop/DATA1/"

degree =[0]*3969
index = 0
count = 0 
file_no = 0
r1 =0.95
#r2 =0.95
lag = 0
file_count = math.floor(52*16/(lag+1))
n = 3969
Data = [[0]*n for x in xrange(file_count)]
Sxy = [[0]*n for x in xrange(n)]
adjacency_matrix1 = [[0]*n for x in xrange(n)]

# here start and end mean that from where to where am doing all the computation 

def multiplication(start,end):
	print start,end
	string = str(start)
	f = open(string,'w')
	for j in xrange(start,end):				# calculate for 3969 values
		for i in xrange (0,file_count):		# file_count is n in the summation
			for k in xrange (0,3969):	#
				Sxy[j][k] = Sxy[j][k] + (Data[i][j])*(Data[i][k])
		for k in range(0,3969):
			f.write(str(Sxy[j][k])+' ')
		f.write('\n')
	f.close()

#this is the main part that iterates over all the files in the folder PATH

for path, dirs, files in os.walk(PATH):
# for subdir in dirs:
	for filename in files:
		file_no = file_no + 1
		fullpath = os.path.join(path,filename)
#		print("file" j " is done")
#		print fullpath, count
		if file_no%(lag+1)==0:
			with open(fullpath,'r') as fi:   # using with automatically closes the file 
				i=0
				while True:
					count = count +1 
					data = fi.read(4)
					if len(data) < 4: 
						break 
		#		try : 						# To take care of any exceptions
					val = struct.unpack('<f',data)[0] 
		#		print val, count
					if abs(val)>100:
						val = 0
				
					Data[((file_no)/(lag+1))-1][i] = val # this is the deviation from normal
		#		print Data[file_no-1][i] , file_no , i
#				Sum[i] = Sum[i] + val
					i = i+1
		#		except : 
		#			pass

print file_no

# To parallelize calculation of clustering coefficient

jobs=[]
i=0
offset=567 # here offset can be any factor of 3969.. number of processes will be made accordingly.. 
while i+offset <=3969:
	p = multiprocessing.Process(target=multiplication, args=(i,i+offset))
	jobs.append(p)
	p.start()
	i+=offset

for p in jobs:
	p.join()

#f = open("out1.txt",'w')
#f.write(str(file_no)+'\n')
#f.close()
os.system("cat 0 567 1134 1701 2268 2835 3402 > out1.txt")
os.system("rm 0 567 1134 1701 2268 2835 3402")

# parallelization done


f=open('out1.txt','r')
Sxy=[]
for i in f:
	i=i.strip('\n')
	i=i.strip(' ')
	li=map(float,i.split(' '))
	if len(li)!=3969:
		print "Wrong"
	Sxy.append(li)
print len(Sxy)

#Calculate r for each index and update the incidence matrix
matrix = [[] for x in xrange(3969)]
for j in xrange (0,3969):
	for k in xrange(0,3969):
		denomi = Sxy[j][j]*Sxy[k][k] 
		if denomi > 0 :
			if ( (( Sxy[j][k] + Sxy[k][j] )/2) / math.sqrt(denomi) ) > r1  :	#this will count connectivity with self too - which is ok really 
				degree[j]=degree[j] + 1
#				adjacency_matrix1[j][k] = 1
				matrix[j].append(k)
degree_total = 0
target = open('Degree','w')
for i in xrange(0,3969):
	target.write(str(degree[i]) + "\n")
	matrix[i] = set(matrix[i])
	degree_total = degree_total + degree[i]

degree_mean = degree_total / 3969

f = open('Result','w')
f.write("Average degree " + str(degree_mean) + "\n")

print "Average degree " , str(degree_mean)
#Ev=[0]*3969
#for i in xrange (0,3969):
#	if degree[i]!=0:
#		for j in xrange(1, degree[i]):
#			for k in xrange(j,degree[i]):
#				if adjacency_matrix[j][k] ==1
#					Ev[i] = Ev[i]+1

print "Calculating clustering coefficient"

cluster_coeff = [0]*3969
for i in xrange (0,3969):
	S = matrix[i]
	edge_count = degree[i] - 1
	summ = 0
	for j in S:
		SS = matrix[j]	
		summ += len(S & SS) 		  # to check how many of the neighbours are connected to each other
	edge_count += summ >> 1
	if degree[i] > 1:
		cluster_coeff[i] = (edge_count*2.0)/(degree[i]*(degree[i]-1)*1.0)

#clustering coefficient
mean = 0
target = open('Cluster','w')
for i in xrange(0,3969):
	target.write(str(cluster_coeff[i]) + "\n")
	mean += cluster_coeff[i]

mean = mean / 3969

f.write("Clustering Coefficient : " + str(mean) + "\n")
print "Clustering Coefficient : " , mean

q = Queue()
p=0
#characteristic path length
for i in xrange(0,3969):
	if degree[i]>1:
		visited=[0]*3969
		# compute shortest path till j 
		for j in matrix[i]:
			q.put((j,1))
#			adjacency_matrix[i][j] = 1
			p+=1
			visited[j] = 1
		
		while (q.empty()==False):
			a = q.get()
			if visited[a[0]] == 0:
				for k in matrix[a[0]]:
					if visited[k] == 0:
#						adjacency_matrix[i][k] = a[1]+1
						p+=1
						visited[k] = 1
						q.put((k,a[1]+1))

count = 0			
for i in xrange(0,3969):
	if degree[i] > 1: 
		count+=1

cpl = (p *1.0)/(count*1.0)
		
print "Characteristic path length : " , cpl 
f.write("Characteristic path length : " + str(cpl) + "\n")
				
		
	
