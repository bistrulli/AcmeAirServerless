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
	private static final Logger logger = Logger.getLogger("MSvalidateidEntry");
	private static ThreadMXBean mgm = ManagementFactory.getThreadMXBean();
	private static HttpClient client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(180)).build();
	private HttpResponse response = null;
	private HashMap<String, Boolean> act_exec=new HashMap<String, Boolean>();
	private HashMap<String, Thread> act_thread=new HashMap<String, Thread>();
	private Long  startCpuTime=null;

	/*
	 * activities
	 */
	public void MSvalidateidEntry_A1(){
		this.act_exec.put("MSvalidateidEntry_A1", true);
		this.doWork(0.15);
	}

	/*
	 * Dnodes
	 */
	public void ReplyNode_MSvalidateidEntry_A1(){
		//ReplyNode Logic
		BufferedWriter writer;
		try {
			writer = this.response.getWriter();
			writer.write("MSvalidateidEntry_A1[MSvalidateidEntry]");
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
		
		//execute the entry activity
		MSvalidateidEntry_A1();
		//execetute the decision node of already executed evt
		if(this.act_exec.get("MSvalidateidEntry_A1")!=null && this.act_exec.get("MSvalidateidEntry_A1")) {
		  this.act_exec.put("MSvalidateidEntry_A1",false);
		  ReplyNode_MSvalidateidEntry_A1();
		}
		Logic.logger.info("time:="+String.valueOf(mgm.getCurrentThreadCpuTime()-this.startCpuTime));
	}

	private void doWork(Double stime) {
		ExponentialDistribution dist = new ExponentialDistribution(stime);
		long delay = Long.valueOf(Math.round(dist.sample() * 1e9));
		long start = mgm.getCurrentThreadCpuTime();
		while ((mgm.getCurrentThreadCpuTime() - start) < delay) {
		}
	}
}
