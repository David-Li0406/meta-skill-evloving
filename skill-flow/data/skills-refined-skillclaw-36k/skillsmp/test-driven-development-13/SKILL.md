### /mnt/data2/nhlstats/.github/skills/test-driven-development/SKILL.md
```markdown
1: ---
2: name: test-driven-development
3: description: Test-Driven Development workflow and best practices for the betting system, including Red-Green-Refactor cycle, test-first development, incremental implementation, and unified Elo refactoring patterns.
4: version: 1.2.0
5: ---
6:
7: # Test-Driven Development (TDD)
8:
9: ## Core TDD Workflow
10:
11: **Red → Green → Refactor**
12:
13: 1. **Red**: Write a failing test for the next piece of functionality
14: 2. **Green**: Write minimal code to make the test pass
15: 3. **Refactor**: Clean up code while keeping tests green
16: 4. **Redeploy**: docker compose down && docker compose up -d
17: 5. **Clear Failed Tasks in DagRun**: Wait for docker containers to start and run the following:
18: ```
19: airflow tasks clear \
20:     --dag-id <your_dag_id> \
21:     --start-date <run_execution_date> \
22:     --only-failed \
23:     --recursive
24: ```
25:
26: ## TDD Process for New Features
27:
28: ### Step 1: Write the Test First
29:
30: Before writing any implementation code, write a test that describes the desired behavior:
31:
32: ```python
33: # tests/test_new_feature.py
34: def test_calculate_edge_returns_difference():
35:     """Edge should be elo_prob minus market_prob."""
36:     elo_prob = 0.65
37:     market_prob = 0.55
38:
39:     edge = calculate_edge(elo_prob, market_prob)
40:
41:     assert edge == 0.10
42: ```
43:
44: **Run it** - it should fail (Red):
45: ```bash
46: pytest tests/test_new_feature.py
47: # FAILED - function doesn't exist yet
48: ```
49:
50: ### Step 2: Write Minimal Implementation
51:
52: Write just enough code to make the test pass:
53:
54: ```python
55: # plugins/betting_logic.py
56: def calculate_edge(elo_prob: float, market_prob: float) -> float:
57:     """Calculate betting edge."""
58:     return elo_prob - market_prob
59: ```
60:
61: **Run it** - test should pass (Green):
62: ```bash
63: pytest tests/test_new_feature.py
64: # PASSED
65: ```
66:
67: ### Step 3: Refactor
68:
69: Add type hints, docstrings, error handling while keeping tests green:
70:
71: ```python
72: def calculate_edge(elo_prob: float, market_prob: float) -> float:
73:     """Calculate betting edge as difference between model and market probabilities.
74:
75:     Args:
76:         elo_prob: Elo model probability (0.0 to 1.0)
77:         market_prob: Market implied probability (0.0 to 1.0)
78:
79:     Returns:
80:         Edge value, positive indicates favorable bet
81:
82:     Raises:
83:         ValueError: If probabilities outside valid range
84:     """
85:     if not (0 <= elo_prob <= 1 and 0 <= market_prob <= 1):
86:         raise ValueError("Probabilities must be between 0 and 1")
87:     return elo_prob - market_prob
88: ```
89:
90: ### Step 4: Add More Test Cases
91:
92: Test edge cases and error conditions:
93:
94: ```python
95: def test_calculate_edge_negative_edge():
96:     """Edge can be negative when market is favored."""
97:     assert calculate_edge(0.45, 0.60) == -0.15
98:
99: def test_calculate_edge_validates_bounds():
100:     """Should reject invalid probability values."""
101:     with pytest.raises(ValueError):
102:         calculate_edge(1.5, 0.5)
103: ```
104:
105:

## ✅ Case Study: Unified Elo Refactoring - COMPLETED

**Project**: Refactoring 9 sport-specific Elo classes to inherit from unified `BaseEloRating` interface

**Timeline**: Completed January 2026

**Methodology**: Strict TDD approach for each sport class

### TDD Process Applied

1. **For Each Sport Class**:
   - Created TDD test file (`test_[sport]_elo_tdd.py`) with failing tests
   - Tests covered: inheritance, required methods, functionality, backward compatibility
   - Refactored class to inherit from `BaseEloRating`
   - Implemented missing abstract methods
   - Added `legacy_update()` for backward compatibility
   - Ran tests until all passed

2. **Test Coverage**:
   - **NHLEloRating**: Existing tests + TDD validation
   - **NBAEloRating**: 3 TDD tests
   - **MLBEloRating**: 10 existing tests
   - **NFLEloRating**: 7 existing tests
   - **EPLEloRating**: 5 TDD tests
   - **Ligue1EloRating**: 6 TDD tests
   - **NCAABEloRating**: 10 TDD tests
   - **WNCAABEloRating**: 10 TDD tests
   - **TennisEloRating**: 12 TDD tests (most complex)

3. **Key Challenges & Solutions**:
   - **Tennis Interface Mismatch**: Created adapter methods (`predict_team()`, `update_team()`) to bridge player-based and team-based interfaces
   - **Backward Compatibility**: Added `legacy_update()` methods to maintain existing API
   - **Import Standardization**: Updated 44 files to use `from plugins.elo import ClassName` pattern

### Results

- **✅ 9/9 sport classes** successfully refactored
- **✅ All existing tests** continue to pass
- **✅ Unified interface** established across all sports
- **✅ Backward compatibility** maintained
- **✅ Code organization** improved with `plugins/elo/` directory

### Lessons Learned

1. **TDD ensures correctness**: Each refactoring was validated by comprehensive tests
2. **Incremental approach**: One sport at a time minimized risk
3. **Documentation is key**: Updated `PROJECT_PLAN.md` and `CHANGELOG.md` after each completion
4. **Complex adaptations possible**: Tennis showed that even significantly different interfaces can be adapted to a unified base

## TDD for Unified Elo Refactoring
106:
107: ### Pattern for Refactoring Sport Elo Classes
108:
109: When refactoring sport-specific Elo classes to inherit from `BaseEloRating`:
110:
111: 1. **Create TDD test file** (`tests/test_{sport}_elo_tdd.py`):
112: ```python
113: """
114: Test suite for {Sport}EloRating using TDD approach.
115: Tests the refactored {Sport}EloRating that inherits from BaseEloRating.
116: """
117:
118: import pytest
119: import sys
120: import os
121: sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
122:
123: from plugins.elo import BaseEloRating, {Sport}EloRating
124:
125: class Test{Sport}EloRatingTDD:
126:     """Test {Sport}EloRating refactoring using TDD."""
127:
128:     def test_{sport}_elo_inherits_from_base(self):
129:         """Test that {Sport}EloRating inherits from BaseEloRating."""
130:         assert issubclass({Sport}EloRating, BaseEloRating)
131:
132:     def test_{sport}_elo_has_required_methods(self):
133:         """Test that {Sport}EloRating implements all abstract methods."""
134:         elo = {Sport}EloRating()
135:
136:         # Check all abstract methods exist
137:         assert hasattr(elo, 'predict')
138:         assert hasattr(elo, 'update')
139:         assert hasattr(elo, 'get_rating')
140:         assert hasattr(elo, 'expected_score')
141:         assert hasattr(elo, 'get_all_ratings')
142:
143:         # Check method signatures
144:         import inspect
145:         predict_sig = inspect.signature(elo.predict)
146:         assert 'home_team' in predict_sig.parameters
147:         assert 'away_team' in predict_sig.parameters
148:         assert 'is_neutral' in predict_sig.parameters
149:
150:     def test_{sport}_elo_backward_compatibility(self):
151:         """Test backward compatibility with existing functionality."""
152:         elo = {Sport}EloRating()
153:         # Test that sport-specific features still work
154:         # (e.g., 3-way predictions for soccer, recency weighting for NHL)
155:
156:     def test_{sport}_elo_update_functionality(self):
157:         """Test update functionality with new interface."""
158:         elo = {Sport}EloRating()
159:
160:         # Initial ratings
161:         initial_home = elo.get_rating("TeamA")
162:         initial_away = elo.get_rating("TeamB")
163:
164:         # Update with home win
165:         elo.update("TeamA", "TeamB", home_won=True)
166:
167:         # Check ratings changed correctly
168:         new_home = elo.get_rating("TeamA")
169:         new_away = elo.get_rating("TeamB")
170:
171:         assert new_home > initial_home  # Winner gains points
172:         assert new_away < initial_away  # Loser loses points
173:
174:     def test_{sport}_elo_get_all_ratings(self):
175:         """Test get_all_ratings method."""
176:         elo = {Sport}EloRating()
177:
178:         # Add some ratings
179:         elo.update("TeamA", "TeamB", home_won=True)
180:         elo.update("TeamC", "TeamD", home_won=False)
181:
182:         all_ratings = elo.get_all_ratings()
183:
184:         assert isinstance(all_ratings, dict)
185:         assert "TeamA" in all_ratings
186:         assert "TeamB" in all_ratings
187:         assert "TeamC" in all_ratings
188:         assert "TeamD" in all_ratings
189: ```
190:
191: 2. **Run tests (Red phase)** - Tests should fail because class doesn't inherit from BaseEloRating yet.
192:
193: 3. **Refactor the sport class (Green phase)**:
194: ```python
195: # plugins/elo/{sport}_elo_rating.py
196: from .base_elo_rating import BaseEloRating
197: from typing import Dict, Union
198:
199: class {Sport}EloRating(BaseEloRating):  # Changed to inherit from BaseEloRating
200:     def __init__(self, k_factor: float = 20.0, home_advantage: float = 100.0, initial_rating: float = 1500.0):
201:         super().__init__(k_factor=k_factor, home_advantage=home_advantage, initial_rating=initial_rating)
202:
203:     def predict(self, home_team: str, away_team: str, is_neutral: bool = False) -> float:
204:         # Implementation...
205:
206:     def update(self, home_team: str, away_team: str, home_won: Union[bool, float], is_neutral: bool = False) -> None:
207:         # Implementation...
208:
209:     def get_rating(self, team: str) -> float:
210:         # Implementation...
211:
212:     def expected_score(self, rating_a: float, rating_b: float) -> float:
213:         return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))
214:
215:     def get_all_ratings(self) -> Dict[str, float]:
216:         return self.ratings.copy()
217:
218:     # Add legacy_update for backward compatibility
219:     def legacy_update(self, home_team: str, away_team: str, result: Union[str, int]) -> float:
220:         """Legacy update method for backward compatibility."""
221:         # Convert legacy result to home_won
222:         # Call self.update() with converted parameters
223:         # Return rating change for compatibility
224: ```
225:
226: 4. **Run tests again (Green phase)** - All tests should pass.
227:
228: 5. **Update project documentation**:
229:    - Update `PROJECT_PLAN.md` to mark task as completed
230:    - Update `CHANGELOG.md` with detailed entry
231:    - Update `.github/copilot-instructions.md` if needed
232:
233: ## TDD for Airflow Tasks
234:
235: ### Test Task Functions Directly
236:
237: ```python
238: # tests/test_dag_tasks.py
239: from unittest.mock import MagicMock, patch
240:
241: def test_update_elo_task_success():
242:     """update_elo_ratings should process games and return count."""
243:     mock_games = pd.DataFrame({
244:         'home_team': ['Lakers', 'Warriors'],
245:         'away_team': ['Celtics', 'Suns'],
246:         'home_won': [True, False]
247:     })
248:
249:     with patch('plugins.nba_games.fetch_recent_games', return_value=mock_games):
250:         result = update_elo_ratings(sport='nba')
251:
252:     assert result['games_processed'] == 2
253:     assert 'ratings_updated' in result
254: ```
255:
256: ## Mocking External Dependencies
257:
258: ### Mock Database Queries
259:
260: ```python
261: @pytest.fixture
262: def mock_db_manager():
263:     with patch('plugins.db_manager.DBManager') as mock:
264:         mock.return_value.fetch_df.return_value = pd.DataFrame()
265:         yield mock.return_value
266: ```
267:
268: ### Mock Kalshi API
269:
270: ```python
271: @pytest.fixture
272: def mock_kalshi_client():
273:     with patch('plugins.kalshi_markets.KalshiClient') as mock:
274:         mock.return_value.get_markets.return_value = [
275:             {'ticker': 'NBA-LAKERS-CELTICS', 'yes_price': 55}
276:         ]
277:         yield mock.return_value
278: ```
279:
280: ### Mock External APIs
281:
282: ```python
283: @patch('requests.get')
284: def test_fetch_games_handles_api_error(mock_get):
285:     """Should handle API failures gracefully."""
286:     mock_get.side_effect = requests.RequestException("API down")
287:
288:     games = fetch_nba_games()
289:
290:     assert games.empty
291: ```
292:
293: ## Incremental Development Pattern
294:
295: Build features one small piece at a time:
296:
297: 1. **Start with core logic** (pure functions, easy to test)
298: 2. **Add data access** (mock database)
299: 3. **Add external integrations** (mock APIs)
300: 4. **Add Airflow orchestration** (task wrappers)
301:
302: ### Example: Adding a New Statistic
303:
304: ```python
305: # Step 1: Test pure calculation
306: def test_win_streak_calculates_correctly():
307:     games = [True, True, False, True]
308:     assert calculate_win_streak(games) == 1
309:
310: # Step 2: Test database integration
311: def test_load_team_recent_games(mock_db):
312:     mock_db.fetch_df.return_value = sample_games_df
313:     games = load_recent_games('Lakers', db=mock_db)
314:     assert len(games) == 5
315:
316: # Step 3: Test full feature
317: def test_get_team_win_streak_end_to_end(mock_db):
318:     result = get_team_win_streak('Lakers', db=mock_db)
319:     assert result >= 0
320: ```
321:
322: ## Coverage Targets
323:
324: **Maintain 85%+ coverage** across all modules:
325:
326: ```bash
327: # Check coverage
328: pytest --cov=plugins --cov=dags --cov-report=term-missing
329:
330: # Fail if below threshold
331: pytest --cov=plugins --cov-fail-under=85
332: ```
333:
334: **Add tests when coverage drops:**
335: ```bash
336: # Identify untested lines
337: pytest --cov=plugins/nba_elo_rating --cov-report=term-missing
338:
339: # Focus on uncovered lines marked with "Missing"
340: ```
341:
342: ## Code Formatting
343:
344: **Run Black before committing:**
345:
346: ```bash
347: black plugins/ dags/ tests/
348: ```
349:
350: **Check without modifying:**
351: ```bash
352: black --check plugins/ dags/ tests/
353: ```
354:
355: ## Test Organization Best Practices
356:
357: ### One Test Class per Class
358:
359: ```python
360: class TestNBAEloRating:
361:     def test_predict_returns_probability(self):
362:         ...
363:
364:     def test_update_modifies_ratings(self):
365:         ...
366:
367:     def test_get_rating_initializes_new_teams(self):
368:         ...
369: ```
370:
371: ### Descriptive Test Names
372:
373: Use pattern: `test_{function}_{scenario}_{expected}`
374:
375: ```python
376: def test_predict_home_favorite_returns_high_probability()
377: def test_predict_even_teams_returns_fifty_fifty()
378: def test_update_home_win_increases_home_rating()
379: ```
380:
381: ### Arrange-Act-Assert Pattern
382:
383: ```python
384: def test_example():
385:     # Arrange - set up test data
386:     elo = NBAEloRating(k_factor=20)
387:
388:     # Act - perform the action
389:     prob = elo.predict('Lakers', 'Celtics')
390:
391:     # Assert - verify the result
392:     assert 0.0 <= prob <= 1.0
393: ```
394:
395: ## When to Write Tests
396:
397: 1. **Before writing new features** (true TDD)
398: 2. **Before fixing bugs** (regression tests)
399: 3. **When coverage drops below 85%**
400: 4. **Before refactoring** (safety net)
401: 5. **When refactoring to unified interfaces** (e.g., BaseEloRating)
402:
403: ## Running Tests
404:
405: ```bash
406: # All tests
407: pytest
408:
409: # Specific file
410: pytest tests/test_nba_elo_rating.py
411:
412: # Specific test
413: pytest tests/test_nba_elo_rating.py::test_predict_returns_probability
414:
415: # With coverage
416: pytest --cov=plugins
417:
418: # Verbose output
419: pytest -v
420:
421: # Stop on first failure
422: pytest -x
423:
424: # Run only failed tests from last run
425: pytest --lf
426: ```
427:
428: ## Quick Reference
429:
430: | Phase | Action | Command |
431: |-------|--------|---------|
432: | Red | Write failing test | `pytest tests/test_new.py` |
433: | Green | Implement minimal code | `pytest tests/test_new.py` |
434: | Refactor | Clean up, add types | `black plugins/` |
435: | Verify | Check coverage | `pytest --cov=plugins` |
436: | Commit | All green, 85%+ coverage | `git commit` |
437:
438: ## Key Principles
439:
440: 1. **Write tests first** - drives better design
441: 2. **Small steps** - one test at a time
442: 3. **Keep tests fast** - mock external dependencies
443: 4. **Descriptive names** - tests are documentation
444: 5. **Maintain coverage** - 85% minimum
445: 6. **Run frequently** - fast feedback loop
446: 7. **Document refactoring** - update CHANGELOG and PROJECT_PLAN
447:
448: ## Unified Elo Refactoring Examples
449:
450: **Successfully refactored using TDD:**
451: - `tests/test_nhl_elo_tdd.py` - NHL with recency weighting
452: - `tests/test_nba_elo_tdd.py` - NBA canonical implementation
453: - `tests/test_epl_elo_tdd.py` - EPL with 3-way outcomes
454: - `tests/test_ligue1_elo_tdd.py` - Ligue1 with 3-way outcomes
455:
456: **Current refactoring status:** 6/9 sports completed using TDD approach
```
