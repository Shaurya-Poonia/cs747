#generating sequence of actions
from myMainKing import act 


def possibleAct(i,j):
	return range(len(act))

def checkValidAct(i,j,a):
	"""checks validity of action 
	Helper function of transition 
	"""
	a1=act[a]
	if i==0 and a1=='d':
		return False
	elif i==6 and a1=='u':
		return False
	elif j==0 and a1=='l':
		return False
	elif  j==9 and a1=='r':
		return False
	elif (i==0 or j==0) and a1=='ld':
		return False
	elif (i==6 or j==0) and a1=='lu':
		return False
	elif (i==0 or j==9) and a1=='rd':
		return False
	elif (i==6 or j==9) and a1=='ru':
		return False
	else:
		return True
	

def transition(i,j,a):
	""" Returns state after taking the action a. 
	If not a valid action returns False
	"""
	if checkValidAct(i,j,a):
		a = act[a]
		if a=='u':
			#change the state to just above the one you are in
			i = i+1
		elif a=='d':
			#change the state to just below
			i = i-1
		elif a=='l':
			#change the state to just left of the one you are in 
			j = j-1
		elif a=='r':
			#change the state to just right to the one you are in 
			j = j+1
		elif a=='lu':
			#change the state to just right to the one you are in 
			j = j-1
			i = i+1
		elif a=='ld':
			#change the state to just right to the one you are in 
			j = j-1
			i = i-1
		elif a=='ru':
			#change the state to just right to the one you are in 
			j = j+1
			i = i+1
		else:
			#change the state to just right to the one you are in 
			j = j+1
			i = i-1			

	else:
		pass

	i,j = windEffect(i,j)
	return i,j

wind = [0,0,0,1,1,1,2,2,1,0]

def windEffect(i,j):
	"""
	adds wind effect to the trasition.
	helper function of transition
	"""
	if(i+wind[j]>6):
		return (6,j)
	else:
		return (i+wind[j],j)
