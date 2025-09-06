
from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def view_products(self):
        print("Viewing products")
        collection_id = random.randint(1, 5)
        self.client.get(
            f"/store/products?collection_id={collection_id}",
            name="/store/products")

    
    @task(4)
    def view_product_detail(self):
        print("Viewing product detail")
        product_id = random.randint(1, 1000)
        self.client.get(
            f"/store/products/{product_id}",
            name="/store/products/:id") 
        
    @task(1)
    def add_to_cart(self):
        print("Adding to cart")
        product_id = random.randint(1, 10)
        self.client.post(
            f"/store/carts/{self.cart_id}/items/",
            json={"product_id": product_id, "quantity": 1},
            name="/store/carts/add")
        

    def on_start(self):
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']

    @task
    def say_hello(self):
        self.client.get("/playground/hello/")
