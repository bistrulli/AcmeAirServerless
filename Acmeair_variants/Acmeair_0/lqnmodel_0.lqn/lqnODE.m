function [t,y,ssR] = lqnODE(X0,MU,NT,NC)
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
p.delta = 10^4; % context switch rate (super fast)

%probchoices
p.P_clientEntryclientEntry_A2clientEntryD0=1.0;
p.P_clientEntryclientEntry_A3clientEntryD1=1.0;
p.P_clientEntryclientEntry_A4clientEntryD2=1.0;
p.P_clientEntryclientEntry_A5clientEntryD3=1.0;
p.P_clientEntryclientEntry_A6clientEntryD4=1.0;
p.P_clientEntryclientEntry_A7clientEntryD5=1.0;
p.P_clientEntry_A1=1.0;
p.P_MSauthEntryMSauthEntry_A1=1.0;
p.P_MSauthEntryMSauthEntry_A2MSauthEntryD0=1.0;
p.P_MSvalidateidEntryMSvalidateidEntry_A1=1.0;
p.P_MSviewprofileEntryMSviewprofileEntry_A1=1.0;
p.P_MSupdateprofileEntryMSupdateprofileEntry_A1=1.0;
p.P_MSupdateMilesEntryMSupdateMilesEntry_A1=1.0;
p.P_MSbookflightsEntryMSbookflightsEntry_A1=1.0;
p.P_MSbookflightsEntryMSbookflightsEntry_A2MSbookflightsEntryD0=1.0;
p.P_MSbookflightsEntryMSbookflightsEntry_A3MSbookflightsEntryD1=1.0;
p.P_MSbookflightsEntryMSbookflightsEntry_A4MSbookflightsEntryD2=1.0;
p.P_MSbookflightsEntryMSbookflightsEntry_A5MSbookflightsEntryD3=1.0;
p.P_MScancelbookingEntryMScancelbookingEntry_A1=1.0;
p.P_MScancelbookingEntryMScancelbookingEntry_A2MScancelbookingEntryD0=1.0;
p.P_MScancelbookingEntryMScancelbookingEntry_A3MScancelbookingEntryD1=1.0;
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
jump=[-1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  -1,  +1,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +1,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +1,  +0;
               +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0,  +0,  +1;
               ];

