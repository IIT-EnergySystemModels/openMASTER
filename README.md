**The open-source Model for the Analysis of SusTainable Energy Roadmaps (openMASTER)**
================================

The **openMASTER** model has been developed at the `Instituto de Investigación Tecnológica (IIT) <https://www.iit.comillas.edu/index.php.en>` of the `Universidad Pontificia Comillas <https://www.comillas.edu/en/>`_.

**Developers**
================================

| Member                     | Username  | Tasks             |
| -------------------------- | --------- | ----------------- |
| Antonio F. Rodríguez Matas | [@afrmatas](https://github.com/afrmatas) | Developer         |
| Manuel Pérez Bravo         | [@mperezbravo](https://github.com/mperezbravo)  | Developer         |

##### Table of Contents  
[Description](#Description)  
[Solvers](#Solvers)



Description
================================

**openMASTER** is a Pyomo-based model designed for sustainable energy policy analysis. It operates as a dynamic, bottom-up, partial equilibrium, linear programming (LP) model, with the primary objective of meeting externally-given energy services demand across various sectors. It achieves this by adhering to technical and policy constraints while minimizing a comprehensive objective function. This function encompasses the total economic costs of energy supply, the social costs associated with greenhouse gas emissions and pollutant releases, as well as to intangible costs such as discomfort.

It is structured according to a scheme of processes and flows, which encompasses the entire energy sector, including the import and domestic consumption of primary energy, energy conversion and storage technologies for final energy production, energy services supply technologies, and the exogenous demand for energy services from various sectors of the economy.

It determines optimal roadmaps that satisfy simultaneously several attributes. Its main contributions are:

- **Dynamic planning**: the scope of the model corresponds to several periods (years) at a long-term horizon, 2030 to 2050 for example.

- **Technological granularity**: the model considers the vintage of end-use technologies. This approach facilitates the representation of technological innovation, including learning curves for efficiency improvements and emissions reductions. Consequently, improvements in vehicle emission standards or household appliances efficiency, among others, can be incorporated along with a detailed definition of technology decommissioning over their lifecycle.  

- **Exogenous demand of energy services**: the model introduces all exogenous demand in the form of energy services, allowing for the implementation of energy efficiency measures and emissions reduction through the investment and operation of end-use technologies. In this regard, it also enables modal shifts in transportation, a crucial aspect for effective decarbonization of this sector.

- **Endogenous behavioural changes**: the model introduces behavioural changes in an endogenous and linear manner. This approach allows the model to determine optimal agent behaviour considering intangible costs such as discomfort, as well as to assess trade-offs, as occurs in the case of remote work, where mobility demand is reduced at the cost of an increase in domestic energy consumption.

- **Non-energy raw material consumption and circular economy in the industrial sector**: the industrial sector is also represented, like all other sectors, on the basis of the demand for energy services (in this case, production of tons of materials). This not only facilitates modelling the reduction in material consumption through recycling but also energy and emissions savings through less energy-intensive processes.

The **objective function**, which represents the costs of the energy sector, includes:
(i)    the domestic consumption and import of primary energy (PE); 
(ii)   fixed and variable O&M costs of conversion technologies (CE); 
(iii)  the cost of raw materials (RM) consumed by industrial supply technologies (ST); 
(iv)   fixed and variable O&M costs of supply technologies (ST); 
(v)    the investment cost of new conversion technology capacity (CE); 
(vi)   the cost of reactivating hibernated capacity of conversion technologies (CE); 
(vii)  the investment cost of new supply technology capacity (ST); 
(viii) the penalty cost of slack variables, which include unsupplied energy services (ESNS), as well as exceeding emission caps and carbon budget constraints; 
(ix)   the cost of agents’ behavioural measures, including both economic costs (such as housing insulation) and intangible costs (such as discomfort).

The model formulates an optimization problem including investment (installation/decommission capacity), operation (generation and storage) and behavioural decisions. The model considers electricity generation reliability constraints, technological and modal choice constraints, and emission caps and carbon budget constraints.

The main results of the model can be structured in these topics:

- **Investment**: installation and decommission decisions on capacity for Conversion Energy Technologies (CE) and Supply Technologies (ST); hibernation and reactivation decisions on capacity for Conversion Energy Technologies (CE)
- **Operation**: primary energy consumption (imports and domestic consumption), final energy generation and storage, energy services supplied, ESNS, etc.
- **Emissions**: CO2 and pollutants (NOx, SOx and PM 2.5) emissions
- **Behavioural changes**: change in energy services demand due to agents' behavioural changes
- **Economic**: investment, operation and behavoiural changes costs

Results are shown in csv files and graphical plots. An interactive Dashboard is available, as well as a Sankey Diagram generator tool.

A careful implementation has been done to avoid numerical problems by scaling parameters, variables and equations of the optimization problem allowing the model to be used for large-scale cases.

Solvers
================================

**GLPK**
As an easy option for installation, we have the free and open-source [GLPK solver](https://www.gnu.org/software/glpk/). However, it takes too much time for large-scale problems. It can be installed using: ``conda install -c conda-forge glpk``.

**CBC**
The [CBC solver](https://github.com/coin-or/Cbc) is our recommendation if you want a free and open-source solver. For Windows users, the effective way to install the CBC solver is downloading the binaries from [this link](https://www.coin-or.org/download/binary/Cbc/Cbc-2.10.5-x86_64-w64-mingw32.zip), copy and paste the *cbc.exe* file to the PATH that is the "bin" directory of the Anaconda or Miniconda environment. It can be installed using: ``conda install -c conda-forge coincbc``.

**Gurobi**
Another recommendation is the use of [Gurobi solver](https://www.gurobi.com/). However, it is commercial solver but most powerful than GPLK and CBC for large-scale problems.
As a commercial solver it needs a license that is free of charge for academic usage by signing up in [Gurobi webpage](https://pages.gurobi.com/registration/).
It can be installed using: ``conda install -c gurobi gurobi`` and then ask for an academic or commercial license. Activate the license in your computer using the ``grbgetkey`` command (you need to be in the university domain if you are installing an academic license).

**Mosek**
Another alternative is the [Mosek solver](https://www.mosek.com/). Note that it is a commercial solver and you need a license for it. Mosek is a good alternative to deal with QPs, SOCPs, and SDPs problems. You only need to use ``conda install -c mosek mosek`` for installation and request a license (academic or commercial).
To request the academic one, you can request [here](https://www.mosek.com/products/academic-licenses/). Moreover, Mosek brings a [license guide](https://docs.mosek.com/9.2/licensing/index.html). But if you are request an academic license, you will receive the license by email, and you only need to locate it in the following path ``C:\Users\(your user)\mosek`` in your computer.

Installation
================================
openMASTER can be installed from its Github repository following these steps:
1. Clone the openMASTER repository, which includes the folder structure and all necessary functions to run the model.
2. Launch the command prompt (Windows: Win+R, type "cmd", Enter).
3. Set up the path to where the repository was cloned, using cd "C:\Users\<username>\...\openMASTER".
4. Install openMASTER via pip by ``pip install .`` (the openMASTER package is contained in this repository, locally). Please note that the openMASTER package has optional dependencies for the graphic tools included to visualize results. To install these optional dependencies, it can also be done via pip by ``pip install .[graphicTool]``
5. Be aware the openMASTER_Data.xlsx file has to be downloaded using [git-lfs](https://git-lfs.com/) or this [link](https://github.com/IIT-EnergySystemModels/openMASTER/raw/main/data/input/openMASTER_Data.xlsx?download=).

Get started
================================
By cloning the openMASTER repository, you can create branches and propose pull-request. Any help will be very appreciated. We suggest the use of [Gurobi](https://www.gurobi.com/academia/academic-program-and-licenses/) (for Academics and Researchers) as a solver to deal with LP problems instead of GLPK.

The openMASTER repository provides a quickstart guide (in the form of a jupyter notebook) for a new user to run their first case with the model. This quickstart guide is under the /notebooks, named `quickstart_openMASTER.ipnyb <https://github.com/IIT-EnergySystemModels/openMASTER/blob/main/notebooks/quickstart_openMASTER.ipynb>`. Before running the cells in this notebook, it is advisable to:
1. Create and activate a virtual environment in the system command prompt on which the dependencies will be installed. To do so, please follow the instructions detailed in the `Python Documentation <https://docs.python.org/3/library/venv.html>`. This virtual python environment will not affect the python version or packages installed in the machine being used, and will avoid incompatibilities between versions of packages being used in openMASTER.
2. Install the openMASTER packages following the `instructions hereby detailed <#How to install>`.
3. Please follow the order of cells in this notebook to create the abstract model, load a DataPortal, solve the instance, and save the model results.

## Scenarios management

The user can create scenarios using the functionality provided by openMASTER. A scenario is defined in openMASTER as a set of inputs which will create a specific output. To help the user keep track of different runs of the model, this functionality creates a new folder within the /scenarios folder in the local clone of the repository. This folder contains a copy of the code used to run the scenario, as well as all the inputs and outputs for future use and development.
To use this functionality of the model, please follow the notebook `scenarios_from_results.ipynb <https://github.com/IIT-EnergySystemModels/openMASTER/blob/main/notebooks/scenarios_from_results.ipynb>`.

## Visualization of results

openMASTER also provides the user with visualization tools for the results obtained with the model, among which:

   * Visualization of results in a Dashboard: openMASTER facilitates the visualization of the main results by means of a dashboard in which several charts are presented. In this dashboard tool, the user can interact with the results by selecting different scenarios, zooming into the timeframes of interest, etc. The data for these charts are imported from the scenarios created by the user, for that reason it is important to first create a result scenario after each run (see above). The steps to follow are:
           1. Run the model and create a scenario (see <## Scenarios managment>) after every run.
           2. Run the ``index.py`` file within the folder `\Dashboard\app <https://github.com/IIT-EnergySystemModels/openMASTER/tree/main/Dashboard/app>`.
           3. A local server will be raised, and its localhost address will be shown on the command prompt window. Please follow this address on your explorer to visualize these results dashboard.
   * Creation of charts from templates: Within the `\Charts folder <https://github.com/IIT-EnergySystemModels/openMASTER/tree/main/Charts>`, the user will find python functions to create basic charts (pie, bar, and area charts), as well as Sankey diagrams of energy flows resulting from the model. Although the functions to create these charts are available in separate python files, two jupyter notebooks are also provided to facilitate their use. The notebook `scenario_charts.ipnynb <https://github.com/IIT-EnergySystemModels/openMASTER/blob/main/Charts/scenario_charts.ipynb>` guides the creation of the more basic charts from different variables within the model, such as pie charts of primary energy use, bar charts of renewable power installed, etc. On the other hand, the notebook `scenario_sankey.ipynb <https://github.com/IIT-EnergySystemModels/openMASTER/blob/main/Charts/scenario_sankey.ipynb>` guides the creation of Sankey diagrams, which imply the intermediate step of creating nodes and flows in a .json file.
