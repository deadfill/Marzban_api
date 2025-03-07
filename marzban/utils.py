import logging
from datetime import datetime, timedelta
from typing import Optional, Dict
from urllib.parse import urlparse, parse_qs

from marzban import MarzbanAPI


class MarzbanTokenCache:
    def __init__(self, client: MarzbanAPI,
                 username: str, password: str,
                 token_expire_minutes: int = 1440):
        self._client = client
        self._username = username
        self._password = password
        self._token_expire_minutes = token_expire_minutes
        self._token: Optional[str] = None
        self._exp_at: Optional[datetime] = None
        self._tokens: Dict[str, str] = {}

    async def get_token(self):
        if not self._exp_at or self._exp_at < datetime.now():
            logging.info(f'Get new token')
            self._token = await self.get_new_token()
            self._exp_at = datetime.now() + timedelta(minutes=self._token_expire_minutes - 1)
        return self._token

    async def get_new_token(self):
        try:
            token = await self._client.get_token(
                username=self._username,
                password=self._password
            )
            return token.access_token
        except Exception as e:
            logging.error(f'{e}', exc_info=True)
            raise e

    def get_token_from_cache(self, username: str) -> Optional[str]:
        return self._tokens.get(username)

    def set_token_in_cache(self, username: str, token: str):
        self._tokens[username] = token

    def remove_token_from_cache(self, username: str):
        self._tokens.pop(username, None)

def parse_url(url: str) -> Dict[str, str]:
    """Parse a URL and return its components.
    
    Args:
        url: The URL to parse
        
    Returns:
        A dictionary containing the URL components
    """
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    
    return {
        'scheme': parsed.scheme,
        'netloc': parsed.netloc,
        'path': parsed.path,
        'params': parsed.params,
        'query': {k: v[0] if len(v) == 1 else v for k, v in query.items()},
        'fragment': parsed.fragment
    }
