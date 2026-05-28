// Barrel export for action palette

export { ActionPalette } from './ActionPalette';
export { ActionResult } from './ActionResult';
export {
  type AppAction,
  type ActionCategory,
  registerCommand,
  unregisterCommand,
  getCommands,
  getCommandsByCategory,
  searchCommands,
  enableCommand,
  disableCommand,
  clearCommands,
  registerMultiple,
  actionsRegistry,
} from './actions-registry';
export { mockActions } from './mock-actions';
