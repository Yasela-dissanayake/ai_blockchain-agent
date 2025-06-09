import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import * as dotenv from "dotenv";

dotenv.config();

if (!process.env.PRIVATE_KEY) {
  throw new Error("Please set your PRIVATE_KEY in a .env file");
}

const config: HardhatUserConfig = {
  solidity: "0.8.28",
  networks: {
    tenderly: {
      url: "https://virtual.sepolia.rpc.tenderly.co/6169cb69-02b6-4536-a17b-498a3f5c0926",
      accounts: [process.env.PRIVATE_KEY],
    },
  },
};

export default config;
