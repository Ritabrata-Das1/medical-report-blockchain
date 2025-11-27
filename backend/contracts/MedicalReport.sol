// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalReport {

    struct Report {
        string patientId;
        string reportHash;
        string description;
        uint timestamp;
        address uploader;
    }

    Report[] public reports;

    mapping (string => mapping(address => bool)) public permission;

    function addReport(string memory patientId, string memory reportHash, string memory description) public {
        reports.push(Report(patientId, reportHash, description, block.timestamp, msg.sender));
    }

    function grantAccess(string memory patientId, address doctor) public {
        permission[patientId][doctor] = true;
    }

    function revokeAccess(string memory patientId, address doctor) public {
        permission[patientId][doctor] = false;
    }

    function getReport(uint index) public view returns (Report memory) {
        Report memory r = reports[index];
        require(permission[r.patientId][msg.sender] || msg.sender == r.uploader, "No Access");
        return r;
    }
}
