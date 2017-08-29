# JiraToKlip
A simple application for converting JIRA information into an excel spreadsheet for Klipfolio
By Joshua ampstead - Merhlim

# Requirements
Requires docker to be run
The config.ini and aws files to be preconfigured and ready

# Config
### config.ini
config.ini contains the config for JIRA authentication and S3 bucket name [JIRA Documentation](https://confluence.atlassian.com/jira/jira-documentation-1556.html)

### aws
aws contains the config for AWS like access keys [AWS Documentation](https://aws.amazon.com/documentation/)

# Run

```
docker run -v /location/of/aws/file/aws:/root/.aws/credentials -v /location/of/config/file/config.ini:/jiratoklip/config.ini merhlim/jiratoklip
```

This will automatically run the program every 600 seconds (10 minutes)
