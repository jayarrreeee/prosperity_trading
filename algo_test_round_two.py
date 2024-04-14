from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List, Dict
import jsonpickle

class Trader:

    def __init__(self):
        self.position_limits = {'STARFRUIT': 20, 'AMETHYSTS': 20, 'ORCHIDS': 100}

    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        conversions = 0
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            acceptable_price = self.calculate_acceptable_price(product, state.observations, order_depth)
            
            print(f"Acceptable price for {product}: {acceptable_price}")
            print(f"Buy Order depth: {len(order_depth.buy_orders)}, Sell order depth: {len(order_depth.sell_orders)}")
    
            # Handling sell orders
            for price, qty in order_depth.sell_orders.items():
                if price <= acceptable_price:
                    print(f"BUY {abs(qty)}x at {price}")
                    orders.append(Order(product, price, abs(qty)))
    
            # Handling buy orders
            for price, qty in order_depth.buy_orders.items():
                if price >= acceptable_price:
                    print(f"SELL {qty}x at {price}")
                    orders.append(Order(product, price, -qty))
            
            result[product] = orders
            conversions += self.handle_conversions(product, state.observations.get('complexObservations', {}).get(product))
        
        traderData = jsonpickle.encode({'lastRunInfo': result})  # Example of serializing some state information
        return result, conversions, traderData

    def calculate_acceptable_price(self, product: str, observations, order_depth: OrderDepth):
        # Implement dynamic pricing based on historical data and observations
        if product in observations['plainValueObservations']:
            return observations['plainValueObservations'][product]
        else:
            return sum(order_depth.buy_orders.keys() | order_depth.sell_orders.keys()) / len(order_depth.buy_orders | order_depth.sell_orders)

    def handle_conversions(self, product, conversion_observation):
        if conversion_observation:
            return int(conversion_observation.askPrice - conversion_observation.bidPrice)  # Simple example of using price spread
        return 0

# Assuming the datamodel and other classes are properly defined elsewhere
