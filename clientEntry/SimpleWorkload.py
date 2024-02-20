from locust import HttpUser, task, between, events
import queue, time, logging
import locust.stats
import numpy as np
import subprocess
from locust.stats import StatsCSVFileWriter

locust.stats.CSV_STATS_INTERVAL_SEC = 1


@events.test_stop.add_listener
def on_test_stop(**kw):
	pass


class SimpleWorkload(HttpUser):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.nreq = 0
		self.act_exec = {}
		self.act_thread = {}
	
	def doWait(self,ttime):
		delay=np.random.exponential(scale=ttime)
		time.sleep(delay)
	
	
	#Activities
	def clientEntry_A1(self):
		self.act_exec["clientEntry_A1"]=True;
		self.doWait(1.0E-5);

		tgt_url = "MSviewprofileEntry";
		self.client.get(tgt_url)
	def clientEntry_A2(self):
		self.act_exec["clientEntry_A2"]=True;
		self.doWait(1.0E-5);

		tgt_url = "MSupdateprofileEntry";
		self.client.get(tgt_url)
	def clientEntry_A3(self):
		self.act_exec["clientEntry_A3"]=True;
		self.doWait(1.0E-5);

		tgt_url = "MSbookflightsEntry";
		self.client.get(tgt_url)
	def clientEntry_A4(self):
		self.act_exec["clientEntry_A4"]=True;
		self.doWait(1.0E-5);

		tgt_url = "MScancelbookingEntry";
		self.client.get(tgt_url)
	def clientEntry_A5(self):
		self.act_exec["clientEntry_A5"]=True;
		self.doWait(1.0E-5);

		tgt_url = "MSqueryflightsEntry";
		self.client.get(tgt_url)
	def clientEntry_A6(self):
		self.act_exec["clientEntry_A6"]=True;
		self.doWait(1.0E-5);

		tgt_url = "MSauthEntry";
		self.client.get(tgt_url)
	def clientEntry_A7(self):
		self.act_exec["clientEntry_A7"]=True;
		self.doWait(0.2);

	
	#Dnodes
	def OrNode_clientEntry_A1(self):
		#OrNode Logic
		label = []
		p = []
		label.append("clientEntry_A2")
		p.append(1.0)
		
		randomChoice = np.random.choice(a=label,p=p)
		if(randomChoice=="clientEntry_A2"):
			self.clientEntry_A2()
	def OrNode_clientEntry_A2(self):
		#OrNode Logic
		label = []
		p = []
		label.append("clientEntry_A3")
		p.append(1.0)
		
		randomChoice = np.random.choice(a=label,p=p)
		if(randomChoice=="clientEntry_A3"):
			self.clientEntry_A3()
	def OrNode_clientEntry_A3(self):
		#OrNode Logic
		label = []
		p = []
		label.append("clientEntry_A4")
		p.append(1.0)
		
		randomChoice = np.random.choice(a=label,p=p)
		if(randomChoice=="clientEntry_A4"):
			self.clientEntry_A4()
	def OrNode_clientEntry_A4(self):
		#OrNode Logic
		label = []
		p = []
		label.append("clientEntry_A5")
		p.append(1.0)
		
		randomChoice = np.random.choice(a=label,p=p)
		if(randomChoice=="clientEntry_A5"):
			self.clientEntry_A5()
	def OrNode_clientEntry_A5(self):
		#OrNode Logic
		label = []
		p = []
		label.append("clientEntry_A6")
		p.append(1.0)
		
		randomChoice = np.random.choice(a=label,p=p)
		if(randomChoice=="clientEntry_A6"):
			self.clientEntry_A6()
	def OrNode_clientEntry_A6(self):
		#OrNode Logic
		label = []
		p = []
		label.append("clientEntry_A7")
		p.append(1.0)
		
		randomChoice = np.random.choice(a=label,p=p)
		if(randomChoice=="clientEntry_A7"):
			self.clientEntry_A7()
	
	@task
	def visit_homepage(self):
		# execetute the entry activity
		self.clientEntry_A1()
		# execetute the decision node of already executed evt
		if(self.act_exec["clientEntry_A1"]!=None and self.act_exec["clientEntry_A1"]):
		  self.act_exec["clientEntry_A1"]=False
		  self.OrNode_clientEntry_A1()
		# execetute the decision node of already executed evt
		if(self.act_exec["clientEntry_A2"]!=None and self.act_exec["clientEntry_A2"]):
		  self.act_exec["clientEntry_A2"]=False
		  self.OrNode_clientEntry_A2()
		# execetute the decision node of already executed evt
		if(self.act_exec["clientEntry_A3"]!=None and self.act_exec["clientEntry_A3"]):
		  self.act_exec["clientEntry_A3"]=False
		  self.OrNode_clientEntry_A3()
		# execetute the decision node of already executed evt
		if(self.act_exec["clientEntry_A4"]!=None and self.act_exec["clientEntry_A4"]):
		  self.act_exec["clientEntry_A4"]=False
		  self.OrNode_clientEntry_A4()
		# execetute the decision node of already executed evt
		if(self.act_exec["clientEntry_A5"]!=None and self.act_exec["clientEntry_A5"]):
		  self.act_exec["clientEntry_A5"]=False
		  self.OrNode_clientEntry_A5()
		# execetute the decision node of already executed evt
		if(self.act_exec["clientEntry_A6"]!=None and self.act_exec["clientEntry_A6"]):
		  self.act_exec["clientEntry_A6"]=False
		  self.OrNode_clientEntry_A6()
		
		

if __name__ == "__main__":
	# Define output file path
    output_file = "locust_results.csv"

    # Create StatsCSVFileWriter instance
    stats_writer = StatsCSVFileWriter(
        file_path=output_file,
        stats=[
            "total_requests",
            "fail_ratio",
            "min_response_time",
            "max_response_time",
            "median_response_time",
            "avg_response_time",
            "current_rps"
        ],
        ignore_non_aggregate=True  # Only write aggregate data
    )

    # Register the stats writer
    env = Environment(user_classes=[SimpleWorkload])
    env.stats_listeners.append(stats_writer)

    # Run Locust in headless mode
    env.run()

    # Stats are now saved to the specified CSV file
	#SimpleWorkload().run()
	
