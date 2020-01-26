import csv
import os
import json
from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from rest_framework.views import APIView
from rest_framework import generics,serializers,mixins, permissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from blueprints import get_data
import pandas as pd
from .filters.filter import *
from datetime import datetime


@api_view(['GET', 'POST'])
def person_api(request):
    if request.method == 'GET':
        qs = Person.objects.all()
        serializer = PersonSerializer(qs, many=True)
        return Response({'data':serializer.data})
    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_data_api(request):
       try:
            data = request.data
            data = json.dumps(data)
            data = json.loads(data)
            print(data)
            if data['data']['tagValue'] == 'Hit Squad':
                print(data['data']['tagValue'].lower())
                df = pd.DataFrame(get_data(data['data']['tagValue'].lower()))
                columns = ['Space Name', 'Blueprint Name', 'Milestone Name', 'Activity', 'Color', 'Tech Solution Type', 'On Shore', 'Off Shore', 'Monthly Volume', 'Cycle Time', 'Participant Name', 'Milestone Number', 'Activity Number']
                df.columns = columns
                if data["data"]['cycleTimeMin'] != ''  and data["data"]['cycleTimeMax'] != '':
                    df = cycle_time_filter(df,data["data"]['cycleTimeMin'],data["data"]['cycleTimeMax'])
              #  if data["data"]['volumeMin'] != ''  and data["data"]['volumeMax'] != '':
               #     df = volume_month_filter(df,data["data"]['volumeMin'],data["data"]['volumeMax'])
                if data['data']['onshoreResourcesMin'] != '' and  data['data']['onshoreResourcesMax'] != '':
                    df = onshore_filter(df,data['data']['onshoreResourcesMin'],data['data']['onshoreResourcesMax'])
                if data['data']['offshoreResourcesMin'] != '' and  data['data']['offshoreResourcesMax'] != '':
                    df = onshore_filter(df,data['data']['offshoreResourcesMin'],data['data']['offshoreResourcesMax'])
                if data['data']['color'] != '':
                    df = color_filter(df,data['data']['color'])
                if data['data']['techSolutionType'] != '':
                    df = tech_solution_filter(df,data['data']['Tech Solution Type'])
                if data['data']['participant'] != '':
                    df = participant_filter(df,data['data']['participant'])
                df.to_csv('media/'+data['data']['tagValue']+'|'+datetime.now().strftime("%m-%d-%Y_%H:%M:%S")+'.csv')
                print('Working')
            if data['data']['tagValue'] == 'Risk Project':
                print(data['data']['tagValue'].lower())
                df = pd.DataFrame(get_data(data['data']['tagValue'].lower()))
                df.to_csv('media/'+data['data']['tagValue']+'|'+datetime.now().strftime("%m-%d-%Y_%H:%M:%S")+'.csv')
                
            if data['data']['tagValue'] == 'Customer Care':
                df = pd.DataFrame(get_data(data['data']['tagValue'].lower()))
                df.to_csv('media/'+data['data']['tagValue']+'|'+datetime.now().strftime("%m-%d-%Y_%H:%M:%S")+'.csv')
                    
            return Response('success', status=status.HTTP_201_CREATED)
       except Exception as e:
           print(e)
           return Response('error', status=status.HTTP_400_BAD_REQUEST)
           
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def make_csv(request):
    df = pd.DataFrame(get_data())
    columns = ['Space Name', 'Blueprint Name', 'Milestone Name', 'Activity', 'Color', 'Tech Solution Type', 'On Shore', 'Off Shore', 'Monthly Volume', 'Cycle Time', 'Participant Name', 'Milestone Number', 'Activity Number']
    #df.columns = columns
    #df = cycle_time_filter(df,5)
    df.to_csv('media/dd.csv')
    return Response('success', status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_file(request):
    files = os.listdir("media")
    return Response({'files':files}, status=status.HTTP_201_CREATED)

