import streamlit as st
from web3 import Web3, HTTPProvider
from eth_account import Account

# Define the address and ABI of the deployed VotingBallot contract on the local Ganache test network
contract_address = "0x......."  # Replace with the actual contract address
contract_abi = [...]  # Replace with the actual contract ABI

# Connect to the local Ganache test network
ganache_url = "http://localhost:8545"  # Update with your Ganache URL
w3 = Web3(HTTPProvider(ganache_url))

# Load the VotingBallot contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Streamlit App
st.title("Voting Ballot")

# Input fields for user information
name = st.text_input("Enter your Name:")
age = st.number_input("Enter your Age:", min_value=18, max_value=100)
vote_choice = st.radio("Vote Choice:", ("Candidate A", "Candidate B", "Candidate C"))

# Register as a voter
if st.button("Register as Voter"):
    if age >= 18:
        # Register the voter by calling the contract function
        account = Account.create()
        private_key = account.privateKey.hex()
        nonce = w3.eth.getTransactionCount(account.address)
        tx = contract.functions.registerVoter(age).buildTransaction({
            'gas': 2000000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'chainId': 5777,  # Replace with the chainId of your network
            'nonce': nonce,
        })
        signed_tx = w3.eth.account.signTransaction(tx, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        st.success("You have been registered as a voter! Transaction Hash: " + tx_hash.hex())
    else:
        st.error("You must be 18 years or older to register as a voter.")

# Submit button to cast the vote
if st.button("Cast Vote"):
    if name and age and vote_choice:
        # Check if the user is eligible to vote (age >= 18)
        if age >= 18:
            # Cast the vote by calling the contract function
            account = Account.create()
            private_key = account.privateKey.hex()
            nonce = w3.eth.getTransactionCount(account.address)
            tx = contract.functions.castVote(vote_choice).buildTransaction({
                'gas': 2000000,
                'gasPrice': w3.toWei('40', 'gwei'),
                'chainId': 5777,  # Replace with the chainId of your network
                'nonce': nonce,
            })
            signed_tx = w3.eth.account.signTransaction(tx, private_key)
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            st.success("Vote successfully cast! Transaction Hash: " + tx_hash.hex())
        else:
            st.error("You must be 18 years or older to vote.")
    else:
        st.error("Please fill in all the information before casting your vote.")
