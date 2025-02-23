______
I decided to use the Python / Django part since I have used Python back then.

First, I added devcontainer.json to the repository that installs the flyctl CLI so that I can do the work in GitHub Codespaces. After that, I deleted the pycache folder since it had already been committed to the repository. And then I generated fly.io personal access token and paste it to GitHub Codespaces secrets `FLY_API_TOKEN`.

I then started running the Django application using `python manage.py runserver` to check if it works. After confirming that it works, I edited fly.toml to include the app name, which is "[REDACTED]", and then deployed the application in fly.io by using `fly launch --copy-config --ha=false`. I put `--ha=false` so that only 1 machine will be created.

After getting the resulting hostname, I then edited `worksample/settings.py` and added the hostname to the `ALLOWED_HOSTS` list and deploy the app again. I then checked the deployed app at https://[REDACTED].fly.dev confirming that it was deployed correctly.

I then started reading the docs on how to extract the information about the underlying Fly Machine. Knowing that fly.io exposes an API for this, I tried running `curl --oauth2-bearer $FLY_API_TOKEN -s https://api.machines.dev/v1/apps/[REDACTED]/machines | jq .[0]` in GitHub Codespaces and it works. The `jq .[0]` part selects the first machine.

I then created the code in `worksample/apps/core/views.py` that fetches the machine information on the API using the Python Requests library.

```py
import os
import requests
import json

api_url = 'https://api.machines.dev/v1/apps/[REDACTED]/machines'
api_token = f"Bearer {os.getenv('FLY_API_TOKEN')}"
api_request = requests.get(api_url, headers={"Authorization": api_token}).text
machine_info = json.loads(api_request)[0]
```

Seeing that the template's object field fits nicely into the API output, I can easily connect the API output to the template homepage using kwargs.

```py
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machines'] = machine_info
        return context
```

And then I started running the code on GitHub Codespaces using `python manage.py runserver`. After confirming that it works, I then now entered my fly.io personal access token to the fly.io secrets using `fly secrets set FLY_API_TOKEN=$FLY_API_TOKEN`

Since the API has an internal endpoint, I changed the endpoint from `https://api.machines.dev` to `http://_api.internal:4280`.

I then deployed the app again using `fly deploy`. And then I checked the deployed app at https://[REDACTED].fly.dev confirming that it was deployed and outputting the correct machine information.

In order to safeguard my access token, I decided to create a read-only token using `fly tokens create readonly` and then enter it to fly.io secrets using `fly secrets set FLY_API_TOKEN=<generated_read_only_token>`.
______
