# Anime.js API Reference

Complete API documentation for anime.js v3/v4.

## Core Function

```javascript
import anime from 'animejs';

const animation = anime({
  targets: '.element',
  translateX: 250,
  duration: 1000
});
```

## Targets

| Type | Example |
|------|---------|
| CSS Selector | `'.class'`, `'#id'`, `'div'` |
| DOM Element | `document.querySelector('.el')` |
| NodeList | `document.querySelectorAll('.els')` |
| Array | `['.el1', domNode, nodeList]` |
| JS Object | `{ prop: 0 }` |

## Animatable Properties

### CSS Transforms (use these!)
```javascript
{
  translateX: 250,      // pixels
  translateY: 100,
  translateZ: 50,
  rotate: '1turn',      // or degrees: 360
  rotateX: 180,
  rotateY: 180,
  rotateZ: 180,
  scale: 2,
  scaleX: 2,
  scaleY: 2,
  skew: 10,
  skewX: 10,
  skewY: 10,
  perspective: 500
}
```

### CSS Properties
```javascript
{
  opacity: 0.5,
  backgroundColor: '#FF0000',
  borderRadius: '50%',
  color: 'rgb(255, 0, 0)',
  fontSize: '2rem'
}
```

### SVG Attributes
```javascript
{
  points: '64 128 8 96 8 32',
  strokeDashoffset: [anime.setDashoffset, 0],
  cx: 100,
  cy: 150,
  r: 50
}
```

### JS Object Properties
```javascript
const obj = { value: 0, progress: 0 };
anime({
  targets: obj,
  value: 100,
  progress: 1,
  round: 1,
  update: () => console.log(obj.value)
});
```

## Property Parameters

```javascript
anime({
  targets: '.el',
  translateX: {
    value: 250,
    duration: 800,
    delay: 200,
    easing: 'easeOutQuad'
  },
  opacity: {
    value: 0.5,
    duration: 400,
    easing: 'easeOutExpo'
  }
});
```

## Animation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `duration` | number/function | 1000 | Duration in ms |
| `delay` | number/function | 0 | Delay before start |
| `endDelay` | number/function | 0 | Delay after end |
| `easing` | string/function | 'easeOutElastic(1, .5)' | Easing function |
| `round` | number | 0 | Round values |
| `loop` | number/boolean | false | Loop count or infinite |
| `direction` | string | 'normal' | 'normal', 'reverse', 'alternate' |
| `autoplay` | boolean | true | Start automatically |

### Function-based Parameters

```javascript
anime({
  targets: '.el',
  translateX: 250,
  delay: (el, i, total) => i * 100,
  duration: (el, i) => 500 + (i * 100),
  easing: (el, i, total) => i % 2 === 0 ? 'easeOutQuad' : 'easeInQuad'
});
```

## Easing Functions

### Built-in Easings
- `linear`
- `easeInQuad`, `easeOutQuad`, `easeInOutQuad`
- `easeInCubic`, `easeOutCubic`, `easeInOutCubic`
- `easeInQuart`, `easeOutQuart`, `easeInOutQuart`
- `easeInQuint`, `easeOutQuint`, `easeInOutQuint`
- `easeInSine`, `easeOutSine`, `easeInOutSine`
- `easeInExpo`, `easeOutExpo`, `easeInOutExpo`
- `easeInCirc`, `easeOutCirc`, `easeInOutCirc`
- `easeInBack`, `easeOutBack`, `easeInOutBack`
- `easeInElastic(amplitude, period)`, `easeOutElastic`, `easeInOutElastic`
- `easeInBounce`, `easeOutBounce`, `easeInOutBounce`

### Cubic Bezier
```javascript
easing: 'cubicBezier(0.42, 0, 0.58, 1)'
```

### Spring (v4)
```javascript
easing: 'spring(mass, stiffness, damping, velocity)'
easing: 'spring(1, 100, 10, 0)'
```

### Steps
```javascript
easing: 'steps(5)'
```

### Custom Function
```javascript
easing: (t) => t * t  // quadratic
```

## Keyframes

### Array Keyframes
```javascript
anime({
  targets: '.el',
  translateX: [0, 100, 200, 100, 0],
  duration: 2000
});
```

### Object Keyframes
```javascript
anime({
  targets: '.el',
  keyframes: [
    { translateX: 100, duration: 500 },
    { translateY: 100, duration: 500, delay: 100 },
    { translateX: 0, duration: 500 },
    { translateY: 0, duration: 500 }
  ]
});
```

### Property Keyframes
```javascript
anime({
  targets: '.el',
  translateX: [
    { value: 100, duration: 500, easing: 'easeOutQuad' },
    { value: 200, duration: 500, easing: 'easeInQuad' }
  ]
});
```

## Stagger

