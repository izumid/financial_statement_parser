import os
from celery import Celery
import json
import requests
from service import api_client

with open(os.path.join(os.getcwd(),"config/config.json")) as jsonfile:
	config_json = json.load(jsonfile)

celery = Celery('tasks', broker= config_json['celery_broker_url'], backend= config_json['celery_result_backend'])

def send_data(url_token,data,user,pasw,grant):
	"""
	Description:
		Send openAI output to another end point.

	Arguments:
		url_token(str): API link that must receice the output of this project;
		data(json): output of this project;
		user(str): user of the end point that must receice the output of this project;
		pasw(str): password of user of the end point that must receice the output of this project; 
		grant(str): type of authentication of end point that must receice the output of this project;
		
	"""

	payload = {"username": user, "password": pasw,"grant_type": grant}

	try:
		response = requests.post(url_token, headers={"Authorization": config_json['header_authorization']}, data=payload)
		token = response.json().get("access_token")
	except Exception as error: 
		return{"error": f"[1.1] Get token: {error}"}
		
	try:
		headers = {"Authorization": f"Bearer{token}" ,"Content-Type": "application/json"}
		requests.post(url=config_json["url_send_data"], headers=headers, json=data)
	except Exception as error:
		return{"error": f"[1.2] Sending .json to end point: {error}"}


@celery.task
def execute_task(id,content):
	"""
	Description:
		Execute task assync to each request made to that API;
		
	Arguments:
		id(str): Id came from another API to this to identify the who requests each document;
		content(list): array with year of each base64 and the base itself e.g [[2020, "sW45sdWQ3F45a"]...];
		
	"""

	try: 
		output = api_client(id,content,config_json)
	except Exception as error:
		return{"error": f"[2.0] Runnning service: {error}"}
	
	send_data(url_token=config_json["header_authorization"],data=output,user=config_json["payload_username"],pasw=config_json["payload_password"],grant=config_json["payload_grant_type"])

	return({"success": f"Completed task!"})