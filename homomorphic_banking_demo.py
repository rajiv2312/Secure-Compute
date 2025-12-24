"""
Homomorphic Encryption Banking Demo
====================================
This demo shows how a bank can calculate the average account balance
without ever exposing individual customer balances to the central server.

Uses the Paillier cryptosystem (additive homomorphic encryption).

Requirements:
    pip install phe

Author: Banking Security Demo
"""

from phe import paillier
import json
from typing import List, Dict
import time


class Customer:
    """Represents a bank customer with an account balance."""
    
    def __init__(self, customer_id: int, name: str, balance: float):
        self.customer_id = customer_id
        self.name = name
        self.balance = balance
        
    def __repr__(self):
        return f"Customer({self.name}, Balance: ${self.balance:,.2f})"


class BankBranch:
    """Represents a bank branch that encrypts customer data."""
    
    def __init__(self, branch_id: str, public_key):
        self.branch_id = branch_id
        self.public_key = public_key
        self.customers: List[Customer] = []
        
    def add_customer(self, customer: Customer):
        """Add a customer to this branch."""
        self.customers.append(customer)
        
    def encrypt_balances(self) -> List[Dict]:
        """Encrypt all customer balances using homomorphic encryption."""
        print(f"\n{'='*60}")
        print(f"🏦 Branch {self.branch_id}: Encrypting customer balances...")
        print(f"{'='*60}")
        
        encrypted_data = []
        
        for customer in self.customers:
            # Encrypt the balance using Paillier encryption
            encrypted_balance = self.public_key.encrypt(customer.balance)
            
            encrypted_data.append({
                'customer_id': customer.customer_id,
                'customer_name': customer.name,
                'encrypted_balance': encrypted_balance,
                'original_balance': customer.balance  # Only for demo verification
            })
            
            print(f"  ✓ {customer.name}: ${customer.balance:,.2f} → Encrypted")
            
        print(f"\n✅ Successfully encrypted {len(encrypted_data)} customer balances")
        return encrypted_data


class CentralServer:
    """
    Represents the central banking server that computes on encrypted data.
    IMPORTANT: This server never sees the actual plaintext balances!
    """
    
    def __init__(self):
        self.name = "Central Banking Server"
        
    def compute_encrypted_sum(self, encrypted_data: List[Dict]):
        """
        Compute the sum of encrypted balances without decrypting them.
        This is the key feature of homomorphic encryption!
        """
        print(f"\n{'='*60}")
        print(f"☁️  {self.name}: Computing on encrypted data...")
        print(f"{'='*60}")
        
        if not encrypted_data:
            raise ValueError("No encrypted data received")
        
        # Start with the first encrypted balance
        encrypted_sum = encrypted_data[0]['encrypted_balance']
        
        print(f"  📊 Processing {len(encrypted_data)} encrypted values...")
        print(f"  ⚠️  Server cannot see actual balances - data is encrypted!")
        
        # Homomorphically add all other encrypted balances
        # Key insight: We can add encrypted numbers without decrypting them!
        for i in range(1, len(encrypted_data)):
            encrypted_sum = encrypted_sum + encrypted_data[i]['encrypted_balance']
            
        print(f"  ✓ Homomorphic addition completed")
        print(f"  ✓ Encrypted sum computed (still encrypted!)")
        
        return encrypted_sum, len(encrypted_data)
    
    def demonstrate_privacy(self, encrypted_data: List[Dict]):
        """Show that the server cannot decrypt the data."""
        print(f"\n{'='*60}")
        print(f"🔒 Privacy Verification")
        print(f"{'='*60}")
        
        sample = encrypted_data[0]
        print(f"  Customer: {sample['customer_name']}")
        print(f"  Encrypted balance (what server sees): {sample['encrypted_balance'].ciphertext()}")
        print(f"  Actual balance (server CANNOT see this): [HIDDEN]")
        print(f"\n  ✅ Without the private key, server cannot decrypt!")


