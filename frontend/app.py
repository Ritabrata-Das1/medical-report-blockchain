"""
Streamlit Frontend for MedicalReport.sol on Hardhat

Tech stack:
- Backend: Solidity + Hardhat (local node at http://127.0.0.1:8545)
- Frontend: Python + Streamlit + Web3.py
- Contract ABI + address: backend/contract_abi.json

Features:
- Add report (file hash + description stored on-chain)
- Grant access to doctor address
- Revoke access
- Get report (with contract-level access control)
- Simple Visualizer (list of all reports from contract)
"""

import json
from pathlib import Path
from datetime import datetime
import hashlib

import streamlit as st
import pandas as pd
from web3 import Web3
from web3.exceptions import ContractLogicError

# -------------------------
# CONFIG
# -------------------------

# Hardhat local RPC
RPC_URL = "http://127.0.0.1:8545"

# Path to backend/contract_abi.json (relative to this file)
ABI_PATH = Path(__file__).resolve().parents[1] / "backend" / "contract_abi.json"


# -------------------------
# HELPER: LOAD CONTRACT
# -------------------------

@st.cache_resource
def load_contract():
    # Connect to Hardhat node
    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    if not w3.is_connected():
        raise RuntimeError(f"Cannot connect to Hardhat node at {RPC_URL}. "
                           f"Make sure 'npx hardhat node' is running.")

    # Load ABI + address from JSON
    if not ABI_PATH.exists():
        raise FileNotFoundError(f"ABI file not found at: {ABI_PATH}")

    with open(ABI_PATH, "r") as f:
        data = json.load(f)

    # EXPECTED STRUCTURE:
    # {
    #   "address": "0x....",
    #   "abi": [ ... ]
    # }
    address = data.get("address")
    abi = data.get("abi")

    if not address or not abi:
        raise ValueError("contract_abi.json must contain 'address' and 'abi' keys.")

    contract = w3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)
    return w3, contract


# -------------------------
# BASIC HASH HELPER
# -------------------------

def compute_sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# -------------------------
# STREAMLIT UI SETUP
# -------------------------

st.set_page_config(
    page_title="Medical Reports on Ethereum (Hardhat + Streamlit)",
    layout="wide"
)

st.title("🩺 Medical Report Management on Ethereum (Hardhat + Streamlit)")

# Try to load contract
try:
    w3, contract = load_contract()
except Exception as e:
    st.error(f"Connection / contract error: {e}")
    st.stop()

st.success("✅ Connected to Hardhat node and contract loaded successfully.")

# Get available accounts from Hardhat
accounts = w3.eth.accounts
if not accounts:
    st.error("No accounts found from Hardhat. Is the node running?")
    st.stop()

# -------------------------
# SIDEBAR: CURRENT USER
# -------------------------

st.sidebar.header("Account Selector")

current_account = st.sidebar.selectbox(
    "Choose Ethereum account (simulated user)",
    options=accounts,
    index=0,
)

st.sidebar.write(f"**Current account:** `{current_account}`")
st.sidebar.info(
    "Accounts are provided by Hardhat local node. "
    "Transactions will be sent from the selected account."
)

# -------------------------
# TABS
# -------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    ["➕ Add Report", "🔐 Manage Access", "📄 Get Report", "📊 Reports Visualizer"]
)

# -------------------------
# TAB 1: ADD REPORT
# -------------------------

with tab1:
    st.header("➕ Add Medical Report")

    st.write(
        "This will call the `addReport(patientId, reportHash, description)` "
        "function on the Solidity contract."
    )

    col1, col2 = st.columns(2)

    with col1:
        patient_id = st.text_input("Patient ID (string)", value="PAT001")
        description = st.text_input("Description", value="Blood Test Report")

    with col2:
        uploaded_file = st.file_uploader(
            "Upload report file (any type) to hash",
            type=None,
            help="The file itself is NOT stored on-chain. Only its SHA-256 hash is.",
        )

    if st.button("Add Report to Blockchain"):
        if not patient_id.strip():
            st.error("Patient ID is required.")
        elif not uploaded_file:
            st.error("Please upload a file to compute its hash.")
        else:
            try:
                file_bytes = uploaded_file.read()
                report_hash = compute_sha256_bytes(file_bytes)

                st.write(f"Computed SHA-256 hash: `{report_hash}`")

                # Send transaction
                tx_hash = contract.functions.addReport(
                    patient_id,
                    report_hash,
                    description
                ).transact({"from": current_account})

                with st.spinner("Waiting for transaction confirmation..."):
                    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

                st.success("✅ Report added successfully on-chain.")
                st.json(
                    {
                        "tx_hash": tx_hash.hex(),
                        "blockNumber": receipt.blockNumber,
                        "gasUsed": receipt.gasUsed,
                        "patientId": patient_id,
                        "reportHash": report_hash,
                        "description": description,
                    }
                )

            except Exception as e:
                st.error(f"Error while adding report: {e}")


# -------------------------
# TAB 2: MANAGE ACCESS
# -------------------------

