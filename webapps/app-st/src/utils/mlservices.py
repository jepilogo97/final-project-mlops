import json

import httpx

from config import get_app_config
from entities import MLServiceConfig
from utils.states import get_mlmodel_service_url_state_kv


def get_mlservices_config_map() -> dict[str, MLServiceConfig]:
    return get_app_config().mlservices


def get_mlservice_config(service_id: str) -> MLServiceConfig:
    svcs = get_app_config().mlservices
    if service_id not in svcs:
        raise RuntimeError(f'app config missing service config for id="{service_id}"')

    return svcs[service_id]


def request_mlservice(resource_path="/predict", **kwargs) -> dict:
    (_, service_url) = get_mlmodel_service_url_state_kv()
    if service_url.endswith("/"):
        service_url = service_url[:-1]

    if not service_url.endswith(resource_path):
        service_url = service_url + resource_path

    try:
        response = httpx.post(service_url, **kwargs).json()
    except json.JSONDecodeError as ex:
        raise RuntimeError("invalid JSON in response body", ex)
    except httpx.RequestError as ex:
        raise RuntimeError(f"HTTP request failed", ex)

    return response
