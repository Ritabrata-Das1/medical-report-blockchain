# Medical Report Blockchain (Solidity + Hardhat + Streamlit)

This is an original academic project; architecture and code written from scratch for my course.

An open source **Medical Report Management & Distribution System** built on a local Ethereum blockchain.

## Features

- Store medical report hashes on a Solidity smart contract
- Grant / revoke doctor access to patient reports
- Retrieve report metadata with access control
- Streamlit frontend for easy demo & UI
- SHA-256 hashing for report verification
- Local Hardhat node for development (no real ETH needed)

## Tech Stack

- **Blockchain**: Solidity, Hardhat, local Ethereum node
- **Frontend**: Python 3, Streamlit, web3.py
- **Others**: SHA-256 hashing, JSON-based config

## How to Run (Short)

1. Start Hardhat node:

```bash
cd backend
npx hardhat node
