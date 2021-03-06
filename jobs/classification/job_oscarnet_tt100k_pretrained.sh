#!/usr/bin/env bash
#SBATCH --job-name oscarnet_tt100k_pretrained
#SBATCH --ntasks 4
#SBATCH --mem 16G
#SBATCH --qos masterhigh
#SBATCH --partition mhigh
#SBATCH --gres gpu:1
#SBATCH --chdir /home/grupo06/m5-project
#SBATCH --output ../logs/%x_%u_%j.out

source /home/grupo06/venv/bin/activate
python src/main.py --exp_name oscarnet_tt100k_pretrained_${SLURM_JOB_ID} --config_file config/oscarnet_tt100k_pretrained.yml