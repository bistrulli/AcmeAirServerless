clear

exp=["min","median","max"];
fsize=32;

for i=1:3
    expname=exp(i);

    data=readmatrix(sprintf("../zoomRes/default/%s/Billable_Instance_Time.csv",expname),"NumHeaderLines",2,"Delimiter",",");
    default_bill=data(:,2:end);
    data=readmatrix(sprintf("../zoomRes/wless/%s/Billable_Instance_Time.csv",expname),"NumHeaderLines",2,"Delimiter",",");
    wless_bill=data(:,2:end);

    billable=cat(1,default_bill,wless_bill);

    ymax=max(billable)*1.10;
    expwidth=(size(billable,1))/2;

    figure('units','normalized','outerposition',[0 0 1 1])
    hold on
    patch([0,expwidth,expwidth,0],[0,0,ymax,ymax],'black',"Linestyle","none",'FaceAlpha',.3,'FaceColor',"#CCCCCC")
    patch([expwidth,expwidth*2.05,expwidth*2.05,expwidth],[0,0,ymax,ymax],'black',"Linestyle","none",'FaceAlpha',.3,'FaceColor',"#FFFFFF")
    h=plot(billable,"LineWidth",1.5);
    box on
    grid on
    text(.5,ymax-ymax*0.035,"Default","FontWeight","bold")
    text(expwidth+0.5,ymax-ymax*0.035,"Wasteless","FontWeight","bold")
    fontsize(gcf,fsize,"pixels");

    ylabel("Billable Instance")
    xlabel("Time (m)")
    ylim([0,ymax])
    xlim([0,expwidth*2.05])
    
    legend(h,"Total Billable Instances")
    exportgraphics(gcf,sprintf("./figures/%s_bill.pdf",expname))
    close()

    
    data=readmatrix(sprintf("../zoomRes/default/%s/Request_Latency.csv",expname),"NumHeaderLines",3,"Delimiter",",");
    default_req_lat=data(:,2:end);
    if(i==3)
        default_req_lat=default_req_lat(2:end,:)
    end
    data=readmatrix(sprintf("../zoomRes/wless/%s/Request_Latency.csv",expname),"NumHeaderLines",3,"Delimiter",",");
    wless_req_lat=data(:,2:end);

    data=cat(1,default_req_lat,wless_req_lat);

    ymax=max(max(data))*1.05;
    expwidth=(size(data,1)+5)/2;

    figure('units','normalized','outerposition',[0 0 1 1])
    hold on
    patch([0,expwidth,expwidth,0],[0,0,ymax,ymax],'black',"Linestyle","none",'FaceAlpha',.3,'FaceColor',"#CCCCCC")
    patch([expwidth,expwidth*2,expwidth*2,expwidth],[0,0,ymax,ymax],'black',"Linestyle","none",'FaceAlpha',.3,'FaceColor',"#FFFFFF")
    h=plot(data,"LineWidth",1.5);
    box on
    grid on
    text(5+0.5,ymax-ymax*0.035,"Default","FontWeight","bold")
    text(expwidth+0.5,ymax-ymax*0.035,"Wasteless","FontWeight","bold")
    fontsize(gcf,fsize,"pixels");

    ylabel("Request Latency (ms)")
    xlabel("Time (m)")
    ylim([0,ymax])
    xlim([5,expwidth*2-5])
    
    legend(h,"Auth","ValidateId","ViewProfile",...
           "UpdateProFile","UpdateMiles","BookFlights",...
           "CancelBooking","QueryFlights","GetrewardMiles")

    exportgraphics(gcf,sprintf("./figures/%s_rt.pdf",expname))
    close()

    data=readmatrix(sprintf("../zoomRes/default/%s/Max_Concurrent_Requests.csv",expname),"NumHeaderLines",2,"Delimiter",",");
    default_conc=data(:,2:end);
    data=readmatrix(sprintf("../zoomRes/wless/%s/Max_Concurrent_Requests.csv",expname),"NumHeaderLines",2,"Delimiter",",");
    wless_conc=data(:,2:end);

    concurrent=cat(1,default_conc,wless_conc);

    ymax=max(max(concurrent))*1.05;
    expwidth=(size(concurrent,1))/2;

    figure('units','normalized','outerposition',[0 0 1 1])
    hold on
    patch([0,expwidth,expwidth,0],[0,0,ymax,ymax],'black',"Linestyle","none",'FaceAlpha',.3,'FaceColor',"#CCCCCC")
    patch([expwidth,expwidth*2.05,expwidth*2.05,expwidth],[0,0,ymax,ymax],'black',"Linestyle","none",'FaceAlpha',.3,'FaceColor',"#FFFFFF")
    h=plot(concurrent,"LineWidth",1.5)
    box on
    grid on
    
    text(.5,ymax-ymax*0.035,"Default","FontWeight","bold")
    text(expwidth+0.5,ymax-ymax*0.035,"Wasteless","FontWeight","bold")
    fontsize(gcf,fsize,"pixels");

    ylabel("Concurrent Requests")
    xlabel("Time (m)")
    ylim([0,ymax])
    xlim([0,expwidth*2.05])

    legend([h],"Auth","ValidateId","ViewProfile",...
           "UpdateProFile","UpdateMiles","BookFlights",...
           "CancelBooking","QueryFlights","GetrewardMiles")

    exportgraphics(gcf,sprintf("./figures/%s_concurrent.pdf",expname))
    close()

end


