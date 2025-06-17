import crypto from "crypto";
import dotenv from "dotenv";
dotenv.config();

const algorithm = "aes-256-cbc";
const key = Buffer.from(process.env.AES_KEY || "", "hex");
const iv = crypto.randomBytes(16); // Can be saved with ciphertext

export function encrypt(text: string): string {
  const cipher = crypto.createCipheriv(algorithm, key, iv);
  let encrypted = cipher.update(text, "utf8", "hex");
  encrypted += cipher.final("hex");
  return iv.toString("hex") + ":" + encrypted;
}

export function decrypt(data: string): string {
  const [ivHex, encryptedText] = data.split(":");
  const decipher = crypto.createDecipheriv(
    algorithm,
    key,
    Buffer.from(ivHex, "hex")
  );
  let decrypted = decipher.update(encryptedText, "hex", "utf8");
  decrypted += decipher.final("utf8");
  return decrypted;
}
