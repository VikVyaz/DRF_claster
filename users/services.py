import stripe
from decouple import config

from materials.models import Course, Lesson

stripe.api_key = config('STRIPE_API_KEY')


def create_stripe_product(product: Course or Lesson):
    if isinstance(product, Course):
        product_type = 'course'
    elif isinstance(product, Lesson):
        product_type = 'lesson'
    else:
        raise AttributeError('Нужен объект Course или Lesson')

    name = product.name
    description = product.description
    product_id = product.pk

    prod = stripe.Product.create(
        name=name,
        metadata={
            'product_type': product_type,
            'product_id': product_id
        },
        description=description
    )

    return prod


def create_stripe_price(amount, name):
    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount,
        recurring={"interval": "month"},
        product_data={"name": name}
    )
    return price


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="subscription",
    )
    return session.get('id'), session.get('url')
