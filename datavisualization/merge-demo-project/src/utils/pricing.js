export const calculateTotal = (items) => {
  return items.reduce((sum, item) => {
    const itemPrice = item.calculatePrice();
    return sum + itemPrice;
  }, 0);
};
