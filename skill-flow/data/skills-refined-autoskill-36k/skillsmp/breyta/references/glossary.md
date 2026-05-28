# Glossary
- Flow definition: versioned EDN map that defines triggers, steps, and orchestration.
- End-user flow: a flow intended for others to use, marked with the `:end-user` tag (MVP).
- Installation: a per-user instance of an end-user flow (implemented as a user-scoped prod profile). A user can have multiple installations per flow.
- Flow profile: runtime configuration (bindings + activation inputs + enabled state) for a flow; can be user-scoped (installations) or workspace-scoped (creator usage).
- Bindings: applied slot values and activation inputs for a profile.
- Activation inputs: `:kind :form` values stored via bindings apply (not supplied at activate).
- Draft bindings: bindings used for draft runs only.
- Trigger routing: trigger store state updated on deploy.
