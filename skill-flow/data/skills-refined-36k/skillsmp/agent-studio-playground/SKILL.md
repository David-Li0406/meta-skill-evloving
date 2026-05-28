---
name: agent-studio-playground
description: Work on Game Playground (frontend /playground and backend game API). Use for adding/debugging games, render modes (scene vs frame), session lifecycle, controls/keyboard, and backend environments (Gymnasium, Snake, Tetris). 游戏游乐场开发：新增/排查游戏、前后端协议、渲染模式(scene/frame)、会话管理、键盘与控制面板。
---

# Agent Studio Game Playground

## Understand the contract (backend API)

- Backend routes live in `backend/main.py`.
- Session selection and env mapping live in `backend/engine/session_manager.py`.
- Gym wrapper (frame rendering) lives in `backend/engine/gym_wrapper.py`.

Endpoints:

- `GET /health`
- `POST /api/game/start` body: `{ "env_id": "<gameId>", "config": { ... } }`
- `POST /api/game/{session_id}/step` body: `{ "action": <int> }`
- `POST /api/game/{session_id}/reset`
- `DELETE /api/game/{session_id}`

Rendering:

- `render.mode === "scene"`: frontend should draw from `render.scene`.
- `render.mode === "frame"`: frontend should display `render.frame` / `state.frame` (often a data URL).

## Understand the frontend wiring

- Lobby: `src/app/playground/page.tsx` + `src/lib/games/registry.ts`
- Game page: `src/app/playground/[gameId]/page.tsx`
- Shared gameplay logic/components: `src/components/features/playground/`
- Scene renderers: `src/components/games/renderers/*`
- Controls/settings: `src/components/games/controls/*`, `src/components/games/settings/*`

## Add a new game (checklist)

1. Register it in `src/lib/games/registry.ts` (`id`, `category`, `renderMode`, `actions`, `available`).
2. Backend:
   - If it’s custom scene mode, add an env in `backend/engine/games/` and map it in `backend/engine/session_manager.py`.
   - If it’s a Gym env, ensure the `env_id` is valid for `gymnasium.make`.
3. Frontend:
   - For `renderMode: "scene"`, add/extend renderer + types under `src/components/games/`.
   - Update keyboard mapping/controls/settings as needed.
4. Verify the API payload shape matches `src/components/features/playground/types.ts`.

## Smoke test the backend game API

Run the bundled script after starting the backend:

- `python docs/skills/agent-studio-playground/scripts/smoke_game_api.py --env-id CartPole-v1 --steps 5`

