import freighterApi from "@stellar/freighter-api";
import * as StellarSdk from "stellar-sdk";

export interface WalletProvider {
  name: string;
  isInstalled: () => Promise<boolean>;
  connect: () => Promise<string>;
  sign: (xdr: string, network: string) => Promise<string>;
  getPublicKey: () => Promise<string>;
}

export const WalletProviders: { [key: string]: WalletProvider } = {
  FREIGHTER: {
    name: "Freighter",
    isInstalled: async () => {
      try {
        await freighterApi.isConnected();
        return true;
      } catch {
        return false;
      }
    },
    connect: async () => {
      try {
        const isConnected = await freighterApi.isConnected();
        if (!isConnected) {
          throw new Error("Please install Freighter wallet");
        }

        // Get the current network
        const network = await freighterApi.getNetwork();
        if (network !== "TESTNET") {
          throw new Error("Please switch to TESTNET in Freighter wallet settings");
        }
        
        const isAllowed = await freighterApi.isAllowed();
        if (!isAllowed) {
          // This will trigger the permission popup
          const publicKey = await freighterApi.getPublicKey();
          if (!publicKey) {
            throw new Error("Permission denied");
          }
        }

        const publicKey = await freighterApi.getPublicKey();
        if (!publicKey) {
          throw new Error("Failed to get public key from Freighter");
        }

        return publicKey;
      } catch (error) {
        console.error("Freighter connect error:", error);
        throw error;
      }
    },
    sign: async (xdr: string, network: string) => {
      try {
        return await freighterApi.signTransaction(xdr, { networkPassphrase: network });
      } catch (error) {
        console.error("Freighter sign error:", error);
        throw new Error("Failed to sign transaction with Freighter");
      }
    },
    getPublicKey: async () => {
      const publicKey = await freighterApi.getPublicKey();
      if (!publicKey) {
        throw new Error("No public key available from Freighter");
      }
      return publicKey;
    }
  },
  // ... rest of the wallet providers remain the same ...
};

declare global {
  interface Window {
    xBull?: any;
    rabet?: any;
  }
} 