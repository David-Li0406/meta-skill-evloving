# Landing Page Wireframes

Quick visual concepts for common landing page sections.

```css live
@import '../../assets/elementary/tokens/sketch.css';
@import '../../assets/elementary/components.css';
```

---

## Hero Section

```jsx live
export default function HeroSection() {
  return (
    <header className="wf-hero">
      <div className="content">
        <span className="badge">
          🎉 Now available for teams
        </span>
        <h1 className="title">
          Build products faster with AI
        </h1>
        <p className="description">
          The modern platform for product teams. Design, prototype,
          and ship — all in one place.
        </p>
        <div className="actions">
          <button className="wf-btn primary">
            Get Started Free
          </button>
          <button className="wf-btn secondary">
            Watch Demo
          </button>
        </div>
        <p className="footnote">
          No credit card required · Free for individuals
        </p>
      </div>
    </header>
  );
}
```

---

## Social Proof Bar

```jsx live
const Logo = ({ name }) => (
  <span className="logo">{name}</span>
);

export default function SocialProof() {
  const logos = ['Acme Inc', 'TechCorp', 'StartupXYZ', 'Enterprise Co', 'ScaleUp'];

  return (
    <section className="wf-social-proof">
      <p className="label">
        Trusted by 10,000+ teams at companies like
      </p>
      <div className="logos">
        {logos.map(logo => (
          <Logo key={logo} name={logo} />
        ))}
      </div>
    </section>
  );
}
```

---

## Feature Grid

```jsx live
function FeatureCard({ icon, title, description }) {
  return (
    <article className="wf-card">
      <div className="icon">{icon}</div>
      <h3 className="title">{title}</h3>
      <p className="description">{description}</p>
    </article>
  );
}

export default function FeatureGrid() {
  const features = [
    { icon: '⚡', title: 'Lightning Fast', desc: 'Built for speed. See changes in milliseconds.' },
    { icon: '🔒', title: 'Secure by Default', desc: 'Enterprise-grade security out of the box.' },
    { icon: '🎨', title: 'Beautiful Design', desc: 'Stunning templates to get started quickly.' },
    { icon: '🔄', title: 'Real-time Sync', desc: 'Collaborate with your team in real-time.' },
    { icon: '📊', title: 'Analytics Built-in', desc: 'Track performance without extra tools.' },
    { icon: '🌐', title: 'Global CDN', desc: 'Deploy to 300+ edge locations worldwide.' },
  ];

  return (
    <section className="wf-features">
      <header className="header">
        <h2 className="title">Everything you need</h2>
        <p className="description">
          All the features you need to build, launch, and grow your product.
        </p>
      </header>
      <div className="wf-grid">
        {features.map(f => (
          <FeatureCard
            key={f.title}
            icon={f.icon}
            title={f.title}
            description={f.desc}
          />
        ))}
      </div>
    </section>
  );
}
```

---

## Pricing Cards

```jsx live
function PricingCard({ plan, onSelect }) {
  return (
    <article className={`wf-card ${plan.popular ? 'featured' : ''}`}>
      {plan.popular && (
        <span className="badge">Most Popular</span>
      )}
      <h3 className="plan-name">{plan.name}</h3>
      <div className="amount">
        {typeof plan.price === 'number' ? (
          <>
            <span>${plan.price}</span>
            <span className="suffix">/mo</span>
          </>
        ) : (
          <span>{plan.price}</span>
        )}
      </div>
      <ul className="features">
        {plan.features.map(f => (
          <li key={f} className="feature">
            <span className="checkmark">✓</span> {f}
          </li>
        ))}
      </ul>
      <button
        onClick={onSelect}
        className={`wf-btn ${plan.popular ? 'action' : 'primary'} full`}
      >
        {plan.price === 'Custom' ? 'Contact Sales' : 'Get Started'}
      </button>
    </article>
  );
}

export default function PricingCards() {
  const [annual, setAnnual] = React.useState(false);

  const plans = [
    { name: 'Starter', price: annual ? 9 : 12, features: ['5 projects', '1 user', 'Basic analytics'] },
    { name: 'Pro', price: annual ? 29 : 39, features: ['Unlimited projects', '5 users', 'Advanced analytics', 'Priority support'], popular: true },
    { name: 'Enterprise', price: 'Custom', features: ['Everything in Pro', 'Unlimited users', 'SSO', 'Dedicated support'] },
  ];

  return (
    <section className="wf-pricing">
      <header className="header">
        <h2 className="title">Simple, transparent pricing</h2>

        <div className="billing">
          <span className={`label ${!annual ? 'active' : ''}`}>Monthly</span>
          <button
            onClick={() => setAnnual(!annual)}
            className={`wf-toggle ${annual ? 'active' : ''}`}
          >
            <span className="thumb"></span>
          </button>
          <span className={`label ${annual ? 'active' : ''}`}>Annual</span>
        </div>
        <span className="save-badge" style={{ visibility: annual ? 'hidden' : 'visible' }}>Save 20% with Annual</span>
      </header>

      <div className="wf-grid pricing" style={{ maxWidth: 'var(--w-container)', margin: '0 auto' }}>
        {plans.map(plan => (
          <PricingCard
            key={plan.name}
            plan={plan}
            onSelect={() => console.log(`Selected ${plan.name}`)}
          />
        ))}
      </div>
    </section>
  );
}
```

---

## CTA Section

```jsx live
export default function CTASection() {
  return (
    <section className="wf-cta">
      <h2 className="title">Ready to get started?</h2>
      <p className="description">
        Join thousands of teams already using our platform to build better products.
      </p>
      <form className="form">
        <input
          type="email"
          placeholder="Enter your email"
          className="input"
        />
        <button className="wf-btn action">
          Start Free Trial
        </button>
      </form>
    </section>
  );
}
```

---

## Footer

```jsx live
function FooterSection({ title, links }) {
  return (
    <div className="section">
      <h4 className="title">{title}</h4>
      <ul className="links">
        {links.map(link => (
          <li key={link}>
            <a href="#" className="link">{link}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function Footer() {
  const sections = [
    { title: 'Product', links: ['Features', 'Pricing', 'Changelog', 'Roadmap'] },
    { title: 'Company', links: ['About', 'Blog', 'Careers', 'Press'] },
    { title: 'Resources', links: ['Documentation', 'API Reference', 'Guides', 'Community'] },
    { title: 'Legal', links: ['Privacy', 'Terms', 'Security', 'Cookies'] },
  ];

  return (
    <footer className="wf-footer">
      <div className="wf-grid footer" style={{ maxWidth: 'var(--w-container)', margin: '0 auto var(--s-6)' }}>
        <div className="brand">
          <div className="name">🚀 ProductCo</div>
          <p className="tagline">Building the future of product development.</p>
        </div>
        {sections.map(section => (
          <FooterSection
            key={section.title}
            title={section.title}
            links={section.links}
          />
        ))}
      </div>
      <div className="bottom">
        <span className="copyright">© 2024 ProductCo. All rights reserved.</span>
      </div>
    </footer>
  );
}
```

---
*Created with [Reactive MD](https://marketplace.visualstudio.com/items?itemName=million-views.reactive-md)*
