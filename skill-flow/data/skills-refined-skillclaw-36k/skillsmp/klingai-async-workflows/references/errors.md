# Error Handling Reference

Common errors and solutions:
1. **State Transition Error**: Verify valid transitions in workflow design
2. **Queue Timeout**: Increase worker timeout or check Redis connection
3. **Stuck Jobs**: Implement job timeout and recovery