const path = require('path');

describe('inkrunner core', () => {
  let inkrunner;
  let story;
  let storyEl;
  let choicesEl;
  let tagsEl;
  let durationInput;
  let intensityInput;
  let saveBtn;
  let loadBtn;

  const buildDOM = () => {
    document.body.innerHTML = `
      <div id="story"></div>
      <div id="choices"></div>
      <div id="tags"></div>
      <button id="save-btn"></button>
      <button id="load-btn"></button>
      <input id="smoke-duration" value="3" />
      <input id="smoke-intensity" value="5" />
    `;
    storyEl = document.getElementById('story');
    choicesEl = document.getElementById('choices');
    tagsEl = document.getElementById('tags');
    durationInput = document.getElementById('smoke-duration');
    intensityInput = document.getElementById('smoke-intensity');
    saveBtn = document.getElementById('save-btn');
    loadBtn = document.getElementById('load-btn');
  };

  const mockStory = ({ canContinue = false, currentChoices = [], currentTags = [], continueImpl } = {}) => {
    const state = {
      toJson: jest.fn(() => 'story-state'),
      LoadJson: jest.fn(),
      currentPathString: 'start'
    };
    const storyObj = {
      canContinue,
      currentChoices,
      currentTags,
      state,
      variablesState: {
        campfire_log: false,
        courage: 0,
        caution: 0,
        met_stranger: false,
        found_artifact: false,
        wolves_spotted: false,
        pocket_compass: true
      },
      Continue: jest.fn(() => {
        if (continueImpl) return continueImpl(storyObj);
        return 'continued text';
      }),
      ChooseChoiceIndex: jest.fn(),
      ChoosePathString: jest.fn()
    };
    return storyObj;
  };

   beforeEach(() => {
     jest.resetModules();
     buildDOM();
     story = mockStory();
 
     global.window.Telemetry = {
       emit: jest.fn(),
       enabled: true,
     };
     global.window.inkjs = { Story: function Stub() {}, Compiler: function Stub() {} };
     global.window.Smoke = {
       trigger: jest.fn(),
       getState: jest.fn(() => ({ smoke: 'state' })),
       loadState: jest.fn(),
     };
     
     // Mock AI Writer modules - disabled by default for base tests
     global.window.ApiKeyManager = {
       getSettings: jest.fn(() => ({ enabled: false })),
       getApiKey: jest.fn(() => null),
       hasApiKey: jest.fn(() => false)
     };
     
     global.window.LoreAssembler = {
       clearHistory: jest.fn(),
       recordChoice: jest.fn(),
       getChoiceHistory: jest.fn(() => []),
       assembleLORE: jest.fn(() => ({})),
       getValidReturnPaths: jest.fn(() => ['campfire'])
     };
 
     jest.spyOn(global.window, 'addEventListener').mockImplementation(() => {});
 
     jest.isolateModules(() => {
       inkrunner = require(path.join(process.cwd(), 'web/demo/js/inkrunner.js'));
       inkrunner.setStory(story);
     });
   });


  it('appendText creates a div with text', () => {
    inkrunner.appendText('hello');
    expect(storyEl.textContent).toBe('hello');
    expect(storyEl.querySelectorAll('div')).toHaveLength(1);
  });

   it('renderChoices creates buttons and handles clicks', async () => {
     const choiceStory = mockStory({ currentChoices: [{ text: 'A' }, { text: 'B' }] });
     inkrunner.setStory(choiceStory);
 
     await inkrunner.renderChoices();
 
     const buttons = choicesEl.querySelectorAll('button.choice-btn');
     expect(buttons.length).toBeGreaterThanOrEqual(2);
     expect(buttons[0].textContent).toBe('A');
 
     buttons[1].dispatchEvent(new window.Event('click'));
     expect(choiceStory.ChooseChoiceIndex).toHaveBeenCalledWith(1);
     expect(storyEl.innerHTML).toBe('');
     expect(window.Telemetry.emit).toHaveBeenCalledWith('choice_selected', undefined);
   });


  it('renderChoices handles touchstart', async () => {
    const choiceStory = mockStory({ currentChoices: [{ text: 'A' }, { text: 'B' }] });
    inkrunner.setStory(choiceStory);

    await inkrunner.renderChoices();
    const buttons = choicesEl.querySelectorAll('button.choice-btn');

    buttons[0].dispatchEvent(new window.Event('touchstart'));

    expect(choiceStory.ChooseChoiceIndex).toHaveBeenCalledWith(0);
  });

  it('handleTags renders tags and triggers smoke', () => {
    durationInput.value = '7';
    intensityInput.value = '9';

    inkrunner.handleTags(['smoke', 'cool']);

    expect(tagsEl.textContent).toBe('Tags: smoke, cool');
    expect(window.Smoke.trigger).toHaveBeenCalledWith({ duration: 7, intensity: 9 });
  });

  it('handleTags shows none when empty', () => {
    inkrunner.handleTags([]);
    expect(tagsEl.textContent).toBe('Tags: none');
  });

  it('saveState writes to localStorage including loreHistory', () => {
    const setItem = jest.spyOn(window.localStorage.__proto__, 'setItem');
    inkrunner.setStory(story);

    inkrunner.saveState();

    expect(setItem).toHaveBeenCalledTimes(1);
    const [key, value] = setItem.mock.calls[0];
    expect(key).toBe('ge-hch.smoke.save');
    const parsed = JSON.parse(value);
    expect(parsed.story).toBe('story-state');
    expect(parsed.smoke).toEqual({ smoke: 'state' });
    expect(parsed.config).toEqual({ duration: 3, intensity: 5 });
    expect(parsed.loreHistory).toBeDefined();
  });

  it('loadState restores story, smoke, inputs, and continues', () => {
    const saved = {
      story: 'saved-story',
      smoke: { s: 1 },
      config: { duration: 11, intensity: 13 },
      loreHistory: [{ text: 'Previous choice', timestamp: 123 }]
    };
    window.localStorage.setItem('ge-hch.smoke.save', JSON.stringify(saved));

    const continuingStory = mockStory({
      canContinue: true,
      continueImpl: (s) => {
        s.canContinue = false;
        return 'restored text';
      },
    });
    inkrunner.setStory(continuingStory);

    inkrunner.loadState();

    expect(continuingStory.state.LoadJson).toHaveBeenCalledWith('saved-story');
    expect(window.Smoke.loadState).toHaveBeenCalledWith({ s: 1 });
    expect(durationInput.value).toBe('11');
    expect(intensityInput.value).toBe('13');
    expect(tagsEl.textContent).toBe('Tags: none');
    expect(storyEl.textContent).toContain('restored text');
    // Verify LORE history restoration
    expect(window.LoreAssembler.clearHistory).toHaveBeenCalled();
    expect(window.LoreAssembler.recordChoice).toHaveBeenCalledWith('Previous choice');
  });

  it('handleChoiceSelection records choice in LORE history', () => {
    const choiceStory = mockStory({ currentChoices: [{ text: 'Test Choice' }] });
    inkrunner.setStory(choiceStory);

    inkrunner.handleChoiceSelection(0, 'Test Choice');

    expect(window.LoreAssembler.recordChoice).toHaveBeenCalledWith('Test Choice');
  });
});

