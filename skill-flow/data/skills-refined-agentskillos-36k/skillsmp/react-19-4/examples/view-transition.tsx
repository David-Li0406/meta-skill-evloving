import { useState, startTransition, addTransitionType, ViewTransition } from "react";

// ViewTransition animates elements when state changes inside startTransition()
// Place around specific elements to animate, not at app root
// Must wrap DOM nodes directly (not text)
// Use addTransitionType() to tag transitions for custom animations

export function TogglePanel() {
  const [show, setShow] = useState(false);

  const handleToggle = () => {
    startTransition(() => {
      setShow((s) => !s);
    });
  };

  return (
    <>
      <button onClick={handleToggle}>Toggle</button>
      <ViewTransition>
        {show && <div>Animated content</div>}
      </ViewTransition>
    </>
  );
}

// List items - wrap each individually for independent animations
export function AnimatedList({ items }: { items: string[] }) {
  return (
    <ul>
      {items.map((item) => (
        <ViewTransition key={item}>
          <li>{item}</li>
        </ViewTransition>
      ))}
    </ul>
  );
}

// Shared element transition - use name prop to animate between routes
export function Thumbnail({ id, fullscreen }: { id: string; fullscreen?: boolean }) {
  return (
    <ViewTransition name={`thumbnail-${id}`}>
      <img src={`/images/${id}.jpg`} className={fullscreen ? "full" : "thumb"} />
    </ViewTransition>
  );
}

// addTransitionType - tag transitions for custom animations per cause
export function NavigationStack({ pages }: { pages: string[] }) {
  const [index, setIndex] = useState(0);

  const goBack = () => {
    startTransition(() => {
      addTransitionType("nav-back");
      setIndex((i) => Math.max(0, i - 1));
    });
  };

  const goForward = () => {
    startTransition(() => {
      addTransitionType("nav-forward");
      setIndex((i) => Math.min(pages.length - 1, i + 1));
    });
  };

  return (
    <>
      <button onClick={goBack}>Back</button>
      <button onClick={goForward}>Forward</button>
      <ViewTransition
        default={{
          "nav-back": "slide-from-left",
          "nav-forward": "slide-from-right",
        }}
      >
        <div>{pages[index]}</div>
      </ViewTransition>
    </>
  );
}
