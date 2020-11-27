import subprocess
import io
import numpy
import os

topology = 'HierarchicalRing'
synthetic = ["transpose","shuffle","neighbor"]
passw = 'root_passw'
step =0.02
routing = 'XY'
packrec = u'packets_received'
avpack = u'average_packet_latency'
avhop = u'average_hops'
packinj = u'packets_injected'
numCpus = [9,16,25,36,49,64]
numDirs = [16,16,32,64,64,64]
numRows = [3,4,5,6,7,8]
nameCirc9 = ["9,1,2","9,1,3","9,1,4"] 
nameCirc16 = ["16,1,6"]
nameCirc25 = ["25,1,7"]
nameCirc36 = ["36,1,8","36,1,10"]
nameCirc49 = ["49,1,9", "49,1,11"]
nameCirc64 = ["64,1,14"]
nameCirc = [nameCirc9, nameCirc16, nameCirc25, nameCirc36, nameCirc49, nameCirc64]
for synt in synthetic:
    for b in range(0,6):
        for el in nameCirc[b]:
            f = open("{}C({}){}{}.csv".format('output',el,synt,numCpus[b]),'w')
            f.close()
            with open("circ_route/C({}).txt".format(el), 'r') as myfile:
                data = myfile.read().replace("\n","")
            for i in numpy.arange(0.02,1.02,step):
                pack_arr = ""    
                aver_laten = ""
                execute = './build/Garnet_standalone/gem5.opt configs/example/garnet_synth_traffic.py --network=garnet2.0 --num-cpus={1} --num-dirs={2} --topology=Circulant --sim-cycles=10000 --inj-vnet=0 --injectionrate={0} --synthetic={4} --routing-algorithm=custom --circ-obr={6} --routing-table=\"{5}\"'.format(i,numCpus[b],numDirs[b],numRows[b],synt,data, el[el.find(",")+1:])
                subprocess.call(execute,shell=True)
                subprocess.call('echo {} | sudo -S {}'.format(passw,'sh ./my_scripts/extract_network_stats.sh'), shell=True)
                with io.open('network_stats.txt', encoding='utf-8') as file:
                    for line in file:
                        if packinj in line:
                            numravn = line.find('=')
                            for j in range(numravn+2,len(line)):
                                if line[j] == ' ':
                                    packinjval = line[numravn+2:j]
                                    break;
                        if packrec in line:
                            numravn = line.find('=')
                            for j in range(numravn+2,len(line)):
                                if line[j] == ' ':
                                    pack_arr = line[numravn+2:j]
                                    break;
                        if avpack in line:               
                            numravn = line.find('=')
                            for j in range(numravn+2,len(line)):
                                if line[j] == ' ':
                                    aver_laten = line[numravn+2:j]
                                    break;
                        if avhop in line:
                            numravn = line.find('=')
                            for j in range(numravn+2,len(line)):
                                if line[j] == ' ':
                                    hop_arr = line[numravn+2:j]
                                    break; 
                if aver_laten != "":        
                    f = open("{}C({}){}{}.csv".format('output',el,synt,numCpus[b]),'a')
                    f.write(pack_arr + ';');
                    f.write(aver_laten + ';');
                    f.write(hop_arr + ';');
                    f.write(packinjval + '\n');
                else:
                    break;
        val = 0.02


