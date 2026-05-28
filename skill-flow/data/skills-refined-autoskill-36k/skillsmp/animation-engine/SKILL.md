---
name: Animation Engine
description: Implement fluid animations for poker gameplay and UI interactions
---

# Animation Engine Skill

## Overview
Create smooth, performant animations that bring the poker experience to life using Framer Motion, CSS animations, and GSAP.

## Animation Libraries

### Primary: Framer Motion
```bash
npm install framer-motion
```

### Heavy Animations: GSAP
```bash
npm install gsap
```

### 3D: React Three Fiber
```bash
npm install @react-three/fiber @react-three/drei three
```

## Card Animations

### Card Deal
```jsx
import { motion } from 'framer-motion';

function DealingCard({ card, seatIndex, delay }) {
  return (
    <motion.div
      className="card"
      initial={{ 
        x: 0, 
        y: 0, 
        scale: 0.5, 
        rotateY: 180,
        opacity: 0 
      }}
      animate={{ 
        x: SEAT_POSITIONS[seatIndex].x, 
        y: SEAT_POSITIONS[seatIndex].y, 
        scale: 1, 
        rotateY: 0,
        opacity: 1 
      }}
      transition={{ 
        duration: 0.4, 
        delay: delay * 0.1,
        ease: [0.25, 0.8, 0.25, 1]  // Custom bezier
      }}
    >
      <CardFace card={card} />
    </motion.div>
  );
}
```

### Card Flip
```jsx
function FlippingCard({ card, isRevealed }) {
  return (
    <motion.div
      className="card-container"
      style={{ perspective: 1000 }}
    >
      <motion.div
        className="card-inner"
        animate={{ rotateY: isRevealed ? 0 : 180 }}
        transition={{ duration: 0.6, ease: "easeInOut" }}
        style={{ transformStyle: 'preserve-3d' }}
      >
        <div className="card-front">
          <CardFace card={card} />
        </div>
        <div className="card-back">
          <CardBack />
        </div>
      </motion.div>
    </motion.div>
  );
}
```

## Chip Animations

### Chip to Pot
```jsx
function ChipsToPot({ amount, fromSeat, onComplete }) {
  const controls = useAnimation();
  
  useEffect(() => {
    controls.start({
      x: POT_POSITION.x - SEAT_POSITIONS[fromSeat].x,
      y: POT_POSITION.y - SEAT_POSITIONS[fromSeat].y,
      scale: 0.5,
      transition: { duration: 0.4, ease: "easeOut" }
    }).then(onComplete);
  }, [amount]);
  
  return (
    <motion.div 
      className="chip-stack"
      animate={controls}
      initial={{ x: 0, y: 0, scale: 1 }}
    >
      <ChipStack amount={amount} />
    </motion.div>
  );
}
```

### Pot to Winner
```jsx
function PotToWinner({ amount, winnerSeat }) {
  return (
    <motion.div
      className="winning-pot"
      initial={{ 
        x: POT_POSITION.x, 
        y: POT_POSITION.y,
        scale: 1 
      }}
      animate={{
        x: SEAT_POSITIONS[winnerSeat].x,
        y: SEAT_POSITIONS[winnerSeat].y,
        scale: 1.2
      }}
      transition={{
        duration: 0.6,
        ease: [0.34, 1.56, 0.64, 1]  // Bouncy
      }}
    >
      <ChipStack amount={amount} />
      <motion.div
        className="win-glow"
        animate={{ 
          scale: [1, 1.5, 1],
          opacity: [0.5, 1, 0]
        }}
        transition={{ duration: 1, repeat: 2 }}
      />
    </motion.div>
  );
}
```

## UI Animations

### Button Interactions
```jsx
const ActionButton = motion(Button);

function BetButton({ onClick, children }) {
  return (
    <ActionButton
      onClick={onClick}
      whileHover={{ scale: 1.05, boxShadow: "0 0 20px rgba(0,245,255,0.5)" }}
      whileTap={{ scale: 0.95 }}
      transition={{ duration: 0.15 }}
    >
      {children}
    </ActionButton>
  );
}
```

### Page Transitions
```jsx
import { AnimatePresence, motion } from 'framer-motion';
import { useRouter } from 'next/router';

function PageTransition({ children }) {
  const router = useRouter();
  
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={router.pathname}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        transition={{ duration: 0.3 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

### Staggered Lists
```jsx
function PlayerList({ players }) {
  return (
    <motion.ul
      initial="hidden"
      animate="visible"
      variants={{
        visible: {
          transition: { staggerChildren: 0.1 }
        }
      }}
    >
      {players.map((player) => (
        <motion.li
          key={player.id}
          variants={{
            hidden: { opacity: 0, y: 20 },
            visible: { opacity: 1, y: 0 }
          }}
        >
          <PlayerCard player={player} />
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

## Timer Animation

### Action Timer with Color Shift
```jsx
function ActionTimer({ duration, onExpire }) {
  const [progress, setProgress] = useState(1);
  
  useEffect(() => {
    const start = Date.now();
    const interval = setInterval(() => {
      const elapsed = (Date.now() - start) / 1000;
      const remaining = 1 - (elapsed / duration);
      
      if (remaining <= 0) {
        clearInterval(interval);
        onExpire();
      } else {
        setProgress(remaining);
      }
    }, 50);
    
    return () => clearInterval(interval);
  }, [duration]);
  
  const color = progress > 0.5 ? '#00ff88' : progress > 0.2 ? '#ffd700' : '#ff4757';
  
  return (
    <motion.div 
      className="timer-ring"
      style={{
        background: `conic-gradient(${color} ${progress * 360}deg, transparent 0)`
      }}
      animate={{ 
        boxShadow: progress < 0.2 
          ? ['0 0 10px #ff4757', '0 0 30px #ff4757', '0 0 10px #ff4757']
          : 'none'
      }}
      transition={{ duration: 0.5, repeat: Infinity }}
    />
  );
}
```

## GSAP for Complex Sequences
```javascript
import gsap from 'gsap';

function useWinAnimation(winnerRef, prizeAmount) {
  useEffect(() => {
    if (!winnerRef.current) return;
    
    const tl = gsap.timeline();
    
    tl.to(winnerRef.current, {
      scale: 1.1,
      duration: 0.3,
      ease: "power2.out"
    })
    .to(winnerRef.current, {
      boxShadow: "0 0 50px #ffd700",
      duration: 0.5
    })
    .to(".chips", {
      y: -50,
      opacity: 0,
      stagger: 0.05,
      duration: 0.4
    }, "-=0.3")
    .to(winnerRef.current, {
      scale: 1,
      boxShadow: "0 0 10px #ffd700",
      duration: 0.5,
      delay: 1
    });
    
    return () => tl.kill();
  }, [prizeAmount]);
}
```

## Performance Best Practices

### 1. Use `transform` and `opacity` only
```css
/* GOOD - GPU accelerated */
.animate { transform: translateX(100px); opacity: 0.5; }

/* BAD - Triggers layout */
.animate { left: 100px; width: 200px; }
```

### 2. Use `will-change` sparingly
```css
.card-animating { will-change: transform; }
```

### 3. Use `layoutId` for shared element transitions
```jsx
<motion.div layoutId={`card-${card.id}`}>
  <Card card={card} />
</motion.div>
```

### 4. Reduce motion for accessibility
```jsx
const prefersReducedMotion = usePrefersReducedMotion();

<motion.div
  animate={{ x: 100 }}
  transition={{ duration: prefersReducedMotion ? 0 : 0.3 }}
/>
```
