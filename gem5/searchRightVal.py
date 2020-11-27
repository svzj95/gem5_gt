import numpy
import subprocess

for i in numpy.arange(196,300,4):
    flag = False
    subprocess.call('./build/Garnet_standalone/gem5.opt configs/example/garnet_synth_traffic.py --network=garnet2.0 --num-cpus=81 --num-dirs={0} --topology=MeshMy --mesh-rows=9 --sim-cycles=10000 --inj-vnet=0 --injectionrate=0.02 --synthetic=uniform_random > output.log'.format(i),shell=True)
    with open('output.log', 'r') as file:
        data = file.read();
        numExit = data.find("Exit");
        if numExit != -1:
            break;
