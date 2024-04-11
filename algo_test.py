class Trader:
    def __init__(self, loss_threshold):
        self.loss_threshold = loss_threshold

    def run(self, state: TradingState):
        result = {}
        for product, order_depth in state.order_depths.items():
            try:
                orders = []
                best_ask = min(order_depth.sell_orders, default=None)
                best_bid = max(order_depth.buy_orders, default=None)
                
                if best_ask is not None and best_bid is not None:
                    mid_price = (order_depth.sell_orders[best_ask] + order_depth.buy_orders[best_bid]) / 2
                    spread = best_ask - best_bid
                    acceptable_price_buy = mid_price - spread * 0.05
                    acceptable_price_sell = mid_price + spread * 0.05

                    # Debugging output
                    print(f'Product: {product}, Best Ask: {best_ask}, Best Bid: {best_bid}, Mid Price: {mid_price}')

                    best_ask_amount = order_depth.sell_orders[best_ask]
                    best_bid_amount = order_depth.buy_orders[best_bid]

                    if best_ask < acceptable_price_buy:
                        estimated_loss = (acceptable_price_buy - best_ask) * best_ask_amount
                        if estimated_loss > self.loss_threshold:
                            orders.append(Order(product, best_ask, -best_ask_amount))

                    if best_bid > acceptable_price_sell:
                        estimated_gain = (best_bid - acceptable_price_sell) * best_bid_amount
                        if estimated_gain > self.loss_threshold:
                            orders.append(Order(product, best_bid, -best_bid_amount))
                
                result[product] = orders

            except Exception as e:
                print(f'Error processing product {product}: {str(e)}')

        return result

