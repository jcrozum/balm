# \[ARTEFACT\] Positive and negative feedback loops enable fast state space mapping and control

This folder contains all the data and code necessary for the reproduction of 
the results discussed in the *Positive and negative feedback loops enable 
fast state space mapping and control* paper. By following the instructions
in this document, you should obtain the figures and tables as presented in
the paper.

 > Note that some of the claims are connected to the method's runtime. As such, 
 these results vary depending on the used hardware.

 > The performance testing was performed on a desktop computer with a 
 Ryzen 5800X CPU fixed to 4.7Ghz (no turbo/OC) and 128GiB of DDR4-3200 
 RAM. All tested software only uses a single CPU core, Furthermore, 
 individual experiments are limited to 64GiB of memory. However, most of the benchmarks can be completed with substantially less memory
 (e.g. 8-16GB).

 > The presented results were measured using Python 3.11 and Debian 12.
 Experiments are running sequentially (each experiment has 
 uncontested access to all resources). In theory, the tested software 
 should also run on macOS and Windows, but we don't provide specific 
 instructions for these.

## Artefact structure

 - [TODO] `env.zip` | A pre-built Python virtual environment with relevant dependencies installed.
 - [TODO] `env_*.sh` | Scripts for creating/testing/destroying the Python virtual environment.
 - [TODO] `models.zip` | An archive with all test input models.
 - [TODO] `results.zip` | An expected output for all experiments.
 - [TODO] `bench/*.py` | Python scripts for running individual benchmarks.

TODO:
 - Migrate to latest aeon.py, also building aeon from source is not set up correctly.

## Environment setup

Almost all relevant software is provided through a single Python virtual 
environment. It is recommended you recreate the environment from scratch
using the process described below. However, in case of issues 
(e.g. a dependency is no longer available online), the exact environment 
used in our testing is also provided as `env.zip`.

 > If you use the provided environment, keep in mind that the 
 `./env/bin/activate` script will not work, as this script is machine specific. 
 However, all dependecies are installed in `./env/lib/python3.11/site-packages` and can be reused when creating a [new environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

To recreate the testing environment from scratch, run the following commands:

```bash
# Ensure that python3 is installed with dev dependencies.
sudo apt-get -y install python3 python3-venv python3-dev

# Ensure that gringo/clingo is available.
sudo apt-get -y install gringo

# Install pint.
sudo apt install ./dependencies/pint_2019-05-24_amd64.deb

# Install mole. 
(cd ./dependencies && tar -xvf mole-140428.tar.gz)
(cd ./dependencies/mole-140428 && make)
# This updates your PATH variable so that mole is available.
# You need to run this command in every other terminal session
# where you plan to work with this artefact.
export PATH=$PATH:`pwd`/dependencies/mole-140428

# Create the virtual environment and install Python dependencies.
# Also unpacks all testing data.
./env_setup.sh

# Check that all software is installed and usable.
./env_check.sh

# If for whatever reason you wish to destroy the current
# environment and start over, you can use this script:
./env_cleanup.sh
```

For the most relevant software (i.e. `nfvsmotifs`, `biodivine_aeon` and 
`mtsNFVS`), we also provide source code. However, this does not cover 
transitive dependencies. Furthermore, `biodivine_aeon` is by default
not compiled from source, as it can take more than 30 minutes on slower
machines. However, `./env_setup.sh` contains an alternative command with 
which `biodivine_aeon` can be installed from source if desired.

TODO: Add mtsNFVS installation.

## Running individual experiments

Each experiment is executed by running a Python script from the `bench` folder. Each `*.py` script should provide exact instructions regarding what is tested, what are the inputs and what is presented as the result.

Typically, each script is designed to output a single tab-separated list
of values, such that the output of multiple scripts can be concatenated to
create a single table. When measuring runtime, this is performed directly by the benchmark script using the Python `time.performance_counter()` method.

For example, to compute attractors using AEON.py, you can run:

```bash
python3 ./bench/attr-aeon.py ./models/bbm-bnet-inputs-random-128/005.bnet
# Expected output: 005.bnet  23740 1
```