# Better Specs

Testing best practices for RSpec, adapted from [betterspecs.org](https://www.betterspecs.org/).

## Keep Descriptions Short

Use `.` for class methods and `#` for instance methods in describe blocks.

```ruby
# Bad
describe "the authenticate method for User"
describe "if the user is an admin"

# Good
describe "User" do
  describe ".authenticate"
  describe "#admin?"
end
```

## Use `context`

Start context block descriptions with 'when', 'with', or 'without' to organize related tests.

```ruby
# Bad
it "has 200 status code if logged in" do
  expect(response).to respond_with(200)
end

it "has 401 status code if not logged in" do
  expect(response).to respond_with(401)
end

# Good
context "when logged in" do
  it { is_expected.to respond_with(200) }
end

context "when logged out" do
  it { is_expected.to respond_with(401) }
end
```

## Keep `it` Descriptions Short

Alternatively, use `is_expected` to remove the `it` description entirely.

```ruby
# Bad
it "results in a true value" do
  expect(subject).to be(true)
end

it "has 422 status code if an unexpected params will be added" do
  expect(subject).to respond_with(422)
end

# Good (explicit subject)
it "returns true" do
  expect(subject).to be(true)
end

# Good (implicit subject)
context "when the parameters are invalid" do
  it { is_expected.to respond_with(422) }
end
```

## Single Expectations

Prefer one assertion per test. Multiple assertions are acceptable when test setup is expensive, such as in system tests.

```ruby
# Good (isolated)
it { is_expected.to respond_with_content_type(:json) }
it { is_expected.to assign_to(:resource) }

# Good (not isolated)
it "creates a resource" do
  expect(response).to respond_with_content_type(:json)
  expect(response).to assign_to(:resource)
end
```

## Test All Cases

Test valid, edge, and invalid cases, not just the happy path.

```ruby
# Bad
it "shows the resource"

# Good
describe "#destroy" do
  context "when resource is found" do
    it "responds with a 200 status"
    it "shows the resource"
  end

  context "when the resource is not found" do
    it "responds with a 404 status"
  end

  context "when the resource is not owned" do
    it "responds with a 404 status"
  end
end
```

## `expect` vs. `should`

Always use the `expect` syntax—never use `should`.

```ruby
# Bad
response.should respond_with_content_type(:json)

# Good
expect(response).to respond_with_content_type(:json)
```

Use `is_expected.to` for one-line expectations with implicit subject.

```ruby
# Bad
it { should respond_with(422) }

# Good
it { is_expected.to respond_with(422) }
```

## `subject`

Use `subject` to clarify what's being tested. Use named subjects for clearer test intent.

```ruby
# Bad
it { expect(assigns("message")).to match(/it was born in Belville/) }

# Good (implicit)
subject { assigns("message") }

it { is_expected.to match(/it was born in Billville/) }

# Good (named)
subject(:hero) { Hero.first }

it "carries a sword" do
  expect(hero.equipment).to include("sword")
end
```

## `let` vs. `let!`

Use `let` for lazy-loaded variables. Use `let!` for immediate evaluation.

```ruby
# Bad
before { @resource = create(:device) }
before { @type = Type.find(@resource.type_id) }

# Good (lazy)
let(:type) { Type.find(resource.type_id) }

# Good (immediate)
let!(:admin) { create(:admin) }
```

## Mocks

Test real behavior when possible. Use mocks sparingly.

## Minimal Data

Create only the test data you need.

## Factories

Use factories instead of fixtures. Avoid complex data setup when possible.

```ruby
# Bad
let(:user) { User.create(attributes) }

# Good
let(:user) { FactoryBot.create(:user) }
```

## Shared Examples

Use shared examples sparingly, only when test patterns are very repetitive.

## Integration

Test actual behavior with real database interactions for models and full request cycles for controllers.

## Avoid "should"

Avoid "should" in test descriptions. Use present tense, third person.

```ruby
# Bad
it "should not update the user's email" do
  user.email.should == original_email
end

# Good
it "does not update the user's email" do
  expect(user.email).to eq(original_email)
end
```
