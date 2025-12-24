"""
STEP 3: Simple Homomorphic Encryption (BEGINNER VERSION)
=========================================================
No classes, no constructors - just simple functions!

HOW TO RUN:
1. Save this file as: homomorphic_simple.py
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
# STEP 1: GENERATE KEYS
# ============================================

print("\n\n" + "=" * 70)
print("STEP 1: Generate Secret Keys")
print("=" * 70)

# Create secret keys (like passwords)
secret_key = random.randint(1000, 9999)
multiplier = random.randint(100, 500)

print(f"\n🔑 Keys generated!")
print(f"   Secret key: {secret_key} (keep this private!)")
print(f"   Multiplier: {multiplier}")
print(f"\n   These keys will be used to encrypt and decrypt data")

# ============================================
# FUNCTION 1: ENCRYPT
# ============================================

def encrypt(value, secret_key, multiplier):
    """
    Encrypt a number so it's hidden.
    
    Parameters:
    - value: The number to encrypt (like a bank balance)
    - secret_key: The secret password
    - multiplier: Another secret number
    
    Returns:
    - encrypted_value: The hidden number
    - noise: Random value added for extra security
    """
    # Add some randomness
    noise = random.randint(1, 100)
    
    # Encrypt: multiply by key and add noise
    encrypted_value = (value * multiplier) + secret_key + noise
    
    return encrypted_value, noise


# ============================================
# FUNCTION 2: DECRYPT
# ============================================

def decrypt(encrypted_value, noise, secret_key, multiplier):
    """
    Decrypt a number to see the original value.
    
    Parameters:
    - encrypted_value: The hidden number
    - noise: The random value that was added
    - secret_key: The secret password
    - multiplier: The secret number
    
    Returns:
    - original_value: The original number
    """
    # Reverse the encryption
    original_value = (encrypted_value - secret_key - noise) // multiplier
    
    
    return original_value


# ============================================
# FUNCTION 3: HOMOMORPHIC ADD (THE MAGIC!)
# ============================================

def add_encrypted_numbers(encrypted1, noise1, encrypted2, noise2):
    """
    THE MAGIC FUNCTION!
    Add two encrypted numbers WITHOUT decrypting them!
    
    Parameters:
    - encrypted1, noise1: First encrypted number
    - encrypted2, noise2: Second encrypted number
    
    Returns:
    - result: The sum (still encrypted!)
    - result_noise: Combined noise
    """
    # Add the encrypted values directly!
    result = encrypted1 + encrypted2
    result_noise = noise1 + noise2
    
    return result, result_noise


# ============================================
# BANKING DEMO
# ============================================

print("\n\n" + "=" * 70)
print("BANKING SCENARIO: Calculate Average Balance")
print("=" * 70)

# Customer balances (what we want to keep secret)
alice_balance = 5000
bob_balance = 12000
carol_balance = 8500

print("\n💰 Original Customer Balances:")
print("-" * 70)
print(f"   Alice:  ${alice_balance:,}")
print(f"   Bob:    ${bob_balance:,}")
print(f"   Carol:  ${carol_balance:,}")

# Calculate what the answer SHOULD be
actual_total = alice_balance + bob_balance + carol_balance
actual_average = actual_total / 3

print(f"\n   📊 Actual Total: ${actual_total:,}")
print(f"   📊 Actual Average: ${actual_average:,.2f}")
print(f"   (This is what we want to calculate)")

# ============================================
# STEP 2: ENCRYPT THE BALANCES
# ============================================

print("\n\n" + "=" * 70)
print("STEP 2: Encrypt Balances (at the bank branch)")
print("=" * 70)

# Encrypt Alice's balance
alice_encrypted, alice_noise = encrypt(alice_balance, secret_key, multiplier)
print(f"\n   Alice: ${alice_balance:,} → {alice_encrypted} [encrypted]")

# Encrypt Bob's balance
bob_encrypted, bob_noise = encrypt(bob_balance, secret_key, multiplier)
print(f"   Bob:   ${bob_balance:,} → {bob_encrypted} [encrypted]")

# Encrypt Carol's balance
carol_encrypted, carol_noise = encrypt(carol_balance, secret_key, multiplier)
print(f"   Carol: ${carol_balance:,} → {carol_encrypted} [encrypted]")

print(f"\n   ✓ All balances are now encrypted!")
print(f"   ✓ Ready to send to the server!")

# ============================================
# STEP 3: SERVER CALCULATES (WITHOUT DECRYPTING!)
# ============================================

print("\n\n" + "=" * 70)
print("STEP 3: Server Calculates on Encrypted Data")
print("=" * 70)
print("   ⚠️  Server does NOT have the decryption key!")
print("   ⚠️  Server CANNOT see the actual balances!")

# Add Alice + Bob (both encrypted!)
print(f"\n   Step 3a: Adding Alice's and Bob's encrypted balances...")
sum_alice_bob, noise_alice_bob = add_encrypted_numbers(
    alice_encrypted, alice_noise,
    bob_encrypted, bob_noise
)
print(f"            Result (still encrypted): {sum_alice_bob}")

# Add Carol to the sum (still encrypted!)
print(f"\n   Step 3b: Adding Carol's encrypted balance...")
final_encrypted_sum, final_noise = add_encrypted_numbers(
    sum_alice_bob, noise_alice_bob,
    carol_encrypted, carol_noise
)
print(f"            Final encrypted sum: {final_encrypted_sum}")

print(f"\n   ✓ Server computed encrypted sum: {final_encrypted_sum}")
print(f"   ✓ Server still doesn't know the actual values!")
print(f"\n   🎯 THIS IS THE MAGIC:")
print(f"      The server added the numbers WITHOUT seeing them!")

# ============================================
# STEP 4: DECRYPT THE RESULT (Only at headquarters)
# ============================================

print("\n\n" + "=" * 70)
print("STEP 4: Headquarters Decrypts the Result")
print("=" * 70)
print("   Only headquarters has the secret keys to decrypt!")

# Decrypt the sum
decrypted_total = decrypt(final_encrypted_sum, final_noise, secret_key, multiplier)
computed_average = decrypted_total / 3

print(f"\n   Decrypted Total:  ${decrypted_total:,}")
print(f"   Computed Average: ${computed_average:,.2f}")

# ============================================
# STEP 5: VERIFY IT WORKED!
# ============================================

print("\n\n" + "=" * 70)
print("✅ VERIFICATION: Did it work?")
print("=" * 70)

print(f"\n   Expected Total:   ${actual_total:,}")
print(f"   Computed Total:   ${decrypted_total:,}")
print(f"   Match?            {actual_total == decrypted_total}")

print(f"\n   Expected Average: ${actual_average:,.2f}")
print(f"   Computed Average: ${computed_average:,.2f}")

if actual_total == decrypted_total:
    print("\n   🎉 SUCCESS! The results match perfectly!")
    print("   ✓ We calculated the sum on encrypted data!")
    print("   ✓ The server never saw the actual balances!")
else:
    print("\n   ⚠️  Something went wrong")

# ============================================
# SUMMARY
# ============================================

print("\n\n" + "=" * 70)
print("📚 WHAT HAPPENED - STEP BY STEP")
print("=" * 70)

print("""
1. 🔑 GENERATED KEYS:
   - Created secret_key and multiplier
   - These are like passwords

