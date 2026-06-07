---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/csharp
  - topic/dotnet
  - topic/language-design
  - topic/pattern-matching
source: https://www.youtube.com/watch?v=7qW92AwlrjM
session_code: DEM304
event: Microsoft Build 2026
speakers: Mads Torgersen, Dustin Campbell
duration_min: 25
aliases:
  - Union types in C#
---

# DEM304 — Union types in C#

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Mads Torgersen (Lead Designer, C# language) & Dustin Campbell (Engineer, C# team)  
> **Duration:** ~25 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=7qW92AwlrjM)

## 🎯 TL;DR
A live-coding demo from the C# language team introducing **union types**, a major new feature shipping in **C# 15 (November)** and already available in **.NET 11 preview**. A union is a named type that can be "one of" a fixed set of case types — e.g. `union Pet(Dog, Cat, Bird)` — giving you a real type to program against instead of falling back to `object`. The payoff is **type safety**: the compiler blocks values that aren't in the set, offers **implicit conversions** from each case type into the union, and crucially makes `switch` **exhaustiveness checking** work so you get a warning until every case (including `null` for nullable cases) is handled. Unions support generics, function/computed members, and static members (but **no extra state** beyond the contained value). They cover both "gluing together pre-existing unrelated types" and classic **discriminated-union** modelling (declaring cases alongside the union). Under the hood the syntax generates a `struct` holding a single `object value` field (boxing), implements `IUnion`, and is driven by a `[Union]` attribute — all of which you can hand-author yourself to make different (e.g. non-boxing/performance) implementation choices.

## 🔑 Key Takeaways
- **Union types ship in C# 15**, releasing in **November**; the bits are already in **preview** (.NET 11 preview / Visual Studio preview / VS Code C# extension pre-release).
- C#'s unions are deliberately a **"Goldilocks" / compromise** design — their own flavour, different from TypeScript's unions and from functional-language discriminated unions.
- Syntax is minimal: `union Pet(Dog, Cat, Bird);` declares a union of those case types — "and it's that simple."
- A union gives you a **real named type** to use instead of widening everything to `object` (the pre-union workaround for unrelated types).
- The compiler provides **implicit conversions** from each case type *into* the union (e.g. a `Dog` is usable where a `Pet` is expected); assigning a non-member type (a `Shark`) is a compile **error** ("cannot implicitly convert type Shark to Pet").
- **Pattern matching / `switch` becomes exhaustive-checked**: you get a warning until all cases are covered, and the warning clears once every case is handled — "compiler help to let us know we've correctly handled everything."
- Exhaustiveness is **smart about `null`**: a `union Pet(Dog, Cat, Bird?)` (nullable case) re-introduces the warning until `null` is also handled.
- You can add **function members** — computed properties, methods, static members — directly on the union for shared abstraction across the cases.
- Unions **may not introduce additional state**: the only state is the actual contained value (the dog/cat/bird); the compiler prevents extra fields. (Function members are fine; state is not.)
- Unions are **fully general**: they can be **generic** (`union Result<T>(Success<T>, Error)`), and case types can be records, interfaces, type parameters, value types, etc. — case types only need to **convert to `object`**, and overlapping cases are allowed.
- Two usage shapes: (1) **bringing together existing unrelated types** you didn't author (the Pet/animals scenario), and (2) **discriminated-union style** where you declare the case types *together with* the union (the `Result<T>` / wire scenario).
- **Records are the natural case type** for discriminated unions — you can **deconstruct** the data straight out of them in the `switch`.
- **Under the hood:** the syntax generates a **`struct`** with a single `object value` auto-property (cases are **boxed** into it), it implements interface **`IUnion`** (which just exposes that `value` property), and the whole thing is recognised via a **`[Union]` attribute**.
- You can **hand-author a union** (apply `[Union]` + provide the required `public object value` property + a **construction member/constructor per case**) to make different implementation choices — e.g. a **non-boxing** layout for performance, or to **retrofit an existing pre-union type** so it gains exhaustiveness + implicit conversions "for free."
- The design took **~5 years**; the team explored **structural (TypeScript-style) unions** but rejected them because **.NET types must exist at runtime**, so C# unions are **nominal (named, declared)** — a structural-ish layer on top via generics remains a possible future.

## 📚 Detailed Notes

