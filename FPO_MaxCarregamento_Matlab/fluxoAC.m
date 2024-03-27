%% FLUXO DE POTÊNCIA MONOFÁSICO ATRAVÉS DO MÉTODO DE INJEÇÃO DE POTÊNCIAS TRADICIONAL

%clc       % limpa a tela do workspace
%close all % fecha qualquer figura previamente apresentada
%clear all % limpa todas as variáveis do problema



%        |Barra | Tipo| Vo | Thetao | Pg | Qg |  Pd |   Qd |    Qmin |     Qmax |
busd = [    1     1    1.060   0       0     0     0     0       0       0;
            2     2    1.045   0      40   42.4  21.7   12.7    -40     50;
            3     2    1.010   0       0   23.4  94.2   19.0     0      40;
            4     3    1.0     0       0     0   47.8   -3.9     0       0;
            5     3    1.0     0       0     0    7.6    1.6     0       0;
            6     2    1.070   0       0   12.2  11.2    7.5    -6      24;
            7     3    1.0     0       0     0    0.0    0.0     0       0;
            8     2    1.090   0       0   17.4   0.0    0.0    -6      24;
            9     3    1.0     0       0     0   29.5   16.6     0       0;
            10    3    1.0     0       0     0    9.0    5.8     0       0;
            11    3    1.0     0       0     0    3.5    1.8     0       0;
            12    3    1.0     0       0     0    6.1    1.6     0       0;
            13    3    1.0     0       0     0   13.5    5.8     0       0;
            14    3    1.0     0       0     0   14.9    5.0     0       0;
            ];
        
%         |  De |  Para   |   R(pu)  |   X(pu) |  B/2 (pu) |   a  |
linedata =  [1      2       0.01938   0.05917    0.0264         1
             1      5       0.05403   0.22304    0.0246         1
             2      3       0.04699   0.19797    0.0219         1
             2      4       0.05811   0.17632    0.0170         1
             2      5       0.05695   0.17388    0.0173         1
             3      4       0.06701   0.17103    0.0064         1
             4      5       0.01335   0.04211    0.0            1
             4      7       0.0       0.20912    0.0        0.978
             4      9       0.0       0.55618    0.0        0.969
             5      6       0.0       0.25202    0.0        0.932
             6     11       0.09498   0.19890    0.0            1
             6     12       0.12291   0.25581    0.0            1
             6     13       0.06615   0.13027    0.0            1
             7      8       0.0       0.17615    0.0            1
             7      9       0.0       0.11001    0.0            1
             9     10       0.03181   0.08450    0.0            1
             9     14       0.12711   0.27038    0.0            1
            10     11       0.08205   0.19207    0.0            1
            12     13       0.22092   0.19988    0.0            1
            13     14       0.17093   0.34802    0.0            1 
            ];
            
%% Etapa 1) Leitura dos dados de ramos:

fb = linedata(:,1);     % barra DE
tb = linedata(:,2);     % barra PARA
nb = max(max(fb),max(tb));    % número de barras
nl = length(fb);           % número de ramos


r = linedata(:,3);      % resistência
x = linedata(:,4);      % reatância
b = linedata(:,5);      % admitância shunt
a = linedata(:,6);      % valor de tap
z = r + i*x;            % Impedâncias dos trechos
y = 1./z;               % Admitâncias dos trechos
b = i*b;                % Compatibilizando b imaginário


%% Etapa 2) Formação da matriz de admitância nodal

Y = zeros(nb,nb);        % Formação da matriz de admitância nodal
 
 % Elementos fora da diagonal
 for k = 1:nl
     Y(fb(k),tb(k)) = Y(fb(k),tb(k)) - y(k)/a(k);
     Y(tb(k),fb(k)) = Y(fb(k),tb(k));
 end
 
 % Elementos da diagonal
 for m = 1:nb
     for n = 1:nl
         if fb(n) == m
             Y(m,m) = Y(m,m) + y(n)/(a(n)^2) + b(n);
         elseif tb(n) == m
             Y(m,m) = Y(m,m) + y(n) + b(n);
         end
     end
 end
 Y;                  % Matriz de admitâncias
 Zbuz = inv(Y);      % Matriz de impedâncias nodais
G = real(Y);                % Matriz de Condutâncias
B = imag(Y);                % Matriz de Susceptâncias

