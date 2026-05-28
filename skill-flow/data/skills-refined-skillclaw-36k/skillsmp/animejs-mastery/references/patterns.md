# Animation Patterns Reference

Production-ready animation patterns for common UI scenarios.

## Entrance Animations

### Fade Up (Most Common)
```javascript
// Single element
anime({
  targets: '.fade-up',
  translateY: [30, 0],
  opacity: [0, 1],
  duration: 600,
  easing: 'easeOutQuad'
});

// Staggered list
anime({
  targets: '.list-item',
  translateY: [30, 0],
  opacity: [0, 1],
  delay: anime.stagger(50),
  duration: 500,
  easing: 'easeOutQuad'
});
```

### Scale In
```javascript
anime({
  targets: '.scale-in',
  scale: [0.9, 1],
  opacity: [0, 1],
  duration: 400,
  easing: 'easeOutQuad'
});
```

### Slide From Side
```javascript
// From left
anime({
  targets: '.slide-left',
  translateX: [-50, 0],
  opacity: [0, 1],
  duration: 500,
  easing: 'easeOutQuad'
});

// From right
anime({
  targets: '.slide-right',
  translateX: [50, 0],
  opacity: [0, 1],
  duration: 500,
  easing: 'easeOutQuad'
});
```

### Pop In (with overshoot)
```javascript
anime({
  targets: '.pop-in',
  scale: [0, 1],
  opacity: [0, 1],
  duration: 500,
  easing: 'easeOutBack'
});
```

## Exit Animations

### Fade Out
```javascript
const fadeOut = (targets, onComplete) => {
  anime({
    targets,
    opacity: [1, 0],
    translateY: [0, -20],
    duration: 300,
    easing: 'easeInQuad',
    complete: onComplete
  });
};
```

### Scale Out
```javascript
anime({
  targets: '.scale-out',
  scale: [1, 0.9],
  opacity: [1, 0],
  duration: 250,
  easing: 'easeInQuad'
});
```

## Micro-interactions

### Button Press
```javascript
const buttonPress = (element) => {
  anime({
    targets: element,
    scale: [1, 0.95, 1],
    duration: 150,
    easing: 'easeInOutQuad'
  });
};

// Usage
button.addEventListener('mousedown', (e) => buttonPress(e.currentTarget));
```

### Button Hover Grow
```javascript
const setupButtonHover = (button) => {
  button.addEventListener('mouseenter', () => {
    anime.remove(button);
    anime({
      targets: button,
      scale: 1.05,
      duration: 200,
      easing: 'easeOutQuad'
    });
  });

  button.addEventListener('mouseleave', () => {
    anime.remove(button);
    anime({
      targets: button,
      scale: 1,
      duration: 200,
      easing: 'easeOutQuad'
    });
  });
};
```

### Card Hover Lift
```javascript
const setupCardHover = (card) => {
  card.addEventListener('mouseenter', () => {
    anime.remove(card);
    anime({
      targets: card,
      translateY: -8,
      boxShadow: '0 12px 40px rgba(0,0,0,0.15)',
      duration: 250,
      easing: 'easeOutQuad'
    });
  });

  card.addEventListener('mouseleave', () => {
    anime.remove(card);
    anime({
      targets: card,
      translateY: 0,
      boxShadow: '0 2px 10px rgba(0,0,0,0.08)',
      duration: 250,
      easing: 'easeOutQuad'
    });
  });
};
```

### Ripple Effect
```javascript
const createRipple = (event, container) => {
  const ripple = document.createElement('span');
  ripple.className = 'ripple';
  
  const rect = container.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);
  
  ripple.style.cssText = `
    position: absolute;
    width: ${size}px;
    height: ${size}px;
    left: ${event.clientX - rect.left - size/2}px;
    top: ${event.clientY - rect.top - size/2}px;
    background: rgba(255,255,255,0.3);
    border-radius: 50%;
    pointer-events: none;
  `;
  
  container.appendChild(ripple);
  
  anime({
    targets: ripple,
    scale: [0, 2],
    opacity: [1, 0],
    duration: 600,
    easing: 'easeOutQuad',
    complete: () => ripple.remove()
  });
};
```

## Feedback Animations

### Success State
```javascript
const showSuccess = (element) => {
  anime({
    targets: element,
    scale: [0.8, 1.1, 1],
    opacity: [0, 1],
    duration: 500,
    easing: 'easeOutBack'
  });
};

// Checkmark draw
const drawCheckmark = (path) => {
  anime({
    targets: path,
    strokeDashoffset: [anime.setDashoffset, 0],
    duration: 400,
    delay: 200,
    easing: 'easeOutQuad'
  });
};
```

