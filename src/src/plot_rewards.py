# Plot rewards
import matplotlib
matplotlib.use('Agg')
import pylab

# Reward shaping
data_rw1 = pylab.loadtxt(open("models/rw_shaping_exp0.0001_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
data_rw2 = pylab.loadtxt(open("models/rw_shaping_exp0.0003_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
data_rw3 = pylab.loadtxt(open("models/rw_shaping_exp0.001_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
data_rw4 = pylab.loadtxt(open("models/rw_shaping_exp0.003_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
data_rw5 = pylab.loadtxt(open("models/rw_shaping_exp0.01_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
pylab.figure()
pylab.plot(data_rw1[:,1], data_rw1[:,0], label='Reward = 0.0001')
pylab.plot(data_rw2[:,1], data_rw2[:,0], label='Reward = 0.0003')
pylab.plot(data_rw3[:,1], data_rw3[:,0], label='Reward = 0.001')
pylab.plot(data_rw4[:,1], data_rw4[:,0], label='Reward = 0.003')
pylab.plot(data_rw5[:,1], data_rw5[:,0], label='Reward = 0.01')
pylab.xlabel('Steps', fontsize=20)
pylab.ylabel('Reward', fontsize=20)
pylab.xticks(fontsize=16)
pylab.yticks(fontsize=16)
pylab.legend()
pylab.grid()
pylab.tight_layout()
pylab.savefig('rewards_reward_shaping.png')

# Pnmac
data_pnmac1 = pylab.loadtxt(open("models/pnmac_exp_0.05_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
data_pnmac2 = pylab.loadtxt(open("models/pnmac_exp_0.1_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
data_pnmac3 = pylab.loadtxt(open("models/pnmac_exp_0.15_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
data_pnmac4 = pylab.loadtxt(open("models/pnmac_exp_0.25_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
data_pnmac5 = pylab.loadtxt(open("models/pnmac_exp_0.5_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
pylab.figure()
pylab.plot(data_pnmac1[:,1], data_pnmac1[:,0], label='Reward = 0.05')
pylab.plot(data_pnmac2[:,1], data_pnmac2[:,0], label='Reward = 0.1')
pylab.plot(data_pnmac3[:,1], data_pnmac3[:,0], label='Reward = 0.15')
pylab.plot(data_pnmac4[:,1], data_pnmac4[:,0], label='Reward = 0.25')
pylab.plot(data_pnmac5[:,1], data_pnmac5[:,0], label='Reward = 0.5')
pylab.xlabel('Steps', fontsize=20)
pylab.ylabel('Reward', fontsize=20)
pylab.xticks(fontsize=16)
pylab.yticks(fontsize=16)
pylab.legend()
pylab.grid()
pylab.tight_layout()
pylab.savefig('rewards_pnmac.png')

# Encounter type
data_encounter1 = pylab.loadtxt(open("models/int_behaviorno_act_encounter_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
data_encounter2 = pylab.loadtxt(open("models/int_behaviorrandom_act_encounter_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
data_encounter3 = pylab.loadtxt(open("models/int_behaviorsingle_act_encounter_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
data_encounter4 = pylab.loadtxt(open("models/int_behaviorsticky_act_encounter_s0/logs/progress.csv"), delimiter=',', skiprows=1, usecols=(2,3))
pylab.figure()
pylab.plot(data_encounter1[:,1], data_encounter1[:,0], label='Reward = No Act')
pylab.plot(data_encounter2[:,1], data_encounter2[:,0], label='Reward = Random Act')
pylab.plot(data_encounter3[:,1], data_encounter3[:,0], label='Reward = Single Act')
pylab.plot(data_encounter4[:,1], data_encounter4[:,0], label='Reward = Sticky Act')
pylab.xlabel('Steps', fontsize=20)
pylab.ylabel('Reward', fontsize=20)
pylab.xticks(fontsize=16)
pylab.yticks(fontsize=16)
pylab.legend()
pylab.grid()
pylab.tight_layout()
pylab.savefig('rewards_encounter.png')