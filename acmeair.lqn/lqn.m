function [X,ssR] = lqn(X0,MU,NT,NC,TF,rep,dt)
import Gillespie.*

% Make sure vector components are doubles
X0 = double(X0);
MU = double(MU);

% Make sure all vectors are row vectors
if(iscolumn(X0))
    X0 = X0';
end
if(iscolumn(MU))
    MU = MU';
end
if(iscolumn(NT))
    NT = NT';
end
if(iscolumn(NT))
    NC = NC';
end

p.MU = MU; 
p.NT = NT;
p.NC = NC;
p.delta = 10^5; % context switch rate (super fast)

%probchoices
p.P_clientEntryclientEntry_A2=1.0;
p.P_clientEntryclientEntry_A3=1.0;
p.P_clientEntryclientEntry_A4=1.0;
p.P_clientEntryclientEntry_A5=1.0;
p.P_clientEntryclientEntry_A6=1.0;
p.P_clientEntryclientEntry_A7=1.0;
p.P_clientEntry_A1=1.0;
p.P_MSauthEntryMSauthEntry_A1=1.0;
p.P_MSauthEntryMSauthEntry_A2=1.0;
p.P_MSvalidateidEntryMSvalidateidEntry_A1=1.0;
p.P_MSviewprofileEntryMSviewprofileEntry_A1=1.0;
p.P_MSupdateprofileEntryMSupdateprofileEntry_A1=1.0;
p.P_MSupdateMilesEntryMSupdateMilesEntry_A1=1.0;
p.P_MSbookflightsEntryMSbookflightsEntry_A1=1.0;
p.P_MSbookflightsEntryMSbookflightsEntry_A2=1.0;
p.P_MSbookflightsEntryMSbookflightsEntry_A3=1.0;
p.P_MSbookflightsEntryMSbookflightsEntry_A4=1.0;
p.P_MSbookflightsEntryMSbookflightsEntry_A5=1.0;
p.P_MScancelbookingEntryMScancelbookingEntry_A1=1.0;
p.P_MScancelbookingEntryMScancelbookingEntry_A2=1.0;
p.P_MScancelbookingEntryMScancelbookingEntry_A3=1.0;
p.P_MSqueryflightsEntryMSqueryflightsEntry_A1=1.0;
p.P_MSgetrewardmilesEntryMSgetrewardmilesEntry_A1=1.0;



