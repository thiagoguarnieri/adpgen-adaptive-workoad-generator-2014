#QoE aware synthetic workload generator. Each cluster represents a QoE profile in the system
import math
import numpy as np
from pprint import pprint
import random
import scipy
import scipy.stats
import sys
import csv

#Implements adaptation flow for each sessions
#==============================================================================#
def cbmg(cluster, duration):
	length = int(duration)
	
	if(length % 3 != 0):
		segments_qtd = (length // 3) + 1
	else:
		segments_qtd = (length // 3)
	
	qtdS = {264:0, 464:0, 750:0, 1264:0, 1864:0, 2564:0}

	#markov adaptation flow of each cluster
	MCLUSTER1 = [0.7480,0.2307,0.0079,0.0009,0.0009,0.0116,0.0454,0.1571,0.7775,0.0135,0.0015,0.0050,0.0309,0.0100,0.2362,0.6893,0.0283,0.0053,0.0385,0.0056,0.0104,0.3313,0.5913,0.0229,0.0335,0.0014,0.0048,0.0093,0.6139,0.3371,0.0198,0.0004,0.0005,0.0005,0.0015,0.9773]
	MCLUSTER2 = [0.9024,0.0403,0.0201,0.0123,0.0066,0.0183,0.0202,0.9331,0.0375,0.0047,0.0018,0.0027,0.0128,0.0151,0.9280,0.0339,0.0053,0.0049,0.0087,0.0055,0.0167,0.9319,0.0262,0.0110,0.0091,0.0050,0.0100,0.0233,0.8910,0.0616,0.0045,0.0016,0.0026,0.0030,0.0056,0.9827]
	MCLUSTER3 = [0.8853,0.1083,0.0026,0.0018,0.0006,0.0014,0.1678,0.4207,0.4020,0.0075,0.0010,0.0010,0.1232,0.0099,0.5056,0.3537,0.0063,0.0013,0.0563,0.0025,0.0027,0.8826,0.0546,0.0013,0.1138,0.0044,0.0067,0.0095,0.6727,0.1929,0.1266,0.0033,0.0028,0.0033,0.0048,0.8592]
	MCLUSTER4 = [0.6634,0.3207,0.0103,0.0019,0.0015,0.0022,0.1050,0.5360,0.3475,0.0098,0.0008,0.0009,0.0967,0.0108,0.6261,0.2553,0.0100,0.0011,0.1305,0.0107,0.0135,0.6315,0.2043,0.0095,0.0862,0.0032,0.0089,0.0128,0.7563,0.1326,0.1506,0.0045,0.0070,0.0080,0.0157,0.8142]
	MCLUSTER5 = [0.7968,0.1890,0.0042,0.0097,0.0001,0.0002,0.0877,0.2234,0.6753,0.0132,0.0002,0.0002,0.0641,0.0055,0.4459,0.4806,0.0036,0.0003,0.0199,0.0005,0.0008,0.9769,0.0014,0.0005,0.0607,0.0029,0.0239,0.0605,0.7961,0.0559,0.0400,0.0015,0.0040,0.0529,0.0116,0.8900]
	MCLUSTER6 = [0.7832,0.1997,0.0059,0.0010,0.0011,0.0091,0.0516,0.1609,0.7663,0.0129,0.0023,0.0060,0.0389,0.0093,0.2288,0.6956,0.0208,0.0066,0.0527,0.0052,0.0087,0.3204,0.5953,0.0177,0.0464,0.0021,0.0040,0.0069,0.6163,0.3243,0.0267,0.0007,0.0007,0.0006,0.0013,0.9700]
	MCLUSTER7 = [0.9501,0.0477,0.0010,0.0004,0.0001,0.0007,0.3004,0.4817,0.2154,0.0021,0.0001,0.0003,0.2035,0.0098,0.5063,0.2733,0.0065,0.0006,0.1194,0.0036,0.0058,0.7349,0.1345,0.0018,0.1255,0.0028,0.0075,0.0133,0.4660,0.3849,0.0887,0.0010,0.0011,0.0013,0.0028,0.9051]


	curr_markov = []
    
    #selects proper markov to be used.
	if cluster == 1:
		curr_markov = MCLUSTER1
	elif cluster == 2:
		curr_markov = MCLUSTER2
	elif cluster == 3:
		curr_markov = MCLUSTER3
	elif cluster == 4:
		curr_markov = MCLUSTER4
	elif cluster == 5:
		curr_markov = MCLUSTER5
	elif cluster == 6:
		curr_markov = MCLUSTER6
	elif cluster == 7:
		curr_markov = MCLUSTER7

    #set segment arrays
	segments = [0] * segments_qtd
    
    #the default player behavior is to get the first segment at the lowest bitrate
	curr_state = 264

    #markov. There is 6 bitrates in world cup 2014
	for count in range(segments_qtd):
        #get current bitrate
		segments[count] = curr_state
		qtdS[curr_state] += 1
        #define the next bitrate
		if curr_state == 264:
			curr_state = next_bitrate(curr_markov[0], curr_markov[1], curr_markov[2], curr_markov[3], curr_markov[4], curr_markov[5])
		elif curr_state == 464:
			curr_state = next_bitrate(curr_markov[6], curr_markov[7], curr_markov[8], curr_markov[9], curr_markov[10], curr_markov[11])
		elif curr_state == 750:
			curr_state = next_bitrate(curr_markov[12], curr_markov[13], curr_markov[14], curr_markov[15], curr_markov[16], curr_markov[17])
		elif curr_state == 1264:
			curr_state = next_bitrate(curr_markov[18], curr_markov[19], curr_markov[20], curr_markov[21], curr_markov[22], curr_markov[23])
		elif curr_state == 1864:
			curr_state = next_bitrate(curr_markov[24], curr_markov[25], curr_markov[26], curr_markov[27], curr_markov[28], curr_markov[29])
		elif curr_state == 2564:
			curr_state = next_bitrate(curr_markov[30], curr_markov[31], curr_markov[32], curr_markov[33], curr_markov[34], curr_markov[35])
    
    #counting number of bitrate switches
	adpup = 0
	adpdown = 0
	for count in range(len(segments)-1):
		if segments[count] < segments[count + 1]:
			adpup = adpup + 1
		elif segments[count] > segments[count + 1]:
			adpdown = adpdown + 1
        
    #returns the average bitrate, session load in kbits, adaptation rise, adaptation fall and number of segments for each bitrate
	return round((sum(segments) / (len(segments) * 1.0)), 2), sum(segments) * 3, adpup, adpdown, qtdS
#==============================================================================#
def read_csv(filename):
	my_arrival = []
	
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			my_arrival += row
	
	return my_arrival
#==============================================================================#
#define what is the next bitrate; This is defined according the probabilities
def next_bitrate(p264, p464, p750, p1264, p1864, p2564):
	max_264 = p264
	max_464 = max_264 + p464
	max_750 = max_464 + p750
	max_1264 = max_750 + p1264
	max_1864 = max_1264 + p1864
    
    #get a value uniformly distributed
	selected = random.uniform(0, 1)

	if(selected <= max_264):
		return 264
	elif(selected > max_264 and selected <= max_464):
		return 464
	elif(selected > max_464 and selected <= max_750):
		return 750
	elif(selected > max_750 and selected <= max_1264):
		return 1264
	elif(selected > max_1264 and selected <= max_1864):
		return 1864
	elif(selected > max_1864):
		return 2564
#==============================================================================#
#==============================================================================#
#==============================================================================#
#MAIN
#THIS IS THE RANDOM SEED FOR GENERATORS
np.random.seed(int(sys.argv[2]))
random.seed(int(sys.argv[2]))

#THIS IS THE ROUND NUMBER TO CONTROL FILE NAMING
exec_round = sys.argv[1]

#CHANGE THIS NUMBER TO SET THE NUMBER OF CLIENTS OF SIMULATION
TOTAL_CLIENTS = 50000

#FRACTIONING
CLUSTER1 = int(math.floor(TOTAL_CLIENTS* 0.15056))#pc-unic-aq
CLUSTER2 = int(math.floor(TOTAL_CLIENTS* 0.19874))#mob-mix-dq(a)
CLUSTER3 = int(math.floor(TOTAL_CLIENTS* 0.18176))#pc-mult-dq(b)
CLUSTER4 = int(math.floor(TOTAL_CLIENTS* 0.16360))#pc-unic-vq
CLUSTER5 = int(math.floor(TOTAL_CLIENTS* 0.05105))#pc-unic-mq
CLUSTER6 = int(math.floor(TOTAL_CLIENTS* 0.10205))#pc-mult-aq
CLUSTER7 = int(math.floor(TOTAL_CLIENTS* 0.15223))#pc-unic-bq

clients_list = CLUSTER1 + CLUSTER2 + CLUSTER3 + CLUSTER4 + CLUSTER5 + CLUSTER6 + CLUSTER7

other_metrics = []
user_ids_on = []
user_ids_off = []
user_ids_qtd = []
ident = 0

print("EXECUTION ROUND " + str(exec_round));
print("TOTAL USERS REQUESTED " + str(clients_list));

#==============================================================================#
#USED TO DEFINE THE ARRIVAL OF THE CLIENTS ALONG THE 14400 SECONDS OF THE SIMULATION. IT CAN BE MANIPULATED TO SIMULATE OTHER ARRIVAL REGIMES (E.G. FLASH CROWDS)
#THE DEFAULT BEHAVIOR IS TO FOLLOW THE ARRIVAL RATE OF A TYPICAL SOCCER GAME.
user_arr = np.random.choice(a = np.arange(1,14401,1), size=clients_list, replace = True, p = read_csv("probabilidades_arrival_global_14400.csv"))

#CLUSTERED CLIENT GENERATION
print("CLUSTER 1");
user_q1 = np.ones(CLUSTER1)
user_on1 = scipy.stats.exponpow.rvs(5.481801223511788557e-01, loc = 9.999999999999998890e-01, scale = 3.101964450019013384e+03, size = CLUSTER1, random_state = int(sys.argv[2]))

for count in range(len(user_on1)):
	avg_bitrate, session_load, adpu, adpd, qtdSe = cbmg(1, round(user_on1[count]))
	other_metrics.append([avg_bitrate, session_load, adpu, adpd, qtdSe[264], qtdSe[464], qtdSe[750], qtdSe[1264], qtdSe[1864], qtdSe[2564]])

print("CLUSTER 2");
user_q2 = scipy.stats.nbinom.rvs(0.63, 0.50, loc = 1, size = CLUSTER2, random_state = int(sys.argv[2]))
user_on2 = scipy.stats.weibull_min.rvs(7.241596281563529303e-01, loc = 9.999999999999997780e-01, scale = 5.723601304711355624e+02, size=np.sum(user_q2), random_state = int(sys.argv[2]))
user_off2 = scipy.stats.gamma.rvs(4.089916556459867181e-01, loc = 1.199999999999999858e+02, scale = 1.645501245862382348e+03, size=(np.sum(user_q2) - CLUSTER2), random_state = int(sys.argv[2]))

for count in range(len(user_on2)):
	avg_bitrate, session_load, adpu, adpd, qtdSe = cbmg(2, round(user_on2[count]))
	other_metrics.append([avg_bitrate, session_load, adpu, adpd, qtdSe[264], qtdSe[464], qtdSe[750], qtdSe[1264], qtdSe[1864], qtdSe[2564]])

print("CLUSTER 3");
user_q3 = scipy.stats.nbinom.rvs(0.85, 0.53, loc = 2, size = CLUSTER3, random_state = int(sys.argv[2]))
user_on3 = scipy.stats.exponweib.rvs(1.553993649548129907e+00, 6.177034703388997183e-01, loc = 9.999999999999998890e-01, scale = 4.161600018864073718e+02, size=np.sum(user_q3), random_state = int(sys.argv[2]))
user_off3 = scipy.stats.weibull_min.rvs(7.199083439084643654e-01, loc = 1.199999999999999858e+02, scale = 6.359945534191638217e+02, size=(np.sum(user_q3) - CLUSTER3), random_state = int(sys.argv[2]))

for count in range(len(user_on3)):
	avg_bitrate, session_load, adpu, adpd, qtdSe = cbmg(3, round(user_on3[count]))
	other_metrics.append([avg_bitrate, session_load, adpu, adpd, qtdSe[264], qtdSe[464], qtdSe[750], qtdSe[1264], qtdSe[1864], qtdSe[2564]])
	
print("CLUSTER 4");
user_q4 = np.ones(CLUSTER4)
user_on4 = scipy.stats.exponweib.rvs(2.352054671207686631e+00, 3.704218277335367127e-01, loc = 9.999999999999998890e-01, scale = 7.610299025547681140e+01, size=CLUSTER4, random_state = int(sys.argv[2]))

for count in range(len(user_on4)):
	avg_bitrate, session_load, adpu, adpd, qtdSe = cbmg(4, round(user_on4[count]))
	other_metrics.append([avg_bitrate, session_load, adpu, adpd, qtdSe[264], qtdSe[464], qtdSe[750], qtdSe[1264], qtdSe[1864], qtdSe[2564]])
	
print("CLUSTER 5");
user_q5 = np.ones(CLUSTER5)
user_on5 = scipy.stats.exponpow.rvs(5.067146617471873782e-01, loc = 9.999999999999998890e-01, scale = 3.110276987222374373e+03, size=CLUSTER5, random_state = int(sys.argv[2]))

for count in range(len(user_on5)):
	avg_bitrate, session_load, adpu, adpd, qtdSe = cbmg(5, round(user_on5[count]))
	other_metrics.append([avg_bitrate, session_load, adpu, adpd, qtdSe[264], qtdSe[464], qtdSe[750], qtdSe[1264], qtdSe[1864], qtdSe[2564]])
	
print("CLUSTER 6");
user_q6 = scipy.stats.geom.rvs(0.60, loc = 2, size = CLUSTER6, random_state = int(sys.argv[2]))
user_on6 = scipy.stats.gamma.rvs(6.869073357253523415e-01, loc = 9.999999999999997780e-01, scale = 1.526245082785458180e+03, size=np.sum(user_q6), random_state = int(sys.argv[2]))
user_off6 = scipy.stats.weibull_min.rvs(7.796782637583832276e-01, loc = 1.199999999999999716e+02, scale = 7.682001629482715543e+02, size=(np.sum(user_q6) - CLUSTER6), random_state = int(sys.argv[2]))

for count in range(len(user_on6)):
	avg_bitrate, session_load, adpu, adpd, qtdSe = cbmg(6, round(user_on6[count]))
	other_metrics.append([avg_bitrate, session_load, adpu, adpd, qtdSe[264], qtdSe[464], qtdSe[750], qtdSe[1264], qtdSe[1864], qtdSe[2564]])

print("CLUSTER 7");
user_q7 = np.ones(CLUSTER7)
user_on7 = scipy.stats.exponpow.rvs(5.195572422877892116e-01, loc = 9.999999999999998890e-01, scale = 2.205270028496806844e+03, size=CLUSTER7, random_state = int(sys.argv[2]))

for count in range(len(user_on7)):
	avg_bitrate, session_load, adpu, adpd, qtdSe = cbmg(7, round(user_on7[count]))
	other_metrics.append([avg_bitrate, session_load, adpu, adpd, qtdSe[264], qtdSe[464], qtdSe[750], qtdSe[1264], qtdSe[1864], qtdSe[2564]])
#==============================================================================#
#GENERATING CLIENT ID AND SESSION ID
qtd_vals = np.concatenate((user_q1,user_q2,user_q3,user_q4,user_q5,user_q6,user_q7))
arrival_vals = user_arr
ontimes_vals = np.concatenate((user_on1,user_on2,user_on3,user_on4,user_on5,user_on6,user_on7))
offtimes_vals = np.concatenate((user_off2,user_off3,user_off6))

print("IDENTIFICATION");
for count in range(len(qtd_vals)):
	for count2 in range(int(qtd_vals[count])):
		user_ids_on.append([ident,count2])
	
	for count3 in range((int(qtd_vals[count])-1)):
		user_ids_off.append([ident,count3])
		
	user_ids_qtd.append([ident])
	ident = ident + 1


print("Saving sythetic metrics")
np.savetxt('synthetics/cluster_ontime_' + str(exec_round) + '.csv', np.column_stack((user_ids_on,ontimes_vals)), header = "client_id,sess_id,timeon", comments='', delimiter=',', fmt="%1.2f")
np.savetxt('synthetics/cluster_offtime_' + str(exec_round) + '.csv', np.column_stack((user_ids_off,offtimes_vals)), header = "client_id,sess_id,timeoff", comments='', delimiter=',', fmt="%1.2f")
np.savetxt('synthetics/cluster_qtd_' + str(exec_round) + '.csv', np.column_stack((user_ids_qtd,qtd_vals)), header = "client_id,qtd", comments='', delimiter=',', fmt="%1.2f")
np.savetxt('synthetics/cluster_other_' + str(exec_round) + '.csv', np.column_stack((user_ids_on,other_metrics)), header = "client_id,sess_id,avg_bitrate,kbits,adp_up,adp_down,q264,q464,q750,q1264,q1864,q2564", comments='', delimiter=',', fmt="%1.2f")
np.savetxt('synthetics/cluster_client_enter_' + str(exec_round) + '.csv', np.column_stack((user_ids_qtd,arrival_vals)), header = "client_id,client_ingress", comments='', delimiter=',', fmt="%1.2f")



