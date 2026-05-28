import { createCliRenderer, Box, Text, InputRenderable, InputRenderableEvents, type KeyEvent, TextAttributes } from '@opentui/core';

async function main() {
  const renderer = await createCliRenderer({
    exitOnCtrlC: true,
    targetFps: 30,
  });

  renderer.setBackgroundColor('#001122');

  // Create a simple input form using declarative approach
  const container = Box({
    flexDirection: 'column',
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  });

  renderer.root.add(container);

  const title = Text({
    content: 'OpenTUI Demo',
    attributes: TextAttributes.BOLD,
    fg: '#00FF00',
  });
  container.add(title);

  const subtitle = Text({
    content: 'A working example',
    fg: '#666666',
    marginBottom: 2,
  });
  container.add(subtitle);

  // Using imperative InputRenderable
  const input = new InputRenderable(renderer, {
    id: 'demo-input',
    width: 30,
    height: 3,
    placeholder: 'Type something...',
    placeholderColor: '#666666',
    backgroundColor: '#1a1a1a',
    textColor: '#FFFFFF',
    cursorColor: '#FFFF00',
    focusedBackgroundColor: '#2a2a2a',
  });

  renderer.root.add(input);
  input.focus();

  const output = Text({
    content: '',
    marginTop: 1,
  });
  container.add(output);

  // Handle input events
  input.on(InputRenderableEvents.INPUT, (value) => {
    output.content = `You typed: ${value}`;
  });

  input.on(InputRenderableEvents.ENTER, (value) => {
    output.content = `Submitted: ${value}`;
  });

  // Add instructions
  const instructions = Box({
    flexDirection: 'column',
    marginTop: 3,
    padding: 1,
    border: true,
    backgroundColor: '#111',
    borderColor: '#333',
  });

  instructions.add(Text({ content: 'Controls:', attributes: TextAttributes.BOLD }));
  instructions.add(Text({ content: 'Type: Enter text', fg: '#888' }));
  instructions.add(Text({ content: 'Enter: Submit', fg: '#888' }));
  instructions.add(Text({ content: 'q: Quit', fg: '#888' }));
  instructions.add(Text({ content: 'Ctrl+C: Quit', fg: '#888' }));

  container.add(instructions);

  // Keyboard shortcuts
  renderer.keyInput.on('keypress', (key: KeyEvent) => {
    if (key.name === 'q') {
      process.exit(0);
    }
  });

  renderer.start();
}

main();
