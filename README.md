# autotrakttv
Programmatically access trakt.tv information through the command line.

# Usage
You'll need to create your own trakt.tv app first. You should then have your own client_id, client_secret, and pin_id. Put this in a file named `secrets` in the `~/.autotrakttv` folder in JSON format:
```
{
  "CLIENT_ID": "<your_client_id>",
  "CLIENT_SECRET": "<your_client_secret>",
  "PIN_ID": "<your_pin_id>"
}
```
After installing the dependencies in requirements.txt, run
```
python cli.py authenticate
```
and follow the instructions. If successful, this will store your access_token in `~/.autotrakttv/auth`.

Then you can run
```
python cli.py -h
```
for available options.
