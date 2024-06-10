import numpy as np
import casadi

class {{name}}Ctrl(object):

	#states name
	{% for n in names %}#X({{loop.index0}})={{n}};
	{% endfor %}
	
	#task ordering
	{% for t in task %}#{{loop.index0}}={{t.name}};
	{% endfor %}
	
	model = None
	stateVar = None
	NT = None
	NC = None
	initX = None
	H = None
	delta=10.0**4
	dt=10**-4
	
	name =  "{{name}}"
	stoich_matrix =  np.matrix([{% for j in jumps %}[{% for i in j %}{% if loop.last %}{% if i>=0 %}+{{i}}{% else %}{{i}}{% endif %}{% else %}{% if i>=0 %}+{{i}},  {% else %}{{i}},  {% endif %}{% endif %}{% endfor %}],
	          {% endfor %}]);
	
	def __init__(self,MU,H=5):
		self.H = H
		self.MU = MU
		self.model = self.model = casadi.Opti()
		self.stateVar = self.model.variable({{names|length}},H+1);
		self.initX = self.model.parameter({{names|length}},1)
		self.NC = self.model.variable(1,{{task|length}});
		self.NT = self.model.variable(1,{{task|length}});
		self.buildOpt()
	
	def buildOpt(self):
		self.model.subject_to(self.stateVar[:,0]==self.initX);
		
		self.model.subject_to(casadi.vec(self.stateVar)>=0)
		self.model.subject_to(self.model.bounded(0,self.NC,1000))
		self.model.subject_to(self.model.bounded(0,self.NT,1000))
		
		for h in range(0,self.H):
			dxF=self.prop_func(self.stateVar[:,h],self.NT, self.NC, self.MU, self.delta,1)
			XhF=[]
			for i in range(self.stoich_matrix.T.shape[0]):
				xhf=0
				for j in range(self.stoich_matrix.T.shape[1]):
					xhf+=self.stoich_matrix.T[i,j]*dxF[j]*self.dt/2
				XhF.append(xhf+self.stateVar[i,h]);
			
			dxF1=self.prop_func(XhF,self.NT, self.NC, self.MU, self.delta,0)
			XhF1=[]
			for i in range(self.stoich_matrix.T.shape[0]):
				xhf1=0
				for j in range(self.stoich_matrix.T.shape[1]):
					xhf1+=self.stoich_matrix.T[i,j]*dxF1[j]*self.dt
				XhF1.append(xhf+XhF[i]);
				
			dxF2=self.prop_func(XhF1,self.NT, self.NC, self.MU, self.delta,1)
			XhF2=[]
			for i in range(self.stoich_matrix.T.shape[0]):
				xhf2=0
				for j in range(self.stoich_matrix.T.shape[1]):
					xhf2+=self.stoich_matrix.T[i,j]*dxF2[j]*self.dt/2
				XhF2.append(xhf+XhF1[i]);
			
		for i in range(self.stoich_matrix.shape[1]):
			self.model.subject_to(self.stateVar[i,h+1]==XhF2[i])
			
		#optionsIPOPT={'print_time':False,'ipopt':{'print_level':0}}
		self.model.solver('ipopt',{})  
	
	def Solve(self,X0,MU,NC_old=None,NT_old=None):
		
		self.model.set_value(self.initX, X0)
			
		obj=0
		for h in range(1,self.H+1):
			obj+=(self.stateVar[-1,h]*MU[0,-1]-10)**2
		
		self.model.minimize(obj)
		self.model.solve()
		
	
	def prop_func(self,X,NT,NC,MU,delta,F):
		Rate=[{% for p in props %}{{p}},
				{% endfor %}]
		return Rate

if __name__ == "__main__":
	ctrl=_2tierCtrl(MU=np.matrix([0 for i in range(7)]))
	print(ctrl.stateVar[:,0])