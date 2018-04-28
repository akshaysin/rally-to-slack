from datetime import datetime
from datetime import timedelta
from pyral import Rally
from slacker import Slacker

slack = Slacker('SLACKAPIKEY')

# Send a message to #integration-testing channel

server="rally1.rallydev.com"

#as we are using an API key, we can leave out the username and password
user=""
password=""

workspace=""
project=""
apikey="RALLYAPIKEY"

#which slack channel does this post to?
channel = ""

#Assume this system runs (via cron) every 15 minutes.
interval = 15 * 60

#format of the date strings as we get them from rally
format = "%Y-%m-%dT%H:%M:%S.%fZ"

#create the rally service wrapper
rally = Rally(server, user, password, apikey=apikey, workspace=workspace, project=project)
# rally.enableLogging('mypyral.log')

#build the query to get only the artifacts (user stories and defects) updated in the last day
querydelta = timedelta(days=-1)
querystartdate = datetime.utcnow() + querydelta;
query = 'LastUpdateDate > ' + querystartdate.isoformat()
title = "*Pulling Rally Report for {0} as of {1}*".format(project,querystartdate) + "\n";
title = title + "==========================================================" + "\n";
title = title + "> _This report only contains the itmes updated in last one day_" + "\n";
title = title + "" + "\n";
slack.chat.post_message(channel=channel, text=title, username="rallyslackbot", as_user=False)

# List mode
response = rally.get('HierarchicalRequirement', fetch=True, query=query, order='LastUpdateDate desc')
for item in response:
    if item.Owner :
        postmessage= "*" + item.FormattedID + "* : " +  item.Name + "\n";
        postmessage=  postmessage + ">_Assigned to_ : " + item.Owner.UserName + "\n";
        postmessage=  postmessage + ">_Current State_ : " + item.ScheduleState + "\n";
        postmessage=  postmessage + ">_Current Testing State_ : " + item.TaskStatus + "\n";
        postmessage = postmessage + 'https://rally1.rallydev.com/#/search?keywords=' + item.FormattedID + '\n';
        postmessage=  postmessage + "" + "\n";
    else:
        postmessage= "*" + item.FormattedID + "* : " +  item.Name + "\n";
        postmessage=  postmessage + ">_Assigned to_ : " + "NA" + "\n";
        postmessage=  postmessage + ">_Current State_ : " + item.ScheduleState + "\n";
        postmessage=  postmessage + ">_Current Testing State_ : " + item.TaskStatus + "\n";
        postmessage = postmessage + 'https://rally1.rallydev.com/#/search?keywords=' + item.FormattedID + '\n';
        postmessage=  postmessage + "" + "\n";
    slack.chat.post_message(channel=channel, text=postmessage, username="rallyslackbot", as_user=False)
slack.chat.post_message(channel=channel, text="*EOM*", username="rallyslackbot", as_user=False)
