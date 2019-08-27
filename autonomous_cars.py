import numpy as puppy
import copy
from collections import Counter

ifile=open("input.txt","r")
ofile=open("output.txt","w")
s=int(ifile.readline())
n=int(ifile.readline())
o=int(ifile.readline())
obstacles=[]
start=[]
end=[]
for i in range(o):
	str1=ifile.readline()
	list1=str1.split(',')
	obstacles.append((int(list1[0]),int(list1[1].rstrip())))
for i in range(n):
	str1=ifile.readline()
	list1=str1.split(',')
	start.append((int(list1[0]),int(list1[1].rstrip())))
for i in range(n):
	str1=ifile.readline()
	list1=str1.split(',')
	end.append((int(list1[0]),int(list1[1].rstrip())))

def go(x,y,a):
	if a=='N':
		if x==0 and y==0:
			return (x,y)
		if x==0 and y==s-1:
			return (x,y)
		if x==0:
			return (x,y)
		return (x-1,y)
	if a=='S':
		if x==s-1 and y==0:
			return (x,y)
		if x==s-1 and y==s-1:
			return (x,y)
		if x==s-1:
			return (x,y)
		return (x+1,y)
	if a=='W':
		if x==0 and y==0:
			return (x,y)
		if x==s-1 and y==0:
			return (x,y)
		if y==0:
			return (x,y)
		return (x,y-1)
	if a=='E':
		if x==0 and y==s-1:
			return (x,y)
		if x==s-1 and y==s-1:
			return (x,y)
		if y==s-1:
			return (x,y)
		return (x,y+1)

def turn_left(move):
	if move=='N':
		return 'W'
	if move=='W':
		return 'S'
	if move=='S':
		return 'E'
	if move=='E':
		return 'N'

def turn_right(move):
	if move=='N':
		return 'E'
	if move=='E':
		return 'S'
	if move=='S':
		return 'W'
	if move=='W':
		return 'N'

#print s
#print n
#print o
#print obstacles
#print start
#print end

city=[[-1 for x in range(s)]for x in range(s)]

for i in range(o):
	a=obstacles[i][0]
	b=obstacles[i][1]
	city[a][b]+=-100

startcount={}
endcount={}
startcount=Counter(start)
endcount=Counter(end)

#print "startcount"
#for i in startcount:
#	print i,startcount[i]
#print "endcount"
#for i in endcount:
#	print i,endcount[i]

storepolicy={}
storeutil={}

#for x in range(s):
#	print city[x]

actions=['W','E','S','N']
gamma=0.9
util=[0 for x in range(n)]

#util=puppy.zeros(n,dtype=int)

for x in range(n):
	if start[x][0]==end[x][0] and start[x][1]==end[x][1]:
		util[x]=100

policyGenerated=False
utilGenerated=False
count=0
count1=0

for z in range(n):
	if z!=0:
		city[end[z-1][0]][end[z-1][1]]-=100
	city[end[z][0]][end[z][1]]+=100

	if util[z]==100:
		continue

	if end[z] in storepolicy:
		if start[z] in storepolicy[end[z]][1]:
			utilGenerated=True

	if utilGenerated==True:
		count1+=1
		for x in range(len(storeutil[end[z]])):
			if start[z] == storeutil[end[z]][x][1]:
#				print storeutil[end[z]][x][0]
				util[z]=storeutil[end[z]][x][0]
				utilGenerated=False
		if utilGenerated==False:
			continue

	if endcount[end[z]]>1:
		policyGenerated=True
		if end[z] not in storepolicy:
			policyGenerated=False

	if policyGenerated==False:
		value=[[0 for x in range(s)]for x in range(s)]
#		value=puppy.zeros((s,s),dtype=int)
		act=[[' ' for x in range(s)]for x in range(s)]
		
#		for x in range(s):
#			print city[x]
#		for x in range(s):
#			print city[x]
#		for x in range(s):
#			print value[x]
		max1=-100000
		d=1
		error=0.1
		prob=0
		errorReached=False
#		for z in range(100):
		prevvalue=[[0 for x in range(s)] for x in range(s)]
#		prevvalue=puppy.zeros((s,s),dtype=int)
		while d>0.1*((0.1)/0.9):
			d=0
			errorReached=True
