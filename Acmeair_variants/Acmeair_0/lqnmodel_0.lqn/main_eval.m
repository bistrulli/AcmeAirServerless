clear

%dimensione dipendi dal numero di nomi
X0=zeros(1,45);
MU=zeros(1,45);

names=["clientEntry","MSauthEntry","MSvalidateidEntry",...
            "MSviewprofileEntry","MSupdateprofileEntry","MSupdateMilesEntry",...
            "MSbookflightsEntry","MScancelbookingEntry","MSqueryflightsEntry",...
            "MSgetrewardmilesEntry"];

MU([7 10 13 16 19 22 31 36 39 42 ])=1.0./[0.02377 0.0652 0.03771 0.04871 0.03522 0.02139 0.02683 0.20939 0.04979 0.02377 ]; 

NTpp=[inf,21,34,26,37,88,63,13,26,67];
NTw=[inf,2,2,2,2,2,5,2,2,2];
NTnc=[inf,ones(1,size(names,2)-1)];
NTgcr=[inf,ones(1,size(names,2)-1)*80];

NTRef=[NTpp;NTw;NTnc;NTgcr];
ctrls=["NTpp","NTw","NTnc","NTgcr"];

for ctrl=1:size(ctrls,2)
    disp(ctrls(ctrl))
    NT=ones(1,size(names,2))*inf;
    NC=ones(1,size(names,2))*1;
    NC(1)=inf;

    RT=zeros(100,10);
    Cost=zeros(100,9);
    for u=1:100
        X0=zeros(1,45);
        X0(7)=u;
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

        pop=RTode.*Tode;
        %disp(pop./NC);
        for ms=1:9
            if(pop(ms+1)/NC(ms+1)>=NTRef(ctrl,ms+1))
                disp(sprintf("SCALE UP %s %f %d",names(ms+1),pop(ms+1)/NC(ms+1),NTRef(ctrl,ms+1)));
                NC(ms+1)=NC(ms+1)+1;
            end
        end

        RT(u,:)=RTode;
        Cost(u,:)=NC(2:end);
    end

    save(sprintf("%s.mat",ctrls(ctrl)),"Cost","RT");
end

wless=load("NTw.mat");
nconc=load("NTnc.mat");
gcr=load("NTgcr.mat");
pp=load("NTpp.mat");

ewless=abs(mean(nconc.RT(:,1))-mean(wless.RT(:,1)))*100/mean(nconc.RT(:,1));
epp=abs(mean(nconc.RT(:,1))-mean(pp.RT(:,1)))*100/mean(nconc.RT(:,1));
egcr=abs(mean(nconc.RT(:,1))-mean(gcr.RT(:,1)))*100/mean(nconc.RT(:,1));

swless=(sum(nconc.Cost,'all')-sum(wless.Cost,'all'))*100/sum(nconc.Cost,'all');
spp=(sum(nconc.Cost,'all')-sum(pp.Cost,'all'))*100/sum(nconc.Cost,'all');
sgcr=(sum(nconc.Cost,'all')-sum(gcr.Cost,'all'))*100/sum(nconc.Cost,'all');

figure;
hold on;
grid on;
scatter(ewless,swless,'filled')
scatter(epp,spp,'filled')
scatter(egcr,sgcr,'filled')
plot(linspace(1,100),linspace(1,100));
legend("Wasteless","ProPack","GCR");
xlabel("%RT")
ylabel("%Saving")
fontsize(24,"pixels")

% NCopt=[inf,sum(y(end,[10]),2),sum(y(end,[13]),2),sum(y(end,[16]),2),sum(y(end,[19]),2),sum(y(end,[22]),2),sum(y(end,[31]),2),sum(y(end,[36]),2),sum(y(end,[39]),2),sum(y(end,[42]),2)];
% NTLqn=[inf,sum(y(end,[8,9,10]),2),sum(y(end,[12,13]),2),sum(y(end,[15,16]),2),sum(y(end,[18,19]),2),sum(y(end,[21,22]),2),sum(y(end,[26,27,28,29,30,31]),2),sum(y(end,[33,34,35,36]),2),sum(y(end,[38,39]),2),sum(y(end,[41,42]),2)];
% NTopt=[inf,ceil(NTLqn(2:end)./NCopt(end,2:end))];

% fileID = fopen('optSol.csv', 'w');
% fprintf(fileID,"name,ncopt,ntopt\n");
% for i=2:length(names)
%     fprintf(fileID,"%s,%f,%d\n",names(i),NCopt(i),NTopt(i));
% end

%for i=1:length(names)
%    disp([names(i),NTopt(i+1)])
%    system(sprintf("sh ../%s/update.sh %d 100 1",names(i),NTopt(i+1)))
%end