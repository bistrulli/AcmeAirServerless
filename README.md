# WasteLess 
This is the replication package tied to the paper "WasteLess: An Optimal Resource Provisioner for Second generation Serverless Applications" submitted to ASE2024 Research Track. WasteLess is implemented in Python and Matlab and depends on several Python packages listed in the `requirements.txt` file.

## Contents of the Package

- Folder `Acmeair_variants` contains all the variants of AcmeAir used for the experimentation
- For each Variant we have a folder for each function and all the script used for deploying and configuring the function Google Cloud Run
- The Workload is specified in the folder `clientEntry` within each variant directory. The file `SimpleWorkload.py` is the locust specification of the workload. In this folder are saved also all the results obtaining by runing the corresponding Acmeair variants uder the three scenarios of the paper, i.e.,no-concurrency, GCR, Wasteless 
- The folder `MPP4LQN` contains the tool to automatically generate a fluidLQN from a python decription of the model
- The folder `results` contains the results of the experimentation. To ease replicability we already included all the results obraining with our experimentations
- The folder `plot` contains the Matlab scripts for generating the plot and the actual paper figures
- The file `extractExpData.py` is the script for preprocessing the data before creating the plots
- The file `runexp.py` contains the code to deploy and tun the experiments on google cloud

## Requirements
The following tools are required to install and run WasteLess:

- `Python 3.9+`
- `pip 21.2.4+`
- `Matlab R2024a+`
- `gcloud`

You can download and install Python from the [Python website](https://www.python.org/).
Matlab instead is a propetary tool that can be downloaded from here [Matlab website](https://www.mathworks.com/products/matlab.html). We just use matlab for genrating plots and a trial version is sufficient. Finally gcloud is the command line utility for interacting with Google Cloud and can be downloaded fom here [Gcloud website](https://cloud.google.com/sdk/docs/install)


## Installation
To install dependencies, run the following command:

```bash
pip install -r requirements.txt
```

This command will automatically download and install all the required packages. Now that you've installed all the dependencies, you're ready to replicate the results. Below, we provide instructions on how to run and use it.

## Experiments Replication

- For reproducing all the paper's plots issue the following commands:

```bash
#To run all the experiments on google cloud run (optional)
python3 runexp.py
#To preoprocess data (optional)
python3 extractExpData.py
#To reproduce the plots
cd plot
#Where matlab is the Matlab executable. Please set this command as an environment variable or specify the full Matlab executable path
matlab  -nodesktop -r "run('plot_overall.m');quit();"