with tab2:
    st.header("🔐 Grant / Revoke Access")

    st.write(
        "These actions call `grantAccess(patientId, doctor)` and "
        "`revokeAccess(patientId, doctor)` on the contract."
    )

    c1, c2 = st.columns(2)

    with c1:
        patient_for_access = st.text_input(
            "Patient ID (for access control)", key="access_patient_id"
        )
        doctor_address = st.selectbox(
            "Doctor Ethereum address",
            options=accounts,
            index=1 if len(accounts) > 1 else 0,
            key="doctor_select",
        )

    with c2:
        st.info(
            "The contract stores permissions as a mapping: "
            "`permission[patientId][doctorAddress] -> bool`"
        )

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    # Grant Access
    with col_btn1:
        if st.button("Grant Access"):
            if not patient_for_access.strip():
                st.error("Patient ID is required.")
            else:
                try:
                    tx_hash = contract.functions.grantAccess(
                        patient_for_access, doctor_address
                    ).transact({"from": current_account})
                    with st.spinner("Waiting for transaction..."):
                        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                    st.success(
                        f"✅ Access granted to {doctor_address} for patient '{patient_for_access}'."
                    )
                except Exception as e:
                    st.error(f"Error while granting access: {e}")

    # Revoke Access
    with col_btn2:
        if st.button("Revoke Access"):
            if not patient_for_access.strip():
                st.error("Patient ID is required.")
            else:
                try:
                    tx_hash = contract.functions.revokeAccess(
                        patient_for_access, doctor_address
                    ).transact({"from": current_account})
                    with st.spinner("Waiting for transaction..."):
                        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                    st.success(
                        f"✅ Access revoked for {doctor_address} on patient '{patient_for_access}'."
                    )
                except Exception as e:
                    st.error(f"Error while revoking access: {e}")

    # Check Access
    with col_btn3:
        if st.button("Check Permission"):
            if not patient_for_access.strip():
                st.error("Patient ID is required.")
            else:
                try:
                    has_perm = contract.functions.permission(
                        patient_for_access, doctor_address
                    ).call()
                    st.info(
                        f"Permission status for doctor `{doctor_address}` on patient "
                        f"`{patient_for_access}`: **{has_perm}**"
                    )
                except Exception as e:
                    st.error(f"Error while checking permission: {e}")


# -------------------------
# TAB 3: GET REPORT
# -------------------------

with tab3:
    st.header("📄 Get Report (with on-chain access control)")

    st.write(
        "This calls `getReport(index)` from the contract. "
        "The contract enforces access: uploader or permitted doctor only."
    )

    report_index = st.number_input(
        "Report index (0, 1, 2, ...)",
        min_value=0,
        step=1,
        value=0,
    )

    if st.button("Fetch Report"):
        try:
            # Call with 'from' so the contract can use msg.sender
            report_tuple = contract.functions.getReport(
                int(report_index)
            ).call({"from": current_account})

            # Solidity struct Report:
            # string patientId;
            # string reportHash;
            # string description;
            # uint timestamp;
            # address uploader;
            patient_id, report_hash, description, timestamp, uploader = report_tuple

            ts_human = datetime.utcfromtimestamp(timestamp).isoformat()

            st.success("✅ Access granted. Report metadata:")
            st.json(
                {
                    "index": int(report_index),
                    "patientId": patient_id,
                    "reportHash": report_hash,
                    "description": description,
                    "timestamp_utc": ts_human,
                    "uploader": uploader,
                }
            )

            st.info(
                "To verify integrity, recompute SHA-256 of the original file locally and "
                "compare with the stored `reportHash`."
            )

        except ContractLogicError as e:
            # This usually means ACCESS DENIED from require() in Solidity
            st.error(f"Contract reverted (likely access denied): {e}")
        except Exception as e:
            st.error(f"Error fetching report: {e}")


# -------------------------
# TAB 4: SIMPLE VISUALIZER
# -------------------------

# ----- Blockchain Visualizer -----
with tab4:
    st.header("Blockchain Visualizer")
    st.write(f"Graphical representation of blocks and links (chain length: {len(blockchain.chain)})")

    rows = blockchain.to_list_of_dicts()

    # Fix: Safe check (avoids off-by-one and empty list errors)
    if not rows:
        st.warning("No blocks to visualize yet.")
    else:
        html = "<div style='display:flex;align-items:center;flex-wrap:wrap;'>"
        for i, b in enumerate(rows):
            html += f"""
            <div style='border:2px solid #FFD300;border-radius:10px;padding:12px;margin-right:16px;min-width:240px;background:#111111;color:#FFD300;box-shadow:0px 0px 10px #FFD300;'>
                <b style='font-size:16px;'>Block {b['index']}</b><br/>
                <small>Patient: {b['patient_id']}</small><br/>
                <small>Hash: {b['hash'][:12]}...</small><br/>
                <small>Prev: {b['previous_hash'][:12]}...</small><br/>
                <small>Uploader: {b['uploader']}</small><br/>
                <small>Time: {b['timestamp']}</small>
            </div>
            """

            # Corrected condition
            if i < len(rows) - 1:
                html += "<div style='font-size:32px;margin-right:16px;color:#FFD300;'>➡️</div>"

        html += "</div>"

        st.components.v1.html(html, height=260)

    # Table view
    df = pd.DataFrame(rows)
    st.subheader("Detailed Block Table")
    st.dataframe(df, use_container_width=True)

    valid, msg = blockchain.is_valid_chain()
    if valid:
        st.success("Chain validation: " + msg)
    else:
        st.error("Chain error: " + msg)

# -------------------------
# FOOTER
# -------------------------

st.markdown("---")
st.markdown(
    """
**How this implements your assignment:**

- Uses a **Solidity smart contract** on a **local Ethereum-like blockchain (Hardhat)**.
- Implements `addReport`, `getReport`, `grantAccess`, and `revokeAccess`.
- Stores **only file hashes** on-chain for privacy.
- Enforces **access control** inside `getReport`.
- Visualizes stored reports from contract in a chain-like UI.
"""
)
st.write("Upload report file below:")
