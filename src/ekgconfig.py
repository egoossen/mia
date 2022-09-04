import json

def load(config_file:str='config.json'):
	with open(config_file) as f:
		cfg_data = json.load(f)
	return cfg_data

def save(cfg_data:dict,config_file:str='config.json'):
	with open(config_file, 'w') as f:
		f.write(json.dumps(cfg_data, indent=4))