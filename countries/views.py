from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.authentication import BasicAuthentication 
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth.mixins import LoginRequiredMixin

from countries.models import Countries
from countries.serializers import CountriesSerializer
from rest_framework.decorators import api_view, authentication_classes , permission_classes

@api_view(['GET','POST',])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def countries_list(request):
    if request.method == 'GET':

        # if request.user.IsAuthenticated:
        user = request.user
        country = Countries.objects.filter(user = user)

        # countries = Countries.objects.all()
        # name = request.GET.get('name',None)
        # if name is not None:
        #     countries = countries.filter(name__icontains=name)

        

        countries_serializer = CountriesSerializer(country,many=True)
        return JsonResponse(countries_serializer.data,safe=False)

    elif request.method == 'POST':
        countries = Countries.objects.all()

        countries_data = JSONParser().parse(request)

        countries_serializer = CountriesSerializer(data=countries_data)

        if Countries.objects.filter(name=countries_data.get("name")).values():
            return JsonResponse({'message':'The country is already exist'},status=status.HTTP_400_BAD_REQUEST)
        # print(arr)
        # print(countries_data.get("name"))

        else:
            if countries_serializer.is_valid():
                countries_serializer.save()
                return JsonResponse(countries_serializer.data,status=status.HTTP_201_CREATED)
            return JsonResponse(countries_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE','PATCH'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def countries_details(request,pk):
    try:
        countries = Countries.objects.get(pk=pk)
    except Countries.DoesNotExist:
        return JsonResponse({'message':'The country does not exist'},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        countries_serializer = CountriesSerializer(countries)
        return JsonResponse(countries_serializer.data)

    elif request.method == 'PUT':
        countries_data = JSONParser().parse(request)
        countries_serializer = CountriesSerializer(countries,data=countries_data)
        if countries_serializer.is_valid():
            countries_serializer.save()
            return JsonResponse(countries_serializer.data)
        return JsonResponse(countries_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        countries_data = JSONParser().parse(request)
        countries_serializer = CountriesSerializer(countries,data=countries_data)
        if countries_serializer.is_valid():
            countries_serializer.save()
            return JsonResponse(countries_serializer.data)
        return JsonResponse(countries_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        countries.delete()
        return JsonResponse({'message':'Country was deleted successfully!'},status=status.HTTP_204_NO_CONTENT)
