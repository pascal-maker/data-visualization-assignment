# Merge Conflict Demo — Basic Example

A hands-on demonstration of how Git merge conflicts are created and resolved using a simple HTML/CSS website.

## Repositories

| Repo | Description |
|------|-------------|
| [merge-demo](https://github.com/pascal-maker/merge-demo) | Basic example — HTML/CSS color conflict |
| [merge-demo-project](https://github.com/pascal-maker/merge-demo-project) | Advanced challenge — multi-file e-commerce conflict |

## Repository Structure

```
merge-demo/
  ├── index.html
  └── style.css
```

## Branches

| Branch | Description |
|--------|-------------|
| `main` | Final resolved state — `h1` color is green |
| `feature-branch` | Feature branch — `h1` color was red |

## What This Demonstrates

### How the Conflict Was Created

1. **Initial commit** — both files created with `h1 { color: blue }`
2. **`feature-branch`** — changed `h1` color to `red`
3. **`main`** — changed `h1` color to `green`
4. Merging `feature-branch` into `main` caused a conflict since both branches modified the same line

### What the Conflict Looked Like

```css
h1 {
<<<<<<< HEAD
    color: green;
=======
    color: red;
>>>>>>> feature-branch
    font-size: 24px;
}
```

### How It Was Resolved

The conflict markers were removed and the `main` branch version (green) was kept:

```css
h1 {
    color: green;
    font-size: 24px;
}
```

## Key Takeaways

- Merge conflicts happen when two branches change the **same line** differently
- Git marks conflicts with `<<<<<<<`, `=======`, and `>>>>>>>` markers
- Resolution requires manually choosing which change to keep (or combining both)
- After resolving, stage the file and create a new commit
