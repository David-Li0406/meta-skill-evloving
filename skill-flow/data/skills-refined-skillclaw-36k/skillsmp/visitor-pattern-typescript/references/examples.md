# Visitor Pattern Examples (TypeScript)

Each example is runnable in Node with ts-node.

## Example 1: Shapes with XML export + AreaVisitor

```ts
type VisitorResult = string | number;

interface Visitor<R = VisitorResult> {
  visitDot(dot: Dot): R;
  visitCircle(circle: Circle): R;
  visitRectangle(rect: Rectangle): R;
  visitCompound(compound: CompoundShape): R;
}

interface Visitable<R = VisitorResult> {
  accept(visitor: Visitor<R>): R;
}

class Dot implements Visitable {
  constructor(public x: number, public y: number) {}
  accept<R>(visitor: Visitor<R>): R {
    return visitor.visitDot(this);
  }
}

class Circle implements Visitable {
  constructor(public x: number, public y: number, public radius: number) {}
  accept<R>(visitor: Visitor<R>): R {
    return visitor.visitCircle(this);
  }
}

class Rectangle implements Visitable {
  constructor(public x: number, public y: number, public w: number, public h: number) {}
  accept<R>(visitor: Visitor<R>): R {
    return visitor.visitRectangle(this);
  }
}

class CompoundShape implements Visitable {
  constructor(public children: Visitable[]) {}
  accept<R>(visitor: Visitor<R>): R {
    return visitor.visitCompound(this);
  }
}

class XmlExportVisitor implements Visitor<string> {
  visitDot(dot: Dot): string {
    return `<dot x="${dot.x}" y="${dot.y}" />`;
  }
  visitCircle(circle: Circle): string {
    return `<circle x="${circle.x}" y="${circle.y}" r="${circle.radius}" />`;
  }
  visitRectangle(rect: Rectangle): string {
    return `<rect x="${rect.x}" y="${rect.y}" w="${rect.w}" h="${rect.h}" />`;
  }
  visitCompound(compound: CompoundShape): string {
    const inner = compound.children.map((c) => c.accept(this)).join("");
    return `<compound>${inner}</compound>`;
  }
}

class AreaVisitor implements Visitor<number> {
  visitDot(): number {
    return 0;
  }
  visitCircle(circle: Circle): number {
    return Math.PI * circle.radius * circle.radius;
  }
  visitRectangle(rect: Rectangle): number {
    return rect.w * rect.h;
  }
  visitCompound(compound: CompoundShape): number {
    return compound.children.reduce((sum, c) => sum + c.accept(this), 0);
  }
}

const shapes: Visitable[] = [
  new Dot(1, 2),
  new Circle(0, 0, 10),
  new Rectangle(0, 0, 3, 4),
  new CompoundShape([new Dot(2, 2), new Circle(1, 1, 2)]),
];

const xmlVisitor = new XmlExportVisitor();
const areaVisitor = new AreaVisitor();

const xml = shapes.map((s) => s.accept(xmlVisitor)).join("\n");
const area = shapes.reduce((sum, s) => sum + s.accept(areaVisitor), 0);

console.log(xml);
console.log("total area", area);

const trace: string[] = [];
class TraceVisitor implements Visitor<void> {
  visitDot() { trace.push("dot"); }
  visitCircle() { trace.push("circle"); }
  visitRectangle() { trace.push("rectangle"); }
  visitCompound(compound: CompoundShape) {
    trace.push("compound");
    compound.children.forEach((c) => c.accept(this));
  }
}

const compound = new CompoundShape([new Dot(0, 0), new Rectangle(0, 0, 1, 1)]);
compound.accept(new TraceVisitor());
if (trace.join(",") !== "compound,dot,rectangle") {
  throw new Error("Double-dispatch or traversal order failed");
}
```

## Example 2: Expression AST evaluation + print visitor

