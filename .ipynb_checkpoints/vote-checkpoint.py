import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Set the default account (use your own account address)
w3.eth.defaultAccount = "0xbFbF556e9a14B3bfF3b53a746d2FfA2e328E1702"  # Replace with your Ethereum account address
# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./compiled/abi.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    # Return the contract from the function
    return contract

# Load the contract
contract = load_contract()

# Streamlit App
st.title("Voting Ballot")

# Input fields for user information
name = st.text_input("Enter your Name:")
age = st.number_input("Enter your Age:", min_value=18, max_value=100)
vote_choice = st.radio("Vote Choice:", ("Candidate A", "Candidate B", "Candidate C"))

# Register as a voter
if st.button("Register as Voter"):
    if age:
        tx_hash = contract.functions.registerVoter(age).transact({"from": w3.eth.defaultAccount})
        st.success("You are now registered as a voter. Transaction Hash: " + tx_hash.hex())

# Cast the vote
if st.button("Cast Vote"):
    if name and vote_choice:
        # Check if the user is eligible to vote (age >= 18)
        if age >= 18:
            # Cast the vote by calling the contract function
            if not contract.functions.voters(w3.eth.defaultAccount).call():
                st.error("You must register as a voter first.")
            else:
                tx_hash = contract.functions.castVote(vote_choice).transact({"from": w3.eth.defaultAccount})
                st.success("Vote successfully cast! Transaction Hash: " + tx_hash.hex())
        else:
            st.error("You must be 18 years or older to vote.")
    else:
        st.error("Please fill in all the information before casting your vote.")