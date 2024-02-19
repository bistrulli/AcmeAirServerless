%clear

N=10;
K=10;
TF=N*K;

%dimensione dipendi dal numero di nomi
X0=zeros(1,45);
MU=zeros(1,45);

X0(7)=300;

%MU([7 10 13 16 19 22 31 36 39 42 ])=1./[0.2 0.05 0.15 0.15 0.2 0.15 0.1 0.05 0.09 0.1 ]; 
MU([7 10 13 16 19 22 31 36 39 42 ])=1./[0.25,...
           0.06204,...
           0.1608,...
           0.14518,...
           0.20688,...
           0.15372,...
           0.14292,...
           0.07316,...
           0.09026,...
           0.1048 ]; 
NT=[1 1 1 1 1 1 1 1 1 1 ]*inf;
NC=[1 1 1 1 1 1 1 1 1 1 ]*inf;

[t,y,ssROde] = lqnODE(X0,MU,NT,NC);

Tode=ssROde(7);
RTode=X0(7)/Tode;

NCopt=[inf,y(end,[10 13 16 19 22 31 36 39 42])];
NTopt=[inf,sum(y(end,[9,10])),y(end,13),y(end,16),y(end,19),y(end,22),...
    sum(y(end,[27,28,29,30,31])),sum(y(end,[34,35,36])),y(end,39),y(end,42)];

% [Tb,RTsim;
%  Tode,RTode];

%writematrix([Tode,RTode],"MPP.csv");
 
%system("java -jar /usr/local/bin/DiffLQN.jar model.lqn");