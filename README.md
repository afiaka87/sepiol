# sepiol


## Dependencies

- python3.5>
- poetry

### Building the Project
```sh
git clone https://github.com/afiaka87/sepiol.git
cd sepiol
poetry build
pip install dist/sepiol-<version_num>.tar.gz
```

### Usage

```s
sepiol --port 6678 \
--host "irc.freenode.net" \
--target "#python" \
--twitch_user_id "<twitch_user_id>" \
--client_id "<twitch_client_id>" \
--secret "<twitch_secret>"
```


### Arguments

```
-t --target         a nickname or channel
-p --port           port of irc server
-h --host           url of irc server, default irc.freenode.net
-u --user-id        your twitch user id
-c --client_id      your twitch app's client id
-s --secret         your twitch app's secret tokey
-m --message        the message to send when you go live
-h --help           explanation of arguments required
```


### Getting your Twitch User ID:
```sh
# Make a POST request 
curl -X GET 'https://api.twitch.tv/helix/users?login=username'
```

JSON Response
```json
{
  "data": [
    {
      "broadcaster_type": "",
      "description": "lorem ipsum",
      "display_name": "display_name",
      "id": "69836134", # Your user ID
      "login": "br4vetrav3ler",
      "offline_image_url": "...",
      "profile_image_url": "...",
      "type": "",
      "view_count": 42 
    }
  ]
}
```

### JQ can find it
```sh
apt install jq
curl -X GET \
'https://api.twitch.tv/helix/users?login=username' | jq -S .data[0].id
"523252" # User ID = 523252
```