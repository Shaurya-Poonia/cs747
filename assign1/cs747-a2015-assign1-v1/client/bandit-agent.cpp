#include <iostream>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <cmath>
#include <math.h>
#include <vector>
#include <sstream>
#include <string>
#include <random>
#define MAXHOSTNAME 256

using namespace std;


//code used for beta distribution 
//source github shared repo
namespace sftrabbit {

  template <typename RealType = double>
  class beta_distribution
  {
    public:
      typedef RealType result_type;

      class param_type
      {
        public:
          typedef beta_distribution distribution_type;

          explicit param_type(RealType a = 2.0, RealType b = 2.0)
            : a_param(a), b_param(b) { }

          RealType a() const { return a_param; }
          RealType b() const { return b_param; }

          bool operator==(const param_type& other) const
          {
            return (a_param == other.a_param &&
                    b_param == other.b_param);
          }

          bool operator!=(const param_type& other) const
          {
            return !(*this == other);
          }

        private:
          RealType a_param, b_param;
      };

      explicit beta_distribution(RealType a = 2.0, RealType b = 2.0)
        : a_gamma(a), b_gamma(b) { }
      explicit beta_distribution(const param_type& param)
        : a_gamma(param.a()), b_gamma(param.b()) { }

      void reset() { }

      param_type param() const
      {
        return param_type(a(), b());
      }

      void param(const param_type& param)
      {
        a_gamma = gamma_dist_type(param.a());
        b_gamma = gamma_dist_type(param.b());
      }

      template <typename URNG>
      result_type operator()(URNG& engine)
      {
        return generate(engine, a_gamma, b_gamma);
      }

      template <typename URNG>
      result_type operator()(URNG& engine, const param_type& param)
      {
        gamma_dist_type a_param_gamma(param.a()),
                        b_param_gamma(param.b());
        return generate(engine, a_param_gamma, b_param_gamma); 
      }

      result_type min() const { return 0.0; }
      result_type max() const { return 1.0; }

      result_type a() const { return a_gamma.alpha(); }
      result_type b() const { return b_gamma.alpha(); }

      bool operator==(const beta_distribution<result_type>& other) const
      {
        return (param() == other.param() &&
                a_gamma == other.a_gamma &&
                b_gamma == other.b_gamma);
      }

      bool operator!=(const beta_distribution<result_type>& other) const
      {
        return !(*this == other);
      }

    private:
      typedef std::gamma_distribution<result_type> gamma_dist_type;

      gamma_dist_type a_gamma, b_gamma;

      template <typename URNG>
      result_type generate(URNG& engine,
        gamma_dist_type& x_gamma,
        gamma_dist_type& y_gamma)
      {
        result_type x = x_gamma(engine);
        return x / (x + y_gamma(engine));
      }
  };

  template <typename CharT, typename RealType>
  std::basic_ostream<CharT>& operator<<(std::basic_ostream<CharT>& os,
    const beta_distribution<RealType>& beta)
  {
    os << "~Beta(" << beta.a() << "," << beta.b() << ")";
    return os;
  }

  template <typename CharT, typename RealType>
  std::basic_istream<CharT>& operator>>(std::basic_istream<CharT>& is,
    beta_distribution<RealType>& beta)
  {
    std::string str;
    RealType a, b;
    if (std::getline(is, str, '(') && str == "~Beta" &&
        is >> a && is.get() == ',' && is >> b && is.get() == ')') {
      beta = beta_distribution<RealType>(a, b);
    } else {
      is.setstate(std::ios::failbit);
    }
    return is;
  }

}

void options(){

  cout << "Usage:\n";
  cout << "bandit-agent\n"; 
  cout << "\t[--numArms numArms]\n";
  cout << "\t[--randomSeed randomSeed]\n";
  cout << "\t[--horizon horizon]\n";
  cout << "\t[--hostname hostname]\n";
  cout << "\t[--port port]\n";
}


