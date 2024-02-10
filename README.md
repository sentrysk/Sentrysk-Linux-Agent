# Linux System Agent

## Provides
- System Info
- Users Info
- Services
- Installed Apps
- NPM Info
- Pip Info
- Docker Info

## How It Works

### Services
```
wmic service get DisplayName,Name,State,Description /format:csv
```
code runs and returns

```
{
    "DisplayName":"",
    "ServiceName":"",
    "Status":"",
    "Description"
}
```