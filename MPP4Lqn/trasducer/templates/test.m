clear

X0=[50,0,0,0,0,0,0,0,0,4,3,11];
rep=1;
TF=2000;
dt=10^-2;
MU=[1,1,1,1];

X = poc(X0,MU, TF, rep, dt);
Xm=mean(X,3);

XCs=cumsum(Xm(1,2:end));
T=linspace(1,ceil(TF/dt),ceil(TF/dt));


plot(XCs./T);
