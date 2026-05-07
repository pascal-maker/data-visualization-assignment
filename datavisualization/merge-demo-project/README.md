# Merge Conflict Demo — Advanced E-commerce Challenge

A multi-file merge conflict scenario simulating two parallel feature teams working on an e-commerce application.

## Repositories

| Repo | Description |
|------|-------------|
| [merge-demo](https://github.com/pascal-maker/merge-demo) | Basic example — HTML/CSS color conflict |
| [merge-demo-project](https://github.com/pascal-maker/merge-demo-project) | Advanced challenge — multi-file e-commerce conflict |

## Repository Structure

```
project/
  └── src/
      ├── components/
      │   ├── Product.js
      │   └── Cart.js
      └── utils/
          └── pricing.js
```

## Branches

| Branch | Description |
|--------|-------------|
| `main` | Final resolved state — discount and tax combined |
| `feature-discount` | Team A — implemented discount system |
| `feature-tax` | Team B — implemented tax calculation system |

## What This Demonstrates

### The Scenario

Two teams developed features in parallel, both modifying `Product.js` and `pricing.js`:

- **Team A (`feature-discount`)** — added `getDiscount()` and updated `calculatePrice()` to subtract a discount
- **Team B (`feature-tax`)** — added `getTax()` and updated `calculatePrice()` to add tax

### How the Conflicts Were Created

1. **Initial commit on `main`** — base `Product` class with no pricing logic
2. **`feature-discount`** branched from `main`, implemented discount
3. **`feature-tax`** branched from `main`, implemented tax
4. `feature-discount` merged into `main` cleanly (fast-forward)
5. Merging `feature-tax` into `main` caused conflicts in both files

### Conflicting Files

**`src/components/Product.js`** — both branches redefined `calculatePrice()` and the constructor differently.

**`src/utils/pricing.js`** — both branches changed how `calculateTotal()` computes item prices.

### How the Conflicts Were Resolved

Both features were combined with correct business logic — **discount applied first, then tax on the discounted price**:

```js
// Product.js
calculatePrice() {
  const priceWithDiscount = this.basePrice - this.getDiscount();
  return priceWithDiscount + this.getTax(priceWithDiscount);
}
```

```js
// pricing.js
export const calculateTotal = (items) => {
  return items.reduce((sum, item) => {
    const itemPrice = item.calculatePrice();
    return sum + itemPrice;
  }, 0);
};
```

## Key Takeaways

- Conflicts across **multiple files** require understanding how changes relate to each other
- Resolution sometimes means **combining both sides** rather than just picking one
- **Business logic matters** — discount before tax is standard practice and must be preserved
- Complex merges should be documented to explain the reasoning behind resolution choices
