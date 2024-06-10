function [t,y,ssR] = lqnODE(X0,MU,NT,NC)
import Gillespie.*

% Make sure vector components are doubles
X0 = double(X0);
MU = double(MU);

% Make sure all vectors are row vectors
if(iscolumn(X0))
    X0 = X0';
end
if(iscolumn(MU))
    MU = MU';
end
if(iscolumn(NT))
    NT = NT';
end
if(iscolumn(NT))
    NC = NC';
end

p.MU = MU; 
p.NT = NT;
p.NC = NC;
p.delta = 10^5; % context switch rate (super fast)

%probchoices
{% for choice in choices %}{% for prob in choice.probs %}p.{{prob}}={{1/choice.probs|length}};
{% endfor %}{% endfor %}

%states name
{% for n in names %}%X({{loop.index}})={{n}};
{% endfor %}

%task ordering
{% for t in task %}%{{loop.index}}={{t.name}};
{% endfor %}

% Jump matrix
jump=[{% for j in jumps %}{% for i in j %}{% if loop.last %}{% if i>=0 %}+{{i}}{% else %}{{i}}{% endif %}{% else %}{% if i>=0 %}+{{i}},  {% else %}{{i}},  {% endif %}{% endif %}{% endfor %};
               {% endfor %}];

T = @(X)propensities_2state(X,p);
opts = odeset('Events',@(t,y)eventfun(t,y,jump,T));
[t,y]=ode15s(@(t,y) jump'*T(y),linspace(0,1000,10001), X0,opts);

ssR=T(y(end,:)');

end

% Propensity rate vector (CTMC)
function Rate = propensities_2state(X, p)
    Rate = [{% for p in props %}{{p}};
    		{% endfor %}];
    Rate(isnan(Rate))=0;
end

function [x,isterm,dir] = eventfun(t,y,jump,T)
dy = jump'*T(y);
%x = norm(dy) - 1e-5;
x=max(abs(dy)) - 1e-5;
isterm = 1;
dir = 0;
end