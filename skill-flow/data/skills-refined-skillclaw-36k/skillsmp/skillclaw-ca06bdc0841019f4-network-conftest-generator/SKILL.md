---
name: network-conftest-generator
description: Use this skill when you need to generate and configure a pytest `conftest.py` for automating tests on H3C network devices, ensuring a consistent testing environment.
---

# Skill body

## Objective
Create a `conftest.py` file that serves as the codebase for setting up and tearing down the testing environment for network devices. This file ensures that all network test cases run in a unified network environment, providing shared device resources, topology configurations, and test data.

## Core Resources: H3C Knowledge Base Retrieval Guide
**Important Strategy:** Retrieval must follow the principles of **"iterative cycles"** and **"full library scans."**

**Available Knowledge Bases (each round of retrieval must cover all the following libraries):**
1. **design_ke** (User design experience library)
2. **background_ke** (Historical background library, conftest.py code repository)
3. **v9_press_example** (Common network configuration library)
4. **example_ke** (Test case implementation library)
5. **cmd_ke** (Specific command line/configuration parameters library)
6. **press_config_des** (Standardized configuration steps/processes)

## Knowledge Base Retrieval Scripts
Use the following `bash` scripts to perform the specified knowledge base retrievals.

1. **Retrieve from design_ke** (stores user historical testing experiences, prioritize this): 
   ```bash
   python {current_skill_path}/script/data_search_h3c_example.py --description "IGMP snooping query group" --indexname "design_ke"
   ```

2. **Retrieve from background_ke** (contains historical background code for conftest.py): 
   ```bash
   python {current_skill_path}/script/data_search_h3c_example.py --description "DPI security test" --indexname "background_ke"
   ```

3. **Retrieve from v9_press_example** (contains common network configurations): 
   ```bash
   python {current_skill_path}/script/data_search_h3c_example.py --description "Switch multi-segment configuration" --indexname "v9_press_example"
   ```

4. **Retrieve from example_ke** (contains implementation code for test cases, including some background configuration code): 
   ```bash
   python {current_skill_path}/script/data_search_h3c_example.py --description "DHCP relay" --indexname "example_ke"
   ```

5. **Retrieve from cmd_ke** (stores network device command lines): 
   ```bash
   python {current_skill_path}/script/data_search_h3c_example.py --description "ip address" --indexname "cmd_ke"
   ```

6. **Retrieve from press_config_des** (stores standardized configuration steps): 
   ```bash
   python {current_skill_path}/script/data_search_h3c_example.py --description "time period configuration" --indexname "press_config_des"
   ```

## Workflow

### Step 1: Initialization Check
**Objective:** Ensure a usable `conftest.py` baseline file exists in the working directory.

1. **Check File:** Use `ls` to check if `conftest.py` exists in the current working directory.
2. **Copy if Missing:**
   - **If the file does not exist:**
     - Read the template file: `{current_skill_path}/templates/conftest.py`.
     - Use the `cp` command to copy this file to the current working directory.
   - **If the file exists:**
     - Proceed to Step 2.

### Step 2: Deep Validation and Iterative Knowledge Retrieval
**Objective:** This is the most critical step. Perform multiple rounds of iterative retrieval, ensuring all databases are traversed in each round. Adjust retrieval terms dynamically to fully understand the business context from various dimensions (background + commands + steps).

**Prohibited Actions:**
- **Do not** predefine all retrieval rounds (e.g., "I plan to check BGP in round 1, neighbors in round 2..."). This is incorrect!
- **Must** complete one round of retrieval, **read and analyze** the returned content before deciding what to check next.

**Mandatory Actions:**
- **Todo List:** After each round of retrieval, update the Todo List, but do not delete the verification step.
- **Concurrent Background Retrieval:** Execute multiple database retrieval commands in parallel during each round.