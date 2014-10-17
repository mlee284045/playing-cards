import factory


class WarGameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.WarGame'


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.Player'
    username = factory.Sequence(lambda i: 'User{}'.format(i))
    # password = factory.PostGenerationMethodCall('set_password', 'password')
    # factory.SubFactory(some_linked_factory)
    # well created factories can populate a database pretty easily
