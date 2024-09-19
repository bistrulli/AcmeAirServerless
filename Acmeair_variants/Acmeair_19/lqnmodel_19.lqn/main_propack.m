clear

%dimensione dipendi dal numero di nomi
X0=zeros(1,45);
MU=zeros(1,45);

MU([7 10 13 16 19 22 31 36 39 42 ])=1.0./[0.03511 0.04276 0.05259 0.0244 0.34627 0.03122 0.06023 0.37589 0.02923 0.03511 ]; 

names=["clientEntry","MSauthEntry","MSvalidateidEntry",...
            "MSviewprofileEntry","MSupdateprofileEntry","MSupdateMilesEntry",...
            "MSbookflightsEntry","MScancelbookingEntry","MSqueryflightsEntry",...
            "MSgetrewardmilesEntry"];

mkdir("ProPackProfile")
 
RT=zeros(100,10);
for ms=1:9
    NC=ones(1,10)*inf;
    NC(1,ms+1)=1;
    disp(sprintf("%s %d",names(ms+1),ms+1))
    disp(NC)
    for u=1:size(RT,1)
        X0(7)=u;
        disp(u)
        
        NT=[inf u u u u u u u u u ];        
        [t,y,ssROde] = lqnODE(X0,MU,NT,NC);
        
        Tode=[ssROde(7),ssROde(10),ssROde(12),...
            ssROde(14),ssROde(16),sum(ssROde([18:20])),...
            ssROde(26),ssROde(30),ssROde(32),...
            sum(ssROde(34:36))
            ];
        RTode=[X0(7)/Tode(1),sum(y(end,8:10))/Tode(2),sum(y(end,12:13))/Tode(3),...
            sum(y(end,15:16))/Tode(4),sum(y(end,18:19))/Tode(5),sum(y(end,21:22))/Tode(6),...
            sum(y(end,27:31))/Tode(7),sum(y(end,33:36))/Tode(8),sum(y(end,38:39))/Tode(9),...
            sum(y(end,41:42))/Tode(10)];
        pop=ceil(RTode.*Tode);
        RT(pop(ms+1),ms+1)=RTode(1,ms+1);
    end
    writematrix([ceil((1:size(RT(RT(:,ms+1)>0,ms+1),1)))',RT(RT(:,ms+1)>0,ms+1)],sprintf("./ProPackProfile/%s.csv",names(ms+1)))
end