%% Leitura de dados de barra:
BMva = 1000;                % Potência base
bus = busd(:,1);            % Número da barra
type = busd(:,2);           % Tipo da barra: 1-Referência, 2-PV, 3-PQ.
V = busd(:,3);              % Tensões especificadas
del = zeros(length(V),1);   % ângulos de fase
Pg = busd(:,5)/BMva;        % Potência Ativa gerada
Qg = busd(:,6)/BMva;        % Potência Reativa gerada
Pl = busd(:,7)/BMva;        % POtência ativa demandada
Ql = busd(:,8)/BMva;        % Potência reativa demandada
Qmin = busd(:,9)/BMva;      % Limite mínimo de reativos
Qmax = busd(:,10)/BMva;     % Limite máximo de reativos
nbus = max(bus);            % Número total de barras
P = Pg - Pl*fator_de_carga;                % Potência liquida ativa COM PARCELA DE FATOR DE CARGA
Q = Qg - Ql*fator_de_carga;                % Potência liquida reativa COM PARCELA DE FATOR DE CARGA
Psp = P;                    % Potência ativa especificada      
Qsp = Q;                    % Potência reativa especificada


pv = find(type == 2 | type == 1);       % Indice de barras PV
npv = length(pv);                       % Numero de barras PV
pq = find(type == 3);                   % Indice de barras PQ
npq = length(pq);                       % Numero de barras PQ

%% Etapa 3) Processo iterativo de Newton-Raphson
Tol = 1;            % variável de tolerância
Iter = 1;           % variável contadora de iterações
while (Tol > 1e-3)   % início do processo iterativo
    P = zeros(nbus,1);
    Q = zeros(nbus,1);
    % Calcular P and Q funcionais
    for i = 1:nbus
        for k = 1:nbus
            P(i) = P(i) + V(i)* V(k)*(G(i,k)*cos(del(i)-del(k)) + B(i,k)*sin(del(i)-del(k)));
            Q(i) = Q(i) + V(i)* V(k)*(G(i,k)*sin(del(i)-del(k)) - B(i,k)*cos(del(i)-del(k)));
        end
    end


    % Calcular resíduos de potências
    dPa = Psp-P;
    dQa = Qsp-Q;
    k = 1;
    dQ = zeros(npq,1);
    for i = 1:nbus
        if type(i) == 3
            dQ(k,1) = dQa(i);
            k = k+1;
        end
    end
    dP = dPa(2:nbus);
    M = [dP; dQ];       % Vetor de resíduos
    
    % Jacobiana
    % J1 - Derivadas parciais de P em relação a angulos 
    J1 = zeros(nbus-1,nbus-1);
    for i = 1:(nbus-1)
        m = i+1;
        for k = 1:(nbus-1)
            n = k+1;
            if n == m
                for n = 1:nbus
                    J1(i,k) = J1(i,k) + V(m)* V(n)*(-G(m,n)*sin(del(m)-del(n)) + B(m,n)*cos(del(m)-del(n)));
                end
                J1(i,k) = J1(i,k) - V(m)^2*B(m,m);
            else
                J1(i,k) = V(m)* V(n)*(G(m,n)*sin(del(m)-del(n)) - B(m,n)*cos(del(m)-del(n)));
            end
        end
    end
    
    % J2 - Derivadas parciais de P em relação a V 
    J2 = zeros(nbus-1,npq);
    for i = 1:(nbus-1)
        m = i+1;
        for k = 1:npq
            n = pq(k);
            if n == m
                for n = 1:nbus
                    J2(i,k) = J2(i,k) + V(n)*(G(m,n)*cos(del(m)-del(n)) + B(m,n)*sin(del(m)-del(n)));
                end
                J2(i,k) = J2(i,k) + V(m)*G(m,m);
            else
                J2(i,k) = V(m)*(G(m,n)*cos(del(m)-del(n)) + B(m,n)*sin(del(m)-del(n)));
            end
        end
    end
    
    % J3 - Derivadas parciais de Q em relação a angulos 
    J3 = zeros(npq,nbus-1);
    for i = 1:npq
        m = pq(i);
        for k = 1:(nbus-1)
            n = k+1;
            if n == m
                for n = 1:nbus
                    J3(i,k) = J3(i,k) + V(m)* V(n)*(G(m,n)*cos(del(m)-del(n)) + B(m,n)*sin(del(m)-del(n)));
                end
                J3(i,k) = J3(i,k) - V(m)^2*G(m,m);
            else
                J3(i,k) = V(m)* V(n)*(-G(m,n)*cos(del(m)-del(n)) - B(m,n)*sin(del(m)-del(n)));
            end
        end
    end
    
    % J4 - Derivadas parciais de Q em relação a V 
    J4 = zeros(npq,npq);
    for i = 1:npq
        m = pq(i);
        for k = 1:npq
            n = pq(k);
            if n == m
                for n = 1:nbus
                    J4(i,k) = J4(i,k) + V(n)*(G(m,n)*sin(del(m)-del(n)) - B(m,n)*cos(del(m)-del(n)));
                end
                J4(i,k) = J4(i,k) - V(m)*B(m,m);
            else
                J4(i,k) = V(m)*(G(m,n)*sin(del(m)-del(n)) - B(m,n)*cos(del(m)-del(n)));
            end
        end
    end
    
    J = [J1 J2; J3 J4];         % Matriz Jacobiana
    
    X = J\M;                    % Definição do vetor X de resíduos de V e angulos
    dTh = X(1:nbus-1);          % Residuos de angulos
    dV = X(nbus:end);           % Residuos de tensões V
    
    % Atualização do vetpr solução:
    del(2:nbus) = dTh + del(2:nbus);
    k = 1;
    for i = 2:nbus
        if type(i) == 3
            V(i) = dV(k) + V(i);
            k = k+1;
        end
    end
    Iter = Iter + 1;           % próxima iteração
    Tol = max(abs(M));         % cálculo de tolerância
