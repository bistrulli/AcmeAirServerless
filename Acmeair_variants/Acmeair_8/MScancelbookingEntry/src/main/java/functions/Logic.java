package functions;

import java.io.BufferedWriter;
import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.lang.management.ThreadMXBean;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpResponse.BodyHandlers;
import java.time.Duration;
import java.util.logging.Logger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.lang.Thread;

import org.apache.commons.math3.distribution.ExponentialDistribution;
import org.apache.commons.math3.distribution.EnumeratedDistribution;
import org.apache.commons.math3.util.Pair;

import com.google.cloud.functions.HttpFunction;
import com.google.cloud.functions.HttpRequest;
import com.google.cloud.functions.HttpResponse;

public class Logic implements HttpFunction {
	private static final Logger logger = Logger.getLogger("MScancelbookingEntry");
	private static ThreadMXBean mgm = ManagementFactory.getThreadMXBean();
	private static HttpClient client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(180)).build();
	private HttpResponse response = null;
	private HashMap<String, Boolean> act_exec=new HashMap<String, Boolean>();
	private HashMap<String, Thread> act_thread=new HashMap<String, Thread>();
	private Long  startCpuTime=null;
	private Long  startExecTime=null;
	

	/*
	 * activities
	 */
	public void MScancelbookingEntry_A1(){
		this.act_exec.put("MScancelbookingEntry_A1", true);
		this.doWork(1.0E-6);
		String url = "https://northamerica-northeast1-modellearning.cloudfunctions.net/msupdatemilesentry";
		var getRequest = java.net.http.HttpRequest.newBuilder().uri(URI.create(url)).GET().build();

		try {
			var getResponse = Logic.client.send(getRequest, BodyHandlers.ofString());
		} catch (IOException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	public void MScancelbookingEntry_A2(){
		this.act_exec.put("MScancelbookingEntry_A2", true);
		this.doWork(1.0E-6);
		String url = "https://northamerica-northeast1-modellearning.cloudfunctions.net/msgetrewardmilesentry";
		var getRequest = java.net.http.HttpRequest.newBuilder().uri(URI.create(url)).GET().build();

		try {
			var getResponse = Logic.client.send(getRequest, BodyHandlers.ofString());
		} catch (IOException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	public void MScancelbookingEntry_A3(){
		this.act_exec.put("MScancelbookingEntry_A3", true);
		this.doWork(0.04767);
	}

	/*
	 * Dnodes
	 */
	public void OrNode_MScancelbookingEntry_A1(){
		//OrNode Logic
		List<Pair<String, Double>> distributionData = new ArrayList<>();
		distributionData.add(new Pair<>("MScancelbookingEntry_A2", 1.0));
		EnumeratedDistribution<String> distribution = new EnumeratedDistribution<>(distributionData);
		String randomChoice = distribution.sample();
		if(randomChoice=="MScancelbookingEntry_A2"){
			MScancelbookingEntry_A2();
		}
	}
	public void OrNode_MScancelbookingEntry_A2(){
		//OrNode Logic
		List<Pair<String, Double>> distributionData = new ArrayList<>();
		distributionData.add(new Pair<>("MScancelbookingEntry_A3", 1.0));
		EnumeratedDistribution<String> distribution = new EnumeratedDistribution<>(distributionData);
		String randomChoice = distribution.sample();
		if(randomChoice=="MScancelbookingEntry_A3"){
			MScancelbookingEntry_A3();
		}
	}
	public void ReplyNode_MScancelbookingEntry_A3(){
		//ReplyNode Logic
		BufferedWriter writer;
		try {
			writer = this.response.getWriter();
			writer.write("MScancelbookingEntry_A3[MScancelbookingEntry]");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	@Override
	public void service(HttpRequest request, HttpResponse response) throws IOException {
		this.response = response;
		mgm.setThreadCpuTimeEnabled(true);
		this.startCpuTime=mgm.getCurrentThreadCpuTime();
		this.startExecTime=System.nanoTime();
		
		//execute the entry activity
		MScancelbookingEntry_A1();
		//execetute the decision node of already executed evt
		if(this.act_exec.get("MScancelbookingEntry_A1")!=null && this.act_exec.get("MScancelbookingEntry_A1")) {
		  this.act_exec.put("MScancelbookingEntry_A1",false);
		  OrNode_MScancelbookingEntry_A1();
		}
		if(this.act_exec.get("MScancelbookingEntry_A2")!=null && this.act_exec.get("MScancelbookingEntry_A2")) {
		  this.act_exec.put("MScancelbookingEntry_A2",false);
		  OrNode_MScancelbookingEntry_A2();
		}
		if(this.act_exec.get("MScancelbookingEntry_A3")!=null && this.act_exec.get("MScancelbookingEntry_A3")) {
		  this.act_exec.put("MScancelbookingEntry_A3",false);
		  ReplyNode_MScancelbookingEntry_A3();
		}
		String logstring=String.format("cpu:=%d  rt:=%d",mgm.getCurrentThreadCpuTime()-this.startCpuTime,
									   System.nanoTime()-this.startExecTime);
		Logic.logger.info(logstring);
	}

	private void doWork(Double stime) {
		ExponentialDistribution dist = new ExponentialDistribution(stime);
		long delay = Long.valueOf(Math.round(dist.sample() * 1e9));
		long start = mgm.getCurrentThreadCpuTime();
		while ((mgm.getCurrentThreadCpuTime() - start) < delay) {
		}
	}
}
