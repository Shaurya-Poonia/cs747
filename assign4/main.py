import myMain1
import myMain
import myMainKing 
import myMainStoch 
import sys
import matplotlib.pyplot as plt


def plot(x,y):
	plt.plot(y,x)
	plt.grid()
  	plt.axis((-1,10,-1,7))
	plt.show()

if __name__ == '__main__':
	option = int(sys.argv[1])
	epCount = list()
	tsCount = range(1,8000,100)
	# tsCount = [80000]
	for timesteps in tsCount:
		if option == 1:
			
			x,y,z = myMain1.run(timesteps)

		elif option == 2:
			
			x,y,z = myMainKing.run(timesteps)		

		elif option == 3:
			
			x,y,z = myMainStoch.run(timesteps)
		
		# plot(x,y)
		print z
		epCount.append(z)
	plt.plot(tsCount,epCount)
	plt.show()
		