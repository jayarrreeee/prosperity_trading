import jsonpickle

class Order:
    def __init__(self, symbol, price, quantity):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

class OrderDepth:
    def __init__(self, buy_orders=None, sell_orders=None):
        if buy_orders is None:
            buy_orders = {}
        if sell_orders is None:
            sell_orders = {}
        self.buy_orders = buy_orders
        self.sell_orders = sell_orders

class TradingState:
    def __init__(self, traderData='', order_depths={}, position={}):
        self.traderData = traderData
        self.order_depths = order_depths
        self.position = position

class Trader:
    def __init__(self, position_limits):
        self.position_limits = position_limits  # Dictionary of product position limits

    def run(self, state: TradingState):
        orders_to_place = {}
        for product, depth in state.order_depths.items():
            current_position = state.position.get(product, 0)
            orders = self.decide_orders(product, depth, current_position)
            if orders:
                orders_to_place[product] = orders
        # Other logic and return statement here

    def decide_orders(self, product, depth, current_position):
        # Trading logic to decide on orders
        orders = []
        acceptable_buy_price = max(depth.buy_orders.keys(), default=0) + 0.01
        acceptable_sell_price = min(depth.sell_orders.keys(), default=float('inf')) - 0.01

        if acceptable_buy_price < 10 and current_position < self.position_limits.get(product, 0):
            # Place a buy order
            quantity_to_buy = min(5, self.position_limits[product] - current_position)  # Example fixed quantity
            orders.append(Order(product, acceptable_buy_price, quantity_to_buy))

        if acceptable_sell_price > 10 and current_position > 0:
            # Place a sell order
            quantity_to_sell = min(5, current_position)  # Example fixed quantity
            orders.append(Order(product, acceptable_sell_price, -quantity_to_sell))

        return orders


# Mock data for testing
position_limits = {'STARFRUIT': 20, 'AMETHYSTS': 20, 'ORCHIDS': 100}
trader = Trader(position_limits)

# Simulated order depth for round 1 and 2
order_depths = {
    'STARFRUIT': OrderDepth({8: 10, 9: 15}, {11: -10, 12: -5}),
    'AMETHYSTS': OrderDepth({9: 20}, {13: -10, 14: -20}),
    'ORCHIDS': OrderDepth({5: 30}, {7: -15, 8: -25})
}

# Current positions assuming some previous trades
current_positions = {'STARFRUIT': 10, 'AMETHYSTS': 5, 'ORCHIDS': 50}

state = TradingState(order_depths=order_depths, position=current_positions)
results = trader.run(state)
print(results)
