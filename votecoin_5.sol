pragma solidity ^0.5.0;

contract VotingBallot {
    struct Voter {
        uint256 age;
        string name;
        bool hasVoted;
    }

    mapping(address => Voter) public voters;
    mapping(string => uint256) public voteCount;

    event EventStarted(uint256 startTime);
    event EventStopped(uint256 stopTime);
    event VoteCasted(address indexed voter, string indexed candidate);

    bool public eventActive;
    uint256 public startTime;
    uint256 public stopTime;

    modifier onlyWhenEventActive() {
        require(eventActive, "Event is not active");
        _;
    }

    function startEvent() public {
        require(!eventActive, "Event is already active");
        eventActive = true;
        startTime = block.timestamp;
        emit EventStarted(startTime);
    }

    function stopEvent() public onlyWhenEventActive {
        eventActive = false;
        stopTime = block.timestamp;
        emit EventStopped(stopTime);
    }

    function castVote(string memory candidate) public onlyWhenEventActive {
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
