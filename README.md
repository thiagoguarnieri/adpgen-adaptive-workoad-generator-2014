# adpgen-adaptive-workoad-generator
AdpGen, a workload generator for live events broadcasted through HTTP Adaptive Streaming

1) Instruções
Para chamar o gerador usar: python generator_cluster_markov_thesis_v2.py [execution round number] [random seed];
Exemplo: python generator_cluster_markov_thesis_v2.py 1 1276;

2) A execução gera os arquivos na pasta "synthetic" que são:
cluster_ontime_x.csv: com a duração de cada sessão de cliente
cluster_offtime_x.csv: com a duração de cada intervalo entre sessões
cluster_qtd_x.csv: com a quantidade de sessões de cada cliente
cluster_other_x.csv: com informações de QoE como taxa de bits média e quantidade de adaptação de cada sessão
cluster_client_enter_x.csv: com o segundo de chegada (a partir do inicio da transmissão) de cada cliente

3)Manipulando regime

a) Quantidade de clientes
Para mudar a quantidade de clientes basta alterar a variável TOTAL_CLIENTS da linha 133

b) Taxa de chegada de clientes

Para alterar o regime de chegada dos clientes, isto é, a fração de clientes que chega a cada segundo, basta alterar o arquivo probabilidades_arrival_global_14400.csv. 
Este arquivo está setado para simular um intervalo de 14400 segundos, mas isso pode ser mudado. Basta que também seja mudado a instrução:
user_arr = np.random.choice(a = np.arange(1,14401,1), size=clients_list, replace = True, p = read_csv("probabilidades_arrival_global_14400.csv"))
