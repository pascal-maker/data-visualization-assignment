export const calculateTotal = (items) => {//this is a comment
  return items.reduce((sum, item) => {//reducing the items to a single value
    const itemPrice = item.calculatePrice();//calculating the price of each item
    return sum + itemPrice;//returning the total price
  }, 0);//initial value of sum is 0
};
