from fastapi import APIRouter, Header, Depends, HTTPException, Response, status

import models_io 
import nftables
import exceptions



router = APIRouter()

@router.get("/{ip_address}")
async def get_ip(family      : models_io.Family_IN = Depends(models_io.Family_IN),
                 table       : models_io.Table_IN = Depends(models_io.Table_IN),
                 set         : models_io.SetName_IN = Depends(models_io.SetName_IN),
                 timeout     : models_io.Timeout_IN = Depends(models_io.Timeout_IN),
                 description : models_io.Description_IN = Depends(models_io.Description_IN),
                 ip_address  : models_io.IP_INPUT = Depends(models_io.IP_INPUT),
):
    return ip_address.ip_address, table.table



@router.post("/{ip_address}", status_code=201, responses={409: {"model": exceptions.HTTPError, "description": "Error for nftables execution",}})
async def post_ip(family      : models_io.Family_IN = Depends(models_io.Family_IN),
                  table       : models_io.Table_IN = Depends(models_io.Table_IN),
                  set         : models_io.SetName_IN = Depends(models_io.SetName_IN),
                  timeout     : models_io.Timeout_IN = Depends(models_io.Timeout_IN),
                  description : models_io.Description_IN = Depends(models_io.Description_IN),
                  ip_address  : models_io.IP_INPUT = Depends(models_io.IP_INPUT),
):
#    try:
    nftables.add_to_set(family.family, table.table, set.set, ip_address.ip_address, timeout.timeout)
    return { "status": "success", "data": {ip_address.ip_address} }
#    except:
#        raise HTTPException(status_code=409, detail="nftables execution failed")

