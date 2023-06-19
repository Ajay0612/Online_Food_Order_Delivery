class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0


class HybridGraphQueue:
    def __init__(self):
        self.graph = {}
        self.queue = Queue()
        self.num_locations = 0

    def add_edge(self, u, v, weight):
        self.graph.setdefault(u, []).append((v, weight))
        self.graph.setdefault(v, []).append((u, weight))

        self.num_locations = max(self.num_locations, u + 1, v + 1)

    def enqueue(self, vertex):
        self.queue.enqueue(vertex)

    def dequeue(self):
        return self.queue.dequeue()

    def is_queue_empty(self):
        return self.queue.is_empty()

    def get_neighbors(self, vertex):
        return self.graph.get(vertex, [])

    def calculate_shortest_path(self, source):
        distances = [float('inf')] * self.num_locations
        distances[source] = 0

        previous = [None] * self.num_locations

        self.enqueue(source)

        while not self.is_queue_empty():
            current = self.dequeue()

            for neighbor, weight in self.get_neighbors(current):
                distance = distances[current] + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    self.enqueue(neighbor)

        return distances, previous


class FoodDeliverySystem:
    def __init__(self, hybrid_graph_queue, shop_location):
        self.hybrid_graph_queue = hybrid_graph_queue
        self.orders = []
        self.delivery_queue = Queue()
        self.shop_location = shop_location

    def order_food(self):
        print("\n----- Order Food -----")
        customer_name = input("Enter customer name: ")
        customer_address = input("Enter customer address (alphabets only): ")
        food_order = input("Enter food order: ")

        order = {
            "customer_name": customer_name,
            "customer_address": customer_address,
            "food_order": food_order,
            "delivered": False  # check if the order has been delivered
        }

        self.orders.append(order)
        self.delivery_queue.enqueue(len(self.orders) - 1)
        print("Order placed successfully! Order ID: {}".format(len(self.orders)))

    def view_order(self):
        print("\n----- View Order -----")
        order_id = int(input("Enter order ID: ")) - 1

        if 0 <= order_id < len(self.orders):
            order = self.orders[order_id]
            print("Customer Name: {}".format(order["customer_name"]))
            print("Customer Address: {}".format(order["customer_address"]))
            print("Food Order: {}".format(order["food_order"]))
            if order["delivered"]:
                print("Order Status: Delivered")
            else:
                print("Order Status: Not Delivered")
        else:
            print("Invalid order ID.")

    def change_order(self):
        print("\n----- Change Order -----")
        order_id = int(input("Enter order ID: ")) - 1

        if 0 <= order_id < len(self.orders):
            if self.orders[order_id]["delivered"]:
                print("Cannot change a delivered order.")
            else:
                new_food_order = input("Enter new food order: ")
                self.orders[order_id]["food_order"] = new_food_order
                print("Order updated successfully.")
        else:
            print("Invalid order ID.")

    def cancel_order(self):
        print("\n----- Cancel Order -----")
        order_id = int(input("Enter order ID: ")) - 1

        if 0 <= order_id < len(self.orders):
            if self.orders[order_id]["delivered"]:
                print("Cannot cancel a delivered order.")
            else:
                self.orders.pop(order_id)
                self.update_delivery_queue()
                print("Order cancelled successfully.")
        else:
            print("Invalid order ID.")

    def update_delivery_queue(self):
        new_delivery_queue = Queue()
        for order_id in self.delivery_queue.items:
            if 0 <= order_id < len(self.orders):
                new_delivery_queue.enqueue(order_id)
        self.delivery_queue = new_delivery_queue

    def deliver_orders(self):
        print("\n----- Deliver Orders -----")
        if self.delivery_queue.is_empty():
            print("No orders to deliver.")
        else:
            while not self.delivery_queue.is_empty():
                order_id = self.delivery_queue.dequeue()
                if 0 <= order_id < len(self.orders):
                    order = self.orders[order_id]
                    if order["delivered"]:
                        continue  # skip the delivered order
                    customer_address = order["customer_address"]
                    customer_location = ord(customer_address) - ord('A')

                    distances, previous = self.hybrid_graph_queue.calculate_shortest_path(self.shop_location)

                    if distances[customer_location] != float('inf'):
                        path = construct_path(previous, customer_location)

                        print("Delivering food to customer {} at {} (distance: {})".format(
                            order["customer_name"], customer_address, distances[customer_location]))
                        print("Delivery path:", "->".join(path))

                        order["delivered"] = True  # mark the order as delivered
                    else:
                        print("Unable to deliver food to customer {} at {}.".format(
                            order["customer_name"], customer_address))
                        print("No path found.")
                else:
                    print("Invalid order ID.")

    def run(self):
        print("----- Food Delivery System -----")
        while True:
            print("--------------------------------")
            print("Enter the number of locations in the city ")
            num_locations = int(input())

            if num_locations == 1:
                print("Delivery is not possible as there is only 1 location (the shop).")
                print("Please enter the number of locations again ")
                continue
            if num_locations < 1:
                print("Invalid number of locations. Please enter a value greater than 1.")
                continue

            adjacency_matrix = []

            for i in range(num_locations):
                print("Enter the distances from location {} to all other locations: ".format(chr(ord('A') + i)))
                row = list(map(int, input().split()))
                adjacency_matrix.append(row)

            self.hybrid_graph_queue = HybridGraphQueue()

            for i in range(num_locations):
                for j in range(num_locations):
                    if adjacency_matrix[i][j] > 0:
                        self.hybrid_graph_queue.add_edge(i, j, adjacency_matrix[i][j])

            shop_location = ord(input("Enter the location of the food shop (A, B, C, ...): ")) - ord('A')
            self.shop_location = shop_location

            break

        while True:
            print("\n---- Food Delivery System Menu ----")
            print("1. Order Food")
            print("2. View Order")
            print("3. Change Order")
            print("4. Cancel Order")
            print("5. Deliver Orders")
            print("6. Exit")

            choice = int(input("Enter your choice (1-6): "))

            if choice == 1:
                self.order_food()
            elif choice == 2:
                self.view_order()
            elif choice == 3:
                self.change_order()
            elif choice == 4:
                self.cancel_order()
            elif choice == 5:
                self.deliver_orders()
            elif choice == 6:
                print("Exiting...")
                print("\n---- Thank you for using our Food Delivery ----")
                break
            else:
                print("Invalid choice. Please try again.")


def construct_path(previous, current):
    path = []
    while current is not None:
        path.insert(0, chr(ord('A') + current))
        current = previous[current]
    return path


def main():
    delivery_system = FoodDeliverySystem(HybridGraphQueue(), 0)
    delivery_system.run()


if __name__ == '__main__':
    main()
