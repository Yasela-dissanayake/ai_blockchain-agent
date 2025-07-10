import { ethers } from "ethers";
import { JsonRpcProvider } from "ethers";
import * as dotenv from "dotenv";
import { saveVehicleToDB } from "../offchain/saveVehicleToDB";
import * as crypto from "crypto";
dotenv.config();

// ✅ Correct contract address (Deployed on Tenderly)
const contractAddress = "0x28234bcb8625184d8bd1a3bdfbaa787ccd73e57d";

// ✅ ABI
const abi = [
  {
    inputs: [
      { internalType: "string", name: "_regNum", type: "string" },
      { internalType: "string", name: "_make", type: "string" },
      { internalType: "string", name: "_model", type: "string" },
      { internalType: "string", name: "_chassisHash", type: "string" },
    ],
    name: "registerVehicle",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
];

// ✅ Proper URL, not the contract address
const provider = new JsonRpcProvider(process.env.WEB3_PROVIDER);

const privateKey = process.env.PRIVATE_KEY;
if (!privateKey) {
  throw new Error("❌ PRIVATE_KEY is not defined in environment variables.");
}

const wallet = new ethers.Wallet(privateKey, provider);
const vehicleContract = new ethers.Contract(contractAddress, abi, wallet);

async function registerVehicle() {
  const vehicleData = {
    registration_number: "VH005",
    make: "Toyota",
    model: "Corolla",
    chassis_number: "VBFDC4353",
    owner_name: "Bimsara Karunarathne",
    national_id: "19991234567",
    address: "234, Galle Road, Colombo",
    contact: "0773442398",
  };

  await saveVehicleToDB(vehicleData);

  // Hash the chassis number for blockchain storage
  // const chassisHash = crypto
  //   .createHash("sha256")
  //   .update(vehicleData.chassis_number)
  //   .digest("hex");

  try {
    const tx = await vehicleContract.registerVehicle(
      vehicleData.registration_number,
      vehicleData.make,
      vehicleData.model
    );
    console.log("⏳ Transaction sent. Waiting for confirmation...");
    await tx.wait();
    console.log("✅ Vehicle registered!");
    console.log(`🔗 Tx hash: ${tx.hash}`);
  } catch (error: any) {
    console.error("❌ Error registering vehicle:", error.message);
  }
}

registerVehicle();
