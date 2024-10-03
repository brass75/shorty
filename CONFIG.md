# The Config file

The configuration for Shorty is stored in a JSON file. This file contains all of the configuration
for the application.

## File structure

The file structure is:

```json
{
  "server": {
    "host": "hostname for the machine>",
    "port": <port for the machine>
  },
  "templates": "<alternate path to templates directory>"
}
```

## Fields
- `server` - This contains the definition of the server. The fields here will be used to define 
the URL provided when a link is shortened.
  - `host` - the hostname or IP for the running server. Default: `localhost`.
  - `port` - optional port number. Defaults to `''`.
  - `schema` - the URI schema (`http` or `https`) to use. If not set or not valid, `http` will be used.
- `templates` - If set, the path to the templates directory. If not set, `src/templates` will be used.