### Error Shake
```javascript
const shakeError = (element) => {
  anime({
    targets: element,
    translateX: [0, -10, 10, -10, 10, -5, 5, 0],
    duration: 500,
    easing: 'easeInOutQuad'
  });
};
```

### Warning Pulse
```javascript
const pulseWarning = (element) => {
  anime({
    targets: element,
    scale: [1, 1.05, 1],
    duration: 600,
    loop: 2,
    easing: 'easeInOutQuad'
  });
};
```

## Loading States

### Skeleton Pulse
```javascript
const skeletonPulse = (selector) => {
  return anime({
    targets: selector,
    opacity: [0.4, 0.8],
    duration: 1200,
    direction: 'alternate',
    loop: true,
    easing: 'easeInOutSine'
  });
};
```

### Dots Loader
```javascript
anime({
  targets: '.loading-dot',
  translateY: [0, -12, 0],
  delay: anime.stagger(100),
  duration: 600,
  loop: true,
  easing: 'easeInOutQuad'
});
```

### Spinner
```javascript
anime({
  targets: '.spinner',
  rotate: 360,
  duration: 1000,
  loop: true,
  easing: 'linear'
});
```

### Progress Bar
```javascript
const animateProgress = (element, percentage) => {
  anime({
    targets: element,
    width: `${percentage}%`,
    duration: 600,
    easing: 'easeOutQuad'
  });
};
```

## Modal & Dialog

### Modal Enter
```javascript
const modalEnter = (overlay, modal) => {
  const tl = anime.timeline({
    easing: 'easeOutQuad'
  });

  tl.add({
    targets: overlay,
    opacity: [0, 1],
    duration: 200
  })
  .add({
    targets: modal,
    scale: [0.95, 1],
    opacity: [0, 1],
    duration: 250
  }, '-=100');

  return tl;
};
```

### Modal Exit
```javascript
const modalExit = (overlay, modal, onComplete) => {
  const tl = anime.timeline({
    easing: 'easeInQuad',
    complete: onComplete
  });

  tl.add({
    targets: modal,
    scale: [1, 0.95],
    opacity: [1, 0],
    duration: 200
  })
  .add({
    targets: overlay,
    opacity: [1, 0],
    duration: 150
  }, '-=50');

  return tl;
};
```

### Drawer Slide
```javascript
// Right drawer
const drawerOpen = (drawer) => {
  anime({
    targets: drawer,
    translateX: ['100%', '0%'],
    duration: 300,
    easing: 'easeOutQuad'
  });
};

const drawerClose = (drawer, onComplete) => {
  anime({
    targets: drawer,
    translateX: ['0%', '100%'],
    duration: 250,
    easing: 'easeInQuad',
    complete: onComplete
  });
};
```

## Data Visualization

### Number Counter
```javascript
const countUp = (element, endValue, duration = 1000) => {
  const obj = { value: 0 };
  
  anime({
    targets: obj,
    value: endValue,
    round: 1,
    duration,
    easing: 'easeOutExpo',
    update: () => {
      element.textContent = obj.value.toLocaleString();
    }
  });
};
```

### Bar Chart Reveal
```javascript
anime({
  targets: '.bar',
  height: (el) => el.getAttribute('data-value') + '%',
  delay: anime.stagger(100),
  duration: 800,
  easing: 'easeOutQuad'
});
```

### Pie Chart Draw
```javascript
anime({
  targets: '.pie-segment',
  strokeDashoffset: [anime.setDashoffset, 0],
  delay: anime.stagger(200),
  duration: 1000,
  easing: 'easeOutQuad'
});
```

### Line Chart Draw
```javascript
anime({
  targets: '.chart-line',
  strokeDashoffset: [anime.setDashoffset, 0],
  duration: 1500,
  easing: 'easeOutQuad'
});
```

## Page Transitions

### Fade Transition
```javascript
const pageTransition = async (outElement, inElement) => {
  // Exit
  await anime({
    targets: outElement,
    opacity: [1, 0],
    translateY: [0, -20],
    duration: 200,
    easing: 'easeInQuad'
  }).finished;

  // Enter
  await anime({
    targets: inElement,
    opacity: [0, 1],
    translateY: [20, 0],
    duration: 300,
    easing: 'easeOutQuad'
  }).finished;
};
```

### Slide Transition
```javascript
const slideTransition = async (direction, outElement, inElement) => {
  const xOut = direction === 'forward' ? -50 : 50;
  const xIn = direction === 'forward' ? 50 : -50;

  await anime({
    targets: outElement,
    opacity: 0,
    translateX: xOut,
    duration: 200,
    easing: 'easeInQuad'
  }).finished;

  await anime({
    targets: inElement,
    opacity: [0, 1],
    translateX: [xIn, 0],
    duration: 300,
    easing: 'easeOutQuad'
  }).finished;
};
```

