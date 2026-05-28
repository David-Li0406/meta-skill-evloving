# Solana Development - Sharp Edges

## Account Ownership Not Verified

### **Id**
account-ownership-bypass
### **Severity**
CRITICAL
### **Description**
Program accepts accounts without verifying it owns them
### **Symptoms**
  - Attackers can pass fake accounts with manipulated data
  - Unauthorized state modifications
  - Fund drainage through spoofed accounts
### **Detection Pattern**
Account<'info,.*>.*without.*constraint
### **Solution**
  // Always use Anchor's typed accounts or verify manually
  #[account(
      constraint = account.owner == expected_owner @ ErrorCode::InvalidOwner
  )]
  pub my_account: Account<'info, MyData>,
  
  // Or manual check
  require!(
      ctx.accounts.data.owner == &crate::ID,
      ErrorCode::InvalidAccountOwner
  );
  
### **References**
  - https://www.soldev.app/course/account-data-matching

## PDA Seed Collision Vulnerability

### **Id**
pda-seed-collision
### **Severity**
CRITICAL
### **Description**
PDA seeds don't include enough unique identifiers
### **Symptoms**
  - Multiple users sharing same PDA
  - Account overwrites
  - Unpredictable program behavior
### **Detection Pattern**
seeds.*=.*\[b"[^"]+"\].*without.*user
### **Solution**
  // Bad: Only static seed
  seeds = [b"vault"]
  
  // Good: Include user-specific data
  seeds = [b"vault", user.key().as_ref()]
  
  // Better: Include nonce for multiple accounts per user
  seeds = [b"vault", user.key().as_ref(), &nonce.to_le_bytes()]
  
### **References**
  - https://www.anchor-lang.com/docs/pdas

## Missing Signer Verification

### **Id**
missing-signer-check
### **Severity**
CRITICAL
### **Description**
Instruction doesn't verify required signers
### **Symptoms**
  - Anyone can call privileged functions
  - Unauthorized fund transfers
  - Admin functions exposed
### **Detection Pattern**
pub.*authority.*AccountInfo.*without.*Signer
### **Solution**
  // Use Signer type for required signers
  #[account(mut)]
  pub authority: Signer<'info>,
  
  // For PDA authority, verify seeds
  #[account(
      seeds = [b"authority"],
      bump,
  )]
  pub pda_authority: Account<'info, AuthorityAccount>,
  
### **References**
  - https://www.soldev.app/course/signer-auth

## Unchecked Arithmetic Operations

### **Id**
arithmetic-overflow
### **Severity**
HIGH
### **Description**
Using +, -, *, / without overflow protection
### **Symptoms**
  - Integer overflow causing zero balances
  - Underflow creating massive values
  - Incorrect fee calculations
### **Detection Pattern**
\+|\-|\*|/(?!/).*u64|u128
### **Solution**
  // Use checked math
  let result = a.checked_add(b).ok_or(ErrorCode::MathOverflow)?;
  let result = a.checked_sub(b).ok_or(ErrorCode::MathUnderflow)?;
  let result = a.checked_mul(b).ok_or(ErrorCode::MathOverflow)?;
  let result = a.checked_div(b).ok_or(ErrorCode::DivisionByZero)?;
  
  // Or use saturating for non-critical paths
  let capped = a.saturating_add(b);
  
### **References**
  - https://doc.rust-lang.org/std/primitive.u64.html#method.checked_add

## Account Not Rent Exempt

### **Id**
rent-exemption-failure
### **Severity**
HIGH
### **Description**
Creating accounts without sufficient lamports for rent exemption
### **Symptoms**
  - Accounts being garbage collected
  - Lost user funds
  - State disappearing after ~2 years
### **Detection Pattern**
init.*space.*without.*rent
### **Solution**
  // Anchor handles this with init, but verify space calculation
  #[account(
      init,
      payer = user,
      space = 8 + MyAccount::INIT_SPACE, // 8 byte discriminator + data
  )]
  pub my_account: Account<'info, MyAccount>,
  
  // Manual: Calculate rent
  let rent = Rent::get()?;
  let lamports = rent.minimum_balance(account_size);
  
### **References**
  - https://docs.solana.com/developing/programming-model/accounts#rent

## Transaction Size Limit Exceeded

### **Id**
transaction-size-limit
### **Severity**
HIGH
### **Description**
Transaction exceeds 1232 byte limit
### **Symptoms**
  - Transactions failing silently
  - "Transaction too large" errors
  - Batch operations failing
### **Detection Pattern**
multiple.*accounts.*single.*transaction
### **Solution**
  // Break into multiple transactions
  // Use lookup tables for repeated accounts
  const lookupTable = await connection.getAddressLookupTable(tableAddress);
  
  const message = new TransactionMessage({
      payerKey: payer.publicKey,
      recentBlockhash,
      instructions,
  }).compileToV0Message([lookupTable.value]);
  
  // Or use Jito bundles for atomic multi-tx
  
### **References**
  - https://docs.solana.com/developing/versioned-transactions

## Compute Unit Budget Exceeded

