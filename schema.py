import graphene
from graphene import Field, List, String, Float, Int, Mutation
from models import BakeryItem, db  # Import the BakeryItem model and db session

# BakeryItemType defines the fields for the BakeryItem object in GraphQL
class BakeryItemType(graphene.ObjectType):
    id = Int()
    name = String()
    price = Float()
    quantity = Int()
    category = String()

# Query class for fetching bakery products
class Query(graphene.ObjectType):
    products = List(BakeryItemType)

    def resolve_products(self, info):
        # Query all products from the database
        return BakeryItem.query.all()

# Mutation to add a product
class AddProduct(Mutation):
    class Arguments:
        name = String(required=True)
        price = Float(required=True)
        quantity = Int(required=True)
        category = String(required=True)

    product = Field(lambda: BakeryItemType)

    def mutate(self, info, name, price, quantity, category):
        # Create a new product and save it to the database
        new_product = BakeryItem(name=name, price=price, quantity=quantity, category=category)
        db.session.add(new_product)
        db.session.commit()
        return AddProduct(product=new_product)

# Mutation to update a product
class UpdateProduct(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String(required=False)
        price = Float(required=False)
        quantity = Int(required=False)
        category = String(required=False)

    product = Field(lambda: BakeryItemType)

    def mutate(self, info, id, name=None, price=None, quantity=None, category=None):
        # Find the product in the database
        product = BakeryItem.query.get(id)
        if not product:
            raise Exception("Product not found")
        
        # Update fields if new values are provided
        if name:
            product.name = name
        if price:
            product.price = price
        if quantity:
            product.quantity = quantity
        if category:
            product.category = category
        
        # Commit the updated product to the database
        db.session.commit()
        return UpdateProduct(product=product)

# Mutation to delete a product
class DeleteProduct(Mutation):
    class Arguments:
        id = Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        # Find and delete the product from the database
        product = BakeryItem.query.get(id)
        if not product:
            return DeleteProduct(success=False)
        
        db.session.delete(product)
        db.session.commit()
        return DeleteProduct(success=True)

# Mutation class to wrap all mutations
class Mutation(graphene.ObjectType):
    add_product = AddProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

# Schema definition with query and mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
