# Melody Realm's Official Discord Bot 
created by **@royalrizen** on Discord

---

<br> 

> [!CAUTION]
> You will have to edit the [settings.yaml](https://github.com/Richard0070/Melody-Discord-Bot/blob/main/settings.yaml) file before hosting the bot. It acts as the dashboard.

<br> 

## Environment Variables

|      Variable Name      |         Description        |
|:------------------------|:---------------------------|
| `TOKEN`                 | Discord bot token          |
| `UPLOADER_TECH_API_KEY` | API key for [uploader.tech](https://uploader.tech/)   |
| `PTERODACTYL_SESSION`   | Gaming4Free Cookie         |
| `XSRF_TOKEN`            | Gaming4Free Cookie         |
| `GRECAPTCHA_VALUE`      | Gaming4Free Cookie         |

<br> 

## Hosting 

You can use [render.com](https://render.com) to host your own private instance. Create a web service and import the GitHub repository. Add the necessary environment variables and deploy. You also need to create a blueprint in render using the existing render.yaml in this repo. Just sync it with your bot instance. Now, go to [cron-jobs](https://cron-job.org/en/) website and create a new ping service using the flask web server url obtained from render's dashboard.

<br>

> [!TIP]
> Custom emojis not working? Add your emojis to the bot from developer portal and edit the [config.py](https://github.com/Richard0070/Melody-Discord-Bot/blob/main/config.py) file.

<br>

**Star this repository if you liked my bot ⭐**
