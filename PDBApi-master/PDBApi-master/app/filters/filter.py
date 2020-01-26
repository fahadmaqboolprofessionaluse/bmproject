import pandas as pd

def cycle_time_filter(df,min,max):
    temp = df['Cycle Time'].map(lambda x: x.rstrip(' Minutes').rstrip('HDW'))
    print(temp)
    df['Cycle Time'] = pd.to_numeric(temp)
    bool_series = df["Cycle Time"].between(min,max,inclusive=True)
    return df[bool_series]

def volume_month_filter(df,min,max):
    df['Monthly Volume'] = pd.to_numeric(df['Monthly Volume'])
    bool_series = df["Monthly Volume"].between(min,max,inclusive=True)
    return df[bool_series]

def onshore_filter(df,min,max):
    df['On Shore'] = pd.to_numeric(df['On Shore'])
    bool_series = df["On Shore"].between(min,max,inclusive=True)
    return df[bool_series]

def offshore_filter(df,min,max):
    df['Off Shore'] = pd.to_numeric(df['Off Shore'])
    bool_series = df["Off Shore"].between(min,max,inclusive=True)
    return bool_series

def color_filter(df,color):
    df = df[df['Color'] == color]
    return df

def milestone_filter(df,name):
    df = df[df['Milestone Name'] == name]
    return df

def activity_filter(df,name):
    df = df[df['Activity'] == name]
    return df

def blueprint_filter(df,name):
    df = df[df['Blueprint Name'] == name]
    return df

def space_filter(df,name):
    df = df[df['Space Name'] == name]
    return df

def tech_solution_filter(df,name):
    df = df[df['Tech Solution Type'] == name]
    return df

def participant_filter(df,name):
    df = df[df['Participant Name'] == name]
    return df