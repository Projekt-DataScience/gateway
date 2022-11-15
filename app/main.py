from microservices import MICROSERVICES
from fastapi import FastAPI, Request, HTTPException, APIRouter
import httpx
import json

class MicroserviceManager:

    def __init__(self, ms_config):
        self.ms_config = ms_config
        self.mapping_db = {}
        self.mapping_db_fallback = None
        self.microservice_timeout = 3.0
        self.app = FastAPI()
        self._create_ms_mapping()
        self.router = APIRouter()
        self.router.add_api_route("/{rest_of_path:path}", self.frontend_backend_mapper, methods=["GET", "POST"])

    async def frontend_backend_mapper(self, request: Request, rest_of_path: str):
        if "/" in rest_of_path:
            path_parts = rest_of_path.split("/")
            if path_parts[0] == 'api':
                # redirect to microservice
                return self._backend_microservice_mapper(
                    request=request,
                    path="/".join(path_parts[1:])
                )

        # redirect to fallback
        return self._redirect_request(
            microservice = self.mapping_db_fallback,
            request = request,
            path = rest_of_path,
            post_data = None,
        )

    def _create_ms_mapping(self):
        for config_name, config in self.ms_config.items():
            fall_back = config['fall_back']

            if fall_back:
                if self.mapping_db_fallback is not None:
                    raise ValueError("Multiple fallbacks defined, only one allowed")
                else:
                    self.mapping_db_fallback = config_name
            else:
                open_api_url = config['url'] + config['openapi_file']
                with httpx.Client(timeout=1.0) as client:
                    try:
                        response = client.get(open_api_url)
                    except httpx.ConnectError as e:
                        response = None

                    if response is None:
                        print(f"Microservice not reachable {config_name}")
                        continue

                json_response = json.loads(response.text)
                paths = json_response['paths'].items()
                print(f"{len(paths)} routes loaded from microservice '{config_name}'")
                for path_name, path in paths:
                    if path_name == '/':
                        continue

                    # strip leading slash
                    path_name = path_name[1:]

                    if path_name in self.mapping_db:
                        raise ValueError("Same route in different microservices")
                    self.mapping_db[path_name] = config_name
                    print(f"route '{path_name}' linked to microservice '{config_name}'")

    def _backend_microservice_mapper(self, request: Request, path : str, post_data=None):
        if not ("/" in path):
            raise HTTPException(status_code=404, detail="Item not found")
        path_parts = path.split("/")
        main_path = path_parts[0] + "/"
        if main_path in self.mapping_db:
            ms_name = self.mapping_db[main_path]
            return self._redirect_request(
                microservice=ms_name,
                path=path,
                post_data=post_data,
                request=request,
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")

    def _redirect_request(self, microservice, path, request, post_data=None):
        ms_url = self.ms_config[microservice]['url']
        url = ms_url + path
        print(f"Contacting '{url}' on ms:{microservice}")
        with httpx.Client(timeout=self.microservice_timeout) as client:
            if post_data is None:
                try:
                    response = client.get(url)
                except httpx.ConnectError as e:
                    response = None
            else:
                try:
                    response = client.post(url)
                except httpx.ConnectError as e:
                    response = None
        if response is None:
            raise HTTPException(status_code=500, detail="Microservice timeout")
        else:
            return response.text
        #
ms_manager = MicroserviceManager(MICROSERVICES)
app = FastAPI()
app.include_router(ms_manager.router)