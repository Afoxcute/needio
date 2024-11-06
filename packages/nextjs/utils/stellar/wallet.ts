import { Wallet } from "@stellar/typescript-wallet-sdk";
import Networks from "@stellar/typescript-wallet-sdk";

export class StellarWallet {
  private wallet: Wallet;
  constructor() {
    this.wallet = new Wallet({ network: "TESTNET" }); // Use TESTNET for development
  }

  async connect() {
    try {
      await this.wallet.connect();
      return {
        address: this.wallet.address,
        publicKey: this.wallet.publicKey,
      };
    } catch (error) {
      console.error("Failed to connect wallet:", error);
      throw error;
    }
  }

  async getBalance() {
    try {
      const balance = await this.wallet.getBalance();
      return balance;
    } catch (error) {
      console.error("Failed to get balance:", error);
      throw error;
    }
  }

  async sendPayment(destination: string, amount: string) {
    try {
      const transaction = await this.wallet.sendPayment({
        destination,
        amount,
        asset: "native", // XLM
      });
      return transaction;
    } catch (error) {
      console.error("Failed to send payment:", error);
      throw error;
    }
  }
}

export const stellarWallet = new StellarWallet();
