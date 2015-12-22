act = dict(zip([i for i in range(4)],['l','r','u','d']))
#create an action dictionary 

from sarsa import * 


def bestAction1(Q,i,j):
	
	psbleActA = range(len(act))

	temp = np.random.uniform()

	#choose greedy
	validQ = [Q[i][j][k] for k in psbleActA]
	maxQA = max(validQ)  

	Alist = [];
	for k in psbleActA:
		if Q[i][j][k]==maxQA:
			Alist.append(k)

	return Alist[np.random.randint(0,len(Alist))]


def getPolicy(Q,i,j,x,y):
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


def run(timesteps):
	#create a two dimensional list of Q
	Q = list()
	for i in range(7):
		temp = list()
		for j in range(10):
			temp.append([0 for i in range(4)])
		Q.append(temp)
	episodes = 0
	while(timesteps):
		Q,timesteps = simulate(Q,(3,0),(3,7),timesteps)
		episodes = episodes+1
	# episodes = episodes*10
	x,y = getPolicy(Q,3,0,3,7)
	# print x
	# print y
	# print episodes
	return x,y,episodes
	# plot(x,y)
	# return len(x)-1
