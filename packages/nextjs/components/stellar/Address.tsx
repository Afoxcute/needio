import { FC } from "react";
import CopyToClipboard from "react-copy-to-clipboard";
import { toast } from "react-hot-toast";

interface AddressProps {
  address?: string;
  className?: string;
}

export const StellarAddress: FC<AddressProps> = ({ address, className }) => {
  if (!address) return null;

  const handleCopy = () => {
    toast.success("Address copied to clipboard!");
  };

  // Format address to show first and last few characters
  const formatAddress = (addr: string) => {
    if (addr.length <= 12) return addr;
    return `${addr.slice(0, 6)}...${addr.slice(-6)}`;
  };

  return (
    <CopyToClipboard text={address} onCopy={handleCopy}>
      <span className={`cursor-pointer font-medium ${className}`} title={address}>
        {formatAddress(address)}
      </span>
    </CopyToClipboard>
  );
}; 