# Solana Development

## Patterns


---
  #### **Name**
PDA Account Pattern
  #### **Description**
Using Program Derived Addresses for deterministic account creation
  #### **When**
Need program-owned accounts with predictable addresses
  #### **Example**
    #[derive(Accounts)]
    #[instruction(user_id: u64)]
    pub struct CreateUserAccount<'info> {
        #[account(
            init,
            payer = authority,
            space = 8 + UserAccount::INIT_SPACE,
            seeds = [b"user", authority.key().as_ref(), &user_id.to_le_bytes()],
            bump
        )]
        pub user_account: Account<'info, UserAccount>,
        #[account(mut)]
        pub authority: Signer<'info>,
        pub system_program: Program<'info, System>,
    }
    

---
  #### **Name**
CPI with Signer Seeds
  #### **Description**
Cross-program invocations using PDA as signer
  #### **When**
Program needs to sign transactions on behalf of PDA accounts
  #### **Example**
    let seeds = &[
        b"vault",
        user.key().as_ref(),
        &[ctx.bumps.vault],
    ];
    let signer_seeds = &[&seeds[..]];
    
    let cpi_ctx = CpiContext::new_with_signer(
        ctx.accounts.token_program.to_account_info(),
        Transfer {
            from: ctx.accounts.vault.to_account_info(),
            to: ctx.accounts.user_token.to_account_info(),
            authority: ctx.accounts.vault.to_account_info(),
        },
        signer_seeds,
    );
    token::transfer(cpi_ctx, amount)?;
    

---
  #### **Name**
Account Validation Pattern
  #### **Description**
Comprehensive account validation with Anchor constraints
  #### **When**
Any instruction that modifies state
  #### **Example**
    #[derive(Accounts)]
    pub struct ProcessTrade<'info> {
        #[account(
            mut,
            seeds = [b"pool", pool.token_a_mint.as_ref()],
            bump = pool.bump,
            has_one = token_a_vault,
            has_one = token_b_vault,
            constraint = !pool.paused @ ErrorCode::PoolPaused
        )]
        pub pool: Account<'info, Pool>,
        #[account(
            mut,
            constraint = token_a_vault.owner == pool.key() @ ErrorCode::InvalidVaultOwner
        )]
        pub token_a_vault: Account<'info, TokenAccount>,
        // ... more accounts with constraints
    }
    

---
  #### **Name**
Zero-Copy Account Pattern
  #### **Description**
Using zero-copy deserialization for large accounts
  #### **When**
Account data exceeds 10KB or needs frequent partial access
  #### **Example**
    #[account(zero_copy)]
    #[repr(C)]
    pub struct OrderBook {
        pub authority: Pubkey,
        pub bids: [Order; 256],
        pub asks: [Order; 256],
        pub bid_count: u64,
        pub ask_count: u64,
    }
    
    // Access without full deserialization
    let order_book = ctx.accounts.order_book.load_mut()?;
    order_book.bids[0] = new_order;
    

---
  #### **Name**
Event Emission Pattern
  #### **Description**
Emitting events for off-chain indexing
  #### **When**
State changes need to be tracked by indexers or UIs
  #### **Example**
    #[event]
    pub struct TradeExecuted {
        pub pool: Pubkey,
        pub user: Pubkey,
        pub amount_in: u64,
        pub amount_out: u64,
        pub timestamp: i64,
    }
    
    emit!(TradeExecuted {
        pool: ctx.accounts.pool.key(),
        user: ctx.accounts.user.key(),
        amount_in,
        amount_out,
        timestamp: Clock::get()?.unix_timestamp,
    });
    

---
  #### **Name**
Versioned Account Migration
  #### **Description**
Supporting account schema upgrades without data loss
  #### **When**
Need to add fields to existing accounts
  #### **Example**
    #[account]
    pub struct UserAccountV2 {
        pub version: u8,
        pub authority: Pubkey,
        pub balance: u64,
        // New field in V2
        pub rewards_earned: u64,
    }
    
    pub fn migrate_account(ctx: Context<Migrate>) -> Result<()> {
        let account = &mut ctx.accounts.user_account;
        require!(account.version == 1, ErrorCode::AlreadyMigrated);
        account.version = 2;
        account.rewards_earned = 0;
        Ok(())
    }
    

## Anti-Patterns


---
  #### **Name**
Missing Account Ownership Check
  #### **Description**
Not verifying the program owns accounts it's modifying
  #### **Why**
Attackers can pass fake accounts with manipulated data
  #### **Instead**
    // Always use Anchor's Account<> wrapper or manual ownership check
    require!(
        account.owner == program_id,
        ErrorCode::InvalidAccountOwner
    );
    

---
  #### **Name**
Predictable PDA Without User Context
  #### **Description**
PDAs derived only from static seeds
  #### **Why**
Anyone can find and potentially manipulate the account
  #### **Instead**
    // Include user-specific data in seeds
    seeds = [b"vault", user.key().as_ref(), &nonce.to_le_bytes()]
    

---
  #### **Name**
Arithmetic Without Overflow Protection
  #### **Description**
Using basic arithmetic operators on token amounts
  #### **Why**
Overflow/underflow can cause exploits or unexpected behavior
  #### **Instead**
    // Use checked math or Anchor's require! with explicit bounds
    let new_balance = current_balance
        .checked_add(deposit_amount)
        .ok_or(ErrorCode::MathOverflow)?;
    

---
  #### **Name**
Hardcoded Compute Budget
  #### **Description**
Assuming fixed compute unit costs
  #### **Why**
Network conditions and program changes affect costs
  #### **Instead**
    // Let users set compute budget, provide estimates
    ComputeBudgetInstruction::set_compute_unit_limit(300_000)
    ComputeBudgetInstruction::set_compute_unit_price(1_000)
    

---
  #### **Name**
Closing Accounts Without Zeroing
  #### **Description**
Closing accounts but leaving data intact
  #### **Why**
Resurrection attacks can restore closed accounts
  #### **Instead**
    // Zero account data before closing
    let dest_starting_lamports = dest_account_info.lamports();
    **dest_account_info.lamports.borrow_mut() = dest_starting_lamports
        .checked_add(source_account_info.lamports())
        .unwrap();
    **source_account_info.lamports.borrow_mut() = 0;
    source_account_info.data.borrow_mut().fill(0);
    

---
  #### **Name**
Single Transaction Assumptions
  #### **Description**
Assuming operations complete in one transaction
  #### **Why**
Complex operations may exceed transaction limits
  #### **Instead**
    // Design multi-instruction flows with intermediate states
    pub enum ProcessingState {
        NotStarted,
        Step1Complete,
        Step2Complete,
        Finalized,
    }
    