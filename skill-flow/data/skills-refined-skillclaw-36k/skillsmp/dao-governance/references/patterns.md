# DAO Governance Engineer

## Patterns


---
  #### **Id**
openzeppelin-governor
  #### **Name**
OpenZeppelin Governor Implementation
  #### **Description**
    Standard on-chain governance using OpenZeppelin's modular
    Governor contract system
    
  #### **When To Use**
    - Full on-chain execution required
    - High-stakes protocol decisions
    - Binding treasury transactions
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    import "@openzeppelin/contracts/governance/Governor.sol";
    import "@openzeppelin/contracts/governance/extensions/GovernorSettings.sol";
    import "@openzeppelin/contracts/governance/extensions/GovernorCountingSimple.sol";
    import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";
    import "@openzeppelin/contracts/governance/extensions/GovernorVotesQuorumFraction.sol";
    import "@openzeppelin/contracts/governance/extensions/GovernorTimelockControl.sol";
    
    contract ProtocolGovernor is
        Governor,
        GovernorSettings,
        GovernorCountingSimple,
        GovernorVotes,
        GovernorVotesQuorumFraction,
        GovernorTimelockControl
    {
        constructor(
            IVotes _token,
            TimelockController _timelock
        )
            Governor("Protocol Governor")
            GovernorSettings(
                7200,      // votingDelay: ~1 day in blocks
                50400,     // votingPeriod: ~1 week in blocks
                100000e18  // proposalThreshold: 100k tokens to propose
            )
            GovernorVotes(_token)
            GovernorVotesQuorumFraction(4) // 4% quorum
            GovernorTimelockControl(_timelock)
        {}
    
        // Required overrides for multiple inheritance
        function votingDelay() public view override(Governor, GovernorSettings)
            returns (uint256)
        {
            return super.votingDelay();
        }
    
        function votingPeriod() public view override(Governor, GovernorSettings)
            returns (uint256)
        {
            return super.votingPeriod();
        }
    
        function quorum(uint256 blockNumber)
            public view override(Governor, GovernorVotesQuorumFraction)
            returns (uint256)
        {
            return super.quorum(blockNumber);
        }
    
        function state(uint256 proposalId)
            public view override(Governor, GovernorTimelockControl)
            returns (ProposalState)
        {
            return super.state(proposalId);
        }
    
        function proposalThreshold()
            public view override(Governor, GovernorSettings)
            returns (uint256)
        {
            return super.proposalThreshold();
        }
    
        function _queueOperations(
            uint256 proposalId,
            address[] memory targets,
            uint256[] memory values,
            bytes[] memory calldatas,
            bytes32 descriptionHash
        ) internal override(Governor, GovernorTimelockControl) returns (uint48) {
            return super._queueOperations(proposalId, targets, values, calldatas, descriptionHash);
        }
    
        function _executeOperations(
            uint256 proposalId,
            address[] memory targets,
            uint256[] memory values,
            bytes[] memory calldatas,
            bytes32 descriptionHash
        ) internal override(Governor, GovernorTimelockControl) {
            super._executeOperations(proposalId, targets, values, calldatas, descriptionHash);
        }
    
        function _cancel(
            address[] memory targets,
            uint256[] memory values,
            bytes[] memory calldatas,
            bytes32 descriptionHash
        ) internal override(Governor, GovernorTimelockControl) returns (uint256) {
            return super._cancel(targets, values, calldatas, descriptionHash);
        }
    
        function _executor()
            internal view override(Governor, GovernorTimelockControl)
            returns (address)
        {
            return super._executor();
        }
    }
    
  #### **Security Notes**
    - Use Timelock for all executions
    - Set reasonable proposal thresholds
    - Monitor for flash loan attacks

---
  #### **Id**
snapshot-governance
  #### **Name**
