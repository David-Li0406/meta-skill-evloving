# Onboarding Flow Wireframes

> Step-by-step wizard patterns for user onboarding.

## About This Recipe

Great onboarding flows guide users through complex setup processes while keeping them engaged. These wireframes explore common patterns.

```css live
@import '../../assets/elementary/tokens/sketch.css';
@import '../../assets/elementary/components.css';
```

## Multi-Step Wizard

```jsx live
function StepIndicator({ step, currentStep, isLast }) {
  const status = step.id < currentStep ? 'complete' :
                 step.id === currentStep ? 'current' : 'pending';

  return (
    <div className="step">
      <div className={`indicator ${status}`}>
        {step.id < currentStep ? '✓' : step.id}
      </div>
      {!isLast && (
        <div className={`connector ${step.id < currentStep ? 'complete' : 'pending'}`} />
      )}
    </div>
  );
}

function WizardContent({ step, isComplete, onNext, onBack, showBack }) {
  return (
    <article className="wf-card">
      <h2 className="title">{step.title}</h2>
      <p className="description">{step.description}</p>

      {!isComplete ? (
        <>
          <div className="content">
            Step {step.id} content here
          </div>
          <nav className="actions">
            {showBack && (
              <button onClick={onBack} className="wf-btn secondary">
                Back
              </button>
            )}
            <button onClick={onNext} className="wf-btn action">
              Continue
            </button>
          </nav>
        </>
      ) : (
        <>
          <div className="icon">🎉</div>
          <button onClick={onNext} className="wf-btn action">
            Get Started
          </button>
        </>
      )}
    </article>
  );
}

const steps = [
  { id: 1, title: 'Welcome', description: 'Let\'s get you started' },
  { id: 2, title: 'Profile', description: 'Tell us about yourself' },
  { id: 3, title: 'Preferences', description: 'Customize your experience' },
  { id: 4, title: 'Complete', description: 'You\'re all set!' },
];

export default function OnboardingWizard() {
  const [currentStep, setCurrentStep] = React.useState(1);

  const step = steps.find(s => s.id === currentStep);
  const isComplete = currentStep >= steps.length;

  return (
    <div className="wf-wizard">
      <nav className="progress">
        {steps.map((s, i) => (
          <StepIndicator
            key={s.id}
            step={s}
            currentStep={currentStep}
            isLast={i === steps.length - 1}
          />
        ))}
      </nav>

      <WizardContent
        step={step}
        isComplete={isComplete}
        onNext={() => setCurrentStep(isComplete ? 1 : currentStep + 1)}
        onBack={() => setCurrentStep(currentStep - 1)}
        showBack={currentStep > 1 && !isComplete}
      />
    </div>
  );
}
```

---
*Created with [Reactive MD](https://marketplace.visualstudio.com/items?itemName=million-views.reactive-md)*
