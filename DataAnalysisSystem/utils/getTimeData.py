from utils import get_df,typeList

def getDurationData():
    df = get_df()
    duration = list(df['duration'])
    durationData = [{
        'value':0,
        'name':'<60min'
    },{
        'value': 0,
        'name': '60-90min'
    },{
        'value': 0,
        'name': '90-120min'
    },{
        'value': 0,
        'name': '>120min',
    }]
    for i in duration:
        if int(i) < 60:
            durationData[0]['value'] = durationData[0]['value'] + 1
        elif (int(i) < 90 and int(i) >= 60):
            durationData[1]['value'] = durationData[1]['value'] + 1
        elif (int(i) < 120 and int(i) >= 90):
            durationData[2]['value'] = durationData[2]['value'] + 1
        else:
            durationData[3]['value'] = durationData[3]['value'] + 1
    return durationData

