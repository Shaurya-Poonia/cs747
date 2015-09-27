import sys

def cleanLine(line):
	line = line.strip().split()
	return [float(i) for i in line]


def readInput(inputFile):

	inputFile = open("../data/"+inputFile,'r')

	nStates  = inputFile.readline().strip()
	nStates = int(nStates)

	nActions = inputFile.readline().strip()
	nActions = int(nActions)

	# R = [[[0]*nStates]*nActions]*nStates
	R = list()

	for i in range(nStates):
		R.append(list())
		for j in range(nActions):
			#line = cleanLine(inputFile.readline())
			temp = cleanLine(inputFile.readline())
			R[i].append(temp)
			# R[i][j] = []
			#for k in range(nStates):
			#	R[i][j][k] = line[k]

	# T = [[[0]*nStates]*nActions]*nStates
	T = list()

	for i in range(nStates):
		T.append(list())
		for j in range(nActions):
			#line = cleanLine(inputFile.readline())
			temp = cleanLine(inputFile.readline())
			T[i].append(temp)
			# R[i][j] = []
			#for k in range(nStates):
			#	R[i][j][k] = line[k]

	dFactor = inputFile.readline().strip()
	dFactor = float(dFactor)

	return nStates,nActions,R,T,dFactor

def bestActionValue(state,nStates,nActions,T,R,dFactor,V):
	stateValue = 0
	stateAction = 0
	stateValueTemp = 0
	for i in range(nActions):
		stateValueTemp = 0
		for j in range(nStates):
			stateValueTemp  = stateValueTemp + T[state][i][j]*(R[state][i][j]+dFactor*V[j])

		if stateValueTemp > stateValue:
			stateValue = stateValueTemp
			stateAction = i
	return stateValue,stateAction 


def valueIteration(inputFile):

	nStates,nActions,R,T,dFactor = readInput(inputFile)
	V = list()
	A = list()

	#initialize v with zeroes
	for i in range(nStates):
		V.append(0)
		A.append(0)

	while(1):
		delta = 0
		v=0
		for i in range(nStates):
			v = V[i]
			V[i],A[i] = bestActionValue(i,nStates,nActions,T,R,dFactor,V)
			if(delta < abs(v-V[i])):
				delta = abs(v-V[i])
		if(delta< 0.000001):
			break

	return V,A

if __name__ == '__main__':
	
	inputFile = sys.argv[1]
	V,A = valueIteration(inputFile)
	zipVA = zip(V,A)
	
	#print value and corresponding action
	for value,action in zipVA:
		print value,action
	
	




	