Snapshot Off-Chain Voting
  #### **Description**
    Gas-free off-chain voting using Snapshot with optional
    on-chain execution via SafeSnap
    
  #### **When To Use**
    - High voting participation needed
    - Gas costs are a barrier
    - Signaling votes before on-chain
  #### **Implementation**
    Snapshot Space Configuration (space.json):
    {
      "name": "Protocol DAO",
      "network": "1",
      "symbol": "PROTO",
      "strategies": [
        {
          "name": "erc20-balance-of",
          "params": {
            "address": "0x...",
            "decimals": 18
          }
        },
        {
          "name": "delegation",
          "params": {
            "strategies": [
              {
                "name": "erc20-balance-of",
                "params": { "address": "0x..." }
              }
            ]
          }
        }
      ],
      "members": [],
      "admins": ["0xAdmin1", "0xAdmin2"],
      "filters": {
        "minScore": 100,
        "onlyMembers": false
      },
      "validation": {
        "name": "basic",
        "params": {
          "minScore": 100
        }
      },
      "voting": {
        "delay": 86400,
        "period": 604800,
        "type": "single-choice",
        "quorum": 1000000
      },
      "plugins": {
        "safeSnap": {
          "safes": {
            "1": { "address": "0xGnosisSafe..." }
          }
        }
      }
    }
    
    Proposal Lifecycle:
    1. Draft proposal in forum
    2. Community discussion (3-7 days)
    3. Create Snapshot vote
    4. Voting period (5-7 days)
    5. If passed + SafeSnap: queue transactions
    6. Execute via Gnosis Safe
    
  #### **Security Notes**
    - Snapshot votes are NOT binding by default
    - Use SafeSnap for on-chain execution
    - Verify voting strategy prevents manipulation

---
  #### **Id**
vetoken-governance
  #### **Name**
Vote-Escrowed Token (veToken) Model
  #### **Description**
    Curve-style voting power based on lock duration,
    aligning long-term incentives with governance
    
  #### **When To Use**
    - Rewarding long-term holders
    - Reducing mercenary capital influence
    - Complex token utility (gauges, bribes)
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
    import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
    
    contract VotingEscrow {
        using SafeERC20 for IERC20;
    
        struct LockedBalance {
            uint256 amount;
            uint256 end;
        }
    
        IERC20 public immutable token;
        uint256 public constant MAXTIME = 4 * 365 days;
        uint256 public constant WEEK = 7 days;
    
        mapping(address => LockedBalance) public locked;
        uint256 public totalLocked;
    
        event Deposit(address indexed user, uint256 amount, uint256 lockTime);
        event Withdraw(address indexed user, uint256 amount);
    
        constructor(address _token) {
            token = IERC20(_token);
        }
    
        function createLock(uint256 amount, uint256 unlockTime) external {
            require(amount > 0, "Amount must be > 0");
            require(locked[msg.sender].amount == 0, "Existing lock");
    
            uint256 roundedUnlock = (unlockTime / WEEK) * WEEK;
            require(roundedUnlock > block.timestamp, "Must be future");
            require(roundedUnlock <= block.timestamp + MAXTIME, "Max 4 years");
    
            token.safeTransferFrom(msg.sender, address(this), amount);
    
            locked[msg.sender] = LockedBalance({
                amount: amount,
                end: roundedUnlock
            });
            totalLocked += amount;
    
            emit Deposit(msg.sender, amount, roundedUnlock);
        }
    
        function withdraw() external {
            LockedBalance memory lock = locked[msg.sender];
            require(lock.amount > 0, "No lock");
            require(block.timestamp >= lock.end, "Lock not expired");
    
            uint256 amount = lock.amount;
            delete locked[msg.sender];
            totalLocked -= amount;
    
            token.safeTransfer(msg.sender, amount);
            emit Withdraw(msg.sender, amount);
        }
    
        function votingPower(address user) public view returns (uint256) {
            LockedBalance memory lock = locked[user];
            if (lock.end <= block.timestamp) return 0;
    
            // Linear decay: power = amount * (timeLeft / maxTime)
            uint256 timeLeft = lock.end - block.timestamp;
            return (lock.amount * timeLeft) / MAXTIME;
        }
    
        function totalVotingPower() external view returns (uint256) {
            // Simplified - production needs checkpoint system
            return totalLocked / 2; // Rough average
        }
    }
    
    veToken Benefits:
    - Longer lock = more voting power
    - Power decays as unlock approaches
    - Discourages short-term speculation
    - Enables gauge voting and bribes
    
  #### **Security Notes**
    - Implement checkpoint system for accurate totals
    - Consider early unlock penalty option
    - Watch for lock manipulation before votes

