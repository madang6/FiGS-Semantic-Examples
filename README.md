# FiGS-Semantic-Examples

Installation steps

1) Clone the Repo & Update submodules

```
git submodule update --recursive --init
```

2) Install acados

```
# Navigate to acados folder (acados root)
cd <repository-path>/FiGS-Semantic-Examples/FiGS-Semantic/acados/

# Compile
mkdir -p build
cd build
cmake -DACADOS_WITH_QPOASES=ON ..
make install -j4

# Add acados paths to bashrc
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"<acados_root>/lib" 
export ACADOS_SOURCE_DIR="<acados_root>"
# As an example:
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"/home/irward/FiGS-Semantic-Examples/FiGS-Semantic/acados/lib"' >> ~/.bashrc
echo 'export ACADOS_SOURCE_DIR="/home/irward/FiGS-Semantic-Examples/FiGS-Semantic/acados"' >> ~/.bashrc
source ~/.bashrc
# And check that it works
echo $LD_LIBRARY_PATH
echo $ACADOS_SOURCE_DIR
```

3) Setup conda environment (in the main directory)

```
# Navigate to environment config location
cd <repository-path>/FiGS-Semantic-Examples/

# Create and activate
conda env create -f environment_x86.yml
conda activate figs-env

# Some packages will need to be installed separately
pip install torch==2.1.2+cu118 torchvision==0.16.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit -y
pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch

# To remove the environment
conda deactivate
conda env remove -n figs-env
```
