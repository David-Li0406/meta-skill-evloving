# 3. Advanced Layout & Container Queries

**Impact: HIGH**

Tailwind 4 brings first-class support for modern CSS layout features that previously required plugins or complex custom CSS.

## 3.1 Native Container Queries

Container queries allow you to style an element based on the size of its parent rather than the viewport.

### Step 1: Define the Container
Apply the `@container` class to the parent.

```tsx
<div className="@container">
  <Card />
</div>
```

### Step 2: Apply Variants
Use the `@` prefix followed by a size (or custom name).

```tsx
function Card() {
  return (
    <div className="flex flex-col @md:flex-row gap-4">
      <div className="w-full @md:w-1/3">Image</div>
      <div className="flex-1">Content</div>
    </div>
  )
}
```

**Common Container Variants:**
- `@xs` (16rem)
- `@sm` (24rem)
- `@md` (28rem)
- `@lg` (32rem)
- `@xl` (36rem)

## 3.2 3D Transforms and Perspective

Tailwind 4 introduces native utilities for 3D manipulation.

```tsx
<div className="perspective-1000">
  <div className="rotate-x-45 rotate-y-12 transform-3d transition-transform">
    3D Card
  </div>
</div>
```

**Key Utilities:**
- `perspective-{val}`: Sets the 3D perspective distance.
- `rotate-x-{val}`, `rotate-y-{val}`, `rotate-z-{val}`.
- `scale-z-{val}`.
- `translate-z-{val}`.
- `transform-3d`: Enables 3D rendering context.

## 3.3 Dynamic Subgrid support

Using `grid-cols-subgrid` or `grid-rows-subgrid` is now fully integrated with the theme engine, allowing nested grids to align perfectly with their parents.

```tsx
<div className="grid grid-cols-4">
  <div className="col-span-3 grid grid-cols-subgrid">
    <div>I align with parent column 1</div>
    <div>I align with parent column 2</div>
    <div>I align with parent column 3</div>
  </div>
</div>
```
