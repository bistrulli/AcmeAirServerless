clear
res=load("../wless.mat");

figure('units','normalized','outerposition',[0 0 1 1])
scatter((res.defconcRt-res.wlessRt)./res.wlessRt*100,(res.defbill-res.wlessbill)./res.wlessbill*100,200,"filled")
xlabel("95th End to End Response Time Ratio (%)")
ylabel("Cumulative Billable Instance Ratio (%)")
box on
grid on
fontsize(gcf,32,"pixels")
exportgraphics(gcf,"figures/ratio.pdf")
close


[p,x]=ecdf(reshape(squeeze(res.optCon(:,:,2)),[1,270]));

figure('units','normalized','outerposition',[0 0 1 1])
hold on
plot(x,p,"LineWidth",2)
xline(80,"r-.")
xlabel("Max Concurrency")
ylabel("P<=x")
box on
grid on
fontsize(gcf,32,"pixels")
exportgraphics(gcf,"figures/concurrency_cdf.pdf")
close()