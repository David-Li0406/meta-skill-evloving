const express = require('express');
const router = express.Router();
const queries = require('../database/queries');
const { NotFoundError, ValidationError } = require('../middleware/errorHandler');

/**
 * GET /api/characters/:id
 * Fetch character details by ID
 */
router.get('/:id', async (req, res, next) => {
  try {
    // 1. Validate input
    const characterId = parseInt(req.params.id, 10);
    
    if (isNaN(characterId) || characterId < 1) {
      throw new ValidationError('Invalid character ID format');
    }
    
    // 2. Query database
    const character = await queries.getCharacterById(characterId);
    
    // 3. Check if found
    if (!character) {
      throw new NotFoundError(`Character with ID ${characterId} not found`);
    }
    
    // 4. Return standard success response
    res.json({
      success: true,
      data: character
    });
  } catch (error) {
    // 5. Pass errors to middleware
    next(error);
  }
});

module.exports = router;
