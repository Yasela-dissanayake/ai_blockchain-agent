import { client } from "./db";
import { encrypt } from "./encryption";

export async function saveVehicleToDB(data: {
  registration_number: string;
  chassis_number: string;
  owner_name: string;
  national_id: string;
  address: string;
  contact: string;
}) {
  await client.connect();

  const encryptedChassis = encrypt(data.chassis_number);

  const query = `
    INSERT INTO vehicles (registration_number, chassis_number, owner_name, national_id, address, contact)
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING *;
  `;

  const values = [
    data.registration_number,
    encryptedChassis,
    data.owner_name,
    data.national_id,
    data.address,
    data.contact,
  ];

  const res = await client.query(query, values);
  await client.end();
  return res.rows[0];
}
