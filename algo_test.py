from datamodel import OrderDepth, UserId, TradingState, Order
from typing import Dict, List

class Trader:
    def __init__(self):
        self.position_limits = {
            "STARFRUIT": 20,
            "AMETHYSTS": 20,
            "ORCHIDS": 100
        }
        self.positions = {key: 0 for key in self.position_limits}
    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        for product, order_depth in state.order_depths.items():
            orders = self.decide_orders(product, order_depth)
            result[product] = orders
        return result

    def decide_orders(self, product: str, order_depth: OrderDepth) -> List[Order]:
        orders = []
        # Basic market making strategy for AMETHYSTS
        if product == "AMETHYSTS":
            midpoint = (order_depth.sell_orders[0][0] + order_depth.buy_orders[0][0]) / 2
            spread = 0.05 * midpoint
            buy_price = midpoint - spread
            sell_price = midpoint + spread
            if self.positions[product] < self.position_limits[product]:
                orders.append(Order(product, buy_price, 1))  # Buy 1 unit
            if self.positions[product] > -self.position_limits[product]:
                orders.append(Order(product, sell_price, -1))  # Sell 1 unit
        
        # Momentum trading strategy for STARFRUIT
        elif product == "STARFRUIT":
            if len(order_depth.sell_orders) > 0 and len(order_depth.buy_orders) > 0:
                if order_depth.sell_orders[0][0] < order_depth.buy_orders[0][0]:
                    # Buy if the sell price is unexpectedly low
                    orders.append(Order(product, order_depth.sell_orders[0][0], 1))
                elif order_depth.sell_orders[0][0] > order_depth.buy_orders[0][0]:
                    # Sell if the buy price is unexpectedly high
                    orders.append(Order(product, order_depth.buy_orders[0][0], -1))

        # Factor-based strategy for ORCHIDS (simplified)
        elif product == "ORCHIDS":
            # Placeholder for complexity: react to external data
            buy_price = min(order.price for order, qty in order_depth.sell_orders)
            sell_price = max(order.price for order, qty in order_depth.buy_orders)
            if self.positions[product] < self.position_limits[product]:
                orders.append(Order(product, buy_price, 2))  # More aggressive buying
            if self.positions[product] > -self.position_limits[product]:
                orders.append(Order(product, sell_price, -2))  # More aggressive selling

        return orders

# Usage
# trader = Trader()
# current_state = TradingState(...)  # This should be filled with the actual trading data
# orders_to_place = trader.run(current_state)

