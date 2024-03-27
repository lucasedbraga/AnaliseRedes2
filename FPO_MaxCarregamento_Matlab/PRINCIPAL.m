clear all
clc
format short %menos casas decimais
tic %calculo do tempo

% Condição inicial
x0 = [1]; %Lambda
xi = 1; % Chute inicial
V = 1; 

% Constante de inequação e limite superior dela A*X<b
A = [];
b = [];

% Constante de restrição de igualdade e valdor dela fixado: Aeq*X = beq
Aeq = [];
beq = [];

% Limites inferiores e superiores para as variáveis do problema X
lb = [0.1];
ub = [1000];

% Resolução
[xsol, fval, exitflag, output, lagrange] = fmincon(@(xi) objecfun(Xi,V), x0, A, b, Aeq, beq,lb,ub, @(xi) nonlconstr(xi,V),options)

fator_de_carga = xsol; % Fator de carga otimizado
fluxoAC % Chama o fluxo de potência
disp(V)
max(lagrange.ineqnonlin) % mostra o maior valor de multiplicador de Lagrange

% Informa o tempo de computação
tempo = toc
