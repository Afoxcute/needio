import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  BarChart, Bar, PieChart, Pie, Cell,
} from 'recharts';
import { toast } from 'react-hot-toast';

interface DashboardProps {
  foodBankId: string;
}

interface PredictionData {
  date: string;
  predicted: number;
  actual: number;
}

interface InventoryItem {
  category: string;
  quantity: number;
  perishable: boolean;
  minStock: number;
}

interface DistributionPlan {
  date: string;
  location: string;
  expectedClients: number;
  allocatedResources: number;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export const FoodBankDashboard: React.FC<DashboardProps> = ({ foodBankId }) => {
  const [predictions, setPredictions] = useState<PredictionData[]>([]);
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [distributionPlans, setDistributionPlans] = useState<DistributionPlan[]>([]);
  const [selectedTimeframe, setSelectedTimeframe] = useState<'week' | 'month' | 'year'>('month');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, [foodBankId, selectedTimeframe]);

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      // Fetch predictions, inventory, and distribution plans
      const [predictionData, inventoryData, planData] = await Promise.all([
        fetchPredictions(),
        fetchInventory(),
        fetchDistributionPlans(),
      ]);

      setPredictions(predictionData);
      setInventory(inventoryData);
      setDistributionPlans(planData);
    } catch (error) {
      toast.error('Failed to fetch dashboard data');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchPredictions = async () => {
    // Implement API call to get predictions
    return [];
  };

  const fetchInventory = async () => {
    // Implement API call to get inventory
    return [];
  };

  const fetchDistributionPlans = async () => {
    // Implement API call to get distribution plans
    return [];
  };

  return (
    <div className="container mx-auto p-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Predictions Chart */}
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">Demand Predictions</h2>
            <div className="timeframe-selector mb-4">
              <select
                value={selectedTimeframe}
                onChange={(e) => setSelectedTimeframe(e.target.value as any)}
                className="select select-bordered w-full"
              >
                <option value="week">Weekly</option>
                <option value="month">Monthly</option>
                <option value="year">Yearly</option>
              </select>
            </div>
            <LineChart width={400} height={300} data={predictions}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="predicted" stroke="#8884d8" />
              <Line type="monotone" dataKey="actual" stroke="#82ca9d" />
            </LineChart>
          </div>
        </div>

        {/* Inventory Status */}
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">Inventory Status</h2>
            <PieChart width={400} height={300}>
              <Pie
                data={inventory}
                dataKey="quantity"
                nameKey="category"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label
              >
                {inventory.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
            <div className="mt-4">
              <h3 className="font-bold">Low Stock Alerts</h3>
              <ul className="list-disc list-inside">
                {inventory
                  .filter((item) => item.quantity < item.minStock)
                  .map((item, index) => (
                    <li key={index} className="text-error">
                      {item.category}: {item.quantity} units remaining
                    </li>
                  ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Distribution Planning */}
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">Distribution Planning</h2>
            <BarChart width={400} height={300} data={distributionPlans}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="expectedClients" fill="#8884d8" />
              <Bar dataKey="allocatedResources" fill="#82ca9d" />
            </BarChart>
            <div className="mt-4">
              <button
                className="btn btn-primary w-full"
                onClick={() => {/* Implement distribution planning */}}
              >
                Create New Distribution Plan
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Action Items */}
      <div className="mt-8">
        <h2 className="text-2xl font-bold mb-4">Recommended Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="card bg-base-100 shadow-xl">
            <div className="card-body">
              <h3 className="card-title text-warning">Inventory Alerts</h3>
              <ul className="list-disc list-inside">
                <li>Order more canned goods (below minimum threshold)</li>
                <li>Check perishable items expiring this week</li>
              </ul>
            </div>
          </div>

          <div className="card bg-base-100 shadow-xl">
            <div className="card-body">
              <h3 className="card-title text-info">Distribution Optimization</h3>
              <ul className="list-disc list-inside">
                <li>Increase capacity for next week's distribution</li>
                <li>Consider adding a new distribution location</li>
              </ul>
            </div>
          </div>

          <div className="card bg-base-100 shadow-xl">
            <div className="card-body">
              <h3 className="card-title text-success">Resource Planning</h3>
              <ul className="list-disc list-inside">
                <li>Schedule additional volunteers for peak hours</li>
                <li>Coordinate with nearby food banks for resource sharing</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="loading loading-spinner loading-lg text-primary"></div>
        </div>
      )}
    </div>
  );
}; 