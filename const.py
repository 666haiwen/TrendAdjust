import os


datasets = ['9nodes', '36nodes']
dataset_id = 0
module_dir = os.path.dirname(__file__)
templatePath = os.path.join(module_dir, 'template', datasets[dataset_id])
runPath = os.path.join(module_dir, 'run')
resPath = os.path.join(module_dir, 'results', datasets[dataset_id])
INTERVAL = 10
