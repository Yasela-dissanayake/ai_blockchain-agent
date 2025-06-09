pragma solidity ^0.8.28;

contract VehicleRegistry {
    struct Vehicle {
        string registrationNumber;
        string owner;
        string make;
        string model;
    }
    mapping(string => Vehicle) public vehicles;
    function registerVehicle(
        string memory _regNum,
        string memory _owner,
        string memory _make,
        string memory _model
    ) public {
        vehicles[_regNum] = Vehicle(_regNum, _owner, _make, _model);
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
        vehicles[_regNum].owner = _newOwner;
    }
}
