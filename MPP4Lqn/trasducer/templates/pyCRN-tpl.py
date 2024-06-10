import numpy as np

class pyCRN(object):

	#states name
	{% for n in names %}#X({{loop.index0}})={{n}};
	{% endfor %}
	
	#task ordering
	{% for t in task %}#{{loop.index0}}={{t.name}};
	{% endfor %}
	
	name =  "{{name}}"
	stoich_matrix =  np.matrix([{% for j in jumps %}[{% for i in j %}{% if loop.last %}{% if i>=0 %}+{{i}}{% else %}{{i}}{% endif %}{% else %}{% if i>=0 %}+{{i}},  {% else %}{{i}},  {% endif %}{% endif %}{% endfor %}],
	           {% endfor %}]);
	
	def prop_func(self,X,p):
		Rate=np.matrix([{% for p in props %}{{p}},
				{% endfor %}])
		Rate[np.isnan(Rate)]=0;
		return Rate.tolist()[0]