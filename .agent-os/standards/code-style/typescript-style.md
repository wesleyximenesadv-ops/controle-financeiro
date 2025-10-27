# 📘 TypeScript Style Guide & Best Practices

A practical guide for writing **clean, consistent, and type-safe TypeScript code**.  
This document serves as a reference for teams and individuals aiming to follow best practices in their projects.

---

## 📑 Table of Contents
1. [General Principles](#-general-principles)  
2. [Project Structure](#-project-structure)  
3. [Naming Conventions](#-naming-conventions)  
4. [Types vs Interfaces](#-types-vs-interfaces)  
5. [Type Safety](#-type-safety)  
6. [Functions](#-functions)  
7. [Classes & Object-Oriented Programming](#-classes--oop)  
8. [Error Handling](#-error-handling)  
9. [Testing](#-testing)  
10. [Performance & Clean Code](#-performance--clean-code)  
11. [Recommended Tools](#-recommended-tools)  
12. [References](#-references)  

---

## ✨ General Principles
- Prefer **clarity over cleverness**.  
- Code should be **self-documenting** — readable without excessive comments.  
- Keep a **consistent style** across the codebase.  
- Follow the **DRY principle** (Don’t Repeat Yourself).  

---

## 📦 Project Structure
- Place source code inside a `src/` directory.  
- Place tests inside `tests/` or next to related files (`User.test.ts`).  
- Use **barrel files** (`index.ts`) sparingly — only when they simplify imports.  
- Keep modules cohesive:  
  ```
  src/
    models/
      User.ts
    services/
      UserService.ts
    utils/
      formatDate.ts
  ```

---

## 📝 Naming Conventions
- **Types & Interfaces:** `PascalCase`  
  ```ts
  interface UserProfile { ... }
  type UserId = string;
  ```
- **Variables & Functions:** `camelCase`  
  ```ts
  const isActive: boolean = true;
  function getUserName(id: UserId): string { ... }
  ```
- **Constants & Enums:** `UPPER_SNAKE_CASE`  
  ```ts
  const API_URL = "https://api.example.com";

  enum UserRole {
    Admin,
    Editor,
    Viewer,
  }
  ```

---

## ✅ Types vs Interfaces
- Use `type` for **primitives, unions, and mapped types**.  
- Use `interface` for **objects meant to be extended**.  

```ts
type ID = string | number;

interface User {
  id: ID;
  name: string;
}
```

---

## 🛡️ Type Safety
- Always **prefer explicit types** over `any`.  
- Use `unknown` instead of `any` when type is not known.  
- Use `as const` to infer literal types.  

```ts
const roles = ["admin", "editor", "viewer"] as const;
type Role = (typeof roles)[number];
```

---

## ⚡ Functions
- Always type **parameters and return values**.  
- Use arrow functions for callbacks.  

```ts
function add(a: number, b: number): number {
  return a + b;
}

const numbers = [1, 2, 3].map((n): string => n.toString());
```

---

## 🧩 Classes & OOP
- Explicitly declare `private`, `protected`, and `public`.  
- Prefer **composition over inheritance**.  

```ts
class User {
  constructor(private id: string, public name: string) {}

  get displayName(): string {
    return `${this.name} (${this.id})`;
  }
}
```

---

## ⚙️ Error Handling
- Always throw **Error objects**, not strings.  
- Narrow error types when possible.  

```ts
try {
  throw new Error("Something went wrong");
} catch (error) {
  if (error instanceof Error) {
    console.error(error.message);
  }
}
```

---

## 🧪 Testing
- Use **type-safe test utilities**.  
- Avoid `any` in tests — it hides potential issues.  
- Organize tests close to the code they validate.  

```ts
import { getUserName } from "./UserService";

test("returns the correct user name", () => {
  expect(getUserName("123")).toBe("Alice");
});
```

---

## 🚀 Performance & Clean Code
- Avoid unnecessary object/array copies.  
- Use `readonly` to prevent accidental mutations.  
- Use `async/await` instead of raw Promises.  

```ts
async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/users/${id}`);
  return res.json();
}
```

---

## 📚 Recommended Tools
- **ESLint** + **Prettier** → enforce formatting & linting.  
- Enable **strict mode** in `tsconfig.json`:  
  ```json
  {
    "compilerOptions": {
      "strict": true,
      "noImplicitAny": true,
      "strictNullChecks": true
    }
  }
  ```
- **Jest** or **Vitest** for testing.  
- **TypeDoc** for auto-generating documentation.  

---

## 🔗 References
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)  
- [TSConfig Reference](https://www.typescriptlang.org/tsconfig)  
- [Effective TypeScript (book)](https://effectivetypescript.com/)  

---