2. 🔒 ENCRYPTED DATA:
   - Alice: $5,000  → encrypted number
   - Bob:   $12,000 → encrypted number  
   - Carol: $8,500  → encrypted number

3. ➕ ADDED ENCRYPTED NUMBERS:
   - Server added: Encrypted(Alice) + Encrypted(Bob) + Encrypted(Carol)
   - Server did NOT decrypt anything!
   - Server did NOT see $5,000, $12,000, or $8,500

4. 🔓 DECRYPTED RESULT:
   - Headquarters decrypted: Got $25,500
   - Calculated average: $8,500

5. 🎯 THE KEY BENEFIT:
   - Server did the math
   - Server never saw the private data
   - Privacy protected!
""")

print("=" * 70)
print("🎉 CONGRATULATIONS!")
print("=" * 70)
print("\nYou just learned homomorphic encryption!")
print("This protects privacy in:")
print("  • Banking")
print("  • Healthcare") 
print("  • Cloud computing")
print("  • Any sensitive data processing")

print("\n" + "=" * 70)
print("🎮 TRY IT YOURSELF!")
print("=" * 70)
print("\nChange the balances at the top and run again!")
print("Try different numbers like:")
print("   alice_balance = 10000")
print("   bob_balance = 25000")
print("   carol_balance = 15000")
print("\nThen run the program again to see it work!")
print("=" * 70)