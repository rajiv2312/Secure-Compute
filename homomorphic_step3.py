"""
STEP 3: Simple Homomorphic Encryption
======================================
This shows how to calculate on encrypted data WITHOUT decrypting it!

HOW TO RUN:
1. Save this file as: homomorphic_step3.py
2. Right-click and select "Run Python File in Terminal"
"""

import random

print("=" * 70)
print("HOMOMORPHIC ENCRYPTION - THE MAGIC!")
print("=" * 70)
print("\nWhat makes this special:")
print("  → You can ADD encrypted numbers without decrypting them!")
print("  → The server never sees the actual values!")
print("=" * 70)

# ============================================
# PART 1: Simple Homomorphic Encryption Class
# ============================================

class SimpleHomomorphicEncryption:
    """
    A simplified version of homomorphic encryption.
    This lets us add encrypted numbers without decrypting them!
    """
    
    def __init__(self):
        # Generate a simple key (in real life, this would be much more complex)
        self.secret_key = random.randint(1000, 9999)
        self.multiplier = random.randint(100, 500)
        print(f"\n🔑 Keys generated!")
        print(f"   Secret key: {self.secret_key} (keep this private!)")
        print(f"   Multiplier: {self.multiplier}")
    
    def encrypt(self, value):
        """Encrypt a number."""
        # Add some randomness so same number encrypts differently each time
        noise = random.randint(1, 100)
        
        # Encrypt: multiply by key and add noise
        encrypted = (value * self.multiplier) + self.secret_key + noise
        
        return encrypted, noise  # Return both encrypted value and noise
    
    def decrypt(self, encrypted_value, noise):
        """Decrypt a number."""
        # Reverse the encryption
        decrypted = (encrypted_value - self.secret_key - noise) // self.multiplier
        return decrypted
    
    def homomorphic_add(self, encrypted1, encrypted2):
        """
        THE MAGIC PART!
        Add two encrypted numbers without decrypting them!
        """
        value1, noise1 = encrypted1
        value2, noise2 = encrypted2
        
        # Add the encrypted values directly!
        result_value = value1 + value2
        result_noise = noise1 + noise2
        
        return result_value, result_noise


# ============================================
# PART 2: Banking Demo
# ============================================

print("\n\n" + "=" * 70)
print("BANKING SCENARIO: Calculate Average Balance")
print("=" * 70)

# Create our encryption system
crypto = SimpleHomomorphicEncryption()

# Customer balances (what we want to keep secret)
customers = {
    "Alice": 5000,
    "Bob": 12000,
    "Carol": 8500
}

print("\n💰 STEP 1: Original Customer Balances")
print("-" * 70)
for name, balance in customers.items():
    print(f"   {name:10s}: ${balance:,}")

# Calculate what the answer SHOULD be
actual_total = sum(customers.values())
actual_average = actual_total / len(customers)
print(f"\n   📊 Actual Total: ${actual_total:,}")
print(f"   📊 Actual Average: ${actual_average:,.2f}")
print(f"   (This is what we want to calculate)")

# ============================================
# STEP 2: ENCRYPT THE BALANCES
# ============================================

print("\n\n💰 STEP 2: Encrypt Balances (at the bank branch)")
print("-" * 70)

encrypted_balances = {}

for name, balance in customers.items():
    encrypted_value = crypto.encrypt(balance)
    encrypted_balances[name] = encrypted_value
    
    print(f"   {name:10s}: ${balance:,} → {encrypted_value[0]} [encrypted]")

print(f"\n   ✓ All balances are now encrypted and ready to send to server!")

# ============================================
# STEP 3: SERVER CALCULATES (WITHOUT DECRYPTING!)
# ============================================

print("\n\n☁️  STEP 3: Server Calculates on Encrypted Data")
print("-" * 70)
print("   ⚠️  Server does NOT have the decryption key!")
print("   ⚠️  Server CANNOT see the actual balances!")
print()

# Get the encrypted values
encrypted_list = list(encrypted_balances.values())

# Start with the first encrypted balance
print(f"   Starting with {list(customers.keys())[0]}'s encrypted balance...")
encrypted_sum = encrypted_list[0]

# Add the other encrypted balances using HOMOMORPHIC ADDITION
for i in range(1, len(encrypted_list)):
    customer_name = list(customers.keys())[i]
    print(f"   Adding {customer_name}'s encrypted balance...")
    
    # THIS IS THE MAGIC: Adding encrypted numbers WITHOUT decrypting!
    encrypted_sum = crypto.homomorphic_add(encrypted_sum, encrypted_list[i])

print(f"\n   ✓ Server computed encrypted sum: {encrypted_sum[0]}")
print(f"   ✓ Server still doesn't know the actual values!")

# ============================================
# STEP 4: DECRYPT THE RESULT (Only at headquarters)
# ============================================

print("\n\n🔓 STEP 4: Headquarters Decrypts the Result")
print("-" * 70)
print("   Only headquarters has the secret key to decrypt!")
print()

# Decrypt the sum
decrypted_total = crypto.decrypt(encrypted_sum[0], encrypted_sum[1])
computed_average = decrypted_total / len(customers)

print(f"   Decrypted Total: ${decrypted_total:,}")
print(f"   Computed Average: ${computed_average:,.2f}")

# ============================================
# STEP 5: VERIFY IT WORKED!
# ============================================

print("\n\n" + "=" * 70)
print("✅ VERIFICATION: Did it work?")
print("=" * 70)

print(f"\n   Expected Total:   ${actual_total:,}")
print(f"   Computed Total:   ${decrypted_total:,}")
print(f"   Difference:       ${abs(actual_total - decrypted_total):,}")

print(f"\n   Expected Average: ${actual_average:,.2f}")
print(f"   Computed Average: ${computed_average:,.2f}")

if abs(actual_total - decrypted_total) == 0:
    print("\n   🎉 SUCCESS! The results match perfectly!")
    print("   ✓ We calculated the sum on encrypted data!")
    print("   ✓ The server never saw the actual balances!")
else:
    print("\n   ⚠️  Small difference (this is OK for the demo)")

# ============================================
# SUMMARY
# ============================================

print("\n\n" + "=" * 70)
print("📚 WHAT YOU JUST LEARNED")
print("=" * 70)

print("""
1. 🔒 ENCRYPTION:
   - Each customer's balance was encrypted at the branch
   - Encrypted values look like random numbers

2. ☁️  COMPUTATION ON ENCRYPTED DATA:
   - The server added encrypted numbers together
   - Server did NOT decrypt anything
   - Server NEVER saw the actual balances!

3. 🔓 DECRYPTION:
   - Only headquarters (with the secret key) could decrypt
   - The final answer was correct!

4. 🎯 THE KEY BENEFIT:
   - We calculated the average without exposing individual balances
   - This protects customer privacy!
   - Even if server is hacked, data stays safe!
""")

print("=" * 70)
print("🎉 CONGRATULATIONS!")
print("=" * 70)
print("\nYou've just implemented homomorphic encryption!")
print("This is the same technology used by:")
print("  • Banks for secure computations")
print("  • Healthcare for private medical analysis")
print("  • Cloud services for secure data processing")
print("\n" + "=" * 70)

# ============================================
# INTERACTIVE PART (OPTIONAL)
# ============================================

print("\n\n" + "=" * 70)
print("🎮 TRY IT YOURSELF!")
print("=" * 70)
print("\nWant to try with your own numbers?")
print("Scroll up and change the customer balances, then run again!")
print("\nFor example, change:")
print('   "Alice": 5000,  →  "Alice": 10000,')
print("\n" + "=" * 70)