describe('inkrunner AI integration', () => {
  let inkrunner;
  let story;

  const buildDOM = () => {
    document.body.innerHTML = `
      <div id="story"></div>
      <div id="choices"></div>
      <div id="tags"></div>
      <button id="save-btn"></button>
      <button id="load-btn"></button>
      <input id="smoke-duration" value="3" />
      <input id="smoke-intensity" value="5" />
    `;
  };

  const mockStory = ({ currentChoices = [] } = {}) => ({
    canContinue: false,
    currentChoices,
    currentTags: [],
    state: {
      toJson: jest.fn(() => 'story-state'),
      LoadJson: jest.fn(),
      currentPathString: 'pines'
    },
    variablesState: {
      courage: 2,
      caution: 1
    },
    Continue: jest.fn(() => 'text'),
    ChooseChoiceIndex: jest.fn(),
    ChoosePathString: jest.fn()
  });

  beforeEach(() => {
    jest.resetModules();
    buildDOM();
    story = mockStory({ currentChoices: [{ text: 'A' }] });

    global.window.Telemetry = { emit: jest.fn() };
    global.window.inkjs = { Story: function() {}, Compiler: function() {} };
    global.window.Smoke = {
      trigger: jest.fn(),
      getState: jest.fn(() => ({})),
      loadState: jest.fn()
    };

    // Enable AI for these tests
    global.window.ApiKeyManager = {
      getSettings: jest.fn(() => ({ 
        enabled: true, 
        creativity: 0.7,
        aiChoiceStyle: 'distinct',
        showLoadingIndicator: true
      })),
      getApiKey: jest.fn(() => 'sk-test-key'),
      hasApiKey: jest.fn(() => true)
    };

    global.window.LoreAssembler = {
      clearHistory: jest.fn(),
      recordChoice: jest.fn(),
      getChoiceHistory: jest.fn(() => []),
      assembleLORE: jest.fn(() => ({
        player_state: { courage: 2, caution: 1, inventory: [] },
        game_state: { current_scene: 'pines', context_type: 'exploration' },
        narrative_context: { recent_choices: [], tone: 'mysterious' }
      })),
      getValidReturnPaths: jest.fn(() => ['campfire', 'return_with_supplies'])
    };

    global.window.PromptEngine = {
      buildAutoPrompt: jest.fn(() => ({
        systemPrompt: 'System prompt',
        userPrompt: 'User prompt',
        templateType: 'exploration'
      }))
    };

    global.window.LLMAdapter = {
      generateProposal: jest.fn(() => Promise.resolve({
        choice_text: 'AI generated choice',
        content: {
          text: 'AI generated content',
          return_path: 'campfire'
        },
        metadata: { confidence_score: 0.85 }
      })),
      generateProposalId: jest.fn(() => 'test-uuid-1234')
    };

    global.window.ProposalValidator = {
      quickValidate: jest.fn(() => ({ valid: true }))
    };

    jest.spyOn(global.window, 'addEventListener').mockImplementation(() => {});

    jest.isolateModules(() => {
      inkrunner = require(path.join(process.cwd(), 'web/demo/js/inkrunner.js'));
      inkrunner.setStory(story);
    });
  });

  it('generates AI proposal when enabled', async () => {
    const proposal = await inkrunner.generateAIProposal();

    expect(window.LoreAssembler.assembleLORE).toHaveBeenCalled();
    expect(window.PromptEngine.buildAutoPrompt).toHaveBeenCalled();
    expect(window.LLMAdapter.generateProposal).toHaveBeenCalled();
    expect(window.ProposalValidator.quickValidate).toHaveBeenCalled();
    expect(proposal).toBeDefined();
    expect(proposal.choice_text).toBe('AI generated choice');
  });

  it('returns null when AI is disabled', async () => {
    window.ApiKeyManager.getSettings.mockReturnValue({ enabled: false });

    const proposal = await inkrunner.generateAIProposal();

    expect(proposal).toBeNull();
    expect(window.LLMAdapter.generateProposal).not.toHaveBeenCalled();
  });

  it('returns null when no API key', async () => {
    window.ApiKeyManager.getApiKey.mockReturnValue(null);

    const proposal = await inkrunner.generateAIProposal();

    expect(proposal).toBeNull();
  });

  it('returns null when validation fails', async () => {
    window.ProposalValidator.quickValidate.mockReturnValue({ 
      valid: false, 
      reason: 'Content blocked' 
    });

    const proposal = await inkrunner.generateAIProposal();

    expect(proposal).toBeNull();
  });

  it('playAIBranch displays content and navigates', () => {
    const storyEl = document.getElementById('story');
    const proposal = {
      id: 'test-id',
      choice_text: 'Test choice',
      content: {
        text: 'Test narrative content',
        return_path: 'campfire'
      }
    };

    inkrunner.playAIBranch(proposal);

    expect(storyEl.innerHTML).toContain('AI-Generated Branch');
    expect(storyEl.innerHTML).toContain('Test narrative content');
    expect(story.ChoosePathString).toHaveBeenCalledWith('campfire');
    expect(window.LoreAssembler.recordChoice).toHaveBeenCalledWith('[AI] Test choice');
    expect(window.Telemetry.emit).toHaveBeenCalledWith('ai_branch_played', expect.any(Object));
  });

  it('injects AI choice only when Director approves', async () => {
    const proposal = {
      id: 'p-approve',
      choice_text: 'Approved choice',
      content: {
        text: 'AI content',
        return_path: 'campfire'
      },
      metadata: { confidence_score: 0.9 }
    };

    const evaluateMock = jest.fn((_proposal, _ctx, options) => {
      expect(options).toHaveProperty('riskThreshold', 0.4);
      return { decision: 'approve', reason: 'ok', riskScore: 0.2, latencyMs: 15 };
    });

    window.Director = { evaluate: evaluateMock };

    const result = await inkrunner.addAIChoice({ forceDirectorEnabled: true, mockProposalOverride: proposal });

    expect(result).toBe('approved');
    expect(evaluateMock).toHaveBeenCalledTimes(1);

    const aiButtons = document.querySelectorAll('.choice-btn.ai-choice, .choice-btn.ai-choice-normal');
    expect(aiButtons.length).toBe(1);
    expect(aiButtons[0].textContent).toBe('Approved choice');

    expect(window.Telemetry.emit).toHaveBeenCalledWith(
      'ai_evaluation',
      expect.objectContaining({
        proposal_id: 'p-approve',
        decision: 'approve',
        writerMs: expect.any(Number),
        directorMs: 15,
        totalMs: expect.any(Number)
      })
    );

    expect(window.Telemetry.emit).toHaveBeenCalledWith(
      'ai_choice_generated',
      expect.objectContaining({ proposal_id: 'p-approve' })
    );
  });

  it('skips AI choice when Director rejects', async () => {
    const proposal = {
      id: 'p-reject',
      choice_text: 'Rejected choice',
      content: {
        text: 'AI content',
        return_path: 'campfire'
      },
      metadata: { confidence_score: 0.2 }
    };

    window.Director = {
      evaluate: jest.fn(() => ({ decision: 'reject', reason: 'too risky', latencyMs: 7, riskScore: 0.9 }))
    };

    const result = await inkrunner.addAIChoice({ forceDirectorEnabled: true, mockProposalOverride: proposal });

    expect(result).toBe('rejected');

    const aiButtons = Array.from(document.querySelectorAll('.choice-btn')).filter(btn =>
      btn.classList.contains('ai-choice') || btn.classList.contains('ai-choice-normal')
    );
    expect(aiButtons.length).toBe(0);

    expect(window.Telemetry.emit).toHaveBeenCalledWith(
      'ai_evaluation',
      expect.objectContaining({
        proposal_id: 'p-reject',
        decision: 'reject',
        directorMs: 7,
        totalMs: expect.any(Number)
      })
    );
  });

  it('retains authored choices when Director rejects AI injection', async () => {
    const choicesEl = document.getElementById('choices');
    const choiceStory = mockStory({ currentChoices: [{ text: 'Authored A' }, { text: 'Authored B' }] });
    inkrunner.setStory(choiceStory);

    window.Director = {
      evaluate: jest.fn(async () => ({ decision: 'reject', reason: 'not coherent', latencyMs: 5, riskScore: 0.8 }))
    };

    await inkrunner.renderChoices();

    const buttons = choicesEl.querySelectorAll('button.choice-btn');
    expect(buttons.length).toBe(2);
    expect(buttons[0].textContent).toBe('Authored A');
    expect(buttons[1].textContent).toBe('Authored B');

    const aiButtons = choicesEl.querySelectorAll('.choice-btn.ai-choice, .choice-btn.ai-choice-normal');
    expect(aiButtons.length).toBe(0);

    expect(window.Telemetry.emit).toHaveBeenCalledWith(
      'ai_evaluation',
      expect.objectContaining({ decision: 'reject' })
    );
  });

  it('handles mixed approved and rejected AI evaluations across calls', async () => {
    window.Director = {
      evaluate: jest.fn()
        .mockResolvedValueOnce({ decision: 'approve', reason: 'ok', riskScore: 0.2, latencyMs: 4 })
        .mockResolvedValueOnce({ decision: 'reject', reason: 'too risky', riskScore: 0.9, latencyMs: 6 })
    };

    const approved = {
      id: 'p-1',
      choice_text: 'Approved choice 1',
      content: { text: 'AI content 1', return_path: 'campfire' },
      metadata: { confidence_score: 0.9 }
    };

    const rejected = {
      id: 'p-2',
      choice_text: 'Rejected choice 2',
      content: { text: 'AI content 2', return_path: 'campfire' },
      metadata: { confidence_score: 0.1 }
    };

    const firstResult = await inkrunner.addAIChoice({ forceDirectorEnabled: true, mockProposalOverride: approved });
    const secondResult = await inkrunner.addAIChoice({ forceDirectorEnabled: true, mockProposalOverride: rejected });

    expect(firstResult).toBe('approved');
    expect(secondResult).toBe('rejected');

    const aiButtons = document.querySelectorAll('.choice-btn.ai-choice, .choice-btn.ai-choice-normal');
    expect(aiButtons.length).toBe(1);
    expect(aiButtons[0].textContent).toBe('Approved choice 1');

    expect(window.Telemetry.emit).toHaveBeenCalledWith(
      'ai_evaluation',
      expect.objectContaining({ proposal_id: 'p-1', decision: 'approve' })
    );
    expect(window.Telemetry.emit).toHaveBeenCalledWith(
      'ai_evaluation',
      expect.objectContaining({ proposal_id: 'p-2', decision: 'reject' })
    );
  });

  it('completes a mixed playthrough with approved then rejected AI evaluations', async () => {
    const choicesEl = document.getElementById('choices');
    const choiceStory = mockStory({ currentChoices: [{ text: 'Authored 1' }, { text: 'Authored 2' }] });
    inkrunner.setStory(choiceStory);

    const approved = {
      id: 'p-approve',
      choice_text: 'Approved choice',
      content: { text: 'AI content', return_path: 'campfire' },
      metadata: { confidence_score: 0.9 }
    };

    const rejected = {
      id: 'p-reject',
      choice_text: 'Rejected choice',
      content: { text: 'AI content 2', return_path: 'campfire' },
      metadata: { confidence_score: 0.1 }
    };

    window.Director = {
      evaluate: jest.fn()
        .mockReturnValueOnce({ decision: 'approve', reason: 'ok', riskScore: 0.2, latencyMs: 5 })
        .mockReturnValueOnce({ decision: 'reject', reason: 'later reject', riskScore: 0.85, latencyMs: 4 })
    };

    const firstResult = await inkrunner.addAIChoice({ forceDirectorEnabled: true, mockProposalOverride: approved });
    expect(firstResult).toBe('approved');

    let aiButtons = choicesEl.querySelectorAll('.choice-btn.ai-choice, .choice-btn.ai-choice-normal');
    expect(aiButtons.length).toBe(1);
    aiButtons[0].dispatchEvent(new window.Event('click'));
    expect(choiceStory.ChoosePathString).toHaveBeenCalledWith('campfire');

    const secondResult = await inkrunner.addAIChoice({ forceDirectorEnabled: true, mockProposalOverride: rejected });
    expect(secondResult).toBe('rejected');

    aiButtons = choicesEl.querySelectorAll('.choice-btn.ai-choice, .choice-btn.ai-choice-normal');
    expect(aiButtons.length).toBe(0);

    expect(window.Director.evaluate).toHaveBeenCalledTimes(2);
    expect(window.Telemetry.emit).toHaveBeenCalledWith(
      'ai_evaluation',
      expect.objectContaining({ proposal_id: 'p-approve', decision: 'approve' })
    );
    expect(window.Telemetry.emit).toHaveBeenCalledWith(
      'ai_evaluation',
      expect.objectContaining({ proposal_id: 'p-reject', decision: 'reject' })
    );
  });


  it('survives a playthrough where Director rejects every AI proposal', async () => {
    const choicesEl = document.getElementById('choices');
    const choiceStory = mockStory({ currentChoices: [{ text: 'Authored 1' }, { text: 'Authored 2' }] });
    inkrunner.setStory(choiceStory);

    window.Director = {
      evaluate: jest.fn(async () => ({ decision: 'reject', reason: 'all rejected', riskScore: 0.95, latencyMs: 3 }))
    };

    await inkrunner.renderChoices();
    await inkrunner.renderChoices(); // simulate next choice point also rejecting

    const buttons = choicesEl.querySelectorAll('button.choice-btn');
    expect(buttons.length).toBe(2);
    expect(buttons[0].textContent).toBe('Authored 1');
    expect(buttons[1].textContent).toBe('Authored 2');

    const aiButtons = choicesEl.querySelectorAll('.choice-btn.ai-choice, .choice-btn.ai-choice-normal');
    expect(aiButtons.length).toBe(0);

    expect(window.Telemetry.emit).toHaveBeenCalledWith(
      'ai_evaluation',
      expect.objectContaining({ decision: 'reject' })
    );
  });
});