T = @(X)propensities_2state(X,p);
opts = odeset('Events',@(t,y)eventfun(t,y,jump,T));
[t,y]=ode15s(@(t,y) jump'*T(y),linspace(0,1000,10001), X0,opts);

ssR=T(y(end,:)');

end

% Propensity rate vector (CTMC)
function Rate = propensities_2state(X, p)
    Rate = [p.P_clientEntryclientEntry_A2clientEntryD0*p.delta*min(X(1),X(17));
    		p.P_clientEntryclientEntry_A3clientEntryD1*p.delta*min(X(2),X(20));
    		p.P_clientEntryclientEntry_A4clientEntryD2*p.delta*min(X(3),X(32));
    		p.P_clientEntryclientEntry_A5clientEntryD3*p.delta*min(X(4),X(37));
    		p.P_clientEntryclientEntry_A6clientEntryD4*p.delta*min(X(5),X(40));
    		p.P_clientEntryclientEntry_A7clientEntryD5*p.delta*min(X(6),X(11));
    		p.P_clientEntry_A1*X(7)/(X(7))*p.MU(7)*min(X(7),p.NC(1));
    		p.P_MSauthEntryMSauthEntry_A1*X(8)/(X(8))*p.delta*min(X(8),p.NT(2)-(X(9)+X(10)));
    		p.P_MSauthEntryMSauthEntry_A2MSauthEntryD0*p.delta*min(X(9),X(14));
    		X(6)/(X(6))*X(10)/(X(10))*p.MU(10)*min(X(10),p.NC(2));
    		p.P_MSvalidateidEntryMSvalidateidEntry_A1*X(12)/(X(12))*p.delta*min(X(12),p.NT(3)-(X(13)));
    		X(9)/(X(9))*X(13)/(X(13))*p.MU(13)*min(X(13),p.NC(3));
    		p.P_MSviewprofileEntryMSviewprofileEntry_A1*X(15)/(X(15))*p.delta*min(X(15),p.NT(4)-(X(16)));
    		X(1)/(X(1))*X(16)/(X(16))*p.MU(16)*min(X(16),p.NC(4));
    		p.P_MSupdateprofileEntryMSupdateprofileEntry_A1*X(18)/(X(18))*p.delta*min(X(18),p.NT(5)-(X(19)));
    		X(2)/(X(2))*X(19)/(X(19))*p.MU(19)*min(X(19),p.NC(5));
    		p.P_MSupdateMilesEntryMSupdateMilesEntry_A1*X(21)/(X(21))*p.delta*min(X(21),p.NT(6)-(X(22)));
    		X(27)/(X(27)+X(29)+X(34))*X(22)/(X(22))*p.MU(22)*min(X(22),p.NC(6));
    		X(29)/(X(27)+X(29)+X(34))*X(22)/(X(22))*p.MU(22)*min(X(22),p.NC(6));
    		X(34)/(X(27)+X(29)+X(34))*X(22)/(X(22))*p.MU(22)*min(X(22),p.NC(6));
    		p.P_MSbookflightsEntryMSbookflightsEntry_A1*X(26)/(X(26))*p.delta*min(X(26),p.NT(7)-(X(27)+X(28)+X(29)+X(30)+X(31)));
    		p.P_MSbookflightsEntryMSbookflightsEntry_A2MSbookflightsEntryD0*p.delta*min(X(27),X(23));
    		p.P_MSbookflightsEntryMSbookflightsEntry_A3MSbookflightsEntryD1*p.delta*min(X(28),X(43));
    		p.P_MSbookflightsEntryMSbookflightsEntry_A4MSbookflightsEntryD2*p.delta*min(X(29),X(24));
    		p.P_MSbookflightsEntryMSbookflightsEntry_A5MSbookflightsEntryD3*p.delta*min(X(30),X(44));
    		X(3)/(X(3))*X(31)/(X(31))*p.MU(31)*min(X(31),p.NC(7));
    		p.P_MScancelbookingEntryMScancelbookingEntry_A1*X(33)/(X(33))*p.delta*min(X(33),p.NT(8)-(X(34)+X(35)+X(36)));
    		p.P_MScancelbookingEntryMScancelbookingEntry_A2MScancelbookingEntryD0*p.delta*min(X(34),X(25));
    		p.P_MScancelbookingEntryMScancelbookingEntry_A3MScancelbookingEntryD1*p.delta*min(X(35),X(45));
    		X(4)/(X(4))*X(36)/(X(36))*p.MU(36)*min(X(36),p.NC(8));
    		p.P_MSqueryflightsEntryMSqueryflightsEntry_A1*X(38)/(X(38))*p.delta*min(X(38),p.NT(9)-(X(39)));
    		X(5)/(X(5))*X(39)/(X(39))*p.MU(39)*min(X(39),p.NC(9));
    		p.P_MSgetrewardmilesEntryMSgetrewardmilesEntry_A1*X(41)/(X(41))*p.delta*min(X(41),p.NT(10)-(X(42)));
    		X(28)/(X(28)+X(30)+X(35))*X(42)/(X(42))*p.MU(42)*min(X(42),p.NC(10));
    		X(30)/(X(28)+X(30)+X(35))*X(42)/(X(42))*p.MU(42)*min(X(42),p.NC(10));
    		X(35)/(X(28)+X(30)+X(35))*X(42)/(X(42))*p.MU(42)*min(X(42),p.NC(10));
    		];
    Rate(isnan(Rate))=0;
end

function [x,isterm,dir] = eventfun(t,y,jump,T)
dy = jump'*T(y);
x = norm(dy) - 1e-5;
%x=max(abs(dy)) - 1e-5;
isterm = 1;
dir = 0;
end