---
  #### **Id**
timelock-controller
  #### **Name**
Timelock for Governance Execution
  #### **Description**
    Mandatory delay between proposal passage and execution,
    allowing community to exit if they disagree
    
  #### **When To Use**
    - All on-chain governance execution
    - Protocol parameter changes
    - Treasury disbursements
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    import "@openzeppelin/contracts/governance/TimelockController.sol";
    
    // Deployment
    address[] memory proposers = new address[](1);
    proposers[0] = address(governor);
    
    address[] memory executors = new address[](1);
    executors[0] = address(0); // Anyone can execute after delay
    
    TimelockController timelock = new TimelockController(
        2 days,    // minDelay
        proposers,
        executors,
        address(0) // No admin (renounced)
    );
    
    Timelock Parameters:
    ┌──────────────────┬────────────────────────────────────┐
    │ Parameter        │ Recommendation                     │
    ├──────────────────┼────────────────────────────────────┤
    │ minDelay         │ 2-7 days for major protocols       │
    │ Proposers        │ Only Governor contract             │
    │ Executors        │ Anyone (after delay) or Governor   │
    │ Admin            │ Renounced (address(0))             │
    └──────────────────┴────────────────────────────────────┘
    
    Emergency Exceptions:
    - Separate Guardian role for critical security
    - Guardian can pause, NOT execute arbitrary code
    - Guardian is multi-sig with security council
    
  #### **Security Notes**
    - Never give admin role to EOA
    - Timelock should own all protocol contracts
    - Emergency guardian separate from governance

## Anti-Patterns


---
  #### **Id**
flash-loan-voting
  #### **Name**
Voting vulnerable to flash loans
  #### **Severity**
critical
  #### **Description**
    Voting power based on current balance allows flash loan
    attackers to borrow massive amounts, vote, then repay
    
  #### **Detection**
    - balanceOf() used directly for voting
    - No snapshot mechanism
    - Voting power computed at vote time
    
  #### **Consequence**
    Attacker can pass any proposal with borrowed tokens,
    completely subverting governance
    

---
  #### **Id**
no-timelock
  #### **Name**
Direct execution without timelock
  #### **Severity**
critical
  #### **Description**
    Proposals execute immediately after passing, giving no
    time for community to respond to malicious proposals
    
  #### **Detection**
    - Governor without TimelockController
    - execute() calls directly to protocol
    
  #### **Consequence**
    Malicious proposal drains treasury before community reacts
    

---
  #### **Id**
low-quorum
  #### **Name**
Quorum too low for security
  #### **Severity**
high
  #### **Description**
    Quorum below 2-4% allows small groups to pass proposals
    when participation is low
    
  #### **Detection**
    - Quorum < 2% of supply
    - No dynamic quorum adjustment
    
  #### **Consequence**
    Important decisions made by tiny minority
    

---
  #### **Id**
no-proposal-threshold
  #### **Name**
Anyone can create proposals
  #### **Severity**
medium
  #### **Description**
    No minimum token holding to propose leads to spam
    and governance fatigue
    
  #### **Detection**
    - proposalThreshold() returns 0
    - No proposal creation restrictions
    
  #### **Consequence**
    Governance flooded with low-quality proposals,
    voter fatigue, reduced participation
    