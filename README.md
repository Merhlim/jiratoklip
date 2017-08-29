# JiraToKlip
A simple application for converting JIRA information into an excel spreadsheet for Klipfolio
By Joshua ampstead - Merhlim

# Requirements
Requires docker to be run
The config.ini and aws files to be preconfigured and ready

# Run

```
docker run -v /location/of/aws/file/aws:/root/.aws/credentials -v /location/of/config/file/config.ini:/jiratoklip/config.ini merhlim/jiratoklip
```

This will automatically run the program every 600 seconds (10 minutes)
