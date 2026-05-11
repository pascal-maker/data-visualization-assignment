class Product {//this is a comment
  constructor(name, basePrice, discountRate = 0, taxRate = 0) {//constructor of the class
    this.name = name;//name of the product
    this.basePrice = basePrice;//base price of the product
    this.discountRate = discountRate;//discount rate of the product
    this.taxRate = taxRate;//tax rate of the product
  }//end of constructor of the class

  calculatePrice() {//calculating the price of the product
    const priceWithDiscount = this.basePrice - this.getDiscount();//calculating the price with discount
    return priceWithDiscount + this.getTax(priceWithDiscount);//returning the price with discount
  }//end of calculating the price of the product

  getDiscount() {//getting the discount of the product
    return this.basePrice * this.discountRate;//returning the discount of the product
  }

  getTax(priceAfterDiscount) {//getting the tax of the product
    return priceAfterDiscount * this.taxRate;//returning the tax of the product
  }
}

module.exports = Product;//exporting the product class
