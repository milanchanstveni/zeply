from typing import Tuple

from eth_account import Account as EthAccount
from eth_keys import keys
from core.blockchain.exceptions import InvalidPrivateKeyError
from core.blockchain.base import (
    Coin,
    Account,
    Key,
    Address,
    generate_seed
)


class ETH(Coin):
    """Ethereum cryptocurrency wrapper"""

    @classmethod
    def is_valid_private_key(cls, private_key: str) -> bool:
        """Validate if a given private key is valid."""
        try:
            Account.from_key(private_key)
            return True
        except:
            return False
    
    @classmethod
    def account(cls, num_of_addresses: int = 1) -> Account:
        """Generate a new Ethereum account."""
        EthAccount.enable_unaudited_hdwallet_features()
        seed = generate_seed(12)
        obj = EthAccount.create_with_mnemonic(passphrase=seed)
        private_key = keys.PrivateKey(obj[0].key)

        addresses = []
        for _ in range(num_of_addresses):
            addresses.append(
                Address(
                    address=obj[0].address,
                    coin_acronym="ETH",
                    coin_name="Ethereum",
                    network="mainnet",
                    is_active=True,
                    seed=seed
                )
            )

        key = Key(
            private_key=private_key.to_hex(),
            public_key=private_key.public_key.to_hex(),
            addresses=addresses,
        )

        return Account(
            coin="ETH",
            key=key
        )
    
    @classmethod
    def account_from_key(cls, key: str) -> Account:
        """Generate a new Ethereum account from a private key."""
        if cls.is_valid_private_key(key) is False:
            raise InvalidPrivateKeyError()

        obj = EthAccount.from_key(key)
        private_key = keys.PrivateKey(obj.key)

        address = Address(
            address=obj.address,
            coin_acronym="ETH",
            coin_name="Ethereum",
            network="mainnet",
            is_active=True,
            seed=generate_seed(12)
        )

        key = Key(
            private_key=private_key.to_hex(),
            public_key=private_key.public_key,
            addresses=[address],
        )

        return Account(
            coin="ETH",
            key=key
        )
