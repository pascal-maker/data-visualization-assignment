class Product {
  constructor(name, basePrice, discountRate = 0, taxRate = 0) {
    this.name = name;
    this.basePrice = basePrice;
    this.discountRate = discountRate;
    this.taxRate = taxRate;
  }

  calculatePrice() {
    const priceWithDiscount = this.basePrice - this.getDiscount();
    return priceWithDiscount + this.getTax(priceWithDiscount);
  }

  getDiscount() {
    return this.basePrice * this.discountRate;
  }

  getTax(priceAfterDiscount) {
    return priceAfterDiscount * this.taxRate;
  }
}

module.exports = Product;
