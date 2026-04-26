import logging as lg

from platformdirs import user_cache_path
from requests.exceptions import ConnectionError, HTTPError, Timeout
from requests_toolbelt.sessions import BaseUrlSession

from egiti.core.exceptions import TemplateNotFoundError


class TemplatesManager:
    def __init__(self):
        self.logger = lg.getLogger('egiti.templates')
        self.cache_path = user_cache_path(appname='egiti')

        self.session = BaseUrlSession(base_url="https://api.github.com")
        self.session.headers.update({
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2026-03-10'
        })

        self.session.timeout = 3

        self.request_attempts = 3
        self.request_attempt_delay = 1
    

    def get_templates_list(self) -> list[str]:
        templates_list = self._get_endpoint('/gitignore/templates')
        if not isinstance(templates_list, list):
            raise TypeError(
                f"Templates list is not list! (type={type(templates_list)})"
            )

        return templates_list


    def get_template(self, template_name: str) -> list:
        template_name = self._get_original_template_name(template_name)

        template_raw = self._get_endpoint(f'/gitignore/templates/{template_name}')
        template_str = template_raw['source']

        template = []

        for template_line in template_str.split('\n'):
            template_line = template_line.strip()

            if template_line and not template_line.startswith('#'):
                template.append(template_line)
        
        return template

    

    def _get_endpoint(self, endpoint: str) -> dict | list:
        for attempt_i in range(1, self.request_attempts + 1):
            try:
                response = self.session.get(endpoint)
                response.raise_for_status()

                return response.json()
            
            except (ConnectionError, Timeout, HTTPError) as e:
                self.logger.error(
                    "Request to %s failed (attempt %d/%d). Error: %s. Retrying in %ds",
                    endpoint, attempt_i, self.request_attempts, str(e), self.request_attempt_delay
                )
        
        raise ConnectionError(
            f"Request to {endpoint} failed after {self.request_attempts} attempts"
        )
    
    
    def _get_original_template_name(self, template_name: str) -> str:
        templates_list = self.get_templates_list()

        for original_template_name in templates_list:
            if original_template_name.lower() == template_name.lower():
                return original_template_name
        
        raise TemplateNotFoundError(
            f"Template \'{template_name}\' not found!"
        )
