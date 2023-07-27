// SPDX-License-Identifier: MIT
pragma solidity ^0.5.0;

contract VotingBallot {
    struct Voter {
        uint256 age;
        string name;
        bool hasVoted;
    }

    mapping(address => Voter) public voters;
    mapping(string => uint256) public voteCount;

    event VoteCasted(address indexed voter, string indexed candidate);

    function castVote(string memory candidate) public {
        require(voters[msg.sender].age >= 18, "You must be 18 years or older to vote.");
        require(!voters[msg.sender].hasVoted, "You have already voted.");
        
        voteCount[candidate]++;
        voters[msg.sender].hasVoted = true;

        emit VoteCasted(msg.sender, candidate);
    }

    function registerVoter(uint256 _age) public {
        require(voters[msg.sender].age == 0, "You are already registered as a voter.");
        voters[msg.sender].age = _age;
    }
}
