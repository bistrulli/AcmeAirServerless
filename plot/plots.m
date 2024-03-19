clear
res=load("../wless.mat");

figure('units','normalized','outerposition',[0 0 1 1])
scatter((res.defconcRt-res.wlessRt)./res.wlessRt*100,(res.defbill-res.wlessbill)./res.wlessbill*100)
fontsize(gcf,24,"pixels")
xlabel("95th E2E Response Time Ratio")
ylabel("Cumulative Billable Instance Ratio")
box on
grid on


[p,x]=ecdf(reshape(squeeze(res.optCon(:,:,2)),[1,270]));

figure('units','normalized','outerposition',[0 0 1 1])
hold on
plot(x,p)
xline(80,"r-.")
fontsize(gcf,24,"pixels")
xlabel("Max Concurrency")
ylabel("P<=x")
box on
grid on