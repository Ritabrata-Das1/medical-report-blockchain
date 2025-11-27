# frontend/settings.py

# RPC URL of the Hardhat local node
RPC_URL = "http://127.0.0.1:8545"

# Paste the deployed contract address printed by `deploy.js`
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

# Path to ABI file relative to this settings file
ABI_PATH = "../backend/contract_abi.json"

# Hardhat accounts: paste 2–3 address + private key pairs from `npx hardhat node` output
# DO NOT use these keys on any real network.
ACCOUNTS = {
    "Hospital_A": {
        "address": "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
        "private_key": "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    },
    "Doctor_1": {
        "address": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
        "private_key": "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"
    },
    "Doctor_2": {
        "address": "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",
        "private_key": "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"
    }
}
