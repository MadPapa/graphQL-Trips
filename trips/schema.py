import graphene
from graphene_django import DjangoObjectType
from .models import *

# setting query


class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        fields = '__all__'


class TripType(DjangoObjectType):
    class Meta:
        model = Trip
        fields = '__all__'


class HotelType(DjangoObjectType):
    class Meta:
        model = Hotel
        fields = '__all__'


class Query(graphene.ObjectType):
    client = graphene.Field(ClientType, id=graphene.ID(required=True))
    clients = graphene.List(ClientType)

    trip = graphene.Field(TripType, id=graphene.ID(required=True))
    trips = graphene.List(TripType)

    hotel = graphene.Field(HotelType, id=graphene.ID(required=True))
    hotels = graphene.List(HotelType)

    def resolve_client(root, info, id):
        return Client.objects.get(pk=id)

    def resolve_clients(root, info, **kwargs):
        return Client.objects.all()

    def resolve_trip(root, info, id):
        return Trip.objects.get(pk=id)

    def resolve_trips(root, info, **kwargs):
        return Trip.objects.all()

    def resolve_hotel(root, info, id):
        return Hotel.objects.get(pk=id)

    def resolve_hotels(root, info, **kwargs):
        return Hotel.objects.all()

# setting mutations


class CreateClient(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        surname = graphene.String(required=True)
        pesel = graphene.String(required=True)
        phoneNumber = graphene.String(required=True)

    client = graphene.Field(ClientType)

    @classmethod
    def mutate(cls, root, info, name, surname, pesel, phoneNumber):
        client = Client()
        client.name = name
        client.surname = surname
        client.pesel = pesel
        client.phoneNumber = phoneNumber
        client.save()
        return CreateClient(client=client)


class UpdateClient(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=False)
        surname = graphene.String(required=False)
        pesel = graphene.String(required=False)
        phoneNumber = graphene.String(required=False)

    client = graphene.Field(ClientType)

    @classmethod
    def mutate(cls, root, info, id, name=None, surname=None, pesel=None, phoneNumber=None):
        client = Client.objects.filter(pk=id)
        if client is None:
            raise Exception('Client does not exist.')
        client = Client.objects.get(pk=id)
        if name:
            client.name = name
        if surname:
            client.surname = surname
        if pesel:
            client.pesel = pesel
        if phoneNumber:
            client.phoneNumber = phoneNumber
        client.save()
        return UpdateClient(client=client)


class DeleteClient(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            client = Client.objects.get(pk=id)
            client.delete()
            success = True
        except Client.DoesNotExist:
            success = False

        return DeleteClient(success=success)


class CreateHotel(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        phoneNumber = graphene.String(required=True)
        website = graphene.String(required=True)
        stars = graphene.String(required=False, default_value="1")

    hotel = graphene.Field(HotelType)

    @classmethod
    def mutate(cls, root, info, name, phoneNumber, website, stars):
        hotel = Hotel()
        hotel.name = name
        hotel.phoneNumber = phoneNumber
        hotel.website = website
        hotel.stars = stars
        hotel.save()

        return CreateHotel(hotel=hotel)


class UpdateHotel(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=False)
        phoneNumber = graphene.String(required=False)
        website = graphene.String(required=False)
        stars = graphene.String(required=False)

    hotel = graphene.Field(HotelType)

    @classmethod
    def mutate(cls, root, info, id, name=None, phoneNumber=None, website=None, stars=None):
        hotel = Hotel.objects.filter(pk=id)
        if hotel is None:
            raise Exception('Hotel does not exist.')
        hotel = Hotel.objects.get(pk=id)
        if name:
            hotel.name = name
        if phoneNumber:
            hotel.phoneNumber = phoneNumber
        if website:
            hotel.website = website
        if stars:
            hotel.stars = stars
        hotel.save()
        return UpdateHotel(hotel=hotel)


class DeleteHotel(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            hotel = Hotel.objects.get(pk=id)
            hotel.delete()
            success = True
        except hotel.DoesNotExist:
            success = False

        return DeleteHotel(success=success)


class CreateTrip(graphene.Mutation):
    class Arguments:
        client = graphene.List(graphene.ID)
        hotel = graphene.ID()
        country = graphene.String()
        city = graphene.String()
        price = graphene.Decimal()
        checkinDate = graphene.DateTime()
        checkoutDate = graphene.DateTime()

    trip = graphene.Field(TripType)

    @classmethod
    def mutate(cls, root, info, client, hotel, country, city, price, checkinDate, checkoutDate):
        clients = Client.objects.filter(pk__in=client)
        hotel = Hotel.objects.get(pk=hotel)
        trip = Trip.objects.create(hotel=hotel, country=country, city=city,
                                   price=price, checkinDate=checkinDate, checkoutDate=checkoutDate)
        trip.client.set(clients)
        trip.save()

        return CreateTrip(trip=trip)


class UpdateTrip(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        clients = graphene.List(graphene.ID, required=False)
        hotel = graphene.ID(required=False)
        country = graphene.String(required=False)
        city = graphene.String(required=False)
        price = graphene.Decimal(required=False)
        checkinDate = graphene.DateTime(required=False)
        checkoutDate = graphene.DateTime(required=False)

    trip = graphene.Field(TripType)

    @classmethod
    def mutate(cls, root, info, id, client=None, hotel=None, country=None, city=None, price=None, checkinDate=None, checkoutDate=None):
        trip = Trip.objects.filter(pk=id)
        if trip is None:
            raise Exception('Trip does not exist.')
        trip = Trip.objects.get(pk=id)
        if client:
            clients = Client.objects.filter(pk__in=client)
            trip.client.set(clients)
        if hotel:
            hotel = Hotel.objects.get(pk=hotel)
            trip.hotel = hotel
        if country:
            trip.country = country
        if city:
            trip.city = city
        if price:
            trip.price = price
        if checkinDate:
            trip.checkinDate = checkinDate
        if checkoutDate:
            trip.checkoutDate = checkoutDate
        trip.save()
        return UpdateTrip(trip=trip)


class DeleteTrip(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            trip = Trip.objects.get(pk=id)
            trip.delete()
            success = True
        except trip.DoesNotExist:
            success = False

        return DeleteTrip(success=success)


class Mutation(graphene.ObjectType):
    create_client = CreateClient.Field()
    update_client = UpdateClient.Field()
    delete_client = DeleteClient.Field()

    create_hotel = CreateHotel.Field()
    update_hotel = UpdateHotel.Field()
    delete_hotel = DeleteHotel.Field()

    create_trip = CreateTrip.Field()
    update_trip = UpdateTrip.Field()
    delete_trip = DeleteTrip.Field()


# creating schema constructor
schema = graphene.Schema(query=Query, mutation=Mutation)
