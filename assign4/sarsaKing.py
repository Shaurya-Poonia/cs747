#generating sequence of actions
import numpy as np
from myMainKing import act
from environKing import * 
epsilon = 0.1
gamma = 1
alpha = 0.1

def simulate(Q,start,goal,timesteps):

	i = start[0]
	j = start[1]
	x,y,a1 = policy1(Q,i,j)
	while(timesteps):
		if(goal[0]==x and goal[1]==y):
			break
		x,y,a1 = policy(Q,x,y,a1)
		timesteps = timesteps-1
	return Q,timesteps

	
def policy1(Q,i,j):

	temp = np.random.uniform()
	if(temp < epsilon):
		#choose random
		a =   np.random.randint(0,len(possibleAct(i,j)))
		x,y = transition(i,j,a) 
		a1 = bestAction(Q,x,y)
		Q[i][j][a] = Q[i][j][a] + alpha * (Q[x][y][a1]-1-Q[i][j][a])
		return x,y,a1
	else:
		#choose greedy
		a = bestAction(Q,i,j)
		x,y = transition(i,j,a) 
		a1 = bestAction(Q,x,y)	
		Q[i][j][a] = Q[i][j][a] + alpha * (Q[x][y][a1]-1-Q[i][j][a])
		return x,y,a1

	
def policy(Q,i,j,a):
	
	# print possibleAct(6,4);
	x,y = transition(i,j,a) 
	a1 = bestAction(Q,x,y)
	
	Q[i][j][a] = Q[i][j][a] + alpha * (Q[x][y][a1]-1-Q[i][j][a])
	return x,y,a1	

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
