from environs import Env
from dataclasses import dataclass

@dataclass
class Config:
    XF_USER: str
    USER_AGENT: str
    XF_TFA_TRUST: str
    PROXY: str
    PROXY_EXISTS: bool

def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        XF_USER=env.str("XF_USER"),
        USER_AGENT=env.str("USER_AGENT"),
        XF_TFA_TRUST=env.str("XF_TFA_TRUST"),
        PROXY=env.str("PROXY"),
        PROXY_EXISTS=env.bool("PROXY_EXISTS"),
    )
