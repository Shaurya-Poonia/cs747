Use run.sh 

./run.sh option 

to for executing the code. 

Option

1: run epsilon greedy sarsa with only 4 moves.
2: run epsilon greedy sarsa with king's moves.
3: run epsilon greedy sarsa with stochastic wind and king's moves.

------------------------------------------------------------------------
By default i am plotting timestamp vs no of episodes graph. 
If you want to check the route agent follows after getting optimal Q.
please comment line 17,34,35,36 
and uncomment line 18,32
-------------------------------------------------------------------------


General code file structure:

main.py :- it is highest abstraction of code. Runs different configurations requested based on option passed as arguement and plots path taken by agent.

myMain(*).py :- runs sarsa and returns no. of episodes for given timestamps and returns path taken by greedy policy once sarsa is finished updating Q values.

sarsa(*).py :- implementation of sarsa algorithm for different configurations

environ(*).py :- environment behavior is coded in these file.

Note: * is marked to indicate set of file with same name format. * means set of three strings {"", "King","Stoch"}. 

"" means basic configuration. 
King means kings move configuration. 
Stoch means stochastic environment.  

