import { ethers } from "ethers";
import { JsonRpcProvider } from "ethers";
import * as dotenv from "dotenv";
dotenv.config();

// ✅ Correct contract address (Deployed on Tenderly)
const contractAddress = "0x28234bcb8625184d8bd1a3bdfbaa787ccd73e57d";

// ✅ ABI
const abi = [
  {
    inputs: [
      { internalType: "string", name: "_regNum", type: "string" },
      { internalType: "string", name: "_owner", type: "string" },
      { internalType: "string", name: "_make", type: "string" },
      { internalType: "string", name: "_model", type: "string" },
    ],
    name: "registerVehicle",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
];

// ✅ Proper URL, not the contract address
const provider = new JsonRpcProvider(
  "https://virtual.sepolia.rpc.tenderly.co/6169cb69-02b6-4536-a17b-498a3f5c0926"
);

const privateKey = process.env.PRIVATE_KEY;
if (!privateKey) {
  throw new Error("❌ PRIVATE_KEY is not defined in environment variables.");
}

const wallet = new ethers.Wallet(privateKey, provider);
const vehicleContract = new ethers.Contract(contractAddress, abi, wallet);

async function registerVehicle() {
  const regNum = "VH003";
  const owner = "Kumudu Dissanayake";
  const make = "TVS";
  const model = "Scooty pept";

  try {
    const tx = await vehicleContract.registerVehicle(
      regNum,
      owner,
      make,
      model
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
