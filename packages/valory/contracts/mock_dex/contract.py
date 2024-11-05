from aea.common import JSONLike
from aea.configurations.base import PublicId
from aea.contracts.base import Contract
from aea.crypto.base import LedgerApi
from aea_ledger_ethereum import EthereumApi

PUBLIC_ID = PublicId.from_str("valory/mock_dex:0.1.0")

class MOCKDEX(Contract):
    """Wrapper class for interacting with the MOCKDEX contract based on the provided ABI."""

    contract_id = PUBLIC_ID

    @classmethod
    def adjustBalance(
        cls,
        ledger_api: EthereumApi,
        contract_address: str,
        user: str,
        token: str,
        new_balance: int,
        from_address: str
    ) -> JSONLike:
        """
        Adjust the balance of a user.

        :param ledger_api: Ethereum API instance for contract interaction.
        :param contract_address: Address of the deployed contract.
        :param user: Address of the user.
        :param token: Token name.
        :param new_balance: New balance to set.
        :return: Transaction dictionary.
        """
        contract_instance = cls.get_instance(ledger_api, contract_address)
        transaction = contract_instance.functions.adjustBalance(user, token, new_balance).build_transaction({
        "from": from_address  # Set the from address here/Otherwise only multisig contract throws an error while preparing the tx data.
    })
        return transaction

    @classmethod
    def deposit(
        cls,
        ledger_api: EthereumApi,
        contract_address: str,
        token: str,
        amount: int
    ) -> JSONLike:
        """
        Deposit tokens into the contract.

        :param ledger_api: Ethereum API instance for contract interaction.
        :param contract_address: Address of the deployed contract.
        :param token: Token name.
        :param amount: Amount of tokens to deposit.
        :return: Transaction dictionary.
        """
        contract_instance = cls.get_instance(ledger_api, contract_address)
        transaction = contract_instance.functions.deposit(token, amount).build_transaction()
        return transaction

    @classmethod
    def withdraw(
        cls,
        ledger_api: EthereumApi,
        contract_address: str,
        user: str,
        token: str,
        amount: int
    ) -> JSONLike:
        """
        Withdraw tokens from the contract.

        :param ledger_api: Ethereum API instance for contract interaction.
        :param contract_address: Address of the deployed contract.
        :param user: Address of the user.
        :param token: Token name.
        :param amount: Amount of tokens to withdraw.
        :return: Transaction dictionary.
        """
        contract_instance = cls.get_instance(ledger_api, contract_address)
        transaction = contract_instance.functions.withdraw(user, token, amount).build_transaction()
        return transaction

    @classmethod
    def getBalance(
        cls,
        ledger_api: EthereumApi,
        contract_address: str,
        user: str,
        token: str
    ) -> JSONLike:
        """
        Get the balance of a user for a specific token.

        :param ledger_api: Ethereum API instance for contract interaction.
        :param contract_address: Address of the deployed contract.
        :param user: Address of the user as a string.
        :param token: Token name as a string.
        :return: Dictionary containing the user's balance.
        """
        contract_instance = cls.get_instance(ledger_api, contract_address)

        user_address = ledger_api.api.to_checksum_address(user)
        token_str = str(token)

        try:
            balance = contract_instance.functions.getBalance(user_address, token_str).call()
        except Exception as e:
            cls.logger.error(f"Error calling getBalance with user {user} and token {token}: {e}")
            return {"balance": None, "error": str(e)}

        return {"balance": balance}


    @classmethod
    def SAFE_CONTRACT_ADDRESS(
        cls,
        ledger_api: EthereumApi,
        contract_address: str
    ) -> JSONLike:
        """
        Retrieve the SAFE_CONTRACT_ADDRESS.

        :param ledger_api: Ethereum API instance for contract interaction.
        :param contract_address: Address of the deployed contract.
        :return: Dictionary containing the SAFE_CONTRACT_ADDRESS.
        """
        contract_instance = cls.get_instance(ledger_api, contract_address)
        safe_address = contract_instance.functions.SAFE_CONTRACT_ADDRESS().call()
        return {"SAFE_CONTRACT_ADDRESS": safe_address}

    @classmethod
    def SAFE_CONTRACT_ADDRESS_SINGLE(
        cls,
        ledger_api: EthereumApi,
        contract_address: str
    ) -> JSONLike:
        """
        Retrieve the SAFE_CONTRACT_ADDRESS_SINGLE.

        :param ledger_api: Ethereum API instance for contract interaction.
        :param contract_address: Address of the deployed contract.
        :return: Dictionary containing the SAFE_CONTRACT_ADDRESS_SINGLE.
        """
        contract_instance = cls.get_instance(ledger_api, contract_address)
        safe_address_single = contract_instance.functions.SAFE_CONTRACT_ADDRESS_SINGLE().call()
        return {"SAFE_CONTRACT_ADDRESS_SINGLE": safe_address_single}
