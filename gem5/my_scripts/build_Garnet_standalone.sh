#!/bin/tcsh
source my_scripts/set_env.cshrc
python `which scons` -j 24 build/Garnet_standalone/gem5.debug
