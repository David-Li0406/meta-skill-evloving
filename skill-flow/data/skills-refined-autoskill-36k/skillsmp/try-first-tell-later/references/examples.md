# Examples from Teaching Practice

This document contains detailed examples of try-first-tell-later pedagogy from actual Python programming courses, showing how the approach works in practice.

## Example 1: Predicting Behavior (KeyError)

**Context**: Students have learned about dictionaries and how to access values with `phonebook["name"]`.

**Prompt**:
```latex
\begin{exercise}
  Vad händer om du försöker läsa ett fält som inte finns för en person?
  Vilket fel kommer du att få?
\end{exercise}
```

**English translation**: "What happens if you try to read a field that doesn't exist for a person? What error will you get?"

**[Student thinking space]**

**Answer**:
```
Svaret är att du får ett KeyError.
```

**Translation**: "The answer is that you get a KeyError."

**Explanation**:
```
Detta måste vi hantera när vi läser informationen.
Låt oss se hur koden för att läsa informationen blir:

[Shows code with try-except handling]
```

**Variation created**:
- **Variant**: Student prediction based on prior knowledge → Actual Python exception behavior
- **Invariant**: Dictionary access for missing keys
- **Discernment**: Critical aspect revealed = Python raises KeyError (doesn't return None or empty string)

---

## Example 2: Design Challenge (Data Structure)

**Context**: Simple phone book program that stores names and phone numbers in a dictionary.

**Prompt**:
```latex
\begin{exercise}
  Hur skulle du modifiera programmet ovan för att även lagra adresser?
  Tänk igenom strukturen innan du fortsätter läsa.
\end{exercise}
```

**Translation**: "How would you modify the program above to also store addresses? Think through the structure before continuing to read."

**[Student thinks through options: nested dictionaries, parallel lists, tuples, etc.]**

**Answer**:
```
Ett första försök skulle kunna vara att använda en nästlad
uppslagslista, där varje person får en uppslagslista med olika fält.
```

**Translation**: "A first attempt could be to use a nested dictionary, where each person gets a dictionary with different fields."

**Code shown**:
```python
contacts = {
    "adam": {
        "phone": "123456",
        "address": "Somewhere 1"
    },
    "betty": {
        "phone": "234567"
        # No address
    }
}
```

**Follow-up prompt**:
```latex
\begin{exercise}
  Vilka problem kan du se med denna approach? Tänk på:
  \begin{itemize}
    \item Vad händer om du skriver fel nyckelnamn i uppslagslistan?
    \item Hur vet andra programmerare vilka fält som finns tillgängliga?
    \item Vad händer om du vill lägga till validering (t.ex. kontrollera
          att telefonnumret har rätt format)?
  \end{itemize}
\end{exercise}
```

**Then shows class-based solution and compares**:
```python
class Person:
    def __init__(self, first_name, last_name, phone=None, address=None):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone = phone
        self.__address = address
```

**Variation created**:
- **Variant**: Nested dictionaries → Class-based approach
- **Invariant**: Need to store multiple pieces of data per person
- **Discernment**: Critical aspects = encapsulation, type safety, clear interface, validation opportunities

---

## Example 3: Conceptual Understanding (Classes vs Objects)

**Prompt**:
```latex
\begin{exercise}
  Vad är en klass och vad är ett objekt?
  Varför vi behöver två olika begrepp i överhuvudtaget?
  Försök att formulera dina egna definitioner innan du fortsätter läsa.
\end{exercise}
```

**Translation**: "What is a class and what is an object? Why do we need two different concepts at all? Try to formulate your own definitions before continuing to read."

**[Student formulates intuitive understanding]**

**Answer with metaphor**:
```
Klassen är som ritningen av huset: den beskriver hur huset ska se ut,
vilka rum och färger det ska ha, etc.

Objekten är de faktiska husen som byggs enligt ritningen.

Du kan bygga många hus (objekt) från samma ritning (klass), och varje
hus kan ha olika färger, inredning osv., men grundstrukturen är densamma.
```

**Translation**: "The class is like the blueprint of a house: it describes how the house should look, what rooms and colors it should have, etc. The objects are the actual houses built according to the blueprint. You can build many houses (objects) from the same blueprint (class), and each house can have different colors, furnishing, etc., but the basic structure is the same."

**Formal definition**:
```
\begin{description}
  \item[Klasser] är ritningarna, specifikationerna.
  \item[Objekt] är instanser av klasser.
\end{description}
```

**Code example**:
```python
class Person:
    def __init__(self, name):
        self.__name = name

# Two objects from the same class
person1 = Person("Alice")
person2 = Person("Bob")
```

**Variation created**:
- **Variant**: Student's informal understanding → Expert definition with metaphor → Code
- **Invariant**: The relationship between template and instances
- **Discernment**: Critical aspect = specification vs. instance, blueprint vs. building

---

## Example 4: Reasoning About Design (Private Attributes)

**Context**: Students have seen attributes defined with `__` prefix.

**Prompt**:
```latex
\begin{exercise}
  Varför tror du att attributen börjar med dubbla understreck (\mintinline{python}{__})?
  Vad betyder detta i Python?
\end{exercise}
```

**Translation**: "Why do you think the attributes start with double underscores? What does this mean in Python?"

**[Student reasons about naming conventions, privacy, etc.]**

**Answer**:
```
De dubbla understrecken gör attributen privata, vilket innebär att de
inte kan nås direkt från utsidan av klassen.

Detta kallas inkapsling (encapsulation) och är en viktig princip i
objektorienterad programmering.
```

**Follow-up reasoning prompt**:
```latex
\begin{exercise}
  Varför tror du det är bra att inte kunna komma åt attributen direkt?
  Vad skulle kunna gå fel om vi tillät det?
\end{exercise}
```

**Translation**: "Why do you think it's good not to be able to access the attributes directly? What could go wrong if we allowed it?"

**Explanation**:
```
Genom att använda metoder för att läsa och skriva attribut kan vi
kontrollera hur data hanteras. Vi kan lägga till validering, loggning,
eller andra funktioner utan att ändra hur användare av klassen
interagerar med den.

Vi kan också förhindra att en programmerare oavsiktligt ändrar ett
attribut på ett sätt som bryter klassens interna logik.
Det förhindrar många möjliga buggar att uppstå.
```

**Variation created**:
- **Variant**: Public attributes → Private attributes with methods
- **Invariant**: Need to access object data
- **Discernment**: Critical aspects = encapsulation, validation, API stability, preventing bugs

---

## Example 5: Predicting Method Behavior (Dunder Methods)

**Prompt**:
```latex
\begin{exercise}
  Vad tror du att \mintinline{python}{__str__()}-metoden gör?
  Hur skiljer den sig från \mintinline{python}{get_name()}?
\end{exercise}
```

**Translation**: "What do you think the `__str__()` method does? How does it differ from `get_name()`?"

**[Student predicts based on name and pattern]**

**Answer**:
```
Dundermetoden __str__() är en speciell metod som Python anropar
automatiskt när vi försöker konvertera objektet till en sträng
(exempelvis med print()) eller str().
```

**Follow-up**:
```latex
\begin{exercise}
  Vad tror du händer när vi skriver \mintinline{python}{print(person)}?
\end{exercise}
```

**Answer**:
```
Python anropar __str__()-metoden automatiskt, d.v.s. person.__str__().
Detta gör att vi kan styra hur våra objekt presenteras när de skrivs ut.
```

**Code example**:
```python
class Person:
    def __str__(self):
        return f"{self.__first_name} {self.__last_name}"

person = Person("Alice", "Smith")
print(person)  # Automatically calls person.__str__()
# Output: Alice Smith
```

**Variation created**:
- **Variant**: Regular methods → Dunder methods (automatic invocation)
- **Invariant**: Need to represent object as string
- **Discernment**: Critical aspect = Python's protocol for type conversion

---

## Example 6: Design Challenge (Inheritance)

**Context**: Students have learned about the `Person` class with various attributes and methods.

**Prompt**:
```latex
\begin{exercise}
  Om du skulle skapa en \mintinline{python}{PersonNick}-klass som är
  precis som \mintinline{python}{Person} men också har ett smeknamn,
  hur skulle du göra det?
\end{exercise}
```

**Translation**: "If you were to create a `PersonNick` class that is exactly like `Person` but also has a nickname, how would you do it?"

**[Student considers: copy all code? Reference Person? Some other approach?]**

**Answer**:
```
Arv låter oss skapa nya klasser baserade på befintliga klasser, och
utöka eller modifiera deras funktionalitet---helt utan kodupprepning.

Så istället för att kopiera all kod från Person, kan vi ärva från den
och bara lägga till det nya vi behöver.
```

**Code shown**:
```python
class PersonNick(Person):
    def __init__(self, first_name, last_name, nick, birthday=None,
                 phone=None, address=None):
        super().__init__(first_name, last_name, birthday, phone, address)
        self.__nick = nick

    def get_name(self):
        if self.__nick:
            return self.__nick
        return self.__first_name
```

**Follow-up prompt**:
```latex
\begin{exercise}
  Hur ska vi tilldela de attribut som \mintinline{python}{Person} redan har?
\end{exercise}
```

**Shows `super()` usage**

**Variation created**:
- **Variant**: Code duplication → Inheritance
- **Invariant**: Need PersonNick with all Person functionality plus nickname
- **Discernment**: Critical aspects = code reuse, extension, `super()` for parent initialization

---

## Example 7: Predicting Arithmetic (Fraction Addition)

**Context**: Teaching operator overloading with a Fraction class.

**Prompt**:
```latex
\begin{exercise}
  Hur kan vi implementera addition av två bråk?
\end{exercise}
```

**Translation**: "How can we implement addition of two fractions?"

**Mathematical explanation provided**:
```
För att addera två bråk a/b + c/d behöver vi:
1. Hitta en gemensam nämnare: b · d
2. Anpassa täljarna: (a·d)/(b·d) + (c·b)/(d·b)
3. Addera täljarna: (a·d + c·b)/(b·d)
```

**Code shown**:
```python
def __add__(self, other):
    if not isinstance(other, Fraction):
        other = Fraction(other)

    new_nominator = (self.__nominator * other.__denominator +
                     other.__nominator * self.__denominator)
    new_denominator = self.__denominator * other.__denominator

    return Fraction(new_nominator, new_denominator)
```

**Then tests it**:
```python
frac_a = Fraction(1, 2)
frac_b = Fraction(1, 3)
print(frac_a + frac_b)  # Works!
print(1 + frac_a)        # Doesn't work!
```

**Follow-up prompt**:
```latex
\begin{exercise}
  Varför fungerar inte \mintinline{python}{1 + frac_a}?
\end{exercise}
```

**Answer with explanation of evaluation order and `__radd__()`**

**Variation created**:
- **Variant**: Manual calculation → `__add__()` → Need for `__radd__()`
- **Invariant**: Mathematical fraction addition rules
- **Discernment**: Critical aspects = operator overloading, left vs right operators, type coercion

---

## Example 8: Experimentation (Operator Implementation)

**Context**: Students have implemented `__add__()` and understand the concept.

**Prompt**:
```latex
\begin{exercise}
  Hur kan vi implementera multiplikation av två bråk, \(\frac{a}{b} \cdot \frac{c}{d}\)?
\end{exercise}
```

**[Student tries to work out the formula: multiply numerators, multiply denominators]**

**Answer**:
```
Formeln är enkel: (a/b) · (c/d) = (a·c)/(b·d)

Vi multiplicerar täljare med täljare och nämnare med nämnare.
```

**Code shown**:
```python
def __mul__(self, other):
    if not isinstance(other, Fraction):
        other = Fraction(other)

    return Fraction(self.__nominator * other.__nominator,
                    self.__denominator * other.__denominator)
```

**Experimentation prompt**:
```latex
\begin{example}
  Multiplicera \(\frac{1}{2}\) och \(2\).
  \begin{minted}{python}
    frac_a = Fraction(1, 2)
    print(frac_a * 2)
    print(2 * frac_a)
  \end{minted}
\end{example}
```

**Observation**: Gets 2/2, which should be simplified to 1.

**Follow-up exercise**:
```latex
\begin{exercise}
  Hur kan vi implementera förkortning av bråk?
  Exempelvis \(\frac{2}{6}\) bör ju skrivas \(\frac{1}{3}\).
\end{exercise}
```

**Variation created**:
- **Variant**: Simple multiplication → Need for simplification
- **Invariant**: Multiplication rules
- **Discernment**: Critical aspect = Maintaining canonical form (simplified fractions)

---

## Example 9: Comparison and Reflection

**Context**: Students have seen both dictionary-based and class-based approaches to storing person data.

**Comparison prompt**:
```latex
\begin{exercise}
  Jämför koden för att skapa personer i de två exemplen.
  Vilka skillnader ser du?
  Vilket sätt tycker du är tydligare och varför?
\end{exercise}
```

**Shows side-by-side**:
```python
# Dictionary approach
contacts = {
    "adam": {
        "phone": "123456",
        "address": "Somewhere 1"
    }
}

# Class approach
from person import Person

contacts = {
    "adam": Person("Adam", "Andersson",
                   phone="123456",
                   address="Somewhere 1")
}
```

**Reflection prompt**:
```latex
\begin{exercise}
  Vilka fördelar ser du med att använda klasser jämfört med
  uppslagslistor? Lista minst tre fördelar.
\end{exercise}
```

**Answer provided**:
```
1. Tydligt vilka argument som behövs och i vilken ordning
2. IDE/editor kan ge autocomplete och type hints
3. Garanterar att alla Person-objekt har samma struktur
4. Kan lägga till validering och logik i metoderna
5. Mer läsbar kod - person.get_name() vs person["first_name"]
6. Förhindrar att fält stavs fel eller saknas
```

**Variation created**:
- **Variant**: Dictionary approach → Class approach
- **Invariant**: Need to store structured data
- **Discernment**: Critical aspects = type safety, encapsulation, API clarity, maintainability

---

## Example 10: Reasoning Chain (Properties)

**Context**: Students have seen getter methods like `get_nominator()`.

**Prompt**:
```latex
\begin{exercise}
  Vad är skillnaden mellan att skriva
  \mintinline{python}{frac.get_nominator()} och
  \mintinline{python}{frac.nominator}?
  Vilket känns mer naturligt?
\end{exercise}
```

**[Student considers syntax and readability]**

**Answer**:
```
Egenskaper låter oss använda attribut-liknande syntax medan vi
fortfarande behåller kontrollen över hur data läses och skrivs.
```

**Shows property decorator**:
```python
class Fraction:
    @property
    def nominator(self):
        return self.__nominator

    @property
    def denominator(self):
        return self.__denominator
```

**Usage**:
```python
frac = Fraction(1, 2)
print(f"{frac.nominator}/{frac.denominator}")  # Looks like attributes!
```

**Follow-up reasoning**:
```latex
\begin{exercise}
  Varför tror du det är bra att använda egenskaper istället för
  att göra attributen publika?
\end{exercise}
```

**Answer**:
```
Egenskaper ger oss inkapsling som vi får via getters och setters,
men samtidigt ser det ut som direkt attributåtkomst.

Vi kan ändra den interna implementationen utan att ändra hur
användare av klassen interagerar med den.

Vi kan också lägga till validering eller beräkningar när värden
läses eller skrivs.
```

**Variation created**:
- **Variant**: `get_nominator()` method → `.nominator` property → Understanding encapsulation
- **Invariant**: Need to access internal data
- **Discernment**: Critical aspects = Properties as controlled attribute access, maintaining encapsulation with natural syntax

---

## Teaching Notes

### What Makes These Examples Effective

1. **Builds on prior knowledge**: Each prompt asks something students can partially reason about
2. **Genuine thinking opportunity**: The questions are worth considering, not trivial
3. **Always provides answer**: Never leaves students hanging
4. **Explicit contrast**: Compares student thinking with expert knowledge
5. **Reveals critical aspects**: Uses the contrast to highlight what matters
6. **Progressive difficulty**: Sequences from simple predictions to complex design challenges
7. **Multiple prompt types**: Uses prediction, design, reasoning, comparison, reflection

### Adaptation for Different Contexts

**For beginners**:
- Use more prediction prompts (lower cognitive load)
- Provide more scaffolding in the prompts
- Use concrete, specific examples

**For advanced students**:
- Use more design and reflection prompts
- Ask for multiple approaches
- Encourage deeper reasoning about trade-offs

**For different subjects**:
- Mathematics: Predict outcomes, derive formulas before showing them
- Web development: Design approaches before showing patterns
- Data structures: Reason about efficiency before explaining

### Common Student Responses

These prompts typically elicit:
- **Prediction prompts**: Mix of correct intuitions and common misconceptions
- **Design prompts**: Multiple valid approaches, some more sophisticated than others
- **Reasoning prompts**: Connections to prior experience, sometimes missing key insights
- **Comparison prompts**: Surface-level differences initially, deeper understanding after guidance
- **Reflection prompts**: Beginning strategic thinking about tool selection

The key is to validate good thinking while gently correcting misconceptions and revealing missed critical aspects.

---

## Example 11: Diagnostic Pre-Test Analysis

This example shows how to use a try-first prompt as both learning activity and diagnostic assessment, following insights from Marton's NCOL on the Teacher's Paradox.

**Learning objective**: Understand why files need explicit resource management (the `with` statement)

**Critical aspects to discern**:
1. Files are system resources that must be released
2. Exceptions can prevent `close()` from being called
3. The `with` statement guarantees cleanup

### Pre-Test Prompt

```latex
\begin{exercise}[Diagnostic: File handling]
  Here's code that processes a file:
  \begin{minted}{python}
file = open("data.txt", "r")
content = file.read()
# ... process content ...
file.close()
  \end{minted}
  
  What problems might occur with this approach?
  List as many as you can think of.
\end{exercise}
```

**Note**: The prompt does NOT mention exceptions, resources, or the `with` statement. Students must discern the critical aspects themselves. This follows Marton's principle: "If we want to find out to what extent they have learned to do so, we should not point out those aspects for them."

### Response Categories

**Category A - Discerns critical aspect (exception safety)**:
> "If an error happens while processing, close() never runs and the file stays open."

**Analysis**: Student sees the critical aspect. Ready for:
- Generalization: show pattern applies to other resources (network, database)
- Solution: introduce `with` statement

**Category B - Surface-level concerns**:
> "The file might not exist" or "The filename could be wrong"

**Analysis**: Student focuses on different aspects (valid but not the learning objective). Needs:
- Contrast: show code that fails vs succeeds at close()
- Concrete example: exception between open and close

**Category C - No problems identified**:
> "It looks fine to me"

**Analysis**: Student hasn't considered edge cases. Needs:
- Concrete failure scenario before any explanation
- Let them experience the problem

### Teaching Response by Category

**For Category A students**:
```latex
\begin{frame}[fragile]
  \begin{remark}
    Du identifierade rätt att undantag kan förhindra close().
    Python har en lösning: \mintinline{python}{with}-satsen.
  \end{remark}
  
  \begin{example}[with-satsen]
    \begin{minted}{python}
with open("data.txt", "r") as file:
    content = file.read()
# file.close() called automatically, even if exception
    \end{minted}
  \end{example}
\end{frame}
```

**For Category B/C students** (need contrast first):
```latex
% First, create contrast to reveal the critical aspect
\begin{frame}[fragile]
  \begin{example}[Vad händer här?]
    \begin{minted}{python}
file = open("data.txt", "r")
content = file.read()
result = int(content)  # Raises ValueError if not a number!
file.close()           # Never reached!
    \end{minted}
  \end{example}
  
  \begin{exercise}
    Kör koden med en fil som innehåller "hello".
    Vad händer? Stängs filen?
  \end{exercise}
\end{frame}

% Then introduce solution after they've experienced the problem
\begin{frame}[fragile]
  \begin{example}[with garanterar close()]
    \begin{minted}{python}
with open("data.txt", "r") as file:
    content = file.read()
    result = int(content)  # Even if this fails...
# ... file is still closed!
    \end{minted}
  \end{example}
\end{frame}
```

### Post-Test

After teaching, re-assess with similar prompt to verify transfer:

```latex
\begin{exercise}[Post-test]
  Here's database connection code:
  \begin{minted}{python}
conn = database.connect("mydb")
data = conn.query("SELECT * FROM users")
# ... process data ...
conn.close()
  \end{minted}
  
  What problems might occur? How would you fix them?
\end{exercise}
```

**Expected improvement**: Students who previously gave Category B/C responses should now:
- Mention exception safety (transfer of critical aspect to new context)
- Suggest context manager / `with` pattern
- Recognize the general pattern applies to all resources

### Variation Pattern Analysis

```latex
\ltnote{%
  \textbf{Diagnostic purpose}: Reveal which students discern 
  the critical aspect (exception safety) before teaching.
  
  \textbf{Pre-test results}: 
  - Category A (discerned): X students
  - Category B (surface): Y students  
  - Category C (none): Z students
  
  \textbf{Variation pattern used}: Contrast
  - What varies: Whether exception occurs before close()
  - What's invariant: The file operations, the need to close
  - Critical aspect revealed: Resource cleanup must be guaranteed
  
  \textbf{Post-test}: Tests transfer to new context (database)
  to verify discernment, not just recall of the specific solution.
  
  \textbf{Post-test results}: W\% now discern critical aspect
  (compared to X\% pre-test).
}
```

### Why This Works

This example demonstrates the dual purpose of try-first prompts:

1. **As learning activity**: Engages prediction, creates cognitive engagement before explanation
2. **As diagnostic**: Reveals which critical aspects students see/miss, informing teaching approach
3. **As post-test**: Verifies learning by testing transfer to new context (database instead of file)

The key insight from Marton: by NOT revealing the critical aspects in the question, we can genuinely assess whether students can discern them. A question like "What happens if an exception occurs before close()?" would point out the critical aspect and defeat the diagnostic purpose.
