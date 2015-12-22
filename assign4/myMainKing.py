#create an action dictionary 
act = dict(zip([i for i in range(8)],['l','r','u','d','lu','ld','ru','rd']))
import matplotlib.pyplot as plt
from sarsaKing import * 


def bestAction1(Q,i,j):
	
	psbleActA = possibleAct(i,j)

	temp = np.random.uniform()

	#choose greedy
	validQ = [Q[i][j][k] for k in psbleActA]
	maxQA = max(validQ)  

	Alist = [];
	for k in psbleActA:
		if Q[i][j][k]==maxQA:
			Alist.append(k)

	return Alist[np.random.randint(0,len(Alist))]


def printPolicy(Q,i,j,x,y):
	row = list()
	col = list()
	for k in range(30):
		a = bestAction1(Q,i,j)
		row.append(i)
		col.append(j)
		i,j = transition(i,j,a)
	count = 0
	for i,j in zip(row,col):
		count = count+1
		if(i==x and j==y):
			break;
		
	return row[:count],col[:count]

def plot(x,y):
	plt.plot(y,x)
	plt.grid()
	x1,x2,y1,y2 = plt.axis()
  	plt.axis((-1,10,-1,7))
	plt.show()

def run(timesteps):
	#create a two dimensional list of Q
	Q = list()
	for i in range(7):
		temp = list()
		for j in range(10):
			temp.append([0 for i in range(8)])
		Q.append(temp)
	episodes=0
	while(timesteps):
		Q,timesteps = simulate(Q,(3,0),(3,7),timesteps)
		episodes = episodes+1
		
	x,y = printPolicy(Q,3,0,3,7)
	# print x
	# print y
	# plot(x,y)
	# return len(x)-1
	return x,y,episodes