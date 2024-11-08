import * as StellarSdk from 'stellar-sdk';
import freighterApi from "@stellar/freighter-api";

export class StellarWallet {
  private server: StellarSdk.Server;

  constructor() {
    this.server = new StellarSdk.Server("https://horizon-testnet.stellar.org");
  }

  async connect(providerName: string) {
    try {
      // First check if Freighter is connected
      const isConnected = await freighterApi.isConnected();
      if (!isConnected) {
        throw new Error("Please install Freighter wallet");
      }

      // Check if we have permission
      const isAllowed = await freighterApi.isAllowed();
      
      if (!isAllowed) {
        // Request permission if not already granted
        await freighterApi.getPublicKey();
      }

      // Get the public key
      const publicKey = await freighterApi.getPublicKey();
      if (!publicKey) {
        throw new Error("Failed to get public key");
      }

      return {
        address: publicKey,
        publicKey: publicKey,
      };
    } catch (error) {
      console.error("Failed to connect wallet:", error);
      throw error;
    }
  }

  async getBalance() {
    try {
      const publicKey = await freighterApi.getPublicKey();
      if (!publicKey) {
        throw new Error("Wallet not connected");
      }

      const account = await this.server.loadAccount(publicKey);
      const balance = account.balances.find((b: any) => b.asset_type === 'native')?.balance || '0';
      return balance;
    } catch (error) {
      console.error("Failed to get balance:", error);
      throw error;
    }
  }

  async sendPayment(destination: string, amount: string) {
    try {
      const sourcePublicKey = await freighterApi.getPublicKey();
      if (!sourcePublicKey) {
        throw new Error("Wallet not connected");
      }

      // Load the source account
      const sourceAccount = await this.server.loadAccount(sourcePublicKey);

      // Build the transaction
      const transaction = new StellarSdk.TransactionBuilder(sourceAccount, {
        fee: StellarSdk.BASE_FEE,
        networkPassphrase: StellarSdk.Networks.TESTNET
      })
        .addOperation(StellarSdk.Operation.payment({
          destination,
          asset: StellarSdk.Asset.native(),
          amount: amount.toString()
        }))
        .setTimeout(180)
        .build();

      // Sign the transaction
      const xdr = transaction.toXDR();
      const signedXDR = await freighterApi.signTransaction(xdr, {
        networkPassphrase: StellarSdk.Networks.TESTNET
      });

      // Submit the signed transaction
      const tx = StellarSdk.TransactionBuilder.fromXDR(
        signedXDR,
        StellarSdk.Networks.TESTNET
      );
      
      const result = await this.server.submitTransaction(tx);
      return result;
    } catch (error) {
      console.error("Failed to send payment:", error);
      throw error;
    }
  }

  async disconnect() {
    try {
      // Clear any stored state
      localStorage.removeItem('stellar_wallet_connected');
      return true;
    } catch (error) {
      console.error("Failed to disconnect wallet:", error);
      throw error;
    }
  }

  async addTrustline(assetCode: string, issuerAddress: string) {
    try {
      const publicKey = await freighterApi.getPublicKey();
      if (!publicKey) {
        throw new Error("Wallet not connected");
      }

      // Load the source account
      const sourceAccount = await this.server.loadAccount(publicKey);

      // Create the custom asset
      const asset = new StellarSdk.Asset(assetCode, issuerAddress);

      // Build the changeTrust transaction
      const transaction = new StellarSdk.TransactionBuilder(sourceAccount, {
        fee: StellarSdk.BASE_FEE,
        networkPassphrase: StellarSdk.Networks.TESTNET,
      })
        .addOperation(
          StellarSdk.Operation.changeTrust({
            asset: asset,
          }),
        )
        .setTimeout(180)
        .build();

      // Convert transaction to XDR
      const xdr = transaction.toXDR();

      // Sign the transaction using Freighter
      const signedXDR = await freighterApi.signTransaction(xdr, {
        networkPassphrase: StellarSdk.Networks.TESTNET,
      });

      // Submit the signed transaction
      const tx = StellarSdk.TransactionBuilder.fromXDR(
        signedXDR,
        StellarSdk.Networks.TESTNET
      );
      const result = await this.server.submitTransaction(tx);
      return result;

    } catch (error) {
      console.error("Failed to add trustline:", error);
      throw error;
    }
  }
}

export const stellarWallet = new StellarWallet();
