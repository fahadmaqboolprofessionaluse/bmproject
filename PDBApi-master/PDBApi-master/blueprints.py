import csv
import os
import requests
import urllib.request
import json
import sys
from pprint import pprint
import re

ignored_sns = ['Servicing', 'Business Process Design']
Blueworks_User = 'bilalmumraiz25@gmail.com'
Blueworks_Password = 'Cavalier_77'
activity_number = 0
milestone_number = 0

def extract_value(prop_name, prop, default=0):
    onr = prop.get(prop_name) 
    if onr:
        return onr[0].get('value',default)
    return default

def extract_value_tst(prop_name, prop, default=0):
    tstvalue = prop.get(prop_name) 
    if tstvalue:
        tstresult=''
        for tstype in tstvalue:
            print (tstype)
            if not tstresult =='':
                tstresult += '|'
            tstresult += tstype.get('name',default)
        return tstresult
    return default

def extract_value_vol(prop_name, prop, default=0):
    volvalue = prop.get(prop_name)
    if volvalue:
        return volvalue[0].get('name',default)
    return default

def extract_cycle_time(prop_name, prop, default=0):
    cyclevalue = prop.get(prop_name)
    if cyclevalue:
        cycletime_numeric = cyclevalue[0].get('value',default)
        
        if cycletime_numeric.startswith ('PT'):
            cycletime_numeric = cycletime_numeric[2:]
            if cycletime_numeric.endswith('M'):
                cycletime_numeric = cycletime_numeric[:-1]+" Minutes"

        if cycletime_numeric.startswith ('P'):
            cycletime_numeric = cycletime_numeric[1:]
            if cycletime_numeric.endswith('M'):
                cycletime_numeric = cycletime_numeric[:-1]+" Months"
        return cycletime_numeric
    return default 

def extract_participant_name(prop_name, prop, default=0):
    participantvalue = prop.get(prop_name)
    if participantvalue:
        return participantvalue[0].get('name',default)
    return default

def count_on_and_offshore(properties):
    onshore = 0
    offshore = 0
    tst = ''
    volume_month = ''
    cycle_time = ''
    participant_name = ''

    for prop in properties:
        onshore += float(extract_value('Onshore Resources', prop))
        offshore += float(extract_value('Offshore Resources', prop))
        tst += extract_value_tst('Tech Solution Type', prop, '')
        volume_month += extract_value_vol('Volume/Mo', prop, '')
        cycle_time += extract_cycle_time('cycle-work-time', prop, '')
        participant_name += extract_participant_name('participants', prop, '')
    return onshore, offshore, tst, volume_month, cycle_time, participant_name

def get_data(type):
    # Pass Log On Credentials Onto xxx Live and select Blueprints tagged with "Hit Squad" 
    response = requests.get('https://us001.blueworkslive.com/bwl/blueprints?tag="{0}"'.format(type), auth=(Blueworks_User, Blueworks_Password))

    # Load Responses for a given Blueprint tagged with "Hit Squad" from BWL into object called "data" in JSON format 
    data=json.loads(response.text)

    #For Each Blueprint found, select a specific Blueprint ID
    for d in data:
        response = requests.get('https://us001.blueworkslive.com/bwl/blueprints/'+d['id'], auth=(Blueworks_User, Blueworks_Password))
        
        data1=json.loads(response.text)

    # for each Milestone, select an Activity colored "Yellow" and find Participant "Name"
        
        save_milestone = 0
        milestone_number = 0
        activity_number = 0

        for milestone in data1['milestones']:
            save_milestone +=milestone_number
            milestone_number = milestone_number +1
            activity_number = milestone_number 
            
            for activity in milestone['activities']:
                
                if 'type' in activity and activity['type']!='activity':
                    continue
                if 'properties' in activity: 

                    # If the activity is a Subprocess, check sub-activity
                    if 'sub-type' in activity and activity ['sub-type'] == 'subprocess':
                        for sub_activity in activity['activities']:
                            if 'type' in sub_activity and sub_activity['type'] !='activity':
                                continue

                            if save_milestone == milestone_number:
                                activity_number = activity_number +.01
                            else:
                                activity_number = milestone_number+(activity_number-int(activity_number)) +.01
                        
                            onshore_count, offshore_count, tst, volume_month, cycle_time, participant_name = count_on_and_offshore(sub_activity['properties'])
                            
                            yield (
                                ", ".join([sn for sn in data1.get('space-names') if sn not in ignored_sns]),

                                data1.get('name', 'NOBPNAME'), 
                                milestone.get('name'), 
                                sub_activity.get('name', 'NONAME'), 
                                sub_activity.get('color'),
                                tst,
                                onshore_count, 
                                offshore_count,
                                volume_month,
                                cycle_time,
                                participant_name, 
                                milestone_number,
                                activity_number,
                                )
                    else:
                        if save_milestone == milestone_number:
                            activity_number = activity_number +.01
                        else:
                            activity_number = milestone_number+(activity_number-int(activity_number)) +.01

                        onshore_count, offshore_count, tst, volume_month, cycle_time, participant_name = count_on_and_offshore(activity['properties'])
                    
                        yield (
                        ", ".join([sn for sn in data1.get('space-names') if sn not in ignored_sns]),

                        data1.get('name', 'NOBPNAME'), 
                        milestone.get('name'), 
                        activity.get('name', 'NONAME'), 
                        activity.get('color'),
                        tst,
                        onshore_count, 
                        offshore_count,
                        volume_month,
                        cycle_time,
                        participant_name,
                        milestone_number,
                        activity_number,
                            )
                            
