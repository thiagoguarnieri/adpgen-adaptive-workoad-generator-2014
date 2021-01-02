# AdpGen Synthetic Workload Generator
AdpGen, a workload generator for live events broadcasted through HTTP Adaptive Streaming, based on 2014 FIFA World Cup event.
https://ieeexplore.ieee.org/document/8969602/

<h1>Instructions</h1>
To call the generator from the command line use: python generator_cluster_markov_thesis_v2.py [execution round number] [random seed];<br />
Example: python generator_cluster_markov_thesis_v2.py 1 1276;<br />

<p>
The output is stored in the <b>synthetic</b> folder:
<ul>
<li>cluster_ontime_x.csv: session duration in seconds</li>
<li>cluster_offtime_x.csv: client inter-session duration</li>
<li>cluster_qtd_x.csv: client number of sessions</li>
<li>cluster_other_x.csv: performance metrics (average bitrate, number of adaptations)</li>
<li>cluster_client_enter_x.csv: client arrival time</li>
</ul>
</p>
  
<h1>Number of clients and arrival regime</h1>

<p>
<b>Number of clients</b><br/>
To change the number of clients, change the value of variable <i>TOTAL_CLIENTS</i> on line 133
</p>
<p>
<b>Arrival regime</b><br/>
Client arrival follows a uniform distribution where probabilities are stored in the file <i>probabilidades_arrival_global_14400.csv</i><br/>
</p>
<p>
To change the file as well as the simulation lengh, please manipulate the following instruction
user_arr = np.random.choice(a = np.arange(1,14401,1), size=clients_list, replace = True, p = read_csv("probabilidades_arrival_global_14400.csv"))
</p>
