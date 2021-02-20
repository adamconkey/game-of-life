#!/bin/bash

MINICONDA_DIR=$HOME/.miniconda3
INSTALL_SH=install_miniconda.sh


install_conda () {
    # Download and execute Miniconda installation script, creates Miniconda
    # environment in MINICONDA_DIR (variable should be set already).
    if [[ "$OSTYPE" == "darwin"* ]] ; then
        curl -o $INSTALL_SH https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    elif [[ "$OSTYPE" == "linux-gnu"* ]] ; then
        curl -o $INSTALL_SH https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    else
        echo -e "\nUnknown OS for installing conda"
        exit
    fi

    chmod +x $INSTALL_SH
    bash $INSTALL_SH -b -p $MINICONDA_DIR
    rm $INSTALL_SH
    
    source $MINICONDA_DIR/etc/profile.d/conda.sh
    conda init
}


# Try to install conda if it's not installed and user wants it, otherwise exit
CONDA_INSTALLED=false
if ! type "conda" &> /dev/null ; then
    echo -e "\nCould not find 'conda'."
    while true; do
        read -p "Do you wish to install and initialize conda ('yes' or 'no')? " yn
        case $yn in
            [Yy]* ) install_conda; break;;
            [Nn]* ) echo "Cannot continue installation without conda. Exiting."; exit 1;;
            * ) echo "Please answer 'yes' or 'no'.";;
        esac
    done
    CONDA_INSTALLED=true
    source $MINICONDA_DIR/etc/profile.d/conda.sh
else
    source $MINICONDA_DIR/etc/profile.d/conda.sh
    conda deactivate
    conda deactivate
fi


# Create the conda environment with installed dependencies
conda env remove -n gol
conda update -y -n base -c defaults conda
conda env create -f conda_env.yaml
