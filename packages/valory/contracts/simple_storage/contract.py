from aea.common import JSONLike
from aea.configurations.base import PublicId
from aea.contracts.base import Contract
from aea.crypto.base import LedgerApi
from aea_ledger_ethereum import EthereumApi

PUBLIC_ID = PublicId.from_str("valory/simple_storage:0.1.0")

class SimpleStorage(Contract):
    """SimpleStorage contract interface for interacting with a deployed SimpleStorage contract."""

    contract_id = PUBLIC_ID

    @classmethod
    def set_stored_data(
        cls,
        ledger_api: EthereumApi,
        contract_address: str,
        value: int
    ) -> JSONLike:
        """
        Set the value of storedData in the SimpleStorage contract.

        :param ledger_api: Ethereum API instance for contract interaction.
        :param contract_address: Address of the deployed contract.
        :param value: Value to store in the contract.
        :return: Transaction dictionary.
        """
        contract_instance = cls.get_instance(ledger_api, contract_address)
        transaction = contract_instance.functions.set(value).build_transaction()
        return transaction

    @classmethod
    def get_stored_data(
        cls,
        ledger_api: EthereumApi,
        contract_address: str
    ) -> JSONLike:
        """
        Retrieve the stored value from the SimpleStorage contract.

        :param ledger_api: Ethereum API instance for contract interaction.
        :param contract_address: Address of the deployed contract.
        :return: Dictionary containing the stored value.
        """
        contract_instance = cls.get_instance(ledger_api, contract_address)
        stored_data = contract_instance.functions.get().call()
        return {"storedData": stored_data}
