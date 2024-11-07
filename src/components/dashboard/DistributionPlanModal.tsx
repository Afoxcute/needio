import React, { useState } from 'react';
import { toast } from 'react-hot-toast';

interface DistributionPlanModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (plan: DistributionPlan) => void;
  currentInventory: InventoryItem[];
}

interface DistributionPlan {
  date: string;
  location: string;
  expectedClients: number;
  allocatedResources: {
    [category: string]: number;
  };
  notes: string;
}

export const DistributionPlanModal: React.FC<DistributionPlanModalProps> = ({
  isOpen,
  onClose,
  onSave,
  currentInventory,
}) => {
  const [plan, setPlan] = useState<DistributionPlan>({
    date: '',
    location: '',
    expectedClients: 0,
    allocatedResources: {},
    notes: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate plan
    if (!plan.date || !plan.location || plan.expectedClients <= 0) {
      toast.error('Please fill in all required fields');
      return;
    }

    // Check if allocated resources are available
    const isValidAllocation = Object.entries(plan.allocatedResources).every(
      ([category, amount]) => {
        const inventoryItem = currentInventory.find(item => item.category === category);
        return inventoryItem && inventoryItem.quantity >= amount;
      }
    );

    if (!isValidAllocation) {
      toast.error('Insufficient inventory for planned distribution');
      return;
    }

    onSave(plan);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="modal modal-open">
      <div className="modal-box">
        <h3 className="font-bold text-lg mb-4">Create Distribution Plan</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-control">
            <label className="label">
              <span className="label-text">Distribution Date</span>
            </label>
            <input
              type="datetime-local"
              className="input input-bordered"
              value={plan.date}
              onChange={(e) => setPlan({ ...plan, date: e.target.value })}
              required
            />
          </div>

          <div className="form-control mt-4">
            <label className="label">
              <span className="label-text">Location</span>
            </label>
            <input
              type="text"
              className="input input-bordered"
              value={plan.location}
              onChange={(e) => setPlan({ ...plan, location: e.target.value })}
              required
            />
          </div>

          <div className="form-control mt-4">
            <label className="label">
              <span className="label-text">Expected Number of Clients</span>
            </label>
            <input
              type="number"
              className="input input-bordered"
              value={plan.expectedClients}
              onChange={(e) => setPlan({ ...plan, expectedClients: parseInt(e.target.value) })}
              required
              min="1"
            />
          </div>

          <div className="form-control mt-4">
            <label className="label">
              <span className="label-text">Resource Allocation</span>
            </label>
            {currentInventory.map((item) => (
              <div key={item.category} className="flex items-center gap-2 mt-2">
                <span className="w-1/3">{item.category}</span>
                <input
                  type="number"
                  className="input input-bordered w-2/3"
                  value={plan.allocatedResources[item.category] || 0}
                  onChange={(e) =>
                    setPlan({
                      ...plan,
                      allocatedResources: {
                        ...plan.allocatedResources,
                        [item.category]: parseInt(e.target.value),
                      },
                    })
                  }
                  min="0"
                  max={item.quantity}
                />
              </div>
            ))}
          </div>

          <div className="form-control mt-4">
            <label className="label">
              <span className="label-text">Notes</span>
            </label>
            <textarea
              className="textarea textarea-bordered"
              value={plan.notes}
              onChange={(e) => setPlan({ ...plan, notes: e.target.value })}
            />
          </div>

          <div className="modal-action">
            <button type="button" className="btn" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              Save Plan
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}; 