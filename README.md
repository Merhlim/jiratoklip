# JiraToKlip
A simple application for converting JIRA information into an excel spreadsheet for Klipfolio
By Joshua ampstead - Merhlim

# Requirements
Requires docker to be run
The config.ini and aws files to be preconfigured and ready

# Config
### config.ini
config.ini contains the config for JIRA authentication. Jira auth requires a username and password of any user that can see all of the projects.

See the config sample file for more information

### aws
aws contains the config for AWS like access keys [AWS Documentation](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

see the aws sample file for more information

# Run

```
docker run -v /location/of/aws/file/aws:/root/.aws/credentials -v /location/of/config/file/config.ini:/jiratoklip/config.ini merhlim/jiratoklip
```

This will automatically run the program every 600 seconds (10 minutes)
