#create an action dictionary 
act = dict(zip([i for i in range(8)],['l','r','u','d','lu','ld','ru','rd']))
from sarsaStoch import * 

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
		if(i==x and j==y):
			break
		i1,j1 = windEffect(i,j)
		a = bestAction1(Q,i1,j1)
		row.append(i)
		col.append(j)
		i,j = transition(i1,j1,a)

	row.append(3)
	col.append(7)
	return row,col

def plot(x,y):
	plt.plot(y,x)
	plt.grid()
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
	# print episodes
	# plot(x,y)
	return x,y,episodes
	# return len(x)-1
