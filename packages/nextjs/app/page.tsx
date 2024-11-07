"use client";

import { useEffect, useState } from "react";
import type { NextPage } from "next";
import { toast } from "react-hot-toast";
import { ArrowsRightLeftIcon, CurrencyDollarIcon, WalletIcon } from "@heroicons/react/24/outline";
import { StellarAddress } from "~~/components/stellar/Address";
import { stellarWallet } from "~~/utils/stellar/wallet";
import freighterApi from "@stellar/freighter-api";
import { AddTokenModal } from "~~/components/stellar/AddToken";

const Home: NextPage = () => {
  const [stellarAddress, setStellarAddress] = useState<string>("");
  const [balance, setBalance] = useState<string>("0");
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [recipientAddress, setRecipientAddress] = useState<string>("");
  const [amount, setAmount] = useState<string>("");
  const [isAddTokenModalOpen, setIsAddTokenModalOpen] = useState(false);

  const handleConnect = async () => {
    try {
      setIsLoading(true);
      
      // Connect wallet with provider name
      const { address } = await stellarWallet.connect("freighter");
      setStellarAddress(address);
      setIsConnected(true);
      
      // Get initial balance
      const balance = await stellarWallet.getBalance();
      setBalance(balance);
      
      toast.success("Wallet connected successfully!");
    } catch (error: any) {
      console.error("Failed to connect wallet:", error);
      toast.error(error.message || "Failed to connect wallet. Please try again!");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisconnect = async () => {
    try {
      await stellarWallet.disconnect();
      setStellarAddress("");
      setBalance("0");
      setIsConnected(false);
      toast.success("Wallet disconnected successfully!");
    } catch (error: any) {
      console.error("Failed to disconnect wallet:", error);
      toast.error(error.message || "Failed to disconnect wallet. Please try again!");
    }
  };

  const handleSend = async () => {
    if (!recipientAddress || !amount) {
      toast.error("Please fill in all fields");
      return;
    }

    try {
      setIsLoading(true);
      await stellarWallet.sendPayment(recipientAddress, amount);
      toast.success("Transaction sent successfully!");

      // Update balance
      const newBalance = await stellarWallet.getBalance();
      setBalance(newBalance);

      // Clear form
      setRecipientAddress("");
      setAmount("");
    } catch (error: any) {
      console.error("Failed to send payment:", error);
      toast.error(error.message || "Failed to send payment. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyAddress = () => {
    navigator.clipboard.writeText(stellarAddress);
    toast.success("Address copied to clipboard!");
  };

  return (
    <div className="flex items-center flex-col flex-grow pt-10">
      <div className="px-5">
        <h1 className="text-center">
          <span className="block text-4xl font-bold mb-2">Stellar Wallet</span>
          <span className="block text-xl text-gray-500">Send and receive XLM with ease</span>
        </h1>

        {!isConnected ? (
          <div className="mt-8 flex justify-center">
            <button
              className={`btn btn-primary btn-lg gap-2 ${isLoading ? "loading" : ""}`}
              onClick={handleConnect}
              disabled={isLoading}
            >
              <WalletIcon className="h-6 w-6" />
              {isLoading ? "Connecting..." : "Connect Wallet"}
            </button>
          </div>
        ) : (
          <div className="mt-8 flex flex-col items-center gap-4">
            <div className="stats shadow w-full max-w-md">
              <div className="stat">
                <div className="stat-title">Wallet Address</div>
                <div className="stat-value text-primary text-sm truncate">
                  <StellarAddress address={stellarAddress} />
                </div>
              </div>
              <div className="stat">
                <div className="stat-title">Balance</div>
                <div className="stat-value text-secondary">{balance} XLM</div>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                className="btn btn-primary btn-sm"
                onClick={() => setIsAddTokenModalOpen(true)}
              >
                Add Token
              </button>
              <button
                className="btn btn-secondary btn-sm"
                onClick={handleDisconnect}
              >
                Disconnect Wallet
              </button>
            </div>
          </div>
        )}
      </div>

      {isConnected && (
        <div className="flex-grow w-full mt-16 px-8 py-12">
          <div className="flex justify-center items-center gap-8 flex-col sm:flex-row">
            <div className="card w-96 bg-base-100 shadow-xl">
              <div className="card-body">
                <h2 className="card-title">
                  <ArrowsRightLeftIcon className="h-6 w-6 text-primary" />
                  Send XLM
                </h2>
                <div className="form-control">
                  <label className="label">
                    <span className="label-text">Recipient Address</span>
                  </label>
                  <input
                    type="text"
                    placeholder="G..."
                    className="input input-bordered w-full"
                    value={recipientAddress}
                    onChange={e => setRecipientAddress(e.target.value)}
                  />
                </div>
                <div className="form-control mt-4">
                  <label className="label">
                    <span className="label-text">Amount (XLM)</span>
                  </label>
                  <input
                    type="number"
                    placeholder="0.0"
                    className="input input-bordered w-full"
                    value={amount}
                    onChange={e => setAmount(e.target.value)}
                  />
                </div>
                <div className="card-actions justify-end mt-4">
                  <button
                    className={`btn btn-primary ${isLoading ? "loading" : ""}`}
                    onClick={handleSend}
                    disabled={isLoading}
                  >
                    {isLoading ? "Sending..." : "Send"}
                  </button>
                </div>
              </div>
            </div>

            <div className="card w-96 bg-base-100 shadow-xl">
              <div className="card-body">
                <h2 className="card-title">
                  <CurrencyDollarIcon className="h-6 w-6 text-secondary" />
                  Receive XLM
                </h2>
                <div className="mt-4">
                  <p className="text-sm mb-2">Your Stellar Address:</p>
                  <div className="bg-base-200 p-4 rounded-lg break-all">
                    <StellarAddress address={stellarAddress} />
                  </div>
                </div>
                <div className="card-actions justify-end mt-4">
                  <button className="btn btn-secondary" onClick={handleCopyAddress}>
                    Copy Address
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <AddTokenModal
        isOpen={isAddTokenModalOpen}
        onClose={() => setIsAddTokenModalOpen(false)}
      />
    </div>
  );
};

export default Home;
