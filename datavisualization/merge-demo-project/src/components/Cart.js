const Product = require('./Product');

class Cart {
  constructor() {
    this.items = [];
  }

  addItem(product) {
    this.items.push(product);
  }

  getItems() {
    return this.items;
  }
}

module.exports = Cart;
