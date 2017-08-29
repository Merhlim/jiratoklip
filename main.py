from jira import JIRA
import boto3
from configparser import SafeConfigParser
import xlsxwriter
from time import strftime
import datetime
from time import sleep

class main:
    print("MAIN")
    config = SafeConfigParser()
    config.read("./config.ini")
    print("Config read - OK")
    s3 = boto3.client("s3")
    jirau, jirap = [config.get("jira", "Username"), config.get("jira", "Password")]
    jira_options = {
        'server': 'https://jira.redmatter.com'
    }
    jira = JIRA(options=jira_options, basic_auth=(jirau,jirap))
    print("JIRA auth - OK")
    components = ["ArchivePurge",
              "'Archiving'",
              "'ARSearchD'",
              "'ASK'",
              "'Billing'",
              "'Cacti'",
              "'CDR2SGAPI'",
              "'CDRMunch'",
              "'Cleanup'",
              "'CoreAPI'",
              "'DGAPI'",
              "'DialPlan'",
              "'diehards'",
              "'Factory'",
              "'Freeswitch'",
              "'FreeSWITCH Scripts'",
              "'GeoShimD'",
              "'hD'",
              "'IDS'",
              "'Kohana'",
              "'Lasso'",
              "'LDAP'",
              "'Monitoring'",
              "'MultiDb'",
              "'MySQL'",
              "'Nagios'",
              "'NonCall Policies'",
              "'Notifier'",
              "'OpenSIPS'",
              "'PHP'",
              "'Portal'",
              "'RabbitMQ'",
              "'ReplicateD'",
              "'RM-billingapps'",
              "'RM-phpsiplib'",
              "'Salt'",
              "'Sapien'",
              "'ScriptEngine'",
              "'Service Gateway'",
              "'SGFS'",
              "'SipgwPing'",
              "'SrcEscalation'",
              "'Storage Gateway'",
              "'SyslogForwarder'",
              "'TextToSpeech'",
              "'Toolbox'",
              "'Voicemail'",
              "'Wallboards'",
              ]
    this = [
        "Production",
        "Stage",
        "Q&A",
        "Dev"
    ]

    def __init__(self):
        print("Initialise")
        data, bugs, escalated, timetakenbf, this_output = self.get_tickets()
        print("Ticket data - OK")
        output = ["Open Tickets", "Closed Tickets", "In progress", "Awaiting rollout"]
        baf_output = ["Bugs", "Features"]
        print("Sending excel format")
        self.excelformat(output, data, baf_output, bugs,escalated,timetakenbf, this_output)
        print("Complete! Uploading spreadsheet")
        self.upload("./dev-ticket-state-counts.xlsx")
        print("Done - Will now Sleep for 6000")
        sleep(6000)
        self.__init__()
        
    def upload(self, file):
        bucket_name = main.config.get("s3", "bucket_name")
        main.s3.upload_file(file, bucket_name, "dev-stuff/"+file)

    def get_tickets(self):
        print("Querying JIRA")
        open_issues = len(main.jira.search_issues("project NOT IN (TRAC,JIRA,TESTPLAT) AND createdDate >= -30d AND status != Closed"))
        closed_issues = len(main.jira.search_issues("project NOT IN (TRAC,JIRA,TESTPLAT) AND createdDate >= -30d AND status IN ('Closed')"))
        in_progress = len(main.jira.search_issues("project NOT IN (TRAC,JIRA,TESTPLAT) AND createdDate >= -30d AND status IN ('In progress','under investigation','paused','pending review','development complete','pending merge','tested')"))
        rollout = len(main.jira.search_issues("project NOT IN (TRAC,JIRA,TESTPLAT) AND createdDate >= -30d AND status IN ('awaiting rollout','on staging')"))
        data = [open_issues, closed_issues, in_progress ,rollout]
        open_bugs = len(main.jira.search_issues("project NOT IN (TRAC,JIRA,TESTPLAT) AND createdDate >= -30d AND type = Bug AND status != Closed"))
        open_features = len(main.jira.search_issues("project NOT IN (TRAC,JIRA,TESTPLAT) AND createdDate >= -30d AND type IN ('Improvement','New feature', 'Story') AND status != Closed"))
        bugs = [open_bugs, open_features]
        raised_issues = main.jira.search_issues("project NOT IN (TRAC,JIRA,TESTPLAT) and labels in (Escalated) and status != Closed")
        issues_with_components = main.jira.search_issues("project = PLAT and component is not EMPTY AND createdDate >= -30d")
        print("Main Queries - Complete")
        id = self.getid(raised_issues)
        output = []
        print("Will now attempt to format data")
        for i in range(0,len(id)):
            temp = []
            ticket = main.jira.issue(id[i])
            temp.append(str(ticket.fields.issuetype.name))
            temp.append(str(ticket.fields.summary))
            temp.append(str(ticket.fields.priority.name))
            try:
                temp.append(str(ticket.fields.assignee.displayName))
            except:
                temp.append("Nobody")
            updatetime = str(ticket.fields.updated)
            updatetime = updatetime.split("T")
            timetaken = updatetime[1].split(".")
            updatetime = updatetime[0]+" "+ timetaken[0]
            temp.append(str(self.timesince(updatetime)))
            output.append(temp)
        tissue = self.getid(main.jira.search_issues("project NOT IN (TRAC,JIRA) and createdDate >= -30d and type = Bug and timespent != 0m"))
        timp = self.getid(main.jira.search_issues("project NOT IN (TRAC,JIRA) AND createdDate >= -30d AND type IN ('Improvement','New feature', 'Story') and timespent != 0m"))
        bugstakenseconds = 0
        featurestakenseconds = 0
        for i in range(0,len(tissue)):
            jar = main.jira.issue(tissue[i])
            bugstakenseconds = bugstakenseconds + jar.fields.timetracking.timeSpentSeconds/3600
        for i in range(0,len(timp)):
            jar = main.jira.issue(timp[i])
            featurestakenseconds = featurestakenseconds + jar.fields.timetracking.timeSpentSeconds/3600
        timeinseconds = [round(bugstakenseconds,0),round(featurestakenseconds,0)]
        this_output = self.this_function()

        #print(test.fields.timetracking.timeSpentSeconds)
        #print(raised_issues)
        #issue = main.jira.issue("PLAT-12583")
        #main.jira.add_comment(issue, "Hello world from python!!!!!!!!")
        #i = issue.fields.summary

        '''
        CREATE DEBUG ISSUE

        new_issue = main.jira.create_issue(project='TESTPLAT', summary='Test issue',
        description='Please ignore', issuetype={'name': 'Bug'},customfield_11500={
            "value": "Internal R&D/Ops"
        }
        , customfield_11306={
                "value": "Production"
        })
        '''
        print("Data format complete - Returning information")
        return data, bugs, output, timeinseconds, this_output

    def getid(self, tl):
        print("GETID - LOADING")
        tlen = len(tl)
        tickets = []
        for i in range(0,tlen):
            spl = str(tl[i]).split("'")
            tickets.append(spl[0])
        print("GETID - RETURNING ID")
        return tickets

    def excelformat(self, l1, l2, l4, l5,output,timetakenbf, this_output):
        workbook = xlsxwriter.Workbook("./dev-ticket-state-counts.xlsx")
        worksheet = workbook.add_worksheet()
        print("Workbook set")
        for i in range(0, len(l1)):
            worksheet.write(0, i, l1[i])
        for i in range(0, len(l2)):
            worksheet.write(1, i, l2[i])
        for i in range(0, len(l4)):
            worksheet.write(3, i, l4[i])
        for i in range(0, len(l5)):
            worksheet.write(4, i, l5[i])
        print("SHEET 1 - Generating sheet 2")
        sheet2 = workbook.add_worksheet()
        for i in range(0,len(output)):
            for a in range(0,len(output[i])):
                sheet2.write_string(i, a,output[i][a])
        print("SHEET 2 - Generating sheet 3")
        sheet3 = workbook.add_worksheet()
        sheet3.write_number(0,0,timetakenbf[0])
        sheet3.write_number(0,1,timetakenbf[1])
        print("SHEET 3 - Generating sheet 4")
        sheet4 = workbook.add_worksheet()

        for i in range(0,len(main.components)):
            sheet4.write_string(i,0,main.components[i])
            sheet4.write_string(i,1,self.get_hours(main.components[i]))
        print("SHEET 4 - Generating sheet 5")
        sheet5 = workbook.add_worksheet()
        for i in range(0,len(main.this)):
            sheet5.write_string(i,0,main.this[i])
        tem = 1
        por = 1
        ary = 1
        var = 1
        for i in range(0,4):
            sheet5.write_string(0,tem,str(this_output[i-1]))
            tem = tem+1
        for i in range(4,8):
            sheet5.write_string(1, por, str(this_output[i]))
            por = por+1
        for i in range(8,12):
            sheet5.write_string(2, ary, str(this_output[i]))
            ary = ary+1
        for i in range(12,16):
            sheet5.write_string(3, var, str(this_output[i]))
            var = var+1
        print("SHEET 5 \n EXCEL DATA READY - PROGRESSING")
        workbook.close()

    def timesince(self,lastupdatedtime):
        print("TIMESINCE - LOADING")
        time_current = strftime("%Y-%m-%d %H:%M:%S")
        time_given = datetime.datetime.strptime(lastupdatedtime, "%Y-%m-%d %H:%M:%S")
        time_current = datetime.datetime.strptime(time_current, "%Y-%m-%d %H:%M:%S")
        time_output = time_current - time_given
        try:
            if str(time_output).split(",")[1].split(":")[0] == "1":
                time_output = str(time_output).split(":")[0] + " Hour"
        except:
            coffee = None
        finally:
            if str(time_output).split(":")[0] + " Hour" == "0 Hour":
                time_output = "Less than an hour"
            elif str(time_output).split(":")[0] + " Hour" != "0 Hour":
                time_output = str(time_output).split(":")[0] + " Hours"
        if time_output == "1 Hours":
            time_output == "1 Hour"
        print("TIMESINCE - RETURNING OUTPUT")
        return time_output

    def get_hours(self,component):
        print("GETHOURS - LOADING")
        id = self.getid(main.jira.search_issues("project = PLAT and component = "+component+" AND createdDate >= -30d AND timespent != 0m"))
        var = 0
        for i in range(0,len(id)):
            issue = main.jira.issue(id[i])
            var = var + issue.fields.timetracking.timeSpentSeconds/3600
        var = round(var, 0)
        print("GETHOURS - RETURNING OUTPUT")
        return str(var)

    def this_function(self):
        omg_this_is_long = [
            "Production=Internal R&D/Ops",
            "Production=Internal Support",
            "Production=Other 3rd Party",
            "Production=Customer",
            "Staging=Internal R&D/Ops",
            "Staging=Internal Support",
            "Staging=Other 3rd Party",
            "Staging=Customer",
            "QA=Internal R&D/Ops",
            "QA=Internal Support",
            "QA=Other 3rd Party",
            "QA=Customer",
            "Development=Internal R&D/Ops",
            "Development=Internal Support",
            "Development=Other 3rd Party",
            "Development=Customer",
        ]
        this_is_an_output = []
        for i in range(0, 16):
            id = len(self.getid(main.jira.search_issues('project = PLAT and "Bug Environment" = "'+omg_this_is_long[i].split("=")[0]+'" and "Bug Found By" = "'+ omg_this_is_long[i].split("=")[1]+'" AND createdDate >= -30d AND issueType = Bug')))
            this_is_an_output.append(id)
        return this_is_an_output

if __name__ == "__main__":
    main()