// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract VehicleRegistry {
    struct Vehicle {
        string registrationNumber;
        string owner;
        string make;
        string model;
    }
    
    mapping(string => Vehicle) public vehicles;
    string[] public registrationNumbers; // Array to keep track of all registration numbers
    
    // Event for better tracking (optional)
    event VehicleRegistered(string indexed registrationNumber, string owner, string make, string model);
    event VehicleTransferred(string indexed registrationNumber, string oldOwner, string newOwner);
    
    function registerVehicle(
        string memory _regNum,
        string memory _owner,
        string memory _make,
        string memory _model
    ) public {
        // Check if vehicle already exists
        require(bytes(vehicles[_regNum].registrationNumber).length == 0, "Vehicle already registered");
        
        vehicles[_regNum] = Vehicle(_regNum, _owner, _make, _model);
        registrationNumbers.push(_regNum);
        
        emit VehicleRegistered(_regNum, _owner, _make, _model);
    }
    
    function getVehicleOwner(
        string memory _regNum
    ) public view returns (string memory) {
        return vehicles[_regNum].owner;
    }
    
    function transferVehicle(
        string memory _regNum,
        string memory _newOwner
    ) public {
        require(bytes(vehicles[_regNum].registrationNumber).length > 0, "Vehicle not found");
        
        string memory oldOwner = vehicles[_regNum].owner;
        vehicles[_regNum].owner = _newOwner;
        
        emit VehicleTransferred(_regNum, oldOwner, _newOwner);
    }
    
    // New functions to help with AI integration
    function getAllRegistrationNumbers() public view returns (string[] memory) {
        return registrationNumbers;
    }
    
    function getVehicleCount() public view returns (uint256) {
        return registrationNumbers.length;
    }
    
    function getVehicleDetails(string memory _regNum) public view returns (
        string memory registrationNumber,
        string memory owner,
        string memory make,
        string memory model
    ) {
        Vehicle memory vehicle = vehicles[_regNum];
        return (vehicle.registrationNumber, vehicle.owner, vehicle.make, vehicle.model);
    }
    
    function vehicleExists(string memory _regNum) public view returns (bool) {
        return bytes(vehicles[_regNum].registrationNumber).length > 0;
    }
}