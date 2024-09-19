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
	private static final Logger logger = Logger.getLogger("MSauthEntry");
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
	public void MSauthEntry_A1(){
		this.act_exec.put("MSauthEntry_A1", true);
		this.doWork(1.0E-5);
		String url = "https://northamerica-northeast1-my-microservice-test-project.cloudfunctions.net/msvalidateidentry";
		var getRequest = java.net.http.HttpRequest.newBuilder().uri(URI.create(url)).GET().build();

		try {
			var getResponse = Logic.client.send(getRequest, BodyHandlers.ofString());
		} catch (IOException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	public void MSauthEntry_A2(){
		this.act_exec.put("MSauthEntry_A2", true);
		this.doWork(0.02433);
	}

	/*
	 * Dnodes
	 */
	public void OrNode_MSauthEntry_A1(){
		//OrNode Logic
		List<Pair<String, Double>> distributionData = new ArrayList<>();
		distributionData.add(new Pair<>("MSauthEntry_A2", 1.0));
		EnumeratedDistribution<String> distribution = new EnumeratedDistribution<>(distributionData);
		String randomChoice = distribution.sample();
		if(randomChoice=="MSauthEntry_A2"){
			MSauthEntry_A2();
		}
	}
	public void ReplyNode_MSauthEntry_A2(){
		//ReplyNode Logic
		BufferedWriter writer;
		try {
			writer = this.response.getWriter();
			writer.write("MSauthEntry_A2[MSauthEntry]");
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
		MSauthEntry_A1();
		//execetute the decision node of already executed evt
		if(this.act_exec.get("MSauthEntry_A1")!=null && this.act_exec.get("MSauthEntry_A1")) {
		  this.act_exec.put("MSauthEntry_A1",false);
		  OrNode_MSauthEntry_A1();
		}
		if(this.act_exec.get("MSauthEntry_A2")!=null && this.act_exec.get("MSauthEntry_A2")) {
		  this.act_exec.put("MSauthEntry_A2",false);
		  ReplyNode_MSauthEntry_A2();
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
