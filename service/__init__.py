import os
import base64

from openai import OpenAI
import time
from datetime import datetime

from pathlib import Path
import json

import sys
sys.path.append(os.getcwd())
import model

# MARK: Response Format
def response_format(main_key,property,response_structure):
	"""
	Function to format the send structure to openIA. Due to tests, a solid structure implies in less token in addition to an more accurate responses.
	
	Args: 
		main_key(list);
		property(dict): {name_key: model.object};
		response_strucutre(path): path to save de structure;

	"""
	name_key = property.keys()


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
			,"properties":{
				 name_key[0]: property[name_key[0]]
				,name_key[1]: property[name_key[1]]
				,name_key[2]: property[name_key[2]]
			}
			,"required": name_key
		}

	if os.path.exists(response_structure): os.remove(response_structure)
	time.sleep(3)
	with open(response_structure, "w") as f: json.dump(dct, f, indent=4)


def debug_code(message,var=None,debug=False):
	"""
	Description:
		Print messages across the process to verify data behaviour.

	Args:
		message(str): text to identify the code process the message are about;
		var(any): variable values to validade;
		debug(bool): true print's the messages
	"""


	if debug is True:
		if not var is None: print(f"[Debug] {message}: {var}")
		else: print(f"[Debug] {message}")


# MARK: Customize Output
def custom_structure(id, open_ai_output):
	"""
	Description:
		If you need, there is a friendly output structure to java systems.

	Args:
		id(str): extends to systems that uses hash codes instead of numeric codes;
		open_ai_output(dict): result from openAI parsing the document based of previously formated response;
	"""

	final_dictionary = {}
	final_dictionary["idBalanco"] = id

	years = []
	for output in open_ai_output:
		for year, category in output.items():
			aux = {}
			for item, info in category.items():
				sub_lst = []
				for k,v in info.items():
					sub_lst.append({"descricao": k, "valor": v})
			
				aux[item] = sub_lst
			years.append({"ano": year, "valores": aux})
			
		final_dictionary["anos"] = years

	return(final_dictionary)