```javascript
import anime from 'animejs';

// Basic stagger
anime({
  targets: '.el',
  translateX: 250,
  delay: anime.stagger(100)  // 0, 100, 200, 300...
});

// Range stagger
anime({
  targets: '.el',
  rotate: anime.stagger([-360, 360])  // distribute from -360 to 360
});

// From specific position
anime({
  targets: '.el',
  translateX: 250,
  delay: anime.stagger(100, { from: 'center' })  // or 'first', 'last', index
});

// With easing
anime({
  targets: '.el',
  translateX: 250,
  delay: anime.stagger(100, { easing: 'easeOutQuad' })
});

// Grid stagger
anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, {
    grid: [14, 5],
    from: 'center'
  })
});

// Grid with axis
anime({
  targets: '.grid-item',
  delay: anime.stagger(100, {
    grid: [10, 5],
    from: 'center',
    axis: 'x'  // or 'y'
  })
});
```

## Timeline

```javascript
const tl = anime.timeline({
  easing: 'easeOutExpo',
  duration: 750
});

// Sequential
tl.add({ targets: '.el1', translateX: 250 })
  .add({ targets: '.el2', translateX: 250 })
  .add({ targets: '.el3', translateX: 250 });

// With offsets
tl.add({ targets: '.el1', translateX: 250 })
  .add({ targets: '.el2', translateX: 250 }, '-=500')  // 500ms before previous ends
  .add({ targets: '.el3', translateX: 250 }, '+=100'); // 100ms after previous ends

// Absolute timing
tl.add({ targets: '.el', translateX: 250 }, 1000);  // at 1000ms

// Relative to previous
tl.add({ targets: '.el2', translateX: 250 }, '-=200');  // 200ms overlap
tl.add({ targets: '.el3', translateX: 250 }, '+=100');  // 100ms gap
```

## Callbacks

```javascript
anime({
  targets: '.el',
  translateX: 250,
  begin: (anim) => console.log('Animation started'),
  update: (anim) => console.log('Progress:', anim.progress),
  complete: (anim) => console.log('Animation complete'),
  loopBegin: (anim) => console.log('Loop started'),
  loopComplete: (anim) => console.log('Loop complete'),
  changeBegin: (anim) => console.log('Change started'),
  changeComplete: (anim) => console.log('Change complete')
});
```

## Controls

```javascript
const animation = anime({
  targets: '.el',
  translateX: 250,
  autoplay: false
});

animation.play();
animation.pause();
animation.restart();
animation.reverse();
animation.seek(500);        // seek to 500ms
animation.seek(animation.duration * 0.5);  // seek to 50%
```

## Properties

```javascript
animation.progress      // 0-1
animation.currentTime   // in ms
animation.duration      // total duration
animation.paused        // boolean
animation.began         // boolean
animation.completed     // boolean
animation.reversed      // boolean
```

## Promises

```javascript
anime({
  targets: '.el',
  translateX: 250
}).finished.then(() => {
  console.log('Done!');
});

// Async/await
async function animate() {
  await anime({ targets: '.el', translateX: 250 }).finished;
  await anime({ targets: '.el', translateY: 250 }).finished;
  console.log('Both done!');
}
```

## Utility Functions

```javascript
// Remove targets from all animations
anime.remove('.el');

// Get current value
anime.get('.el', 'translateX');         // '0px'
anime.get('.el', 'translateX', 'px');   // 0

// Set value instantly
anime.set('.el', { translateX: 250 });

// Random value
anime.random(0, 100);  // random between 0-100

// Run function on tick
anime.tick = (t) => console.log(t);

// Get engine running status
anime.running;  // array of running animations

// Suspend/resume engine
anime.suspendWhenDocumentHidden = false;
```

## SVG Specific

### Line Drawing
```javascript
anime({
  targets: 'path',
  strokeDashoffset: [anime.setDashoffset, 0],
  easing: 'easeInOutSine',
  duration: 1500,
  delay: (el, i) => i * 250,
  direction: 'alternate',
  loop: true
});
```

### Motion Path
```javascript
const path = anime.path('svg path');

anime({
  targets: '.el',
  translateX: path('x'),
  translateY: path('y'),
  rotate: path('angle'),
  easing: 'linear',
  duration: 2000,
  loop: true
});
```

### Morphing
```javascript
anime({
  targets: 'polygon',
  points: [
    { value: '64 128 8.574 96 8.574 32 64 0 119.426 32 119.426 96' },
    { value: '64 68 8.574 96 8.574 32 64 0 119.426 32 119.426 96' }
  ],
  easing: 'easeOutQuad',
  duration: 1000,
  loop: true,
  direction: 'alternate'
});
```

## V4 Specific

### New Imports (v4)
```javascript
import {
  animate,
  createTimeline,
  stagger,
  utils,
  svg,
  eases,
  spring,
  onScroll,
  createScope
} from 'animejs';
```

### createScope for React (v4)
```javascript
import { createScope, animate } from 'animejs';
import { useEffect, useRef } from 'react';

function Component() {
  const root = useRef(null);
  const scope = useRef(null);

  useEffect(() => {
    scope.current = createScope({ root }).add(() => {
      animate('.box', { translateX: 250 });
    });

    return () => scope.current.revert();
  }, []);

  return <div ref={root}><div className="box" /></div>;
}
```

### onScroll (v4)
```javascript
import { animate, onScroll } from 'animejs';

animate('.element', {
  translateX: 250,
  autoplay: onScroll({
    target: '.element',
    enter: 'bottom top',
    leave: 'top bottom'
  })
});
```
