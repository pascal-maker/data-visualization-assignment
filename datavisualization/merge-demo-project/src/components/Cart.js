const Product = require('./Product');

class Cart {//this is a comment
  constructor() {//constructor of the class
    this.items = [];//array to store items
  }

  addItem(product) {//adding product to the cart
    this.items.push(product);//adding product to the cart
  }

  getItems() {//returning all items in the cart
    return this.items;//returning all items in the cart
  }
}

module.exports = Cart;//exporting the cart class
