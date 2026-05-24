clear

exp=["singleInstance","wrong","wastLess"];

billsingle=[];
billwrong=[];
billwLess=[];
rtsingle=[];
rtwrong=[];
rtwLess=[];
w=zeros(14,4);

for i=1:4
    dataTable=readtable(sprintf("%s/Billable_Instance_Time/Billable_Instance_Time_%d.csv",exp(1),i),...
        "Delimiter",",","NumHeaderLines",4);
    billsingle(:,i)=table2array(dataTable(:,2));
end

for i=1:4
    dataTable=readtable(sprintf("%s/Request_Latency/Request_Latency_%d.csv",exp(1),i),...
        "Delimiter",",","NumHeaderLines",4);
    rtsingle(:,i)=table2array(dataTable(:,2));
end

for i=1:4
    dataTable=readtable(sprintf("%s/Billable_Instance_Time/Billable_Instance_Time_%d.csv",exp(2),i),...
        "Delimiter",",","NumHeaderLines",4);
    billwrong(:,i)=table2array(dataTable(:,2));
end

for i=1:4
    dataTable=readtable(sprintf("%s/Request_Latency/Request_Latency_%d.csv",exp(2),i),...
        "Delimiter",",","NumHeaderLines",4);
    rtwrong(:,i)=table2array(dataTable(:,2));
end

for i=1:4
    dataTable=readtable(sprintf("%s/Billable_Instance_Time/Billable_Instance_Time_%d.csv",exp(3),i),...
        "Delimiter",",","NumHeaderLines",4);
    billwLess(:,i)=table2array(dataTable(:,2));
end

for i=1:4
    dataTable=readtable(sprintf("%s/Request_Latency/Request_Latency_%d.csv",exp(3),i),...
        "Delimiter",",","NumHeaderLines",4);
    rtwLess(:,i)=table2array(dataTable(1:12,2));
end

for i=1:4
    disp(i)
    dataTable=readtable(sprintf("%s/Max_Concurrent_Requests/Max_Concurrent_Requests_%d.csv",exp(3),i),...
        "Delimiter",",","NumHeaderLines",4);
    wconc(:,i)=table2array(dataTable(:,2));
end

for i=1:4
    disp(i)
    dataTable=readtable(sprintf("%s/Max_Concurrent_Requests/Max_Concurrent_Requests_%d.csv",exp(2),i),...
        "Delimiter",",","NumHeaderLines",4);
    gcrconc(:,i)=table2array(dataTable(:,2));
end


dataTable=readtable("singleInstance/Cloud_Run_Revision_-_Request_Count_for_fun1_[SUM].csv",...
    "Delimiter",",","NumHeaderLines",4);
w=table2array(dataTable(:,2));

fotsize=50;

f=figure('units','normalized','outerposition',[0 0 1 1]);
plot(w,"LineWidth",2)
grid on
box on
xlabel("Time(m)")
ylabel("Req/s")
fontsize(f,fotsize,"pixels")
%title('(A)','Units', 'normalized', 'Position',[0.05, 0.9, 0]);
exportgraphics(f,"./introPlot/users.pdf");
close(f);


f=figure('units','normalized','outerposition',[0 0 1 1]);
hold on
plot(sum(billsingle(1:15,:),2),"LineWidth", 3)
%plot(sum(billwLess(2:16,:),2),"LineWidth",3,"LineStyle","--")
plot(sum(billwrong,2),"LineWidth",3,"LineStyle","-.")
grid on
box on
xlabel("Time(m)")
ylabel("Billable Instance/s")
fontsize(f,fotsize,"pixels")
legend(["No-concurrency","GCR"])
%xlim([2,15])
%t = title('(B)','Units', 'normalized', 'Position',[0.05, 0.9, 0]); 
exportgraphics(f,"./introPlot/bill.pdf");
close(f);

% boxplot
% f=figure('units','normalized','outerposition',[0 0 1 1]);
% boxplot([rtsingle(:,1)/1000,rtwLess(:,1)/1000,rtwrong(:,1)/1000],["No-concurrency","WasteLess","GCR"])
% %xlabel("Time(m)")
% ylabel("Response Time(s)")
% grid on;
% fontsize(f,fotsize,"pixels")
% xlim([0.74,3.27])
% ylim([0,28])
% %t = title('(C)','Units', 'normalized', 'Position',[0.05, 0.9, 0]);
% exportgraphics(f,"./introPlot/rt.pdf");
% close(f);

% CDF
f=figure('units','normalized','outerposition',[0 0 1 1]);
hold on
%boxplot([rtsingle(:,1)/1000,rtwLess(:,1)/1000,rtwrong(:,1)/1000],["No-concurrency","WasteLess","GCR"])
[pnoconc,xnoconc]=ecdf(rtsingle(:,1)/1000);
[pwless,xwless]=ecdf(rtwLess(:,1)/1000);
[pgcr,xgcr]=ecdf(rtwrong(:,1)/1000);
plot(xnoconc,pnoconc,"LineStyle","-","LineWidth",4)
plot(xwless,pwless,"LineStyle","--","LineWidth",4)
plot(xgcr,pgcr,"LineStyle","-.","LineWidth",4)
xlabel("Time(s)")
ylabel("P")
grid on;
box on;
fontsize(f,fotsize,"pixels")
legend("No-concurrency","WasteLess","GCR","Location","southeast")
%t = title('(C)','Units', 'normalized', 'Position',[0.05, 0.9, 0]);
exportgraphics(f,"./introPlot/cdfrt.pdf");
close(f);






