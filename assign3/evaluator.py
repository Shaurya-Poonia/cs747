import csv,sys
import matplotlib.pyplot as plt

def fillLocalQ(inData):
	nStates = int(inData[0][0])
	nActions = int(inData[1][0])
	dF = float(inData[2][0])
	episode = [[int(x[0]),int(x[1]),float(x[2])] for x in inData[3:-1]]
	Q  = [[0 for x in range(nActions)] for x in range(nStates)]
	T  = [[0 for x in range(nActions)] for x in range(nStates)]
	return nStates,nActions,dF,Q,T,episode

def fillLocalV(inData):
	nStates = int(inData[0][0])
	nActions = int(inData[1][0])
	dF = float(inData[2][0])
	episode = [[int(x[0]),int(x[1]),float(x[2])] for x in inData[3:-1]]
	episode.append(int(inData[-1][0]))
	V  = [ 0 for x in range(nStates)]
	return nStates,nActions,dF,V,episode


def sarsaOnPolicy(Q,T,nStates,nActions,dF,episode,alpha):

	for i in xrange(0,len(episode)-1):
		St = episode[i][0]
		At = episode[i][1]
		Rt1 = episode[i][2]
		
		St1 = episode[i+1][0]
		At1= episode[i+1][1]
		#update Q
		Q[St][At] = Q[St][At] + alpha*(Rt1+dF*Q[St1][At1]-Q[St][At]) 
		T[St][At] = T[St][At]+1

	St = episode[-2][0]
	St1 = episode[-1][1]
	Rt1 = episode[-2][2]
	At = episode[-2][1]
	At1 = Q[St1].index(max(Q[St1]))
	Q[St][At] = Q[St][At] + alpha*(Rt1+dF*Q[St1][At1]-Q[St][At])
	return Q,T



def TD(V,nStates,nActions,dF,episode,alpha):

	for i in xrange(0,len(episode)-2):
		St = episode[i][0]
		Rt1 = episode[i][2]
		St1 = episode[i+1][0]
		#update V
		V[St] = V[St] + alpha*(Rt1+dF*V[St1]-V[St]) 

	St = episode[-2][0]
	St1 = episode[-1]
	Rt1 = episode[-2][2]
	V[St] = V[St] + alpha*(Rt1+dF*V[St1]-V[St])
	return V



if __name__ == '__main__':
	inData  = list(csv.reader(open("data/"+sys.argv[1],'r'),delimiter='\t'))

	alpha = 0.0125

	nStates,nActions,dF,V,episode = fillLocalV(inData)
	
	for i in range(1):
		
		# nStates,nActions,dF,Q,T,episode = fillLocalQ(inData)
		# for i in range(1):
		# 	Q,T = sarsaOnPolicy(Q,T,nStates,nActions,dF,episode,alpha)
		# T = [[y/sum(x)for y in x]for x in T]
		# V = [sum([Q[j][i]*T[j][i] for i in range(nActions)]) for j in range(nStates)]
		# V1 = [round(x,6) for x in V]
		# print V1

		# for i in range(1):
		# 	Q,T = sarsaOfPolicy(Q,T,nStates,nActions,dF,episode,alpha)
		# T = [[y/sum(x)for y in x]for x in T]
		# V = [sum([Q[j][i]*T[j][i] for i in range(nActions)]) for j in range(nStates)]
		# V2 = [round(x,6) for x in V]
		# print V2
		for i in range(1):
			V = TD(V,nStates,nActions,dF,episode,alpha)
		V3 = [round(x,6) for x in V]
		for i in V3:
			print i
		# V4 =  [float(x[0]) for x in list(csv.reader(open(sys.argv[2],'r')))]
		# print V4
		# print sum([(x-y)*(x-y) for x,y in zip(V1,V4)])
		# print sum([(x-y)*(x-y) for x,y in zip(V2,V4)])
		# print sum([(x-y)*(x-y) for x,y in zip(V3,V4)])
		# err.append(sum([(x-y)*(x-y) for x,y in zip(V3,V4)]))
		# alpha = alpha+0.00001	
	# plt.plot([0.012+0.00001*i for i in range(100)],err)	
	# plt.show()



