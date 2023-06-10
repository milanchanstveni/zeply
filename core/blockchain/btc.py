from bitcoin import (
    random_key as generate_private_key,
    privtopub as private_key_to_public_key,
    privtoaddr as private_key_to_address,
)
from core.blockchain.exceptions import InvalidPrivateKeyError
from core.blockchain.base import (
    Coin,
    Account,
    Key,
    Address,
    generate_seed
)


class BTC(Coin):
    """Bitcoin Cryptocurrency Wrapper"""

    @classmethod
    def is_valid_private_key(self, private_key: str) -> bool:
        """Validate if a given private key is valid."""
        try:
            private_key_to_public_key(private_key)
            return True
        except:
            return False

    @classmethod
    def account(cls, num_of_addresses: int = 1) -> Account:
        """Generate a new Bitcoin account."""
        private_key = generate_private_key()
        addresses = []
        for _ in range(num_of_addresses):
            addresses.append(
                Address(
                    address=private_key_to_address(private_key),
                    coin_acronym="BTC",
                    coin_name="Bitcoin",
                    network="mainnet",
                    is_active=True,
                    seed=generate_seed(12)
                )
            )

        key = Key(
            private_key=private_key,
            public_key=private_key_to_public_key(private_key),
            addresses=addresses
        )

        return Account(
            coin="BTC",
            key=key
        )
    
    @classmethod
    def account_from_key(cls, key: str) -> Account:
        """Generate a new Bitcoin account from a private key."""
        if cls.is_valid_private_key(key) is False:
            raise InvalidPrivateKeyError()

        address = Address(
            address=private_key_to_address(key),
            coin_acronym="BTC",
            coin_name="Bitcoin",
            network="mainnet",
            is_active=True,
            seed=generate_seed(12)
        )

        key = Key(
            private_key=key,
            public_key=private_key_to_public_key(key),
            addresses=[address]
        )

        return Account(
            coin="BTC",
            key=key
        )
