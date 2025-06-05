from app.repositories.shopping_cart_repository import ShoppingCartRepository


class ShoppingCartService:
    @staticmethod
    def get_user_cart(user_id):
        return ShoppingCartRepository.get_cart_by_user_id(user_id)

    @staticmethod
    def get_cart_items(user_id):
        return ShoppingCartRepository.get_cart_items(user_id)

    @staticmethod
    def add_book_to_cart(user_id, book_id):
        return ShoppingCartRepository.add_to_cart(user_id, book_id)

    @staticmethod
    def remove_from_cart(user_id, book_id):
        return ShoppingCartRepository.remove_from_cart(user_id, book_id)

    @staticmethod
    def clear_cart(user_id):
        items = ShoppingCartRepository.get_cart_items(user_id)
        for item in items:
            ShoppingCartRepository.remove_from_cart(user_id, item.book_id)
