from core.blockchain.base import (
    Coin,
    Account,
    generate_seed
)
from core.blockchain.btc import BTC
from core.blockchain.eth import ETH


class Crypto:
    """Cryptocurrency Wrapper"""

    @classmethod
    def get_coin(cls, coin: str) -> Coin:
        """Get a cryptocurrency wrapper."""
        if coin.upper() == "BTC":
            return BTC
        elif coin.upper() == "ETH":
            return ETH
        else:
            raise NotImplementedError()