end

   
% Final do processo iterativo

num=nb;

Vm = V.*(cos(del)+j*sin(del));      % Obtenção dos valores de tensão complexos
Del = 180/pi*del;                   % Angulos dem graus
fb = linedata(:,1);            % barra DE
tb = linedata(:,2);            % barra PARA
b = linedata(:,5);             % B shunt
a = linedata(:,6);             % tap
nl = length(fb);            % número de ramos
Pl = busd(:,7);             % potência ativa de carga
Ql = busd(:,8);             % potência reativa de carga

nb = length(Vm);            % Numero de barras
Iij = zeros(nb,nb);         % correntes ramais
Sij = zeros(nb,nb);         % fluxos complexos

% INjeções de correntes nas barras do sistema
 I = Y*Vm;
 Im = abs(I);
 Ia = angle(I);
 
%Fluxos de correntes nas linhas
 for m = 1:nb
     for n = 1:nl
         if fb(n) == m
             p = tb(n);
             Iij(m,p) = -(Vm(m) - Vm(p)*a(n))*Y(m,p)/a(n)^2 + b(n)/a(n)^2*Vm(m);  
             Iij(p,m) = -(Vm(p) - Vm(m)/a(n))*Y(p,m) + b(n)*Vm(p);
         elseif tb(n) == m
             p = fb(n);
             Iij(m,p) = -(Vm(m) - Vm(p)/a(n))*Y(p,m) + b(n)*Vm(m);
             Iij(p,m) = -(Vm(p) - Vm(m))*Y(m,p)/a(n)^2 + b(n)/a(n)^2*Vm(p);
         end
     end
 end
 
 Iijr = real(Iij);
 Iiji = imag(Iij);

 % Fluxos de potências
 for m = 1:nb
     for n = 1:nb
         if m ~= n
             Sij(m,n) = Vm(m)*conj(Iij(m,n))*BMva;
         end
     end
 end
 
 Pij = real(Sij);
 Qij = imag(Sij);
 
 % Perdas nas linhas:
 Lij = zeros(nl,1);
 for m = 1:nl
     p = fb(m); q = tb(m);
     Lij(m) = Sij(p,q) + Sij(q,p);
 end
 
 Lpij = real(Lij);
 Lqij = imag(Lij);
 
 % Potências injetadas em cada barra
 Si = zeros(nb,1);
 for i = 1:nb
     for k = 1:nb
         Si(i) = Si(i) + conj(Vm(i))* Vm(k)*Y(i,k)*BMva;
     end
 end
 Pi = real(Si);
 Qi = -imag(Si);
 Pg = Pi+Pl;    % potências geradas
 Qg = Qi+Ql;    % potências reativas geradas
 
