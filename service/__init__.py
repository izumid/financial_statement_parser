import os

from openai import OpenAI
import time
from datetime import datetime

import json

import sys
sys.path.append(os.getcwd())
import model


def debug_code(message,var=None,debug=False):
	"""
	Description:
		Print messages across the process to verify data behaviour.

	Args:
		message(str): text to identify the code process the message are about;
		var(any): variable values to validade;
		debug(bool): true print's the messages;
	"""

	if debug is True:
		if not var is None: print(f"[Debug] {message}: {var}")
		else: print(f"[Debug] {message}")


# MARK: Customize Output
def custom_structure(id,key_name,result_set):
	"""
	Description:
		If you need, there is a friendly output structure to java systems.

	Args:
		id(str): extends to systems that uses hash codes instead of numeric codes;
		open_ai_output(dict): result from openAI parsing the document based of previously formated response;
	"""

	final_dictionary = {}
	final_dictionary[key_name["k1"]] = id
	file = []

	for output in result_set:
		data = {}

		for year, category in output[1].items():
			aux = {}

			for item, info in category.items():
				sub_lst = []

				for k,v in info.items():
					sub_lst.append({key_name["k10"]: k, key_name["k11"]: v})
			
				aux[item] = sub_lst
			data[key_name["k5"]] = year
			data[key_name["k6"]] = aux
			
		file.append({key_name["k3"]: output[0], key_name["k4"]: data})
	final_dictionary[key_name["k2"]] = file

	return(final_dictionary)


# MARK: openIA Request 
def open_ia_request(base64,token,response_structure,filename,gpt_version,wait_time,debug):
	"""
	Description:
		Send the bs64 file to openIA API and request the parsed data based on model structure.

	Args:
		base64(list[[float, str]...]): [0] is the document's year, [1] is the base code;
		token(str): token access to openAI requests;
		response_structure(str): json structure to insure correct data format when requesting parsing from openIA API;
		filename(str): name of file send as information in request body;
		gpt_version(str): used different versions to control the requests costs/quality of receveid data;
		wait_time(int): seconds to wait between request openAI API has token time limits between requests;
		debug(bool): print informations of key code parts to check data behaviour;
	"""

	result_set = []
	path_result = os.path.join(os.getcwd(),"__result")
	client = OpenAI(api_key=token)
	with open(response_structure, 'r') as jfile:  rf_schema =  json.load(jfile)

	i = 0
	for array in base64:
		debug_code(f"GPT's read bs64 [[{array[0]}],[{array[1][:20]}...]] request", i, debug)
		api_start = time.time()

		msg = [
			{"role": "system", "content": "Você é um especialista em contabilidade. Você é capaz de localizar as categorias listadas abaixo. Após a extração, você deve devolver os dados no formato JSON"},
			{"role": "user", "content": [
					{"type": "file", "file":  {"filename": f"{filename}", "file_data": f"data:application/pdf;base64,{array[1]}",}	},
					{"type": "text", "text": "Comece analisando duas vezes o documento inteiro. Procure pelas demonstrações contábeis sintetizadas referente os anos da estrutura json fornecida. Utilize a estrutura fornecida para todos os anos presentes no documento"},
				]
			},
		]

		open_ai_output = client.chat.completions.create(
			model = gpt_version,
			messages=msg,
			response_format={
				"type": "json_schema",
				"json_schema": {
					"name": "gpt_parser",
					"schema": rf_schema,
					"strict": False,
				}
			}
		)

		result = json.loads(open_ai_output.choices[0].message.content)
	
		debug_code(message=f"request duration (sec): {(time.time() - api_start)}", debug=debug)
		time.sleep(wait_time)

		debug_code(message=f"request duration (sec): {(time.time() - api_start)}", debug=debug)
		result_set.append((array[0],result))
		i += 1

	if debug:
		path_response_result = os.path.join(path_result,"open_ai_output.json")
		if os.path.exists(path_response_result):  os.remove(path_response_result)	
		with open(path_response_result, "w") as jsf: json.dump(result_set, jsf, indent=4)
		
	return(result_set)

# MARK: Response Format
def request_format(main_key,property,response_structure):
	"""
	Function to format the send structure to openIA. Due to tests, a solid structure implies in less token in addition to an more accurate responses.
	
	Args: 
		main_key(list);
		property(dict): {name_key: model.object};
		response_strucutre(path): path to save de structure;

	"""
	
	dct = {
		"title": "Beta"
		,"type": "object"
		,"additionalProperties": bool(0)
		,"properties": {}
		,"required": main_key
	}

	for x in main_key:
		dct["properties"][x] = {
			"title": x
			,"type": "object"
			,"additionalProperties": bool(0)
			,"properties": property
			,"required": list(property.keys())
		}

	if os.path.exists(response_structure): os.remove(response_structure)
	time.sleep(5)
	with open(response_structure, "w") as f: json.dump(dct, f, indent=4)


# MARK: openIA Request
def api_client(id,base64,config_json,online=True):
	"""
	Description:
		Send the bs64 file to openIA API and request the parsed data based on model structure.

	Args:
		id(str): extends to systems that uses hash codes instead of numeric codes;
		base64(list[[float, str]...]): [0] is the document's year, [1] is the base code;
		online(bool): Used to controll if will be request data to openAI or a previously saved one;
	"""

	response_structure = os.path.join(os.getcwd(),"config/response_format.json")
	year = int(datetime.now().year)
	main_key = [str(i) for i in range(year-3,year+1,1)]
	debug = config_json["debug"]
	path_result = os.path.join(os.getcwd(),"__result")	
	cof = config_json["custom_output_format"]
	property = {
		cof["k7"]: model.Asset.model_json_schema()
		,cof["k8"]: model.Liabilities.model_json_schema()
		,cof["k9"]: model.IncomeStatement.model_json_schema()
	}

	
	start = time.time()

	if not os.path.exists(response_structure) or config_json["response_format"]:
		request_format(main_key=main_key,property=property,response_structure=response_structure)
	else:
		with open(response_structure, 'r') as jfile: rf_schema =  json.load(jfile)
		
		if int(list(rf_schema["properties"].keys())[-1]) < year:
			request_format(main_key=main_key,property=property,response_structure=response_structure)

	if online:
		result_set = open_ia_request(
			 base64 = base64
			,token = config_json["token"]
			,response_structure = response_structure
			,filename = config_json["filename"]
			,gpt_version = config_json["gpt_version"]
			,wait_time = config_json["sec_wait_between_request"]
			,debug = debug
		)
	else:
		with open(os.path.join(path_result,"open_ai_output.json")) as jsf: result_set = json.load(jsf)
	
	final_dictionary = custom_structure(id=id,key_name=config_json["custom_output_format"],result_set=result_set)
	with open(os.path.join(path_result,"result.json"), "w") as f: json.dump(final_dictionary, f, indent=4)
	debug_code(message=f"Total Request duration (sec): {(time.time() - start)}",debug=debug)

	return(final_dictionary)