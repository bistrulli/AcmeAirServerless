clear

%dimensione dipendi dal numero di nomi
X0=zeros(1,{{names| length}});
MU=zeros(1,{{names| length}});

{% for t in task %}{%if t.ref%}{%for e in t.getEntries()%}{%for a in e.getActivities()%}{%if a.__class__.__name__=="Activity"%}X0({{loop.index}})={{t.tsize}};{%endif%}{%endfor%}{%endfor%}{%endif%}{%endfor%}

MU([{% for t in task %}{%for e in t.getEntries()%}{%for a in e.getActivities()%}{%if a.__class__.__name__=="Activity"%}{{names.index("X"+e.name+"_"+a.name)+1}} {%endif%}{%endfor%}{%endfor%}{%endfor%}])=1.0./[{% for t in task %}{%for e in t.getEntries()%}{%for a in e.getActivities()%}{%if a.__class__.__name__=="Activity"%}{{a.stime}} {%endif%}{%endfor%}{%endfor%}{%endfor%}]; 
NT=[{% for t in task %}{{t.tsize}} {%endfor%}];
NC=[{% for t in task %}{{t.proc.mult}} {%endfor%}];

names=[{% for t in task %}{%for e in t.getEntries()%}"{{e.name}}"{%if not loop.last%},{%endif%}{%endfor%}{%if not loop.last%},{%endif%}{%endfor%}];

[t,y,ssROde] = lqnODE(X0,MU,NT,NC);

{% for t in task %}{%if t.ref%}{%for e in t.getEntries()%}{%for a in e.getActivities()%}{%if a.__class__.__name__=="Activity"%}Tode=ssROde({{loop.index}});{%endif%}{%endfor%}{%endfor%}{%endif%}{%endfor%}
{% for t in task %}{%if t.ref%}{%for e in t.getEntries()%}{%for a in e.getActivities()%}{%if a.__class__.__name__=="Activity"%}RTode=X0({{loop.index}})/Tode;{%endif%}{%endfor%}{%endfor%}{%endif%}{%endfor%}

NCopt=[inf,{%for t in task%}{%if not t.ref%}{%for e in t.getEntries()%}sum(y(end,[{%for a in e.getActivities()%}{%if a.__class__.__name__=="Activity"%}{{names.index("X"+e.name+"_"+a.name)+1}}{%if not loop.last%},{%endif%}{%endif%}{%endfor%}]),2){%endfor%}{%endif%}{%if not loop.last and not t.ref%},{%endif%}{%endfor%}];
NTLqn=[inf,{%for t in task%}{%if not t.ref%}{%for e in t.getEntries()%}sum(y(end,[{%for a in e.getActivities()%}{%if loop.first%}{{names.index("X"+e.name+"_"+a.name)}},{%endif%}{{names.index("X"+e.name+"_"+a.name)+1}}{%if not loop.last%},{%endif%}{%endfor%}]),2){%endfor%}{%endif%}{%if not loop.last and not t.ref%},{%endif%}{%endfor%}];
NTopt=[inf,ceil(NTLqn(2:end)./NCopt(end,2:end))];

fileID = fopen('optSol.csv', 'w');
fprintf(fileID,"name,ncopt,ntopt\n");
for i=2:length(names)
    fprintf(fileID,"%s,%f,%d\n",names(i),NCopt(i),NTopt(i));
end

%for i=1:length(names)
%    disp([names(i),NTopt(i+1)])
%    system(sprintf("sh ../%s/update.sh %d 100 1",names(i),NTopt(i+1)))
%end