### Framing: what unions are and the "Goldilocks" stance
Mads Torgersen (lead designer of C#) and Dustin Campbell (engineer on the C# team) present **one feature: union types**, landing in **C# 15** (out in November), with bits already in preview. They set expectations up front: lots of languages already have "unions," but they're **all different** — TypeScript has unions, most functional languages have some form of **discriminated unions** — and C# is adding **its own** take, jokingly called the **"Goldilocks"** (or "compromise") version. So existing union knowledge transfers only partially; the session shows "how unions *should* be" from scratch.

### Scenario 1 — the problem: unrelated types and the `object` fallback
The demo opens with modern C# (top-level statements) and a set of types representing **animals/pets** — mostly `record`s plus a few other types (`Dog`, `Cat`, `Bird`, etc.). The framing premise: in the real world these come from **separate libraries** (a "dog library," a "cat library") that **don't share a base type or interface** — "dog and cat people" don't talk to each other.

To process "pets" together today, the only common ancestor is **`object`**, so the code builds a **`List<object>`**, iterates with `foreach`, and uses a **`switch` expression** over each item to deconstruct it into a description string written to the console. Problems demonstrated:
- **No type safety** — nothing stops a non-pet from entering the list. The demo deliberately includes a **`Shark`** ("there are four somethings… one of them is not what I'd consider a pet").
- The `switch` shows a **squiggle/warning**: because the value is `object`, the compiler can't prove the switch is **exhaustive** — "you're not checking for crocodiles and snails" and every other thing an `object` could be.

This is "the best we can do in C# up until now," and it's unsatisfying.

### Scenario 1 — the fix: declaring a union
The key idea: even though these types were **not** created with a notion of "pet," **why not create a "pet" concept they can belong to?** That's a union type. Syntax:

```csharp
union Pet(Dog, Cat, Bird);   // a union of the case types that make up "Pet"
```

You just type `union`, name it, and list the member (case) types. Immediate effects once `Pet` exists:
- Change `List<object>` → **`List<Pet>`**. The line that added a `Shark` now **errors**: *"cannot implicitly convert type Shark to Pet."* Fix = delete that line.
- That error message is informative in two directions — it implies the **other types *can* be implicitly converted to `Pet`**. So a union gets **implicit conversions from each case type into the union** (a `Dog` flows in wherever a `Pet` is expected). "Implicit conversions, check."
- In the `switch`, a `Shark` pattern now also **errors** ("expression of type Pet cannot be handled by a pattern of type Shark") — remove it.
- **Best part:** the earlier "could not be proven exhaustive" warning on the switch is **gone** — all cases are covered and you get **compiler help confirming** every case is handled correctly.

To prove the safety net, they **comment out one case type** in the union → the **exhaustiveness warning returns**. So the compiler ensures you hit **all** the cases **and nothing but** the cases — the essence of the strong typing unions give you.

### Exhaustiveness is `null`-aware
The check is **smart**. If you declare, say, `union Pet(Dog, Cat, Bird?)` with a **nullable** case (a "nullable bird"), the warning comes **back** — because now **`null`** is one of the possible values and must also be handled in the switch. Until `null` is covered, the switch is **not exhaustive**. This shows exhaustiveness reasons about nullability, not just the listed types.

### Adding members to a union (abstraction without extra state)
A bare `union Pet(Dog, Cat, Bird);` is like a one-liner type — valid, but you can do more by adding **braces and members**:

```csharp
union Pet(Dog, Cat, Bird)
{
    public string Description => /* switch on this — what kind of pet is this — to build the text */;
}
```

You can **move the description logic onto the union itself** as a **computed/calculated property** (e.g. `Description`), switching internally on which case the value is. Callers then just use `pet.Description` instead of switching externally. So you can attach your **own function members** that compute things over the cases.

**Important constraint:** the team **draws a line at anything that introduces more state.** Conceptually, the state of a union value **is just** the contained dog/cat/bird — it should carry **no additional state**, and the compiler **prevents** you from adding fields. But **function members are totally fine**: computed properties, methods, and any **static members** you want. This lets you do **abstraction** and implement the common operations across the cases in one place. Mads expects this — "add a computed member + switch internally" — to be **how most people use the feature.**

### Scenario 2 — discriminated-union style: `Result<T>` over the wire
The team acknowledges a common critique: their demos use toy domains (person/student, pets/dogs/cats). So they switch to a scenario *"closer to real code"* — and in fact **the #1 scenario people asked for** when requesting unions: **modelling data coming off the wire**, where you either get a **success (with a payload)** or an **error**.

They start from two **records** (existing, current-day C# features — "not new… old features you're not using yet"):

```csharp
record Success<T>(T Data);   // generic payload
record Error(string Message);
```

Then **glue them together with a union**, using generics:

```csharp
union Result<T>(Success<T>, Error);   // two cases: a successful payload of T, or an error
```

A method can now return `Result<T>` and return **one of the two** case values. They build sample data as a **`Queue<Result<int>>`** (simulating items arriving off the wire), enqueueing e.g. a `Success(42)` and a `new Error("...")`. Because of the **implicit conversions**, each case value flows straight into the `Result<int>` queue.

Processing loop:

```csharp
while (queue.TryDequeue(out var result))
{
    var text = result switch
    {
        Success<int>(var data) => /* use data, e.g. 42 */ ...,
        Error(var message)     => throw /* or handle */ ...,
    };
}
```

Key points demonstrated:
- You **switch on `result`** and match `Success<int>` first; because `Success` is a **record**, you can **deconstruct** the payload directly (`Success<int>(var data)`) — *"that's why you should use record: you can deconstruct the data right out of it."*
- The moment only `Success` is handled, the **exhaustiveness warning appears again** — "because I haven't handled `Error`" — reminding you to deal with errors. Handling `Error` (grab `message`, then `throw` it in the demo) clears it.
- Running it: prints/uses **42** for the success, then **throws** on the error. The cheeky framing: *"we're in the business of giving you more errors… and you love us for it"* — because you get **tighter control** of your scenario.

### Two distinct usage patterns (and why both matter)
Mads explicitly **contrasts the two scenarios**:
- **Scenario 1 (Pet):** unions over **pre-existing types declared elsewhere** — you're *bringing together* things others already made.
- **Scenario 2 (Result):** you **declare the case types together with the union** — you're modelling the **whole package** ("the kinds of things it can be"). This is what functional programmers would call a **discriminated union**; C# is *"essentially emulating that here."* He expects this to be a **common pattern** too.

He also reiterates how **general** the feature is: unions can be **generic**, can have **members**, and can do most things other types can. **Case types** can be almost anything — records, **interfaces**, **type parameters**, value types — the only requirement is that they **convert to `object`**, and there's **no restriction on overlap** between case types.

### "How the sausage is made" — what a union is under the hood
Dustin asks the real-world question: this feels *magical*; historically writing this kind of type in C# needs **a lot of boilerplate** — so what's actually generated? They **comment out the `union` syntax** and **re-write the equivalent by hand** to reveal the underlying shape (which also compiles and works). The generated form is a **`struct`** — a *"very prescriptive / opinionated"* shape:

1. **It's a `struct`.** You tell the compiler *"treat this as a union"* via a **`[Union]` attribute** (already in **.NET 11 preview 4**). Without the rest, the attribute alone produces several **errors** that spell out exactly what a union must have.
2. **Required `value` property.** A union *"must have a **public instance `value` property of type `object`**."* (This is the same `value` member you'd see if you dotted into a syntax-generated union.) It's just an **auto-property backed by a single `object` field** that holds whatever the union currently is — boxed/wrapped inside the struct.
3. **At least one "union creation member."** How do you create instances? **Constructors.** You add **one constructor per case**, each taking that case type and assigning it into the big `value` field:
   ```csharp
   [Union]
   struct Result<T>
   {
       public object value { get; }            // required
       public Result(Success<T> value) => this.value = value;  // construction member per case
       public Result(Error value)      => this.value = value;
   }
   ```
   As each constructor is added, the corresponding error disappears; once a case is constructible the union "has" that case ("now it's a union of one thing," then add the other).
4. **`IUnion` interface.** When generating from syntax, the compiler also makes the type **implement `IUnion`** (also already in **.NET 11**), which **just exposes the `value` property** — nothing more. It lets you do a **runtime check** for "is this a union?" / read the value generically in runtime code.

So a syntax-generated union is, concretely: a **`struct` with a single reference (`object`) field**, that **boxes/casts on the way in and out**.

### Why expose the hand-authored form? Two reasons
The whole point of revealing the underpinnings is so you can **make different implementation choices** than the default (which boxes case types into an `object` field):

1. **Performance / avoiding boxing.** If you're in a **tight loop** and want a union of **two small value types**, the default **boxes on every union value creation** — an allocation that can be expensive. Instead you can **choose your own storage**: e.g. a field of each value type **plus a discriminator field** saying which one is active, avoiding the boxing. (They note there are *additional* tricks — you can have the compiler **generate different usage code that also avoids boxing** — not shown.) The tradeoff: it's **more complicated from a developer standpoint**, but saves the allocations. Aside: *"Copilot's going to write that part anyway… as long as you teach it."*
2. **Retrofitting existing hand-rolled unions.** Before this feature ("~20+ years without unions"), people built their **own** union-like types with conventions like *"// do not derive from this class"* or *"// do not assign other types."* Rather than the new feature **stomping all over** that work, you can put the **`[Union]` attribute on your existing type** (and add a few members to satisfy the compiler) so your **existing type becomes a real union** in the compiler's eyes — gaining **exhaustiveness**, **implicit conversions**, and the rest **for free**.

Mads frames this as classic C# design philosophy: many C# features are **built on patterns/conventions** the compiler treats specially (rather than being baked rigidly into the type system) — and you can implement them yourself. Unions follow the same approach: the syntax gives the **basics**, but you **can go deep**. Most people will **never need** the manual route, but it's good to know the default is *"a `struct` with a single reference field that boxes and casts."*

### Q&A — TypeScript envy and why C# went nominal
Audience question: TypeScript/JavaScript developers know unions, but use them differently (e.g. because JS lacks overloads, unions are used on inbound parameters). What was the **internal design debate**?

- **TypeScript unions are structural**: you don't declare them by name — you can **cook one up on the spot** (`dog | cat | bird` as the type of something) and the compiler figures it out. The C# team had **"envy"** of that and **actually tried** designing down that path.
- **Why it didn't work for C#:** TypeScript types **vanish at compile time** — they don't exist at runtime. But **C#/.NET types must mean something at runtime** — you have to be able to **ask questions about them at runtime** — so unions **can't be thrown away**. For that, it's **better to have real, named (declared) types**.
- **Result:** C# unions are **nominal — declared, named unions of types**. They kept TypeScript's notion that *"a union is a union **of types**"*, but made them **nominal** rather than structural.
- **Future possibility:** you could get some structural-ish feel back via **generics** — e.g. a library type like `Union<T1, T2>` — *"we haven't done that yet, but it's a possibility."* They **may revisit** a structural layer on top later ("there are proposals"). Analogy: like **delegates / function types** — C# has **no anonymous function types** but gives you ways to **declare** them. C#'s unions sit **right in the middle** between TypeScript's structural unions and functional languages' fully-nominal discriminated unions — *"trying to do kind of both."*

### Closing: maturity, timeline, and how to try it
- The design **took roughly five years** to reach this **"very simple" form** — they explored **many paths** and are happy to discuss at length.
- **Availability today (preview):** the current **Visual Studio preview** has union support; **.NET 11 preview**; **VS Code** with the **C# extension pre-release** (insiders). What was demoed *"will be there in about a couple of weeks"* and will keep improving — there are **some bugs** in the current preview, but it's usable: **"go try it."**
- They direct attendees to the **green dev tools area / Experts Zone pavilion** ("big cube hanging overhead") to continue the conversation.

## 🛠️ Products / Features / Technologies Mentioned
- **Union types (C#)** — the headline feature: a named type that is "one of" a fixed set of case types, with implicit conversions in and exhaustiveness-checked pattern matching.
- **`union` keyword / syntax** — `union Name(CaseA, CaseB, …);` (optionally with `{ … }` members) to declare a union.
- **`[Union]` attribute** — marks a hand-authored `struct`/`class` as a union for the compiler; in **.NET 11 preview 4**.
- **`IUnion` interface** — implemented by syntax-generated unions; exposes the `value` property for runtime checks; in **.NET 11**.
- **`value` property (object)** — required public instance member on any union; backing store for the contained (boxed) case value.
- **Pattern matching / `switch` expression** — gains **exhaustiveness checking** over union cases (including `null` for nullable cases).
- **Records** — recommended case types; enable **deconstruction** of payload data directly in `switch` patterns.
- **`struct`** — the underlying representation the union syntax generates (single `object` reference field).
- **Generics** — unions and their case types can be generic (e.g. `Result<T>`, `Success<T>`).
- **Top-level statements** — used in the demo's modern C# entry point.
- **C# 15** — the language version delivering unions, releasing November.
- **.NET 11** — the runtime/SDK preview carrying the supporting types/attribute.
- **Visual Studio (preview)** — IDE with union support today.
- **VS Code + C# extension (pre-release/insiders)** — editor support for unions in preview.
- **GitHub Copilot** — name-checked as able to write the more complex (non-boxing) hand-authored union code.
- **TypeScript** — referenced as the structural-union comparison point.

## 🚀 Announcements / What's New
- **Union types are coming to C# 15**, which **releases in November**. This is the central announcement of the session.
- **Preview available now:** the feature and its supporting APIs are shipping in **.NET 11 preview** — specifically the **`[Union]` attribute and `IUnion` interface are in .NET 11 preview 4**.
- **Tooling preview:** union support is in the **current Visual Studio preview** and in **VS Code via the pre-release C# extension** (insiders); the team notes the demoed experience *"will be there in about a couple of weeks"* and improve further (some bugs exist in the current preview).
- **Roadmap / future direction (not committed):** a possible **structural-style layer on top** (e.g. a generic `Union<T1, T2>` library type) to recover some TypeScript-like flexibility — *"we haven't done that yet… we may come back to it";* described as proposals, **not** an announced deliverable.

## 💡 Demos
- **Demo 1 — Pets via `object` → `union Pet(Dog, Cat, Bird)`:** Started with a `List<object>` + non-exhaustive `switch` (with a rogue `Shark`), then introduced a union. Proved: non-member assignment (`Shark`) becomes a **compile error**, **implicit conversions** from case types work, and the `switch` **exhaustiveness warning disappears** once all cases are covered (and **reappears** when a case is commented out, or when a **nullable** case adds `null`). Also showed adding a **computed `Description` member** on the union itself.
- **Demo 2 — `Result<T>` over the wire (discriminated-union style):** Declared `record Success<T>` and `record Error`, glued them with `union Result<T>(Success<T>, Error)`, queued sample results (`Success(42)`, an `Error`), and looped with a `switch` that **deconstructs the record payload**. Proved exhaustiveness nags until **`Error` is handled**, then **ran it live** — printed/used **42** and **threw** on the error.
- **Demo 3 — "Under the hood" hand-authored union:** Commented out the `union` syntax and **rebuilt the equivalent by hand** — a `struct` with **`[Union]`**, the required **`public object value`** auto-property, and **one constructor per case** — watching the compiler errors clear one by one until it was a valid union, plus noting the generated form also implements **`IUnion`**.

## 📊 Notable Stats / Quotes
- **~5 years** of design work to reach "this very simple design."
- **C# 15**, **out in November**; **.NET 11 preview 4** already carries `[Union]` + `IUnion`.
- **"We call it Goldilocks… but you could also call it the compromise version."** — on C#'s union design sitting between TypeScript and functional-language unions.
- **"Cannot implicitly convert type Shark to Pet."** — the error that simultaneously teaches that the *other* types **can** convert into the union.
- **"It's reminding us to deal with the errors, which is what you've always wanted."** — on exhaustiveness forcing error handling.
- **"We're in the business of giving you more errors… and you love us for giving you more errors"** — because it's tighter control over your scenario.
- **"The state of this thing is just the actual dog or cat or bird that's inside"** — rationale for forbidding extra state on a union.
- **"TypeScript has it easy because all the types go away at compile time… but [.NET] types have to mean something at runtime"** — the core reason C# unions are nominal, not structural.
- **"Copilot's going to write that part anyway… as long as you teach it."** — on the more complex non-boxing hand-authored unions.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install the **.NET 11 preview** + Visual Studio preview (or VS Code C# pre-release extension) and write a `union Pet(Dog, Cat, Bird);`, then watch the exhaustiveness warning behaviour (comment out a case; add a nullable case).
  - Build a `Result<T>` / `Option<T>`-style discriminated union with `record` cases and confirm record **deconstruction** in `switch`.
  - Hand-author a **non-boxing** union of two value types (per-type fields + discriminator + `[Union]`) and benchmark allocations vs the default boxed `struct` form.
  - Try retrofitting an existing hand-rolled "union-like" type by adding `[Union]` + the required `value` property/constructors.
- [ ] Questions:
  - What exactly does the compiler emit for **non-boxing usage** (the "different code on usage" they didn't show)? Where is that documented?
  - How do unions interact with **nullable reference type** analysis and **generic constraints** in more complex cases?
  - Is there a planned **`Union<T1, T2>` library/structural layer**, and what's its status in the roslyn proposals?
  - How do unions serialize (System.Text.Json) given they're a `struct` over an `object` field?
- [ ] Relevant to:
  - C#/.NET codebases modelling **result/error**, **state machines**, parser/AST nodes, or any "one-of-N" domain currently faked with base classes, `object`, or enums + payloads.

## 🔗 Related
- [[OD806 - NET 11 in depth]] — broader .NET 11 release context that ships the union-supporting APIs (`[Union]`, `IUnion`).
- [[Pattern matching in C#]] — unions plug directly into `switch`/pattern matching and add exhaustiveness checking.
- [[Records in C#]] — the recommended case type for discriminated unions; enables payload deconstruction.
- [[C# language design]] — the "feature built on a compiler-recognised pattern/attribute" philosophy behind unions.
- [[Discriminated unions]] — functional-language concept C#'s Scenario 2 emulates.
- [[TypeScript union types]] — the structural-union comparison the team drew (and rejected for runtime reasons).
- Source list: [[2026 Build Session List]]