# MARK: openIA Request 
def open_ia_request(base64,filename,token,gpt_version,wait_time,response_format,debug):
	"""
	Description:
		Send the bs64 file to openIA API and request the parsed data based on model structure.

	Args:
		base64(list[[float, str]...]): [0] is the document's year, [1] is the base code;
		filename(str): name of file send as information in request body;
		token(str): token access to openAI requests;
		gpt_version(str): used different versions to control the requests costs/quality of receveid data;
		waitime(int): seconds to wait between request openAI API has token time limits between requests;
		response_format(json): json structure to insure correct data format when requesting parsing from openIA API;
		debug(bool): print informations of key code parts to check data behaviour;
	"""

	open_ai_output = []
	i = 0
	for array in base64:
		debug_code(f"GPT's read bs64 [[{array[0]}],[{array[1][:20]}...]] request", i, debug)

		api_start = time.time()

		#result = request(token=token,filename=filename,gpt_version=gpt_version,base64_string=array[1],response_format=response_format,debug=debug)
		
	 	## AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
		path_result = os.path.join(os.getcwd(),"__result")
		path_response_structure = os.path.join(os.getcwd(),"config/response_format.json")
		client = OpenAI(api_key=token)
		year = int(datetime.now().year)
		required_year = [str(i) for i in range(year-3,year+1,1)]
		ativo = model.Ativo.model_json_schema()
		passivo = model.Passivo.model_json_schema()
		demonstracao = model.DemonstracaoResultadoExercicio.model_json_schema()

		msg = [
			{"role": "system", "content": "Você é um especialista em contabilidade. Você é capaz de localizar as categorias listadas abaixo. Após a extração, você deve devolver os dados no formato JSON"},
			{"role": "user", "content": [
					{"type": "file", "file":  {"filename": f"{filename}", "file_data": f"data:application/pdf;base64,{array[1]}",}	},
					{"type": "text", "text": "Comece analisando duas vezes o documento inteiro. Procure pelas demonstrações contábeis sintetizadas referente os anos da estrutura json fornecida. Utilize a estrutura fornecida para todos os anos presentes no documento"},
				]
			},
		]

		if not os.path.exists(path_response_structure):
			response_format(required_year,ativo,passivo,demonstracao,path_response_structure)
		else:
			with open(path_response_structure, 'r') as jfile: rf_schema =  json.load(jfile)
			
			if int(list(rf_schema["properties"].keys())[-1]) < year:
				response_format(required_year,ativo,passivo,demonstracao,path_response_structure)

		with open(path_response_structure, 'r') as jfile:  rf_schema =  json.load(jfile)

		openAi_result = client.chat.completions.create(
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

		result = json.loads(openAi_result.choices[0].message.content)

		if debug:
			path_response_result = os.path.join(path_result,"openAi_result.json")
			if os.path.exists(path_response_result):  os.remove(path_response_result)	
			with open(path_response_result, "w") as jsf: json.dump(result, jsf, indent=4)

	
		## BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB	

		debug_code(message=f"request duration (sec): {(time.time() - api_start)}", debug=debug)
		time.sleep(wait_time)

		debug_code(message=f"request duration (sec): {(time.time() - api_start)}", debug=debug)
		open_ai_output.append(result)
		
		i += 1

		if debug:
			with open(os.path.join(path_result,"open_ai_output.json"), "w") as f: json.dump(open_ai_output, f, indent=4)

	return(open_ai_output)

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

	path_result = os.path.join(os.getcwd(),"__result")	
	debug = config_json["debug"]
	start = time.time()

	if online:
		open_ai_output = open_ia_request(
			 base64 = base64
			,filename = config_json["filename"]
			,token = config_json["token"]
			,gpt_version = config_json["gpt_version"]
			,wait_time = config_json["sec_wait_between_request"]
			,response_format = config_json["response_format"]
			,debug = debug
		)
	else:
		with open(os.path.join(path_result,"open_ai_output.json")) as jsf: open_ai_output = json.load(jsf)
	
	final_dictionary = custom_structure(id, open_ai_output)
	with open(os.path.join(path_result,"result.json"), "w") as f: json.dump(final_dictionary, f, indent=4)
	debug_code(message=f"Total Request duration (sec): {(time.time() - start)}",debug=debug)

	return(final_dictionary)


# MARK: Generate bs64
def pdf_to_bs64(path_file,path_destination,filename,delimiter=",",multi_bs64=True):
	"""
	Description:

	Argument:
		path_file(path): path to pdf file for converting;
		path_destination(path): destination path of converted pdf (base64 code);
		filename(str): name of pdf file;
		delimiter(char): char to separated the text informations;
		multi_bs64(bool): generate a mult array file or a single;
	"""	

	extension = ".json"
	list_base64 = []

	for pdf_file in os.listdir(path_file):
		filename_pdf = Path(pdf_file).suffix
		
		if filename_pdf == ".pdf":
			with open(os.path.join(path_file,pdf_file), "rb") as f: data = f.read()
			bs64 = base64.b64encode(data).decode("utf-8-sig")

			if multi_bs64 == False:
				abs_path_destination = os.path.join(path_destination,Path(pdf_file).stem+extension)
				if os.path.isfile(abs_path_destination): os.remove(abs_path_destination)
				time.sleep(3)
				
				with open(abs_path_destination, "w") as f: f.write(str([[2020+1/10,bs64]]).replace("'",'"'))
			else: list_base64.append(bs64)


	list_size = len(list_base64)-1
	if multi_bs64 ==  True:
		filename = filename + extension
		abs_path_destination = os.path.join(path_destination,filename)

		if os.path.isfile(abs_path_destination): os.remove(abs_path_destination)
		time.sleep(3)

	
		with open(abs_path_destination, "w") as f: f.write("[")
		for i in range(len(list_base64)):
			if len(list_base64) == 1:
				with open(abs_path_destination, "a") as f: f.write(str([2020+i/10,list_base64[i]]).replace("'",'"'))
			else:
				if i < list_size: 
					with open(abs_path_destination, "a") as f: f.write(str([2020+i/10,list_base64[i]]).replace("'",'"')+delimiter)
				else: 
					with open(abs_path_destination, "a") as f: f.write(str([2020+i/10,list_base64[i]]).replace("'",'"'))
		with open(abs_path_destination, "a") as f: f.write("]")


# MARK: Read bs64 Text File
def debug_process(genbase,online,id):
	"""
	Debug process locally, isolating the error in input data or waited output by another api.

	Args:
		gebnase(bool): Used to generate the base64 file, based on structure: [[year, basecode]];
		online(bool): Used to controll if will be request data to openAI or a previously saved one;
		id(str): Id came from another API to this to identify the who requests each document;
	"""

	path_result = os.path.join(os.getcwd(),"__result")
	if not os.path.exists:  os.makedirs(path_result)
	#filename = "BALANCETE 2T2024_assinado.json"
	filename = "DRE 2T2024_assinado.json"
	#filename = "BP_2022.json"

	with open(os.path.join(os.getcwd(),"config/config.json")) as jsonfile: config_json = json.load(jsonfile)
	with open(os.path.join(os.getcwd(),r"_file_test",filename), 'r', encoding='utf-8') as file: base64 = json.load(file)

	if genbase:
		pdf_to_bs64(path_file=os.path.join(os.getcwd(),"_file_test/01_baby/text_flow"),path_destination=os.path.join(os.getcwd(),"_file_test"),filename="bs64",delimiter=",",multi_bs64=False)
		pdf_to_bs64(path_file=os.path.join(os.getcwd(),"_file_test/01_baby/table"),path_destination=os.path.join(os.getcwd(),"_file_test"),filename="bs64",delimiter=",",multi_bs64=False)
		pdf_to_bs64(path_file=os.path.join(os.getcwd(),"_file_test/03_caveman/text_flow"),path_destination=os.path.join(os.getcwd(),"_file_test"),filename="bs64",delimiter=",",multi_bs64=False)

	result = api_client(id=id,base64=base64,config_json=config_json,online=online)

	with open(os.path.join(path_result,"result.json"), "w") as f: json.dump(result, f, indent=4)

debug_process(genbase=False,online=True,id="762")