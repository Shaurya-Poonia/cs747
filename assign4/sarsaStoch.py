#generating sequence of actions
import numpy as np
from myMainStoch import act
from environStoch import * 
epsilon = 0.1
gamma = 1
alpha = 0.1

def simulate(Q,start,goal,timesteps):

	i = start[0]
	j = start[1]
	x,y,a1,x1,y1 = policy1(Q,i,j)
	count = 0
	while(timesteps):
		count = count+1
		if(goal[0]==x and goal[1]==y):
			break
		x,y,a1,x1,y1 = policy(Q,x,y,a1,x1,y1)

		timesteps = timesteps-1
	return Q,timesteps

	
def policy1(Q,i,j):

	temp = np.random.uniform()
	if(temp < epsilon):
		#choose random
		i1,j1 = windEffect(i,j);
		a =   possibleAct(i1,j1)[np.random.randint(0,len(possibleAct(i,j)))]
		x,y = transition(i1,j1,a)
		x1,y1 = windEffect(x,y) 
		a1 = bestAction(Q,x1,y1)
		Q[i][j][a] = Q[i][j][a] + alpha * (Q[x][y][a1]-1-Q[i][j][a])
		return x,y,a1,x1,y1
	else:
		#choose greedy
		i1,j1 = windEffect(i,j);
		a = bestAction(Q,i1,j1)
		x,y = transition(i1,j1,a) 
		x1,y1 = windEffect(x,y)
		a1 = bestAction(Q,x1,y1)	
		Q[i][j][a] = Q[i][j][a] + alpha * (Q[x][y][a1]-1-Q[i][j][a])
		return x,y,a1,x1,y1

	
def policy(Q,i,j,a,i1,j1):
	
	# print possibleAct(6,4);
	# i1,j1 = windEffect(i,j)
	x,y = transition(i1,j1,a) 
	x1,y1 = windEffect(x,y)
	a1 = bestAction(Q,x1,y1)
	
	Q[i][j][a] = Q[i][j][a] + alpha * (Q[x][y][a1]-1-Q[i][j][a])
	return x,y,a1,x1,y1	

def bestAction(Q,i,j):
	
	psbleActA = possibleAct(i,j)

	temp = np.random.uniform()
	
	if(temp < epsilon):
		
		return psbleActA[np.random.randint(0,len(psbleActA))]
	
	else:
		#choose greedy
		validQ = [Q[i][j][k] for k in psbleActA]
		maxQA = max(validQ)  
	
		Alist = [];
		for k in psbleActA:
			if Q[i][j][k]==maxQA:
				Alist.append(k)

		return Alist[np.random.randint(0,len(Alist))]