#variable
data=$(date +'%Y-%m-%dT%H:%M:%S')

#path
path='C:/Users/edils/repos/customer_fidelity'
path_to_envs='C:/users/edils/anaconda3/envs/customer_fidelity/lib/site-packages'

$path_to_envs/papermill $path/src/models/v15_customer_fidelity_program_deploy_clean.ipynb $path/reports/v15_customer_fidelity_program_deploy_clean_$data.ipynb