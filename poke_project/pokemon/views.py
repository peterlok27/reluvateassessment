from django.shortcuts import render
from pokemon.models import Pokemon
from pokemon.serializers import PokemonSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
"""
1. pokemon/unownedpokemon/ - a GET request here should return a serialised list of
all the pokemon that the user does not currently own
2. pokemon/mypokemon/ - a GET request here should return a serialised list of the
pokemon owned by the user
3. pokemon/allpokemon/ - a GET request here should return a serialised list of all
pokemon in the dataset
4. pokemon/addpokemon/ - a POST request here should add a pokemon to the user’s
collection
5. pokemon/releasepokemon/ - a POST request here should allow a user to discard
one of his pokemons in his collection
"""

class PokemonList(APIView): # Endpoint number 3 
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        Pokemons = Pokemon.objects.all()
        serializer = PokemonSerializer(Pokemons, many=True)
        return Response(serializer.data)

class UnownedPokemon(APIView): #This is assuming that the list is consisting of all pokemons even if they are owned by other users. Endpoint number 1
    def get(self,request, format = None):
        user = request.user
        Pokemons = Pokemon.objects.exclude(owner = user)
        serializer = PokemonSerializer(Pokemons, many=True)
        return Response(serializer.data)
        
class OwnedPokemon(APIView): # Endpoint number 2
    def get(self,request, format = None):
        user = request.user
        Pokemons = Pokemon.objects.filter(owner = user)
        serializer = PokemonSerializer(Pokemons, many=True)
        return Response(serializer.data)

class AddPokemon(APIView): #Endpoint number 4
    def get_object(self, pk):
        try:
            return Pokemon.objects.get(pk=pk)
        except Pokemon.DoesNotExist:
            raise Http404

    def post(self,request,pk,format=None):
        user = request.user
        Pokemon = self.get_object(pk)
        serializer = PokemonSerializer(Pokemon, data={'owner': user}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReleasePokemon(APIView): #Endpoint number 5
    def get_object(self, pk):
        try:
            return Pokemon.objects.get(pk=pk)
        except Pokemon.DoesNotExist:
            raise Http404

    def post(self,request,pk,format=None):
        Pokemon = self.get_object(pk)

        serializer = PokemonSerializer(Pokemon, data= {'owner': None} , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