### **Id**
compute-unit-exhaustion
### **Severity**
HIGH
### **Description**
Program exceeds default 200k compute units
### **Symptoms**
  - Transaction failures with "exceeded CUs"
  - Complex operations failing
  - Loops causing issues
### **Detection Pattern**
for.*in.*iter|while.*loop
### **Solution**
  // Request more compute units
  const modifyComputeUnits = ComputeBudgetProgram.setComputeUnitLimit({
      units: 400000
  });
  
  // Set priority fee
  const addPriorityFee = ComputeBudgetProgram.setComputeUnitPrice({
      microLamports: 1000
  });
  
  // Add to transaction
  transaction.add(modifyComputeUnits, addPriorityFee, ...instructions);
  
### **References**
  - https://docs.solana.com/developing/programming-model/runtime#compute-budget

## Account Resurrection Attack

### **Id**
account-resurrection
### **Severity**
HIGH
### **Description**
Closed accounts can be resurrected with old data
### **Symptoms**
  - Closed accounts reappearing
  - Old state being restored
  - Double-spend possibilities
### **Detection Pattern**
close.*=.*without.*zero
### **Solution**
  // Zero data before closing
  pub fn close_account(ctx: Context<CloseAccount>) -> Result<()> {
      let account = &ctx.accounts.my_account;
      let dest = &ctx.accounts.destination;
  
      // Zero the data
      let mut data = account.try_borrow_mut_data()?;
      data.fill(0);
  
      // Transfer lamports and close
      **dest.lamports.borrow_mut() = dest.lamports()
          .checked_add(account.lamports())
          .unwrap();
      **account.lamports.borrow_mut() = 0;
  
      Ok(())
  }
  
### **References**
  - https://www.soldev.app/course/closing-accounts

## Token Mint Without Freeze Authority

### **Id**
missing-freeze-authority
### **Severity**
MEDIUM
### **Description**
Creating tokens without ability to freeze malicious accounts
### **Symptoms**
  - Cannot freeze attacker accounts
  - No recourse for stolen tokens
  - Compliance issues
### **Detection Pattern**
initialize_mint.*freeze_authority.*None
### **Solution**
  // Include freeze authority for compliance
  token::initialize_mint(
      CpiContext::new(
          ctx.accounts.token_program.to_account_info(),
          InitializeMint {
              mint: ctx.accounts.mint.to_account_info(),
              rent: ctx.accounts.rent.to_account_info(),
          },
      ),
      decimals,
      &ctx.accounts.authority.key(),
      Some(&ctx.accounts.freeze_authority.key()), // Don't use None
  )?;
  
### **References**
  - https://spl.solana.com/token#freezing-accounts

## Single Oracle Price Dependency

### **Id**
oracle-price-manipulation
### **Severity**
MEDIUM
### **Description**
Relying on single price oracle without validation
### **Symptoms**
  - Flash loan price manipulation
  - Stale price exploitation
  - Oracle failure causing issues
### **Detection Pattern**
price.*oracle.*single|get_price.*without.*staleness
### **Solution**
  // Use multiple oracles and validate
  let pyth_price = get_pyth_price(&ctx.accounts.pyth_oracle)?;
  let switchboard_price = get_switchboard_price(&ctx.accounts.switchboard)?;
  
  // Check staleness
  require!(
      pyth_price.publish_time > Clock::get()?.unix_timestamp - MAX_STALENESS,
      ErrorCode::StalePrice
  );
  
  // Check deviation
  let deviation = calculate_deviation(pyth_price.price, switchboard_price);
  require!(deviation < MAX_DEVIATION, ErrorCode::PriceDeviation);
  
### **References**
  - https://docs.pyth.network/price-feeds/best-practices

## CPI to Unverified Program

### **Id**
missing-program-id-check
### **Severity**
MEDIUM
### **Description**
Cross-program invocation without verifying target program ID
### **Symptoms**
  - Calls to malicious programs
  - Fund theft via fake programs
  - State corruption
### **Detection Pattern**
CpiContext::new.*without.*program.*check
### **Solution**
  // Verify program ID before CPI
  #[account(
      constraint = token_program.key() == token::ID @ ErrorCode::InvalidProgram
  )]
  pub token_program: Program<'info, Token>,
  
  // Or manual check
  require!(
      ctx.accounts.external_program.key() == expected_program::ID,
      ErrorCode::InvalidProgramId
  );
  
### **References**
  - https://www.soldev.app/course/arbitrary-cpi

## Unprotected Lamport Withdrawal

### **Id**
lamport-drain
### **Severity**
MEDIUM
### **Description**
SOL can be drained from program accounts
### **Symptoms**
  - Program accounts emptied
  - Rent collection failing
  - Accounts becoming non-rent-exempt
### **Detection Pattern**
lamports.*borrow_mut.*sub|transfer.*sol
### **Solution**
  // Always check minimum balance
  let rent = Rent::get()?;
  let min_balance = rent.minimum_balance(account.data_len());
  
  require!(
      account.lamports() - withdraw_amount >= min_balance,
      ErrorCode::InsufficientBalance
  );
  
  // Or mark accounts as rent-exempt in constraints
  #[account(
      mut,
      constraint = vault.lamports() >= Rent::get()?.minimum_balance(vault.data_len())
  )]
  