import crypto from "crypto";
import dotenv from "dotenv";
dotenv.config();

const ALGORITHM = "aes-256-cbc";

// Must be 32 bytes (64 hex characters) for AES-256
const KEY = Buffer.from(process.env.AES_KEY!, "hex");

if (KEY.length !== 32) {
  throw new Error("AES_KEY must be a 32-byte (256-bit) hex string");
}

export function encrypt(data: string): string {
  const iv = crypto.randomBytes(16); // 16 bytes IV
  const cipher = crypto.createCipheriv(ALGORITHM, KEY, iv);

  let encrypted = cipher.update(data, "utf8", "hex");
  encrypted += cipher.final("hex");

  return iv.toString("hex") + ":" + encrypted;
}

export function decrypt(encryptedData: string): string {
  const [ivHex, encrypted] = encryptedData.split(":");

  if (!ivHex || !encrypted) {
    throw new Error("Invalid encrypted format. Expecting 'iv:encrypted'");
  }

  const iv = Buffer.from(ivHex, "hex");
  const decipher = crypto.createDecipheriv(ALGORITHM, KEY, iv);

  let decrypted = decipher.update(encrypted, "hex", "utf8");
  decrypted += decipher.final("utf8");

  return decrypted;
}
