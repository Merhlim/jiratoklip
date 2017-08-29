# JiraToKlip
An application designed convert information queried from JIRA into an excel workbook that gets sent to a S3 bucket that then gets sent to klipfolio to create charts and tables


This is specificaly for redmatter and will not work anywhere else


By Joshua ampstead - Merhlim

# Requirements

Requires docker to be run


The config.ini and aws files to be preconfigured and ready

# Config
### config.ini
config.ini contains the config for JIRA authentication. Jira auth requires a username and password of any user that can see all of the projects.


It also contains the S3 bucket name for the script to process 


See the config sample file for more information

### aws
aws contains the config for AWS e.g. access keys [AWS Documentation](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)


see the aws sample file for more information

# Run

```
docker run -v /location/of/aws/file/aws:/root/.aws/credentials -v /location/of/config/file/config.ini:/jiratoklip/config.ini merhlim/jiratoklip
```


This will automatically run the program every 600 seconds (10 minutes)
