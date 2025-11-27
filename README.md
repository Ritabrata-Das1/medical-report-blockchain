# Medical Report Management & Distribution System (Open Source Project)

A fully open-source, blockchain-powered system for securely storing medical report hashes, managing doctor access permissions, and providing a transparent audit trail — implemented using **Solidity**, **Ethereum (Hardhat)**, and a **Python + Streamlit frontend**.

This project is created as part of an Open Source Software assignment and is licensed under the **MIT License**, allowing anyone to use, modify, and contribute.

---

## ⚡ Project Overview

The Medical Report Management System is an innovative open-source solution designed to address the challenges in secure medical data handling.  
Traditional healthcare systems suffer from:

- tampering or alteration of medical records  
- unauthorized access to patient data  
- lack of audit trails  
- difficulty in verifying authenticity  

This project solves these issues by storing **cryptographic hashes** of reports on a blockchain and implementing an access-controlled verification system.

The actual medical files are **never stored on-chain**, ensuring privacy and legal compliance (HIPAA-friendly approach).

---

## 🚀 Features

### 🔐 Core Blockchain Features  
- **Private Ethereum Blockchain** (Hardhat local node)  
- **Smart Contract** for:
  - Adding medical report hashes  
  - Granting doctor access  
  - Revoking access  
  - Retrieving report metadata  
- **Immutable audit trail** using blockchain blocks  
- **Chain validation**  

### 🧪 Report Management Features  
- SHA-256 hashing of uploaded files  
- Ability to verify if a report has been altered  
- PDF receipt containing:
  - Block Index  
  - Patient ID  
  - Timestamp  
  - Uploader wallet  
  - Stored report hash  

### 🧑‍⚕️ Access Control  
- Per-patient access list managed through the smart contract  
- Doctors only read report metadata if permission is granted  

### 💻 Frontend UI (Streamlit)  
- Easy-to-use dashboard  
- Add report  
- Manage doctor access  
- Retrieve report metadata  
- Visual chain explorer  

### 🌐 Open Source Qualities  
- Active GitHub repository  
- MIT License  
- Clean architecture  
- Maintainer guidelines  
- Ready for community contributions  

---

## 🏗 Tech Stack

### **Backend (Blockchain & Smart Contract)**
- **Solidity**
- **Hardhat**
- **Ethers.js**
- **Local Ethereum Node (npx hardhat node)**

### **Frontend**
- **Python 3.11**
- **Streamlit**
- **Requests / JSON-RPC**
- **PDF generation**
- **SHA-256 hashing**

### **Other Tools**
- Git & GitHub  
- MIT License  
- GitHub Desktop / CLI  

---

## 📁 Project Structure

