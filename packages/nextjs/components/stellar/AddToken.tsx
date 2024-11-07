import { FC, useState } from "react";
import { toast } from "react-hot-toast";
import { stellarWallet } from "~~/utils/stellar/wallet";

interface AddTokenModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AddTokenModal: FC<AddTokenModalProps> = ({ isOpen, onClose }) => {
  const [assetCode, setAssetCode] = useState("");
  const [issuerAddress, setIssuerAddress] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleAddToken = async () => {
    if (!assetCode || !issuerAddress) {
      toast.error("Please fill in all fields");
      return;
    }

    try {
      setIsLoading(true);
      await stellarWallet.addTrustline(assetCode, issuerAddress);
      toast.success(`Successfully added ${assetCode} token`);
      setAssetCode("");
      setIssuerAddress("");
      onClose();
    } catch (error: any) {
      console.error("Failed to add token:", error);
      toast.error(error.message || "Failed to add token");
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <dialog id="add_token_modal" className="modal modal-open">
      <div className="modal-box">
        <h3 className="font-bold text-lg mb-4">Add Custom Token</h3>
        <div className="form-control">
          <label className="label">
            <span className="label-text">Asset Code</span>
          </label>
          <input
            type="text"
            placeholder="e.g., USDC"
            className="input input-bordered w-full"
            value={assetCode}
            onChange={e => setAssetCode(e.target.value.toUpperCase())}
          />
        </div>
        <div className="form-control mt-4">
          <label className="label">
            <span className="label-text">Issuer Address</span>
          </label>
          <input
            type="text"
            placeholder="G..."
            className="input input-bordered w-full"
            value={issuerAddress}
            onChange={e => setIssuerAddress(e.target.value)}
          />
        </div>
        <div className="modal-action">
          <button className="btn" onClick={onClose}>Cancel</button>
          <button
            className={`btn btn-primary ${isLoading ? "loading" : ""}`}
            onClick={handleAddToken}
            disabled={isLoading}
          >
            {isLoading ? "Adding..." : "Add Token"}
          </button>
        </div>
      </div>
      <form method="dialog" className="modal-backdrop">
        <button>close</button>
      </form>
    </dialog>
  );
}; 