/*
  Read command line arguments, and set the ones that are passed (the others remain default.)
*/
bool setRunParameters(int argc, char *argv[], int &numArms, int &randomSeed, unsigned long int &horizon, string &hostname, int &port){

  int ctr = 1;
  while(ctr < argc){

    //cout << string(argv[ctr]) << "\n";

    if(string(argv[ctr]) == "--help"){
      return false;//This should print options and exit.
    }
    else if(string(argv[ctr]) == "--numArms"){
      if(ctr == (argc - 1)){
	return false;
      }
      numArms = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--randomSeed"){
      if(ctr == (argc - 1)){
	return false;
      }
      randomSeed = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--horizon"){
      if(ctr == (argc - 1)){
	return false;
      }
      horizon = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--hostname"){
      if(ctr == (argc - 1)){
	return false;
      }
      hostname = string(argv[ctr + 1]);
      ctr++;
    }
    else if(string(argv[ctr]) == "--port"){
      if(ctr == (argc - 1)){
	return false;
      }
      port = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else{
      return false;
    }

    ctr++;
  }

  return true;
}


int ucb2(int numArms, std::vector<float> empReward, std::vector<int> armEpochCount,int currentNumPlays,float alpha){

    float temp =0;
    int returnArm = 0;
    float T_r = 0;
    T_r = std::ceil(pow(1+alpha,armEpochCount[0]));
    temp = empReward[0] + sqrt((1+alpha)*log(exp(1)*currentNumPlays/T_r)/(2*T_r));
    for(int i=1;i<numArms;i++){

      T_r = std::ceil(pow(1+alpha,armEpochCount[i]));
      if(temp < empReward[i] + sqrt((1+alpha)*log(exp(1)*currentNumPlays/T_r)/(2*T_r))){
        temp = empReward[i] + sqrt((1+alpha)*log(exp(1)*currentNumPlays/T_r)/(2*T_r));
        returnArm = i;
      }

    }
    return returnArm;
}

int thompson(int numArms,int prevArm,int reward){
  static vector<int> armSuccess;
  static vector<int> armFailure;
  
  int i;
  if(prevArm==-1){
    for(i=0;i<numArms;i++){
      armSuccess.push_back(0);
      armFailure.push_back(0);
    }
  }else if(reward==1){
      armSuccess[prevArm]+=1;
  }else {
      armFailure[prevArm]+=1;
  }
  //random number generator
  std::random_device rd;
  std::mt19937 genRnd(rd());

  float bestSample = -1;
  float bestArm = 0;
  for(i=0;i<numArms;i++){
    sftrabbit::beta_distribution<> beta(armSuccess[i]+1, armFailure[i]+1);
    float betaSample = beta(genRnd); 
    if(betaSample>bestSample){
      bestSample = betaSample; 
      bestArm = i;  
    }
          
  } 
  return bestArm;
}

int main(int argc, char *argv[]){
  
  // Run Parameter defaults.
  int numArms = 5;
  int randomSeed = time(0);
  unsigned long int horizon = 1000;
  string hostname = "localhost";

  int port = 5000;

  //Set from command line, if any.
  if(!(setRunParameters(argc, argv, numArms, randomSeed, horizon, hostname, port))){
    //Error parsing command line.
    options();
    return 1;
  }

  struct sockaddr_in remoteSocketInfo;
  struct hostent *hPtr;
  int socketHandle;

  bzero(&remoteSocketInfo, sizeof(sockaddr_in));
  
  if((hPtr = gethostbyname((char*)(hostname.c_str()))) == NULL){
    cerr << "System DNS name resolution not configured properly." << "\n";
    cerr << "Error number: " << ECONNREFUSED << "\n";
    exit(EXIT_FAILURE);
  }

  if((socketHandle = socket(AF_INET, SOCK_STREAM, 0)) < 0){
    close(socketHandle);
    exit(EXIT_FAILURE);
  }

  memcpy((char *)&remoteSocketInfo.sin_addr, hPtr->h_addr, hPtr->h_length);
  remoteSocketInfo.sin_family = AF_INET;
  remoteSocketInfo.sin_port = htons((u_short)port);

  if(connect(socketHandle, (struct sockaddr *)&remoteSocketInfo, sizeof(sockaddr_in)) < 0){
    close(socketHandle);
    exit(EXIT_FAILURE);
  }


  char sendBuf[256];
  char recvBuf[256];

  int armToPull = 0;
  armToPull = thompson(numArms,-1,-1);
  sprintf(sendBuf, "%d", armToPull);
  cout << "Sending action " << armToPull << ".\n";
  while(send(socketHandle, sendBuf, strlen(sendBuf)+1, MSG_NOSIGNAL) >= 0){
      int reward = 0;
      recv(socketHandle, recvBuf, 256, 0);
      sscanf(recvBuf, "%d", &reward);
      cout << "Received reward " << reward << ".\n";
      armToPull = thompson(numArms,armToPull,reward);
      sprintf(sendBuf, "%d", armToPull);
      cout << "Sending action " << armToPull << ".\n";
  }

  /*int alpha = 0.01;
  int armToPull = 0;
  int currentNumPlays = 0;
  std::vector<float> empReward(numArms);
  std::vector<int> armEpochCount(numArms);
  std::vector<int> armSelectionCount(numArms);

  float reward = 0;
  for(int i=0;i<numArms;i++){
    armToPull = i;
    sprintf(sendBuf, "%d", armToPull);
    cout << "Sending action " << armToPull << ".\n";
    if(send(socketHandle, sendBuf, strlen(sendBuf)+1, MSG_NOSIGNAL) >= 0){
      recv(socketHandle, recvBuf, 256, 0);
      sscanf(recvBuf, "%f", &reward);
      cout << "Received reward " << reward << ".\n";
      empReward[armToPull] = reward;
      armEpochCount[armToPull] = 1;
      armSelectionCount[armToPull] = 1;
      currentNumPlays++;
    }
  }

  armToPull = ucb2(numArms, empReward,armEpochCount,currentNumPlays,alpha);
  sprintf(sendBuf, "%d", armToPull);
  cout << "Sending action " << armToPull << ".\n";

  while(send(socketHandle, sendBuf, strlen(sendBuf)+1, MSG_NOSIGNAL) >= 0){

    recv(socketHandle, recvBuf, 256, 0);
    sscanf(recvBuf, "%f", &reward);
    cout << "Received reward " << reward << ".\n";
    armSelectionCount[armToPull] += 1;
    armEpochCount[armToPull] += 1;
    empReward[armToPull] = (empReward[armToPull]*(armSelectionCount[armToPull]-1)+reward)/armSelectionCount[armToPull];


    float T_r1=0;
    float T_r = 0;
    T_r1 = std::ceil(pow(1+alpha,armEpochCount[armToPull]));
    T_r = std::ceil(pow(1+alpha,armEpochCount[armToPull]-1));

    //running for the epoch
    for(int i=0;i<T_r1-T_r;i++){
      sprintf(sendBuf, "%d", armToPull);
      cout << "Sending action " << armToPull << ".\n";
      if(send(socketHandle, sendBuf, strlen(sendBuf)+1, MSG_NOSIGNAL) >= 0){       
        
        recv(socketHandle, recvBuf, 256, 0);
        sscanf(recvBuf, "%f", &reward);
        cout << "Received reward " << reward << ".\n";
        
        armSelectionCount[armToPull] += 1;
        empReward[armToPull] = (empReward[armToPull]*(armSelectionCount[armToPull]-1)+reward)/armSelectionCount[armToPull];
        currentNumPlays++;
      }

    }
    
    armToPull = ucb2(numArms, empReward,armEpochCount,currentNumPlays,alpha);
    sprintf(sendBuf, "%d", armToPull);
    cout << "Sending action " << armToPull << ".\n";
    currentNumPlays++;
  }*/

  close(socketHandle);
  cout << "Terminating.\n";

}
          
