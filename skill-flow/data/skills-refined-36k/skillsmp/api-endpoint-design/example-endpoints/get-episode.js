const express = require('express');
const router = express.Router();
const queries = require('../database/queries');
const { ValidationError } = require('../middleware/errorHandler');

/**
 * GET /api/episodes
 * List episodes with optional filtering
 */
router.get('/', async (req, res, next) => {
  try {
    // 1. Parse and validate query parameters
    const showId = req.query.showId ? parseInt(req.query.showId, 10) : null;
    const season = req.query.season ? parseInt(req.query.season, 10) : null;
    
    if (showId !== null && (isNaN(showId) || showId < 1)) {
      throw new ValidationError('Invalid showId parameter');
    }
    
    if (season !== null && (isNaN(season) || season < 1)) {
      throw new ValidationError('Invalid season parameter');
    }
    
    // 2. Build filters object
    const filters = {};
    if (showId) filters.showId = showId;
    if (season) filters.season = season;
    
    // 3. Query with filters
    const episodes = await queries.getEpisodes(filters);
    
    // 4. Return paginated response
    res.json({
      success: true,
      data: {
        episodes,
        count: episodes.length,
        filters: filters
      }
    });
  } catch (error) {
    next(error);
  }
});

module.exports = router;