#			print "next"
			for x in range(s):
				for y in range(s):
					if city[x][y]==99:
						value[x][y]=99
						continue
					temp=value[x][y]
					max1=-100000
					for a in range(4):
						sum1=0
#						print sum1
#						print max1
						for b in range(4):
							if b==a:
								prob=0.7
							else:
								prob=0.1
							papa=go(x,y,actions[b])
#							sum1=round(sum1+(prob*(city[x][y]+gamma*value[papa[0]][papa[1]])),5)
							sum1=sum1+prob*value[papa[0]][papa[1]]
#							print sum1,actions[b],papa,prob
						if sum1>=max1:
							max1=sum1
#							print max1
							act[x][y]=actions[a]
#					value[x][y]=max1
					value[x][y]=city[x][y]+gamma*max1
					if abs(value[x][y]-prevvalue[x][y])>=d:
						d=abs(value[x][y]-prevvalue[x][y])
						errorReached=False
			prevvalue=copy.deepcopy(value)
		if endcount[end[z]]>1:
			storepolicy[end[z]]=(act,[start[z]])
#		print "utilities"
#		for x in range(s):
#			print value[x]
#		print "policy"
#		for x in range(s):
#			print act[x]
		count+=1
	if policyGenerated==True:
		act=storepolicy[end[z]][0]
#	count2=0
	for j in range(10):
		curr=start[z]
		puppy.random.seed(j)
		iterr=puppy.random.random_sample(1000000)
		k=0
		while(curr!=end[z]):
#			count2+=1
#			print curr,util
			util[z]=util[z]+city[curr[0]][curr[1]]
			move=act[curr[0]][curr[1]]
			if iterr[k]<=0.7:
				curr=go(curr[0],curr[1],move)
#				print move,round(iterr[k],2)
#				util=util+value[curr[0]][curr[1]]
			elif iterr[k]>0.7 and iterr[k]<=0.8:
#				print move
				move=turn_right(move)
#				move=turn_left(turn_left(move))
#				prev=curr
				curr=go(curr[0],curr[1],move)
#				print move,round(iterr[k],2)
#				if prev==curr:
#					util-=1
#				util=util+value[curr[0]][curr[1]]
			elif iterr[k]>0.8 and iterr[k]<=0.9:
#				print move
				move=turn_left(move)
#				prev=curr
				curr=go(curr[0],curr[1],move)
#				print move,round(iterr[k],2)
#				if prev==curr:
#					util-=1
#				util=util+value[curr[0]][curr[1]]
			elif iterr[k]>0.9 and iterr[k]<=1.0:
#				print move
				move=turn_left(turn_left(move))
#				prev=curr
#				move=turn_right(move)
				curr=go(curr[0],curr[1],move)
#				print move,round(iterr[k],2)
#				if prev==curr:
#					util-=1
#				util=util+value[curr[0]][curr[1]]
			k+=1
#			print util[z]
			if curr==end[z]:
				util[z]=util[z]+100
#		print util[z]
#		print "----------"
	if endcount[end[z]]>1:
		if policyGenerated==False:
			if start[z] not in storepolicy[end[z]][1]:
				storepolicy[end[z]][1].append(start[z])
			storeutil[end[z]]=[(util[z],start[z])]

	alreadyThere=False
	if policyGenerated==True:
		if start[z] not in storepolicy[end[z]][1]:
			storepolicy[end[z]][1].append(start[z])
		for x in range(len(storeutil[end[z]])):
			if start[z] == storeutil[end[z]][x][1]:
				alreadyThere=True
		if alreadyThere==False:
			storeutil[end[z]].append((util[z],start[z]))

	policyGenerated=False
#	print count2

for x in range(n):
	if util[x]==100 and start[x][0]==end[x][0] and start[x][1]==end[x][1]:
		util[x]+=900
#print util
#for i in storepolicy:
#	print i,storepolicy[i]
#for i in storeutil:
#	print i,storeutil[i]	
#print "hh"
answer=0.0
for x in range(n):
	answer=puppy.floor(float(util[x]/10.0))
	print int(answer)
	ofile.write(str(int(answer)))
	ofile.write("\n")
#print count
#print count1
ifile.close()
ofile.close()