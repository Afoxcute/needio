use near_sdk::borsh::{self, BorshDeserialize, BorshSerialize};
use near_sdk::collections::{LookupMap, UnorderedMap};
use near_sdk::json_types::U128;
use near_sdk::serde::{Deserialize, Serialize};
use near_sdk::{env, near_bindgen, AccountId, Balance, PanicOnDefault, Promise};

#[derive(BorshDeserialize, BorshSerialize, Serialize, Deserialize)]
#[serde(crate = "near_sdk::serde")]
pub struct ContributionMetrics {
    data_quality: u8,
    model_improvement: u8,
    participation_frequency: u8,
    timestamp: u64,
}

#[derive(BorshDeserialize, BorshSerialize, Serialize, Deserialize)]
#[serde(crate = "near_sdk::serde")]
pub struct RedemptionOption {
    name: String,
    cost: Balance,
    available: bool,
    description: String,
}

#[near_bindgen]
#[derive(BorshDeserialize, BorshSerialize, PanicOnDefault)]
pub struct FoodBankToken {
    owner: AccountId,
    total_supply: Balance,
    balances: LookupMap<AccountId, Balance>,
    contributions: UnorderedMap<AccountId, Vec<ContributionMetrics>>,
    redemption_options: UnorderedMap<String, RedemptionOption>,
    min_contribution_threshold: Balance,
    reward_rate: u8, // Percentage of contribution value
}

#[near_bindgen]
impl FoodBankToken {
    #[init]
    pub fn new(owner: AccountId, total_supply: U128) -> Self {
        let mut contract = Self {
            owner,
            total_supply: total_supply.0,
            balances: LookupMap::new(b"b"),
            contributions: UnorderedMap::new(b"c"),
            redemption_options: UnorderedMap::new(b"r"),
            min_contribution_threshold: 10,  // Minimum contribution to earn rewards
            reward_rate: 5,  // 5% reward rate
        };

        // Initialize redemption options
        contract.add_redemption_option(
            "supplier_discount".to_string(),
            100,  // 100 tokens
            "10% discount on supplier purchases".to_string(),
        );
        contract.add_redemption_option(
            "analytics_access".to_string(),
            200,  // 200 tokens
            "Access to advanced analytics dashboard".to_string(),
        );
        contract.add_redemption_option(
            "grant_opportunity".to_string(),
            500,  // 500 tokens
            "Priority consideration for grant programs".to_string(),
        );

        contract
    }

    #[payable]
    pub fn record_contribution(
        &mut self,
        food_bank: AccountId,
        metrics: ContributionMetrics,
    ) {
        self.assert_owner();
        assert!(
            metrics.data_quality <= 100 &&
            metrics.model_improvement <= 100 &&
            metrics.participation_frequency <= 100,
            "Metrics must be between 0 and 100"
        );

        // Calculate reward based on metrics
        let reward = self.calculate_reward(&metrics);
        
        // Record contribution
        let mut contributions = self.contributions.get(&food_bank)
            .unwrap_or_else(|| Vec::new());
        contributions.push(metrics);
        self.contributions.insert(&food_bank, &contributions);

        // Distribute reward tokens
        if reward > 0 {
            self.mint(food_bank, reward);
        }
    }

    pub fn redeem_tokens(
        &mut self,
        option_id: String,
        amount: U128,
    ) -> Promise {
        let account_id = env::predecessor_account_id();
        let balance = self.balances.get(&account_id).unwrap_or(0);
        let amount = amount.0;

        // Verify redemption option exists and is available
        let option = self.redemption_options.get(&option_id)
            .expect("Redemption option not found");
        assert!(option.available, "This redemption option is not available");
        assert!(amount >= option.cost, "Insufficient tokens for redemption");
        assert!(balance >= amount, "Insufficient balance");

        // Update balance
        let new_balance = balance - amount;
        self.balances.insert(&account_id, &new_balance);
        self.total_supply -= amount;

        // Process redemption benefit
        self.process_redemption_benefit(&account_id, &option)
    }

    fn calculate_reward(&self, metrics: &ContributionMetrics) -> Balance {
        let average_score = (metrics.data_quality as u32 +
            metrics.model_improvement as u32 +
            metrics.participation_frequency as u32) / 3;
        
        if average_score as Balance >= self.min_contribution_threshold {
            (average_score as Balance * self.reward_rate as Balance) / 100
        } else {
            0
        }
    }

    fn process_redemption_benefit(
        &self,
        account_id: &AccountId,
        option: &RedemptionOption,
    ) -> Promise {
        match option.name.as_str() {
            "supplier_discount" => {
                // Implement supplier discount logic
                Promise::new(account_id.clone())
                    .function_call(
                        "apply_supplier_discount".to_string(),
                        vec![],
                        0,
                        env::prepaid_gas() / 3,
                    )
            },
            "analytics_access" => {
                // Grant analytics access
                Promise::new(account_id.clone())
                    .function_call(
                        "grant_analytics_access".to_string(),
                        vec![],
                        0,
                        env::prepaid_gas() / 3,
                    )
            },
            "grant_opportunity" => {
                // Process grant opportunity
                Promise::new(account_id.clone())
                    .function_call(
                        "process_grant_application".to_string(),
                        vec![],
                        0,
                        env::prepaid_gas() / 3,
                    )
            },
            _ => env::panic_str("Invalid redemption option"),
        }
    }

    // Admin functions
    pub fn add_redemption_option(
        &mut self,
        name: String,
        cost: Balance,
        description: String,
    ) {
        self.assert_owner();
        let option = RedemptionOption {
            name: name.clone(),
            cost,
            available: true,
            description,
        };
        self.redemption_options.insert(&name, &option);
    }

    pub fn update_reward_rate(&mut self, new_rate: u8) {
        self.assert_owner();
        assert!(new_rate <= 100, "Reward rate must be <= 100");
        self.reward_rate = new_rate;
    }

    // View functions
    pub fn get_balance(&self, account_id: AccountId) -> U128 {
        U128(self.balances.get(&account_id).unwrap_or(0))
    }

    pub fn get_contributions(&self, account_id: AccountId) -> Vec<ContributionMetrics> {
        self.contributions.get(&account_id).unwrap_or_else(|| Vec::new())
    }

    pub fn get_redemption_options(&self) -> Vec<(String, RedemptionOption)> {
        self.redemption_options.iter().collect()
    }

    // Internal helper functions
    fn mint(&mut self, account_id: AccountId, amount: Balance) {
        let balance = self.balances.get(&account_id).unwrap_or(0);
        self.balances.insert(&account_id, &(balance + amount));
        self.total_supply += amount;
    }

    fn assert_owner(&self) {
        assert_eq!(
            env::predecessor_account_id(),
            self.owner,
            "Only the owner can call this method"
        );
    }
} 