%states name
%X(1)=XclientEntry_clientEntry_A1ToMSviewprofileEntry;
%X(2)=XclientEntry_clientEntry_A2ToMSupdateprofileEntry;
%X(3)=XclientEntry_clientEntry_A3ToMSbookflightsEntry;
%X(4)=XclientEntry_clientEntry_A4ToMScancelbookingEntry;
%X(5)=XclientEntry_clientEntry_A5ToMSqueryflightsEntry;
%X(6)=XclientEntry_clientEntry_A6ToMSauthEntry;
%X(7)=XclientEntry_clientEntry_A7;
%X(8)=XMSauthEntry_a;
%X(9)=XMSauthEntry_MSauthEntry_A1ToMSvalidateidEntry;
%X(10)=XMSauthEntry_MSauthEntry_A2;
%X(11)=XMSauthEntry_clientEntry_A6ToMSauthEntry;
%X(12)=XMSvalidateidEntry_a;
%X(13)=XMSvalidateidEntry_MSvalidateidEntry_A1;
%X(14)=XMSvalidateidEntry_MSauthEntry_A1ToMSvalidateidEntry;
%X(15)=XMSviewprofileEntry_a;
%X(16)=XMSviewprofileEntry_MSviewprofileEntry_A1;
%X(17)=XMSviewprofileEntry_clientEntry_A1ToMSviewprofileEntry;
%X(18)=XMSupdateprofileEntry_a;
%X(19)=XMSupdateprofileEntry_MSupdateprofileEntry_A1;
%X(20)=XMSupdateprofileEntry_clientEntry_A2ToMSupdateprofileEntry;
%X(21)=XMSupdateMilesEntry_a;
%X(22)=XMSupdateMilesEntry_MSupdateMilesEntry_A1;
%X(23)=XMSupdateMilesEntry_MSbookflightsEntry_A1ToMSupdateMilesEntry;
%X(24)=XMSupdateMilesEntry_MSbookflightsEntry_A3ToMSupdateMilesEntry;
%X(25)=XMSupdateMilesEntry_MScancelbookingEntry_A1ToMSupdateMilesEntry;
%X(26)=XMSbookflightsEntry_a;
%X(27)=XMSbookflightsEntry_MSbookflightsEntry_A1ToMSupdateMilesEntry;
%X(28)=XMSbookflightsEntry_MSbookflightsEntry_A2ToMSgetrewardmilesEntry;
%X(29)=XMSbookflightsEntry_MSbookflightsEntry_A3ToMSupdateMilesEntry;
%X(30)=XMSbookflightsEntry_MSbookflightsEntry_A4ToMSgetrewardmilesEntry;
%X(31)=XMSbookflightsEntry_MSbookflightsEntry_A5;
%X(32)=XMSbookflightsEntry_clientEntry_A3ToMSbookflightsEntry;
%X(33)=XMScancelbookingEntry_a;
%X(34)=XMScancelbookingEntry_MScancelbookingEntry_A1ToMSupdateMilesEntry;
%X(35)=XMScancelbookingEntry_MScancelbookingEntry_A2ToMSgetrewardmilesEntry;
%X(36)=XMScancelbookingEntry_MScancelbookingEntry_A3;
%X(37)=XMScancelbookingEntry_clientEntry_A4ToMScancelbookingEntry;
%X(38)=XMSqueryflightsEntry_a;
%X(39)=XMSqueryflightsEntry_MSqueryflightsEntry_A1;
%X(40)=XMSqueryflightsEntry_clientEntry_A5ToMSqueryflightsEntry;
%X(41)=XMSgetrewardmilesEntry_a;
%X(42)=XMSgetrewardmilesEntry_MSgetrewardmilesEntry_A1;
%X(43)=XMSgetrewardmilesEntry_MSbookflightsEntry_A2ToMSgetrewardmilesEntry;
%X(44)=XMSgetrewardmilesEntry_MSbookflightsEntry_A4ToMSgetrewardmilesEntry;
%X(45)=XMSgetrewardmilesEntry_MScancelbookingEntry_A2ToMSgetrewardmilesEntry;


%task ordering
%1=T_clientEntry;
%2=T_MSauthEntry;
%3=T_MSvalidateidEntry;
%4=T_MSviewprofileEntry;
%5=T_MSupdateprofileEntry;
%6=T_MSupdateMilesEntry;
%7=T_MSbookflightsEntry;
%8=T_MScancelbookingEntry;
%9=T_MSqueryflightsEntry;
%10=T_MSgetrewardmilesEntry;


% Jump matrix
stoich_matrix=[-1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  -1,  +1,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +1,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               ];
    
tspan = [0, TF];
pfun = @propensities_2state;
 
T=@(X)propensities_2state(X,p);
X = zeros(length(X0), ceil(TF/dt) + 1, rep);
ssR=zeros(size(stoich_matrix,1),ceil(TF/dt) + 1, rep);
for i = 1:rep
    [t, x] = directMethod(stoich_matrix, pfun, tspan, X0, p);
    tsin = timeseries(x,t);
    tsout = resample(tsin, linspace(0, TF, ceil(TF/dt)+1), 'zoh');
    X(:, :, i) = tsout.Data';
    for j=1:size(X,2)
        ssR(:,j,i)=T(X(:, j, i));
    end
end

end

