from typing import List, Union, Any
from tortoise.query_utils import Prefetch

from core.log import LOG
from api.v0.exceptions.http import (
    UnknownError,
    InvalidCoin,
    ObjectNotFound
)
from api.v0.schemas.address import AddressPayload
from db.models import (
    Address,
    Key,
    Account
)
from core.blockchain import (
    Crypto,
    Account as AccountResponse
)


async def generate_address(payload: AddressPayload) -> AccountResponse:
    try:
        coin = Crypto.get_coin(payload.coin)
        account = coin.account()
        key = account.key
        address = key.addresses[0]

        address_db = await Address.create(**dict(
            address=address.address,
            coin_acronym=address.coin_acronym,
            coin_name=address.coin_name,
            network=address.network,
            is_active=address.is_active,
            seed=address.seed,
        ))

        key_db = await Key.create(**dict(
            private_key=key.private_key,
            public_key=key.public_key,
        ))

        await key_db.addresses.add(address_db)
        account.key.addresses[0].id = address_db.id
        account.key.id = key_db.id

        account_db = await Account.create(**dict(
            key=key_db,
            coin=payload.coin,
        ))
        account.id = account_db.id

        return account

    except (NotImplementedError, Exception) as e:
        if type(e) == NotImplementedError:
            raise InvalidCoin()

        LOG.error(str(e))
        
        raise UnknownError()


async def list_addresses() -> List[Account.model]:
    try:
        db_accounts = await Account.model_list.from_queryset(Account.all())
        return db_accounts.dict()["__root__"]

    except (NotImplementedError, Exception) as e:
        if type(e) == NotImplementedError:
            raise InvalidCoin()

        LOG.error(str(e))
        
        raise UnknownError()


async def fetch_address(id: int) -> Account.model:
    try:
        obj = await Account.get_or_none(id=id)
        if not obj:
            raise ObjectNotFound()

        # db_account = await Account.model.from_queryset_single(
        #     Account.get_or_none(id=id)
        # )
        db_account = await Account.model.from_tortoise_orm(obj)

        return db_account

    except (NotImplementedError, ObjectNotFound, Exception) as e:
        if type(e) == NotImplementedError:
            raise InvalidCoin()

        if type(e) == ObjectNotFound:
            raise

        LOG.error(str(e))
        
        raise UnknownError()