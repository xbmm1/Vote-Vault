# Vote-Vault 
<div style="text-align:left">
  <img src="Images/logoA.png" alt="Logo" width="80">
</div>

## votecoin.sol
* This contract defines a simple Voting Ballot where voters can register with their age and cast votes for different candidates. The contract keeps track of the number of votes each candidate receives and prevents multiple votes from the same address.
#
# vote.py
* Replace the contract_address and contract_abi with the actual values specific to your deployed VotingBallot.sol contract on the Ganache test network. Also, ensure you have installed the required Python packages (streamlit, web3, and eth_account) before running the program.

* This Streamlit app provides input fields for user information, such as name, age, and vote choice. Users can register as voters by clicking the "Register as Voter" button, and then cast their votes by clicking the "Cast Vote" button. The transactions are signed and sent using a newly generated Ethereum account.

* This program allows for a user to login in as a admin to view vote results and save them as a CSV file.

![picture 1](Images/voteA.png)
![picture 2](Images/logoA.png)
![An image shows a wallet with bitcoin.](Images/localhost.png)
