/**
 * Styles for icon-wc component
 */
const styles = `
:host {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.5em;
  height: 1.5em;
  vertical-align: middle;
  line-height: 1;
}

:host([size="xs"]) {
  width: 1em;
  height: 1em;
}

:host([size="sm"]) {
  width: 1.25em;
  height: 1.25em;
}

:host([size="md"]) {
  width: 1.5em;
  height: 1.5em;
}

:host([size="lg"]) {
  width: 2em;
  height: 2em;
}

:host([size="xl"]) {
  width: 2.5em;
  height: 2.5em;
}

:host([size="2xl"]) {
  width: 3em;
  height: 3em;
}

svg {
  width: 100%;
  height: 100%;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

/* Error state */
:host([data-error]) {
  opacity: 0.5;
}

/* Hidden state for missing icons */
:host([hidden]) {
  display: none;
}
`;

export { styles };