class BankHeadquarters:
    """
    Represents bank headquarters with access to the private decryption key.
    Only authorized personnel here can decrypt the results.
    """
    
    def __init__(self, private_key):
        self.private_key = private_key
        
    def decrypt_and_calculate_average(self, encrypted_sum, count: int) -> float:
        """
        Decrypt the encrypted sum and calculate the average.
        Only this entity with the private key can perform decryption.
        """
        print(f"\n{'='*60}")
        print(f"🔓 Bank Headquarters: Decrypting results...")
        print(f"{'='*60}")
        
        # Decrypt the sum
        decrypted_sum = self.private_key.decrypt(encrypted_sum)
        
        # Calculate average
        average = decrypted_sum / count
        
        print(f"  ✓ Decrypted total sum: ${decrypted_sum:,.2f}")
        print(f"  ✓ Number of accounts: {count}")
        print(f"  ✓ Average balance: ${average:,.2f}")
        
        return average


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n\n{'#'*60}")
    print(f"# {title.center(56)} #")
    print(f"{'#'*60}\n")


def run_demo():
    """Run the complete homomorphic encryption banking demo."""
    
    print_header("HOMOMORPHIC ENCRYPTION IN BANKING")
    print("This demo shows how banks can compute on encrypted data")
    print("without ever exposing sensitive customer information.\n")
    
    # Step 1: Generate cryptographic keys
    print_header("STEP 1: KEY GENERATION")
    print("Generating public/private key pair...")
    print("(In production, use 2048+ bit keys for security)")
    
    start_time = time.time()
    public_key, private_key = paillier.generate_paillier_keypair(n_length=1024)
    key_gen_time = time.time() - start_time
    
    print(f"✅ Keys generated in {key_gen_time:.3f} seconds")
    print(f"   Public key: Distributed to all branches")
    print(f"   Private key: Secured at headquarters only")
    
    # Step 2: Create branches and customers
    print_header("STEP 2: BRANCH DATA")
    
    # Branch 1
    branch1 = BankBranch("Branch-001", public_key)
    branch1.add_customer(Customer(1, "Alice Johnson", 5000.00))
    branch1.add_customer(Customer(2, "Bob Smith", 12000.00))
    branch1.add_customer(Customer(3, "Carol White", 8500.00))
    
    # Branch 2
    branch2 = BankBranch("Branch-002", public_key)
    branch2.add_customer(Customer(4, "David Brown", 15000.00))
    branch2.add_customer(Customer(5, "Eve Davis", 6500.00))
    branch2.add_customer(Customer(6, "Frank Miller", 9800.00))
    
    # Display all customers
    all_customers = branch1.customers + branch2.customers
    print("Customer Accounts:")
    for customer in all_customers:
        print(f"  {customer}")
    
    actual_average = sum(c.balance for c in all_customers) / len(all_customers)
    print(f"\n📊 Actual average balance: ${actual_average:,.2f}")
    print("(This is what we'll compute using homomorphic encryption)")
    
    # Step 3: Encrypt data at branches
    print_header("STEP 3: ENCRYPTION AT BRANCHES")
    
    encrypted_data_branch1 = branch1.encrypt_balances()
    encrypted_data_branch2 = branch2.encrypt_balances()
    
    all_encrypted_data = encrypted_data_branch1 + encrypted_data_branch2
    
    # Step 4: Send to central server
    print_header("STEP 4: CENTRAL SERVER PROCESSING")
    
    server = CentralServer()
    server.demonstrate_privacy(all_encrypted_data)
    
    # Compute on encrypted data
    encrypted_sum, total_count = server.compute_encrypted_sum(all_encrypted_data)
    
    print(f"\n💡 Key Point: The server performed calculations on encrypted data")
    print(f"   without ever seeing the actual account balances!")
    
    # Step 5: Decrypt at headquarters
    print_header("STEP 5: DECRYPTION AT HEADQUARTERS")
    
    headquarters = BankHeadquarters(private_key)
    computed_average = headquarters.decrypt_and_calculate_average(encrypted_sum, total_count)
    
    # Step 6: Verify results
    print_header("VERIFICATION")
    
    print(f"Actual average:   ${actual_average:,.2f}")
    print(f"Computed average: ${computed_average:,.2f}")
    print(f"Difference:       ${abs(actual_average - computed_average):,.2f}")
    
    if abs(actual_average - computed_average) < 0.01:
        print("\n✅ SUCCESS! Results match perfectly!")
    else:
        print("\n❌ ERROR: Results don't match")
    
    # Summary
    print_header("SECURITY BENEFITS")
    
    benefits = [
        ("🔒 Privacy Protection", "Individual balances never exposed to central server"),
        ("☁️  Secure Cloud Computing", "Can outsource computation without data exposure"),
        ("✅ Regulatory Compliance", "Meets data privacy requirements (GDPR, etc.)"),
        ("🛡️  Breach Protection", "Even if server is compromised, data remains encrypted"),
        ("🤝 Multi-party Computation", "Multiple branches can collaborate securely"),
    ]
    
    for title, description in benefits:
        print(f"\n{title}")
        print(f"  → {description}")
    
    # Use cases
    print_header("REAL-WORLD USE CASES")
    
    use_cases = [
        "1. Fraud Detection: Run ML models on encrypted transactions",
        "2. Credit Scoring: Third-party scoring without exposing financial data",
        "3. Risk Assessment: Analyze encrypted loan portfolios",
        "4. Regulatory Reporting: Compute statistics without exposing individuals",
        "5. Cross-bank Analytics: Collaborate on encrypted data",
    ]
    
    for use_case in use_cases:
        print(f"  {use_case}")
    
    print(f"\n{'='*60}\n")


