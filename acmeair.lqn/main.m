%clear

N=10;
K=10;
TF=N*K;

%dimensione dipendi dal numero di nomi
X0=zeros(1,45);
MU=zeros(1,45);

X0(7)=1;

MU([7 10 13 16 19 22 31 36 39 42 ])=1./[0.2932465211611641 0.06779581230199999 0.14995238461600002 0.17713556017 0.22599922449800006 0.17767207436926147 0.14241448226547715 0.06435561010616775 0.10841151708800001 0.10528620681 ]; 
NT=[1 1 1 1 1 1 1 1 1 1 ]*inf;
NC=[1 1 1 1 1 1 1 1 1 1 ]*inf;

[t,y,ssROde] = lqnODE(X0,MU,NT,NC);

%X(10)=XMSauthEntry_MSauthEntry_A2;
%X(13)=XMSvalidateidEntry_MSvalidateidEntry_A1;
%X(16)=XMSviewprofileEntry_MSviewprofileEntry_A1;
%X(19)=XMSupdateprofileEntry_MSupdateprofileEntry_A1;
%X(22)=XMSupdateMilesEntry_MSupdateMilesEntry_A1;
%X(31)=XMSbookflightsEntry_MSbookflightsEntry_A5;
%X(36)=XMScancelbookingEntry_MScancelbookingEntry_A3;
%X(39)=XMSqueryflightsEntry_MSqueryflightsEntry_A1;
%X(42)=XMSgetrewardmilesEntry_MSgetrewardmilesEntry_A1;

names=["MSauthEntry","MSvalidateidEntry","MSviewprofileEntry","MSupdateprofileEntry",...
      "MSupdateMilesEntry","MSbookflightsEntry","MScancelbookingEntry","MSqueryflightsEntry"...
      "MSgetrewardmilesEntry"];

% NTopt=[inf,ceil(sum(y(end,8:11))/y(end,10)),ceil(sum(y(end,12:14)/y(end,13))),...
%            ceil(sum(y(end,15:17)/y(end,16))),ceil(sum(y(end,18:20)/y(end,19))),...
%            ceil(sum(y(end,21:25)/y(end,22))),ceil(sum(y(end,26:32)/y(end,31))),...
%            ceil(sum(y(end,33:37)/y(end,36))),ceil(sum(y(end,38:40)/y(end,39))),...
%            ceil(sum(y(end,41:45)/y(end,42)))];
NTopt=[inf,80*ones(1,9)];
NCopt=[inf,y(end,[10 13 16 19 22 31 36 39 42 ])];

for i=1:length(names)
    disp([names(i),NTopt(i+1)])
    system(sprintf("sh ../%s/update.sh %d 100 1",names(i),NTopt(i+1)))
end

Tode=ssROde(1);
RTode=X0(7)/Tode;