```ts
type ExprVisitor<R> = {
  visitLiteral(node: Literal): R;
  visitAdd(node: Add): R;
  visitMultiply(node: Multiply): R;
  visitNegate(node: Negate): R;
};

interface Expr {
  accept<R>(visitor: ExprVisitor<R>): R;
}

class Literal implements Expr {
  constructor(public value: number) {}
  accept<R>(visitor: ExprVisitor<R>): R {
    return visitor.visitLiteral(this);
  }
}

class Add implements Expr {
  constructor(public left: Expr, public right: Expr) {}
  accept<R>(visitor: ExprVisitor<R>): R {
    return visitor.visitAdd(this);
  }
}

class Multiply implements Expr {
  constructor(public left: Expr, public right: Expr) {}
  accept<R>(visitor: ExprVisitor<R>): R {
    return visitor.visitMultiply(this);
  }
}

class Negate implements Expr {
  constructor(public expr: Expr) {}
  accept<R>(visitor: ExprVisitor<R>): R {
    return visitor.visitNegate(this);
  }
}

class EvalVisitor implements ExprVisitor<number> {
  visitLiteral(node: Literal): number {
    return node.value;
  }
  visitAdd(node: Add): number {
    return node.left.accept(this) + node.right.accept(this);
  }
  visitMultiply(node: Multiply): number {
    return node.left.accept(this) * node.right.accept(this);
  }
  visitNegate(node: Negate): number {
    return -node.expr.accept(this);
  }
}

class PrintVisitor implements ExprVisitor<string> {
  visitLiteral(node: Literal): string {
    return node.value.toString();
  }
  visitAdd(node: Add): string {
    return `(${node.left.accept(this)} + ${node.right.accept(this)})`;
  }
  visitMultiply(node: Multiply): string {
    return `(${node.left.accept(this)} * ${node.right.accept(this)})`;
  }
  visitNegate(node: Negate): string {
    return `(-${node.expr.accept(this)})`;
  }
}

const expr: Expr = new Add(new Literal(2), new Multiply(new Literal(3), new Negate(new Literal(4))));

const evalVisitor = new EvalVisitor();
const printVisitor = new PrintVisitor();

console.log(expr.accept(printVisitor));
console.log(expr.accept(evalVisitor));
```

## Example 3: Permission visitor with diagnostics

```ts
type Decision = "allow" | "deny";

type VisitorDiag = { node: string; message: string };

interface OrgVisitor<R> {
  visitTeam(team: Team): R;
  visitUser(user: User): R;
  visitServiceAccount(sa: ServiceAccount): R;
}

interface OrgNode {
  accept<R>(visitor: OrgVisitor<R>): R;
}

class Team implements OrgNode {
  constructor(public name: string, public members: OrgNode[]) {}
  accept<R>(visitor: OrgVisitor<R>): R {
    return visitor.visitTeam(this);
  }
}

class User implements OrgNode {
  constructor(public id: string, public role: "admin" | "member") {}
  accept<R>(visitor: OrgVisitor<R>): R {
    return visitor.visitUser(this);
  }
}

class ServiceAccount implements OrgNode {
  constructor(public name: string, public scope: "read" | "write") {}
  accept<R>(visitor: OrgVisitor<R>): R {
    return visitor.visitServiceAccount(this);
  }
}

class PermissionVisitor implements OrgVisitor<Decision> {
  diagnostics: VisitorDiag[] = [];

  visitTeam(team: Team): Decision {
    for (const m of team.members) {
      const d = m.accept(this);
      if (d === "deny") return "deny";
    }
    return "allow";
  }

  visitUser(user: User): Decision {
    if (user.role === "admin") return "allow";
    this.diagnostics.push({ node: `user:${user.id}`, message: "Non-admin" });
    return "deny";
  }

  visitServiceAccount(sa: ServiceAccount): Decision {
    if (sa.scope === "write") return "allow";
    this.diagnostics.push({ node: `sa:${sa.name}`, message: "Read-only" });
    return "deny";
  }
}

const org: OrgNode = new Team("core", [
  new User("u1", "member"),
  new ServiceAccount("svc", "read"),
]);

const visitor = new PermissionVisitor();
const decision = org.accept(visitor);
console.log(decision, visitor.diagnostics);
```

## Disambiguation snippet

```ts
// Visitor vs Strategy: Strategy swaps algorithms at runtime; Visitor adds operations over element types.
// Visitor vs Command: Command is a request object; Visitor is a cross-cutting operation over a structure.
// Visitor vs Mediator: Mediator coordinates peers; Visitor runs algorithms over elements.
// Visitor vs discriminated-union switch: union switch branches by type; Visitor organizes by algorithm.

type Visitor = { visitX(x: unknown): unknown };

type Strategy = { run(input: unknown): unknown };

type Command = { execute(): void };

type Mediator = { notify(sender: unknown, event: unknown): void };
```
