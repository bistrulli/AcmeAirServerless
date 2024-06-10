clear
res=load("../results/wless.mat");

%percentage improvement
defrt_imp=(res.defconcRtAvg'-res.wlessRtAvg')*100./res.defconcRtAvg';
nort_imp=(res.noconcRtAvg'-res.wlessRtAvg')*100./res.noconcRtAvg';

defbill_imp=(res.defbill'-res.wlessbill')*100./res.defbill';
nobill_imp=(res.noconcbill'-res.wlessbill')*100./res.noconcbill';

figure('units','normalized','outerposition',[0 0 1 1]);
positions = [1, 1.35];
boxplot([defrt_imp,nort_imp],["\textbf{A}:$\frac{(GCR-WL)*100}{GCR}$","\textbf{B}:$\frac{(No Conc-WL)*100}{No Conc}$"])
% title("95th Request Latency Percentage Improvement")
ylabel("%")
box on;
grid on;
fontsize(gcf,32,"pixels")
set(gca,'TickLabelInterpreter','latex')
exportgraphics(gcf,"figures/overall_latency.pdf")
close


figure('units','normalized','outerposition',[0 0 1 1]);
positions = [1, 1.35];
boxplot([defbill_imp,nobill_imp],["\textbf{A}:$\frac{(GCR-WL)*100}{GCR}$","\textbf{B}:$\frac{(No Conc-WL)*100}{No Conc}$"]);
ylabel("%")
box on;
grid on;
fontsize(gcf,32,"pixels")
set(gca,'TickLabelInterpreter','latex')
exportgraphics(gcf,"figures/overall_billable.pdf")
close

%Run Kolmogorov-Smirnoff test
[hdef,pdef]=kstest2(res.wlessRtAvg,res.defconcRtAvg,'Alpha',0.05);
[hno,pno]=kstest2(res.wlessRtAvg,res.noconcRtAvg,'Alpha',0.05);