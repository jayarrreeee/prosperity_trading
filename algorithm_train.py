from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    def __init__(self, loss_threshold):
        self.loss_threshold = loss_threshold  # Initialize the trader with the loss threshold

    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            
            mid_price = (order_depth.sell_orders[min(order_depth.sell_orders.keys())] + 
                         order_depth.buy_orders[max(order_depth.buy_orders.keys())]) / 2
            spread = min(order_depth.sell_orders.keys()) - max(order_depth.buy_orders.keys())
            acceptable_price_buy = mid_price - spread * 0.05
            acceptable_price_sell = mid_price + spread * 0.05
            
            print(f"Acceptable Buy Price : {acceptable_price_buy}")
            print(f"Acceptable Sell Price : {acceptable_price_sell}")
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
    
            if order_depth.sell_orders:
                best_ask = min(order_depth.sell_orders.keys())
                best_ask_amount = order_depth.sell_orders[best_ask]
                estimated_loss = (acceptable_price_buy - best_ask) * best_ask_amount
                if best_ask < acceptable_price_buy and estimated_loss > self.loss_threshold:
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))
    
            if order_depth.buy_orders:
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_amount = order_depth.buy_orders[best_bid]
                estimated_gain = (best_bid - acceptable_price_sell) * best_bid_amount
                if best_bid > acceptable_price_sell and estimated_gain > self.loss_threshold:
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_amount))
            
            result[product] = orders
        return result

# Example initialization and usage
trader_bot = Trader(loss_threshold=-100)  # Set an example threshold

