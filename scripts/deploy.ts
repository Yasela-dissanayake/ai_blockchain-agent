const { ethers } = require("hardhat");

async function main() {
  // Get the contract to deploy
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // Deploy the contract
  const VehicleRegistry = await ethers.getContractFactory("VehicleRegistry");
  const vehicleRegistry = await VehicleRegistry.deploy();
  console.log(
    "VehicleRegistry contract deployed to:",
    vehicleRegistry.address
  );
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });