function [c, ceq] = nonlconstr(xi,v)


fator = xi; % Valor atualizado da variável otimizada

fluxoAC;  % Roda o fluxo de potência para atualziar os valores

c = [V-1.15;  %limite superior de tensão V<1.05
     -V+0.95; %limite inferior de tensão V>0.95
];

ceq = [];
