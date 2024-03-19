clear

%dimensione dipendi dal numero di nomi
X0=zeros(1,45);
MU=zeros(1,45);

X0(7)=1;

MU([7 10 13 16 19 22 31 36 39 42 ])=1.0./[0.06446 0.02104 0.05356 0.0213 0.02289 2.7689 0.02919 0.03525 0.03064 0.06446 ]; 
NT=[1 1 1 1 1 1 1 1 1 1 ];
NC=[1 1 1 1 1 1 1 1 1 1 ];

names=["clientEntry","MSauthEntry","MSvalidateidEntry","MSviewprofileEntry","MSupdateprofileEntry","MSupdateMilesEntry","MSbookflightsEntry","MScancelbookingEntry","MSqueryflightsEntry","MSgetrewardmilesEntry"];

[t,y,ssROde] = lqnODE(X0,MU,NT,NC);

Tode=ssROde(7);
RTode=X0(7)/Tode;

NCopt=[inf,sum(y(end,[10]),2),sum(y(end,[13]),2),sum(y(end,[16]),2),sum(y(end,[19]),2),sum(y(end,[22]),2),sum(y(end,[31]),2),sum(y(end,[36]),2),sum(y(end,[39]),2),sum(y(end,[42]),2)];
NTLqn=[inf,sum(y(end,[8,9,10]),2),sum(y(end,[12,13]),2),sum(y(end,[15,16]),2),sum(y(end,[18,19]),2),sum(y(end,[21,22]),2),sum(y(end,[26,27,28,29,30,31]),2),sum(y(end,[33,34,35,36]),2),sum(y(end,[38,39]),2),sum(y(end,[41,42]),2)];
NTopt=[inf,ceil(NTLqn(2:end)./NCopt(end,2:end))];

fileID = fopen('optSol.csv', 'w');
fprintf(fileID,"name,ncopt,ntopt\n");
for i=2:length(names)
    fprintf(fileID,"%s,%f,%d\n",names(i),NCopt(i),NTopt(i));
end

%for i=1:length(names)
%    disp([names(i),NTopt(i+1)])
%    system(sprintf("sh ../%s/update.sh %d 100 1",names(i),NTopt(i+1)))
%end