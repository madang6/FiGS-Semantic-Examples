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
```
3) Setup conda environment (in the main directory)
```
# Navigate to environment config location
cd <repository-path>/FiGS-Semantic-Examples/

# Create and activate
conda env create -f environment_x86.yml
conda activate figs-env
