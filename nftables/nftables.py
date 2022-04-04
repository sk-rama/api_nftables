from __future__ import annotations
from typing import List, Optional, ClassVar
from pydantic import BaseModel, Extra
import subprocess
import app_config


cfg = app_config.get_settings()

class Metainfo(BaseModel):
    version: str
    release_name: str
    json_schema_version: int


class Set(BaseModel):
    family: str
    name: str
    table: str
    type: str
    handle: int
    flags: List[str]
    elem: List[str]


class Nftable(BaseModel):
    set: Optional[Set] = None


class Model(BaseModel, extra=Extra.ignore):
    nftables: List[Nftable]


def get_elements(nft_family, nft_table, nft_set):
    # nft -j list set inet table_filter ip_drop_chile
    cmd = f'nft -j list set {nft_family} {nft_table} {nft_set}'
    return cmd

def add_to_set(family, table, set_name, ip, timeout=None):
    # nft add element inet table_filter ip_drop_chile {10.0.0.1 timeout 120s }
    if timeout:
        cmd = f'{cfg.sudo_path} nft add element {family} {table} {set_name} {{ {ip} timeout {timeout}s }}'
    else:
        cmd = f'{cfg.sudo_path} nft add element {family} {table} {set_name} {{ {ip} }}'
    print(cmd)
    return subprocess.run(cmd, shell=True, check=True)
    