% Propensity rate vector (CTMC)
function Rate = propensities_2state(X, p)
    Rate = [p.P_clientEntryclientEntry_A2*X(1)/(X(1))*X(16)/(X(16))*p.MU(16)*min(X(16),p.NC(4));
    		p.P_clientEntryclientEntry_A3*X(2)/(X(2))*X(19)/(X(19))*p.MU(19)*min(X(19),p.NC(5));
    		p.P_clientEntryclientEntry_A4*X(3)/(X(3))*X(31)/(X(31))*p.MU(31)*min(X(31),p.NC(7));
    		p.P_clientEntryclientEntry_A5*X(4)/(X(4))*X(36)/(X(36))*p.MU(36)*min(X(36),p.NC(8));
    		p.P_clientEntryclientEntry_A6*X(5)/(X(5))*X(39)/(X(39))*p.MU(39)*min(X(39),p.NC(9));
    		p.P_clientEntryclientEntry_A7*X(6)/(X(6))*X(10)/(X(10))*p.MU(10)*min(X(10),p.NC(2));
    		p.P_clientEntry_A1*X(7)/(X(7))*p.MU(7)*min(X(7),p.NC(1));
    		p.P_MSauthEntryMSauthEntry_A1*X(8)/(X(8))*p.delta*min(X(8),p.NT(2)-(X(9)+X(10)));
    		p.P_MSauthEntryMSauthEntry_A2*X(9)/(X(9))*X(13)/(X(13))*p.MU(13)*min(X(13),p.NC(3));
    		0;
    		p.P_MSvalidateidEntryMSvalidateidEntry_A1*X(12)/(X(12))*p.delta*min(X(12),p.NT(3)-(X(13)));
    		0;
    		p.P_MSviewprofileEntryMSviewprofileEntry_A1*X(15)/(X(15))*p.delta*min(X(15),p.NT(4)-(X(16)));
    		0;
    		p.P_MSupdateprofileEntryMSupdateprofileEntry_A1*X(18)/(X(18))*p.delta*min(X(18),p.NT(5)-(X(19)));
    		0;
    		p.P_MSupdateMilesEntryMSupdateMilesEntry_A1*X(21)/(X(21))*p.delta*min(X(21),p.NT(6)-(X(22)));
    		0;
    		0;
    		0;
    		p.P_MSbookflightsEntryMSbookflightsEntry_A1*X(26)/(X(26))*p.delta*min(X(26),p.NT(7)-(X(27)+X(28)+X(29)+X(30)+X(31)));
    		p.P_MSbookflightsEntryMSbookflightsEntry_A2*X(27)/(X(27)+X(29)+X(34))*X(22)/(X(22))*p.MU(22)*min(X(22),p.NC(6));
    		p.P_MSbookflightsEntryMSbookflightsEntry_A3*X(28)/(X(28)+X(30)+X(35))*X(42)/(X(42))*p.MU(42)*min(X(42),p.NC(10));
    		p.P_MSbookflightsEntryMSbookflightsEntry_A4*X(29)/(X(27)+X(29)+X(34))*X(22)/(X(22))*p.MU(22)*min(X(22),p.NC(6));
    		p.P_MSbookflightsEntryMSbookflightsEntry_A5*X(30)/(X(28)+X(30)+X(35))*X(42)/(X(42))*p.MU(42)*min(X(42),p.NC(10));
    		0;
    		p.P_MScancelbookingEntryMScancelbookingEntry_A1*X(33)/(X(33))*p.delta*min(X(33),p.NT(8)-(X(34)+X(35)+X(36)));
    		p.P_MScancelbookingEntryMScancelbookingEntry_A2*X(34)/(X(27)+X(29)+X(34))*X(22)/(X(22))*p.MU(22)*min(X(22),p.NC(6));
    		p.P_MScancelbookingEntryMScancelbookingEntry_A3*X(35)/(X(28)+X(30)+X(35))*X(42)/(X(42))*p.MU(42)*min(X(42),p.NC(10));
    		0;
    		p.P_MSqueryflightsEntryMSqueryflightsEntry_A1*X(38)/(X(38))*p.delta*min(X(38),p.NT(9)-(X(39)));
    		0;
    		p.P_MSgetrewardmilesEntryMSgetrewardmilesEntry_A1*X(41)/(X(41))*p.delta*min(X(41),p.NT(10)-(X(42)));
    		0;
    		0;
    		0;
    		];
    Rate(isnan(Rate))=0;
end