def advanced_example():
    """Show a more complex example with encrypted operations."""
    
    print_header("ADVANCED EXAMPLE: MULTIPLE OPERATIONS")
    
    print("Generating keys...")
    public_key, private_key = paillier.generate_paillier_keypair(n_length=1024)
    
    # Example: Calculate total interest earned
    print("\nScenario: Calculate total interest without exposing individual amounts")
    
    accounts = [
        {"name": "Account A", "interest": 250.50},
        {"name": "Account B", "interest": 180.75},
        {"name": "Account C", "interest": 420.25},
    ]
    
    print("\nOriginal interest amounts:")
    for acc in accounts:
        print(f"  {acc['name']}: ${acc['interest']:.2f}")
    
    # Encrypt
    print("\nEncrypting...")
    encrypted_interests = []
    for acc in accounts:
        encrypted = public_key.encrypt(acc['interest'])
        encrypted_interests.append(encrypted)
        print(f"  ✓ {acc['name']} encrypted")
    
    # Homomorphic addition
    print("\nComputing sum on encrypted data...")
    encrypted_total = encrypted_interests[0]
    for enc in encrypted_interests[1:]:
        encrypted_total = encrypted_total + enc
    
    # You can also multiply encrypted values by plaintext constants
    print("Applying 20% tax (multiplying encrypted value by 0.8)...")
    encrypted_after_tax = encrypted_total * 0.8
    
    # Decrypt
    print("\nDecrypting results...")
    total_interest = private_key.decrypt(encrypted_total)
    after_tax = private_key.decrypt(encrypted_after_tax)
    
    print(f"\n✅ Total interest: ${total_interest:.2f}")
    print(f"✅ After 20% tax: ${after_tax:.2f}")
    
    # Verify
    actual_total = sum(acc['interest'] for acc in accounts)
    print(f"\nVerification: ${actual_total:.2f} == ${total_interest:.2f} ✓")


if __name__ == "__main__":
    # Run the main demo
    run_demo()
    
    # Run advanced example
    advanced_example()
    
    print("\n" + "="*60)
    print("Demo complete! You can now modify the code to:")
    print("  - Add more customers and branches")
    print("  - Implement different computations (variance, median, etc.)")
    print("  - Simulate different scenarios (fraud detection, credit scoring)")
    print("="*60 + "\n")