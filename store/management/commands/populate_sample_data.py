from django.core.management.base import BaseCommand
from store.models import Collection, Product


class Command(BaseCommand):
    help = 'Populate sample data for SQLite database'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample collections and products...')
        
        try:
            # Create collections
            electronics, created = Collection.objects.get_or_create(
                title='Electronics',
                defaults={'featured_product': None}
            )
            if created:
                self.stdout.write(f'Created collection: {electronics.title}')
            
            clothing, created = Collection.objects.get_or_create(
                title='Clothing',
                defaults={'featured_product': None}
            )
            if created:
                self.stdout.write(f'Created collection: {clothing.title}')
            
            books, created = Collection.objects.get_or_create(
                title='Books',
                defaults={'featured_product': None}
            )
            if created:
                self.stdout.write(f'Created collection: {books.title}')
            
            # Create sample products
            products_data = [
                {
                    'title': 'Smartphone',
                    'slug': 'smartphone',
                    'description': 'Latest model smartphone',
                    'unit_price': 699.99,
                    'inventory': 50,
                    'collection': electronics
                },
                {
                    'title': 'Laptop',
                    'slug': 'laptop',
                    'description': 'High-performance laptop',
                    'unit_price': 1299.99,
                    'inventory': 25,
                    'collection': electronics
                },
                {
                    'title': 'T-Shirt',
                    'slug': 't-shirt',
                    'description': 'Comfortable cotton t-shirt',
                    'unit_price': 29.99,
                    'inventory': 100,
                    'collection': clothing
                },
                {
                    'title': 'Jeans',
                    'slug': 'jeans',
                    'description': 'Classic blue jeans',
                    'unit_price': 89.99,
                    'inventory': 75,
                    'collection': clothing
                },
                {
                    'title': 'Programming Book',
                    'slug': 'programming-book',
                    'description': 'Learn Python programming',
                    'unit_price': 49.99,
                    'inventory': 30,
                    'collection': books
                }
            ]
            
            for product_data in products_data:
                product, created = Product.objects.get_or_create(
                    slug=product_data['slug'],
                    defaults=product_data
                )
                if created:
                    self.stdout.write(f'Created product: {product.title}')
            
            self.stdout.write(
                self.style.SUCCESS('Successfully populated sample data!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error populating data: {e}')
            )
