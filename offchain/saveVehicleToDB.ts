import { supabase } from "./supabaseClient";
import { encrypt } from "./encryption";

export async function saveVehicleToDB(data: {
  registration_number: string;
  make: string;
  model: string;
  chassis_number: string;
  owner_name: string;
  national_id: string;
  address: string;
  contact: string;
}) {
  const encryptedChassis = encrypt(data.chassis_number);
  const encryptedOwner = encrypt(data.owner_name);
  const encryptedNIC = encrypt(data.national_id);
  const encryptedAdress = encrypt(data.address);
  const encrypteContact = encrypt(data.contact);

  const { data: inserted, error } = await supabase
    .from("vehicles")
    .insert([
      {
        chassis_number: encryptedChassis,
        owner_name: encryptedOwner,
        national_id: encryptedNIC,
        address: encryptedAdress,
        contact: encrypteContact,
      },
    ])
    .select();

  if (error) {
    console.error("Failed to insert:", error.message);
    throw error;
  }

  return inserted?.[0];
}
