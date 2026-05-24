clear
res=load("../results/wless.mat");

%percentage improvement
defrt_imp=(res.defconcRtAvg'-res.wlessRtAvg')*100./res.defconcRtAvg';
nort_imp=(res.noconcRtAvg'-res.wlessRtAvg')*100./res.noconcRtAvg';
propack_imp=(res.propackRtAvg'-res.wlessRtAvg')*100./res.propackRtAvg';

defbill_imp=(res.defbill'-res.wlessbill')*100./res.defbill';
nobill_imp=(res.noconcbill'-res.wlessbill')*100./res.noconcbill';
propackbill_imp=(res.propackbill'-res.wlessbill')*100./res.propackbill';

figure('units','normalized','outerposition',[0 0 1 1]);
positions = [1, 1.35];
boxplot([defrt_imp,nort_imp,propack_imp],["\textbf{A}:$\frac{(GCR-WL)*100}{GCR}$","\textbf{B}:$\frac{(No Conc-WL)*100}{No Conc}$", ...
    "\textbf{C}:$\frac{(ProPack-WL)*100}{ProPack}$"])

% preleva i diversi elementi per tag
boxes    = findobj(gca,'Tag','Box');
whiskers = findobj(gca,'Tag','Whisker');
caps     = findobj(gca,'Tag','Cap');
medians  = findobj(gca,'Tag','Median');
outliers = findobj(gca,'Tag','Outliers');

% imposta LineWidth
set(boxes,    'LineWidth',1.5);
set(whiskers, 'LineWidth',1.5);
set(caps,     'LineWidth',1.5);

% mediana un po' più spessa e magari colorata
set(medians,  'LineWidth',2.0);

% outliers: marker più grosso e bordo spesso
set(outliers, 'Marker','o', 'MarkerSize',6, 'LineWidth',1.5, ...
               'MarkerEdgeColor','black');

% title("95th Request Latency Percentage Improvement")
ylabel("%")
box on;
grid on;
fontsize(gcf,32,"pixels")
set(gca,'TickLabelInterpreter','latex')
exportgraphics(gcf,"figures/overall_latency.png")
close


figure('units','normalized','outerposition',[0 0 1 1]);
positions = [1, 1.35];
boxplot([defbill_imp,nobill_imp,propackbill_imp],["\textbf{A}:$\frac{(GCR-WL)*100}{GCR}$","\textbf{B}:$\frac{(No Conc-WL)*100}{No Conc}$", ...
    "\textbf{C}:$\frac{(ProPack-WL)*100}{ProPack}$"]);


% preleva i diversi elementi per tag
boxes    = findobj(gca,'Tag','Box');
whiskers = findobj(gca,'Tag','Whisker');
caps     = findobj(gca,'Tag','Cap');
medians  = findobj(gca,'Tag','Median');
outliers = findobj(gca,'Tag','Outliers');

% imposta LineWidth
set(boxes,    'LineWidth',1.5);
set(whiskers, 'LineWidth',1.5);
set(caps,     'LineWidth',1.5);

% mediana un po' più spessa e magari colorata
set(medians,  'LineWidth',2.0);

% outliers: marker più grosso e bordo spesso
set(outliers, 'Marker','o', 'MarkerSize',6, 'LineWidth',1.5, ...
               'MarkerEdgeColor','black');

ylabel("%")
box on;
grid on;
fontsize(gcf,32,"pixels")
set(gca,'TickLabelInterpreter','latex')
exportgraphics(gcf,"figures/overall_billable.png")
close

%Run Kolmogorov-Smirnoff test
[hdef,pdef]=kstest2(res.wlessRtAvg,res.defconcRtAvg,'Alpha',0.05);
[hno,pno]=kstest2(res.wlessRtAvg,res.noconcRtAvg,'Alpha',0.05);
[hpp,ppp]=kstest2(res.wlessRtAvg,res.propackRtAvg,'Alpha',0.05);

%prctile(reshape(squeeze(res.optCon(:,:,2)),[1,270]),50)
