from aea.common import JSONLike
from aea.configurations.base import PublicId
from aea.contracts.base import Contract
from aea.crypto.base import LedgerApi
from aea_ledger_ethereum import EthereumApi

PUBLIC_ID = PublicId.from_str("valory/oracle:0.1.0")

class ORACLE(Contract):
    """The Oracle contract for interacting with an already deployed contract."""

    contract_id = PUBLIC_ID

    @classmethod
    def get_latest_answer(
        cls,
        ledger_api: EthereumApi,
        contract_address: str
    ) -> JSONLike:
        """Fetch the latest answer from the Oracle contract."""
        contract_instance = cls.get_instance(ledger_api, contract_address)
        latest_answer = contract_instance.functions.latestAnswer().call()
        return dict(answer=latest_answer)

    @classmethod
    def get_latest_timestamp(
        cls,
        ledger_api: EthereumApi,
        contract_address: str
    ) -> JSONLike:
        """Fetch the latest timestamp from the Oracle contract."""
        contract_instance = cls.get_instance(ledger_api, contract_address)
        latest_timestamp = contract_instance.functions.latestTimestamp().call()
        return dict(timestamp=latest_timestamp)
