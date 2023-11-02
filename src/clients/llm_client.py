import requests
import string
import os
import tomllib
from importlib.resources import files
import logging

log = logging.getLogger(__name__)


toml_str = files('src.clients.templates').joinpath('prompt_templates.toml').read_text()
config = tomllib.loads(toml_str)
template_str = config['palm']['template']['prompt_template']

PROMPT_TEMPLATE = string.Template(template_str)

PALM_API_KEY = os.environ["PALM_API_KEY"]

class LLMClient:
    URL = "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText" 
    
    def __init__(self):
        pass

    def get_llm_advice(self, problem_description_short: str, code: str, reference_code: str):
        prompt = PROMPT_TEMPLATE.safe_substitute({
            'PROBLEM': problem_description_short,
            'CODE' : code,
            'REF': reference_code
        })

        payload = {
            "prompt": {
                "text": prompt
                },
            "temperature": 0.5,
            "candidate_count": 1
        }

        headers = {
            'Content-Type': 'application/json'
        }

        params = {
            'key': PALM_API_KEY  
        }

        log.info('sending request to %s with payload %s', self.URL, payload)
        response = requests.post(self.URL, json=payload, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f'received non 200 response code from client, payload={payload}')
        return response.json()['candidates'][0]['output']

