
# 🚀 **Medical Report Blockchain Manager (Open Source Project)**

Secure medical report storage & permission-controlled access using Blockchain + Hardhat + Python Streamlit.

---

## 📌 **Overview**

The **Medical Report Blockchain Manager** is an open-source project designed to securely manage medical reports using blockchain technology.
It ensures **tamper-proof** storage of report hashes, **fine-grained access control**, and an easy-to-use **frontend interface** for hospitals, doctors, and patients.

This project demonstrates blockchain’s real-world application in healthcare, while being simple enough for academic and OSS contribution purposes.

---

## ⭐ **Key Features**

### 🔐 Core (Blockchain)

* Store report metadata securely on the blockchain
* SHA-256 hashing for tamper detection
* Private Hardhat local blockchain
* Smart Contract (Solidity) with:

  * `addReport`
  * `getReport`
  * `grantAccess`
  * `revokeAccess`

### 🖥️ Frontend (Python + Streamlit)

* Add a report (upload any file → hash computed)
* View reports (permission enforced)
* Manage doctor access
* Blockchain visualizer (linked blocks)
* File hash verification
* Activity log
* PDF receipt generation (optional)

### 🎯 Extra OSS Features


* Cleaner UI improvements
* Modular code for future extensions

---

## 🧰 **Tech Stack**

### **Blockchain / Backend**

* **Solidity** – smart contracts
* **Hardhat** – contract compilation, local blockchain, deployment
* **Node.js + NPM** – project management
* **Ethers.js** – contract interaction
* **JSON ABI Export** – used by Streamlit frontend

### **Frontend**

* **Python 3.11+**
* **Streamlit** – UI framework
* **reportlab** (optional) – PDF generation
* **requests, web3.py** – interact with Hardhat node

---

## 📁 **Project Structure**

```
medical-blockchain/
│
├── backend/                 # Hardhat + Smart Contracts
│   ├── contracts/
│   │   └── MedicalReport.sol
│   ├── scripts/
│   │   └── deploy.js
│   ├── contract_abi.json
│   ├── hardhat.config.js
│   └── package.json
│
├── frontend/                # Python Streamlit UI
│   ├── app.py
│   ├── settings.py
│   ├── utils.py
│   └── requirements.txt
│
└── README.md
```

---

## ⚙️ **Installation & Setup**

### **1️⃣ Backend Setup (Hardhat)**

```
cd backend
npm install --legacy-peer-deps
npx hardhat compile
npx hardhat node
```

### **2️⃣ Deploy Contract**

Open a new terminal:

```
cd backend
npx hardhat run scripts/deploy.js --network localhost
```

This generates:

✔ Contract address
✔ `contract_abi.json` file

---

### **3️⃣ Frontend Setup (Streamlit)**

```
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔗 How Components Work Together

1. The user interacts through **Streamlit (app.py)**
2. Streamlit uses **web3.py** to call the deployed **Solidity contract**
3. Contract stores **tamper-proof hashes** on blockchain
4. Access control ensures only authorized doctors can view records
5. Blockchain visualizer shows linked block data

---

## 🧪 **Testing**

Unit tests you can perform:

### ✔ Add Report Test

Upload `bloodtest.pdf` → get SHA-256 hash → stored in blockchain

### ✔ Access Denied Test

Login as Doctor_2 → attempt to access → “Access Denied”

### ✔ Access Granted Test

Hospital_A → grant access → Doctor_1 → “Access Granted”

### ✔ Chain Validation Test

Streamlit visualizer → “Chain Valid”

### ✔ Hash Verification Test

Reupload file → hash matches → proves authenticity

---

## 🤝 **Contributing Guidelines (For OSS Project)**

This project welcomes open-source contributions.

### ✔ 1. Fork the Repository

Click **Fork** → create copy in your GitHub.

### ✔ 2. Clone

```
git clone <your-fork-url>
```

### ✔ 3. Create a Branch

```
git checkout -b fix-ui-color
```

### ✔ 4. Make Changes

Examples of valid contributions:

* Bug fixes
* UI improvements
* Refactoring backend
* Improve smart contract
* Add comments / docs
* Create tests

### ✔ 5. Commit

```
git commit -m "Fix: Improved UI contrast in blockchain visualizer"
```

### ✔ 6. Push

```
git push origin fix-ui-color
```

### ✔ 7. Open Pull Request

Go to GitHub → Open PR
A maintainer (you or reviewer) leaves feedback or merges.

---

## 📜 **License**

Licensed under the **MIT License**, allowing:

* Personal + commercial use
* Modification
* Redistribution

---

## 🧾 **Maintainer**

**Your Name**
Open-source contributor
(Replace with your details)

---


