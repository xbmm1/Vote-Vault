import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd 

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Streamlit App
st.title("Vote Vault")

# Set the default account (use your own account address)
# Input Ethereum Account Address
eth_account_address = st.text_input("Enter Your Ethereum Account Address (Ganache Account):")
w3.eth.defaultAccount = eth_account_address

#w3.eth.defaultAccount = "0x0251224033eAC627bA58948f63AF0f7b9958CA57"  # Replace with your Ethereum account address

# Cache the contract on load
@st.cache_resource #(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load vote contract ABI
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

# Check if session state exists, if not, create an empty dictionary
if "session_state" not in st.session_state:
    st.session_state.session_state = {}

# Load the contract
contract = None
try:
    contract = load_contract()
except ValueError as e:
    st.error("Error loading contract. Please ensure the Smart Contract Address is valid.")

# Input fields for user information
name = st.text_input("Enter your Name:")
age = st.number_input("Enter your Age:", min_value=18, max_value=100)


# Register as a voter
if st.button("Register as Voter"):
    if age:
        tx_hash = contract.functions.registerVoter(age).transact({"from": w3.eth.defaultAccount})
        st.success("You are now registered as a voter. Transaction Hash: " + tx_hash.hex())

vote_choice = st.radio("Vote Choice:", ("Candidate A", "Candidate B", "Candidate C"))

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
                st.balloons()
        else:
            st.error("You must be 18 years or older to vote.")
    else:
        st.error("Please fill in all the information before casting your vote.")
        
# Create a button in the sidebar to log in as an admin
if not st.session_state.get("logged_in"):
    admin_username = st.sidebar.text_input("Username")
    admin_password = st.sidebar.text_input("Password", type="password")

    # Check if the admin credentials are correct (you should implement your own validation logic here)
    if admin_username == "admin" and admin_password == "admin123":
        st.session_state.logged_in = True
        st.success("Login successful! You are now logged in as an admin.")
        st.snow()
    else:
        b = 42#st.success("Please login to view results.")
        
def get_results_df():
    vote_counts = {}
    candidates = ["Candidate A", "Candidate B", "Candidate C"]
    for candidate in candidates:
        vote_counts[candidate] = contract.functions.voteCount(candidate).call()

    # Create a DataFrame to store the results
    results_df = pd.DataFrame(vote_counts.items(), columns=["Candidate", "Vote Count"])
    
    # Save the DataFrame to a CSV file
    results_df.to_csv("voting_results.csv", index=False)
    
    return results_df
    
# If logged in as an admin, display the results or any other admin-specific content here
if st.session_state.get("logged_in"):
    st.subheader("Voting Results")
    # Add code to display the voting results
    
    # Define a variable to store the voting results DataFrame
    results_df = None
    
    # Button to trigger vote count function
    if st.button("Get Vote Count"):
        results_df = get_results_df()

        # Display the voting results as a bar chart
        st.bar_chart(results_df.set_index("Candidate"))

        # Display the vote counts as text
        st.write("Vote Counts:")
        for candidate, count in results_df.values:
            st.write(f"{candidate}: {count}")
        
    # Button to save results to CSV
    if st.button("Save Results to CSV") and results_df is not None:
        
        # Save the results to the custom CSV file name provided by the user
        results_df.to_csv(csv_file_name, index=False)
        st.success(f"Voting results saved to '{csv_file_name}'.")
    
# Load the image from a local file
image_path = "images/voteA.png"  # Replace with the actual path to your image
st.image(image_path, width=5, use_column_width=True)