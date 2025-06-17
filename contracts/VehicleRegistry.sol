// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract VehicleRegistry {
    struct Vehicle {
        string registrationNumber;
        string hash;
    }

    struct VehicleNode {
        string prev;
        string next;
        bool exists;
    }

    mapping(string => Vehicle) public vehicles;
    mapping(string => VehicleNode) private vehicleLinks;

    string[] public registrationNumbers;
    string public head;
    string public tail;
    uint256 public vehicleCount;

    event VehicleRegistered(string indexed registrationNumber, string hash);
    event VehicleTransferred(string indexed registrationNumber, string oldOwner, string newOwner);

    function registerVehicle(
        string memory _regNum,
        string memory _hash
    ) public {
        require(bytes(vehicles[_regNum].registrationNumber).length == 0, "Vehicle already registered");

        vehicles[_regNum] = Vehicle(_regNum, _hash);
        registrationNumbers.push(_regNum);

        // Linked list logic
        if (vehicleCount == 0) {
            head = _regNum;
            tail = _regNum;
        } else {
            vehicleLinks[tail].next = _regNum;
            vehicleLinks[_regNum].prev = tail;
            tail = _regNum;
        }

        vehicleLinks[_regNum].exists = true;
        vehicleCount++;

        emit VehicleRegistered(_regNum, _hash);
    }

    // function transferVehicle(string memory _regNum, string memory _newOwner) public {
    //     require(bytes(vehicles[_regNum].registrationNumber).length > 0, "Vehicle not found");

    //     string memory oldOwner = vehicles[_regNum].owner;
    //     vehicles[_regNum].owner = _newOwner;

    //     emit VehicleTransferred(_regNum, oldOwner, _newOwner);
    // }

    // === Doubly Linked List Traversal Functions ===
    function getNextVehicle(string memory _regNum) public view returns (string memory) {
        require(vehicleLinks[_regNum].exists, "Vehicle not found");
        return vehicleLinks[_regNum].next;
    }

    function getPreviousVehicle(string memory _regNum) public view returns (string memory) {
        require(vehicleLinks[_regNum].exists, "Vehicle not found");
        return vehicleLinks[_regNum].prev;
    }

    function getFirstVehicle() public view returns (string memory) {
        return head;
    }

    function getLastVehicle() public view returns (string memory) {
        return tail;
    }

    // === Original AI helper functions ===
    function getAllRegistrationNumbers() public view returns (string[] memory) {
        return registrationNumbers;
    }

    function getVehicleCount() public view returns (uint256) {
        return registrationNumbers.length;
    }

    function getVehicleDetails(string memory _regNum) public view returns (
        string memory registrationNumber,
        string memory hash
    ) {
        Vehicle memory vehicle = vehicles[_regNum];
        return (vehicle.registrationNumber, vehicle.hash);
    }

    function getVehicleHash(string memory _regNum) public view returns (string memory) {
        return vehicles[_regNum].hash;
    }

    function getVehicleOwner(string memory _regNum) public view returns (string memory) {
        require(vehicleExists(_regNum), "Vehicle not found");
        return vehicles[_regNum].hash;
    }

    function vehicleExists(string memory _regNum) public view returns (bool) {
        return bytes(vehicles[_regNum].registrationNumber).length > 0;
    }
}
