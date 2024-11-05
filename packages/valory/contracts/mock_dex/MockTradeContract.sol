// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract MockDEX {
    // Stores balances by user and token type
    mapping(address => mapping(string => uint256)) private balances;

    // Multisig addresses with write privileges
    address public constant SAFE_CONTRACT_ADDRESS = 0xF195bb4EA1DDB568d3bA0F8a5F42b70728C8D72f;
    address public constant SAFE_CONTRACT_ADDRESS_SINGLE = 0x71C36E25504aDF60ab1BcE3EbD3d4E8b5Dd6b27d;

    // Events
    event Deposit(address indexed user, string token, uint256 amount);
    event Withdrawal(address indexed user, string token, uint256 amount);
    event BalanceAdjusted(address indexed user, string token, uint256 newBalance);

    // Modifier to restrict function access to only the multisig addresses
    modifier onlyMultisig() {
        require(
            msg.sender == SAFE_CONTRACT_ADDRESS || msg.sender == SAFE_CONTRACT_ADDRESS_SINGLE,
            "Only multisig addresses can perform this action"
        );
        _;
    }

    // Deposit function for users to add token balances
    function deposit(string memory token, uint256 amount) external {
        require(amount > 0, "Amount must be greater than zero");
        balances[msg.sender][token] += amount;
        emit Deposit(msg.sender, token, amount);
    }

    // Function for users to check their token balance
    function getBalance(address user, string memory token) external view returns (uint256) {
        return balances[user][token];
    }

    // Multisig function to adjust a user's balance for a given token
    function adjustBalance(address user, string memory token, uint256 newBalance) external onlyMultisig {
        balances[user][token] = newBalance;
        emit BalanceAdjusted(user, token, newBalance);
    }

    // Optional: Allow multisig addresses to withdraw on behalf of users for rebalancing
    function withdraw(address user, string memory token, uint256 amount) external onlyMultisig {
        require(balances[user][token] >= amount, "Insufficient balance");
        balances[user][token] -= amount;
        emit Withdrawal(user, token, amount);
    }
}