## Scroll Animations

### Reveal on Scroll (with IntersectionObserver)
```javascript
const setupScrollReveal = (selector) => {
  const elements = document.querySelectorAll(selector);
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        anime({
          targets: entry.target,
          translateY: [30, 0],
          opacity: [0, 1],
          duration: 600,
          easing: 'easeOutQuad'
        });
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  elements.forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
  });
};
```

### Parallax Effect
```javascript
const setupParallax = (selector, speed = 0.5) => {
  const element = document.querySelector(selector);
  
  window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    anime.set(element, {
      translateY: scrolled * speed
    });
  });
};
```

## Stagger Patterns

### From Center
```javascript
anime({
  targets: '.item',
  scale: [0, 1],
  delay: anime.stagger(100, { from: 'center' })
});
```

### Grid Wave
```javascript
anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, {
    grid: [10, 10],
    from: 'center'
  })
});
```

### Random Stagger
```javascript
anime({
  targets: '.item',
  opacity: [0, 1],
  translateY: [20, 0],
  delay: () => anime.random(0, 500)
});
```

## React Patterns

### useAnime Hook
```typescript
import { useEffect, useRef } from 'react';
import anime from 'animejs';

export function useAnime(params: anime.AnimeParams, deps: unknown[] = []) {
  const ref = useRef<HTMLElement>(null);
  const animationRef = useRef<anime.AnimeInstance | null>(null);

  useEffect(() => {
    if (ref.current) {
      animationRef.current = anime({
        targets: ref.current,
        ...params
      });
    }

    return () => {
      animationRef.current?.pause();
    };
  }, deps);

  return { ref, animation: animationRef };
}
```

### Animated List Component
```tsx
import { useEffect, useRef } from 'react';
import anime from 'animejs';

interface AnimatedListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  staggerDelay?: number;
}

export function AnimatedList<T>({
  items,
  renderItem,
  keyExtractor,
  staggerDelay = 50
}: AnimatedListProps<T>) {
  const listRef = useRef<HTMLUListElement>(null);

  useEffect(() => {
    if (listRef.current) {
      anime({
        targets: listRef.current.children,
        translateY: [20, 0],
        opacity: [0, 1],
        delay: anime.stagger(staggerDelay),
        duration: 500,
        easing: 'easeOutQuad'
      });
    }
  }, [items, staggerDelay]);

  return (
    <ul ref={listRef}>
      {items.map((item, index) => (
        <li key={keyExtractor(item)} style={{ opacity: 0 }}>
          {renderItem(item, index)}
        </li>
      ))}
    </ul>
  );
}
```

### Animated Modal Hook
```tsx
import { useRef, useCallback } from 'react';
import anime from 'animejs';

export function useModalAnimation() {
  const overlayRef = useRef<HTMLDivElement>(null);
  const modalRef = useRef<HTMLDivElement>(null);

  const animateIn = useCallback(() => {
    if (!overlayRef.current || !modalRef.current) return;

    anime.timeline()
      .add({
        targets: overlayRef.current,
        opacity: [0, 1],
        duration: 200,
        easing: 'easeOutQuad'
      })
      .add({
        targets: modalRef.current,
        scale: [0.95, 1],
        opacity: [0, 1],
        duration: 250,
        easing: 'easeOutQuad'
      }, '-=100');
  }, []);

  const animateOut = useCallback((onComplete: () => void) => {
    if (!overlayRef.current || !modalRef.current) return;

    anime.timeline({ complete: onComplete })
      .add({
        targets: modalRef.current,
        scale: [1, 0.95],
        opacity: [1, 0],
        duration: 200,
        easing: 'easeInQuad'
      })
      .add({
        targets: overlayRef.current,
        opacity: [1, 0],
        duration: 150,
        easing: 'easeInQuad'
      }, '-=50');
  }, []);

  return { overlayRef, modalRef, animateIn, animateOut };
}
```

## Accessibility

### Reduced Motion Wrapper
```typescript
const prefersReducedMotion = () =>
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export const safeAnimate = (params: anime.AnimeParams) => {
  if (prefersReducedMotion()) {
    return anime({ ...params, duration: 0 });
  }
  return anime(params);
};
```

### Focus Management with Animation
```javascript
const showModal = (modal) => {
  anime({
    targets: modal,
    scale: [0.95, 1],
    opacity: [0, 1],
    duration: 250,
    easing: 'easeOutQuad',
    complete: () => {
      // Focus first focusable element after animation
      const focusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      focusable?.focus();
    }
  });
};
```
