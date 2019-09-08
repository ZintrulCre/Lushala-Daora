#!/bin/bash
#SBATCH --partition=cloud
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=8

module load Python/3.4.3-goolf-2015a

mpiexec python MultiNode.py