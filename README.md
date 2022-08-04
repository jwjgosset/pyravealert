# Rave Alert Mobile setup

The following assumes the reader has knowledge on setting up CAP inbound.  Instructions can be found under docs folder.

## Quick legacy support bin

The package comes a cli tool "ravealert" which is meant to quickly support legacy systems.  In short, it simply creates the CAP XML compliant message
based on the input arguments.  There are default CAP properties set, these include:

- identifer = guaranteed to be unique in the format "hostname-timestamp-randomx10"
- sender = always the hostname its generated from
- sent = now
- msgType = Alert

Some other elements are ignored.  For those that can be modified, see the --help of the command.

An example call for WASP Test Alerts is:

```bash
ravealert -e "WASP Test Alert" -H "Test of the Rave Alert system" -d "This is a test of the Rave alert system" -i "No actions required" -w "https://ottawa.seismo.ca/systems/wasp/" -c Infra
```

As per the example, our Rave system is setup that Infra alerts go to the GeekOnDuty.  To note the, --url and credentials are not shown in the example.

## Environment variables

Some settings can be set by environment variables or in .env file in cwd.  For the list, see pyravealert/config.py.
