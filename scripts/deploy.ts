import { ethers } from "hardhat";

async function main() {
    const [deployer] = await ethers.getSigners();
    const VehicleRegistry = await ethers.getContractFactory("VehicleRegistry");
    const vehicleRegistry = await VehicleRegistry.deploy();
    await vehicleRegistry.deployed();
    console.log("VehicleRegistry deployed to:", vehicleRegistry.address);
  }
  main();
  