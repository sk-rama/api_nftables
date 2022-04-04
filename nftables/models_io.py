from pydantic import BaseModel, validator, Field
from typing import Literal
import ipaddress
import app_config


cfg = app_config.get_settings()


class IpAddress(str):

    @classmethod
    def __get_validators__(cls):
    # one or more validators may be yielded which will be called in the
    # order to validate the input, each validator will receive as an input
    # the value returned from the previous validator
#        yield cls.validate
        yield cls.validate_2
    @classmethod
    def validate(cls, v):
        try:
            ip = ipaddress.ip_address(v)
        except:
            raise TypeError('valid ip address as string is required')
        return v

    @classmethod
    def validate_2(cls, v):
        if v.startswith('192'):
            raise TypeError('ip address may not start with string 192')
        return v

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            title='Valid IP Address',
            # some example 
            example=f'112.31.56.247',
        )

    def __set__(self, obj, value):
        try:
            ip = ipaddress.ip_address(value)
        except:
            raise TypeError('valid ip address as string is required - descriptors error')
        return value

    def __get__(self, obj):
        return self.value

#    def __repr__(self):
#        return f'ip address: {str(self)}'


class IP_INPUT(BaseModel):
    ip_address: IpAddress = Field(description='https://en.wikipedia.org/wiki/IP_address')

    @validator('ip_address')
    def not_in_whitelist(cls, v):
        ip_network = ipaddress.IPv4Network(v)
        for item in cfg.ip_whitelist:
            item_whitelist = ipaddress.IPv4Network(item)
            if ip_network.subnet_of(item_whitelist):
                raise ValueError('ip address is in whitelist')
        return v



class Family_IN(BaseModel):
    family: Literal[cfg.nft_families]

class Table_IN(BaseModel):
    table: Literal[cfg.nft_tables]

class SetName_IN(BaseModel):
    set: Literal[cfg.nft_sets]

class Timeout_IN(BaseModel):
    timeout: int = Field(None, ge=0, le=31_536_000)

class Description_IN(BaseModel):
    desc: Literal[cfg.nft_desc]





