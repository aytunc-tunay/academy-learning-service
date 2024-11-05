# Portfolio Rebalancer Service

A service to manage and rebalance cryptocurrency portfolios based on customizable target allocations and price data from either [CoinMarketCap](https://coinmarketcap.com/) or [CoinGecko](https://www.coingecko.com/).

The Portfolio Rebalancer interacts with a mock decentralized exchange (DEX) contract and enables multisig contract-authorized rebalancing actions to adjust token holdings to maintain user-defined allocations.

---

## System Requirements

- [Python](https://www.python.org/downloads/release/python-31015/) `==3.10`
- [Tendermint](https://docs.tendermint.com/v0.34/introduction/install.html) `==0.34.19`
- [IPFS node](https://docs.ipfs.io/install/command-line/#official-distributions) `==0.6.0`
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [Poetry](https://python-poetry.org/)
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Set Docker permissions for non-root access](https://docs.docker.com/engine/install/linux-postinstall/)

---

## Run Your Own Portfolio Rebalancer Agent

### Get the Code

1. Clone this repository:

    ```bash
    git clone git@github.com:aytunc-tunay/academy-learning-service.git
    ```
2. Change the branch:

    ```bash
    cd academy-learning-service
    git checkout session8_final_project
    ```

3. Create the virtual environment:

    ```bash
    poetry shell
    poetry install
    ```

4. Sync packages:

    ```bash
    autonomy packages sync --update-packages
    ```

---

### Prepare the Data

1. Prepare a `keys.json` file containing wallet addresses and private keys for each agent:

    ```bash
    autonomy generate-key ethereum -n 4
    ```

2. Prepare a `ethereum_private_key.txt` file with one of the private keys from `keys.json` (no newline at the end).

4. Create two [Safes on Gnosis](https://app.safe.global/welcome):
    - Set the Safe threshold to **1 out of 4** for one and **3 out of 4** for the other.
    - Use the single-signer Safe for testing, while the other is for full service operation.
4. Deploy the mock DEX contract in `packages/valory/contracts/mock_dex/MockTradeContract.sol` on Gnosis
    - Don't forget to replace this two safe address with the ones in contract for transaction authorization.


4. Fund the Safe and agents with test assets (xDAI and tokens) using [Tenderly](https://tenderly.co/) or a similar virtual testnet.

5. Add initial deposits to the mock DEX contract. 

6. Make a copy of the sample environment file and edit the variables:

    ```bash
    cp sample.env .env
    ```

---

### Environment Variables

Add the following environment variables in `.env` to configure the rebalancer:

- **API and Key Settings**:
  - `COINGECKO_API_KEY`: API key for CoinGecko
  - `COINMARKETCAP_API_KEY`: API key for CoinMarketCap
  - `API_SELECTION`: Either `coingecko` or `coinmarketcap` to set the price source
- **Mock DEX and Safe Contract Addresses**:
  - `MOCK_CONTRACT_ADDRESS`: Address of the deployed mock DEX contract
  - `PORTFOLIO_ADDRESS`: Address of the portfolio (the agent holding the assets)
  - `SAFE_CONTRACT_ADDRESS_SINGLE`: Address of the single-signer Safe
  - `SAFE_CONTRACT_ADDRESS`: Address of the multi-signer Safe
- **Rebalancing Settings**:
  - `TOKENS_TO_REBALANCE`: List of tokens to track, e.g., `["ETH", "USDC"]`
  - `TARGET_PERCENTAGES`: Desired allocations for each token, e.g., `[75.0, 25.0]`
  - `VARIATION_THRESHOLD`: Maximum allowed deviation from target before rebalancing, e.g., `3.0`

---

### Run a Single Agent Locally

1. Verify that `ALL_PARTICIPANTS` in `.env` includes only one address.

2. Start the agent:

    ```bash
    bash run_agent.sh
    ```

---

### Run the Full Rebalancing Service (4 agents) via Docker Compose

1. Ensure `ALL_PARTICIPANTS` in `.env` includes four addresses.

2. Start Docker:

    ```bash
    docker
    ```

3. Start the service:

    ```bash
    bash run_service.sh
    ```

4. Check service logs for an agent (in a new terminal):

    ```bash
    docker logs -f learningservice_abci_0
    ```

---

### Overview of Functionality

The Portfolio Rebalancer monitors portfolio allocations based on USD values, aiming to keep token balances aligned with target allocations. When token values exceed the threshold, rebalancing occurs by adjusting token amounts and updating balances via multisend transactions to the mock DEX contract. Reports are also stored in IPFS for transparency and auditability.
