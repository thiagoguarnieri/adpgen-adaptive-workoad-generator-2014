# adpgen-adaptive-workoad-generator
AdpGen, a workload generator for live events broadcasted through HTTP Adaptive Streaming

<h1>Instructions</h1>
To call the generator from the command line use: python generator_cluster_markov_thesis_v2.py [execution round number] [random seed];<br />
Example: python generator_cluster_markov_thesis_v2.py 1 1276;<br />

<p>
The output is stored in the <b>synthetic</b> folder:
<ul>
<li>cluster_ontime_x.csv: com a duração de cada sessão de cliente</li>
<li>cluster_offtime_x.csv: com a duração de cada intervalo entre sessões</li>
<li>cluster_qtd_x.csv: com a quantidade de sessões de cada cliente</li>
<li>cluster_other_x.csv: com informações de QoE como taxa de bits média e quantidade de adaptação de cada sessão</li>
<li>cluster_client_enter_x.csv: com o segundo de chegada (a partir do inicio da transmissão) de cada cliente</li>
</ul>
</p>
  
<u1>Number of clients and arrival regime</u1>

a) Number of clients
Para mudar a quantidade de clientes basta alterar a variável TOTAL_CLIENTS da linha 133

b) Arrival regime

Para alterar o regime de chegada dos clientes, isto é, a fração de clientes que chega a cada segundo, basta alterar o arquivo probabilidades_arrival_global_14400.csv. 
Este arquivo está setado para simular um intervalo de 14400 segundos, mas isso pode ser mudado. Basta que também seja mudado a instrução:
user_arr = np.random.choice(a = np.arange(1,14401,1), size=clients_list, replace = True, p = read_csv("probabilidades_arrival_global_14400.csv"))
