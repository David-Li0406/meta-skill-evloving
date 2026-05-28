/**
 * Transaction broadcast utilities
 */

import { Transaction, PrivateKey, P2PKH } from "@bsv/sdk";

const WOC_BROADCAST_URL = "https://api.whatsonchain.com/v1/bsv/main/tx/raw";

export interface Utxo {
  txid: string;
  vout: number;
  satoshis: number;
  script: string;
}

export async function fetchUtxos(address: string): Promise<Utxo[]> {
  const response = await fetch(
    `https://api.whatsonchain.com/v1/bsv/main/address/${address}/unspent`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch UTXOs: ${response.status}`);
  }

  const data = await response.json();
  return data.map((u: { tx_hash: string; tx_pos: number; value: number }) => ({
    txid: u.tx_hash,
    vout: u.tx_pos,
    satoshis: u.value,
    script: "", // Will be set when building tx
  }));
}

export async function broadcastTx(txHex: string): Promise<string> {
  const response = await fetch(WOC_BROADCAST_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ txhex: txHex }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Broadcast failed: ${text}`);
  }

  const txid = await response.text();
  return txid.replace(/"/g, "");
}

export async function fundAndBroadcast(
  tx: Transaction,
  privateKey: PrivateKey,
  feeRate = 1
): Promise<string> {
  const address = privateKey.toAddress().toString();
  const utxos = await fetchUtxos(address);

  if (utxos.length === 0) {
    throw new Error(`No UTXOs found for address ${address}`);
  }

  // Calculate fee (estimate based on tx size + input size)
  const baseFee = Math.ceil(tx.toBinary().length * feeRate);
  const inputFee = 150 * feeRate; // ~150 bytes per input
  const outputFee = 34 * feeRate; // ~34 bytes for change output
  const estimatedFee = baseFee + inputFee + outputFee + 50; // buffer

  // Find enough UTXOs
  let totalInput = 0;
  const selectedUtxos: Utxo[] = [];

  for (const utxo of utxos) {
    selectedUtxos.push(utxo);
    totalInput += utxo.satoshis;
    if (totalInput >= estimatedFee) break;
  }

  if (totalInput < estimatedFee) {
    throw new Error(
      `Insufficient funds: have ${totalInput}, need ${estimatedFee}`
    );
  }

  // Add inputs
  for (const utxo of selectedUtxos) {
    tx.addInput({
      sourceTXID: utxo.txid,
      sourceOutputIndex: utxo.vout,
      unlockingScriptTemplate: new P2PKH().unlock(privateKey),
      sequence: 0xffffffff,
    });
  }

  // Add change output if needed
  const change = totalInput - estimatedFee;
  if (change > 546) {
    // dust threshold
    tx.addOutput({
      lockingScript: new P2PKH().lock(address),
      satoshis: change,
    });
  }

  // Sign and broadcast
  await tx.sign();
  const txHex = tx.toHex();
  return broadcastTx(txHex);
}
