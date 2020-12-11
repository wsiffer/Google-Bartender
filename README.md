# Google Home Enabled Smart-Bartender
Using the original project from [HackerShack](https://github.com/HackerShackOfficial/Smart-Bartender), this project implements a Flask server to control the bartender with Google Home Instead!(or any other IFTTT service) This bartender is built from a Raspberry Pi 3 and some common DIY electronics.

There is a better way to exectue this I am sure, but this way worked for me as I was new to python and required minimal changes to the original [Smart-bartender](https://www.youtube.com/watch?v=2DopvpNF7J4) features

Hardware setup replicates the original [hackster.io](https://www.hackster.io/hackershack/smart-bartender-5c430e) post. I have not checked to see if the OLED or LED lights work, but the pumps definately do. 
## Prerequisites for the Raspberry Pi
Make sure you can connect a screen and keyboard to your Raspberry Pi. I like to use VNC to connect to the Pi. I created a [tutorial](https://www.youtube.com/watch?v=2iVK8dn-6x4) about how to set that up on a Mac.

Make sure the following are installed:
* Python 3+ (should already be installed on most Raspberry Pi)
* [pip](https://www.raspberrypi.org/documentation/linux/software/python.md)
* Docker - explained below
* SSH connection - this is useful for updating the drinks while running the bartender "headless"
### Enable Docker
Docker is a server control system that allows different software components to be installed in what are called "containers". You can read more about it [here](https://docs.docker.com/get-docker/)

Once this repository is cloned to a directory on your pi, download docker using the following command:

```
curl -sSL https://get.docker.com | sh
```

in the terminal. 

## Web Accounts Setup
### Google Home
Use the standard procedure found [here](https://support.google.com/googlenest/answer/7029485?co=GENIE.Platform%3DiOS&hl=en-AU&oco=0)

Once your google home is setup and connected to the internet, make some test requests to make sure everything works properly. If it works then move on to setting up your relay!
### Webhook Relay
##### The webhook relay is only required for instances where you do not have access to port forwarding on your internet network. (school, work, strict parents, etc)
Login to [webhook relay](https://my.webhookrelay.com/login) with your google acct. Although that is probably not required, I find it easier to sign in with google whenever possible

Use the following steps to setup your relay service 
* Click `Webhook Wizard` on the left
* Name your bucket something cool like `bartenderRelay` (try to avoid spaces for ease of setup later)
* Click continue (dont worry about configuring the webhook provider yet) until you get to `Create Output`
* Name your output something like `bartender`
* Set the `Output Destination` to `http://your.pi.local.ip:5000/webhook`
* Set your output destination as `http://your-pi-ip:5000/webhook` and make sure `type internal` is checked
* Click next, then click `Generate Key` These keys are VERY important, so dont lose them. Copy your key and secret somewhere safe.
* Click Next and then click Finish

The key and secret will be used in a bit, but in the meantime navigate to `Buckets` and make sure your newly created bucket is listed

### IFTTT

###### If-This-Then-That
[IFTTT](https://ifttt.com/) is a service that helps to make custom home automation services. 

Use the following steps to setup your automation for the bartender:
* Login to IFTTT with the same google account you used to setup your google home - this is very important
* Click `Create` in the upper right corner of the page
* Click the `+` and search for `Google Assistant` - Click on it and select `Say a phrase with a text ingredient`
* Follow the instructions by putting in `Make me a $` where it asks what you want to say, (you can add other ways if you want)
* Add a response that you want your google home to say when you give it that command and click `Create Trigger`

Note: there is a bug with IFTTT where when I say `make me a Long Island` the `text field` is `a Long Island`. I accounted for this bug within the app, if something changes then I will post an update commit. It is important to know this bug so when you choose a response for your Google Home to say, it is `Telling the bartender to make you $` not `Telling the bartender to make you a $`
* Click the `+` for the `then that` section, search for `Webhooks` and `Make web request`
* Go to your recently created webhook relay [bucket](https://my.webhookrelay.com/buckets) and copy the web link in the `input` column. Paste that link in the `URL` section of the IFTTT webhook settings. 

NOTE: If you are not using webhook relay, then the URL will be the IP address and port followed by `:5000/webhook` i.e. `http://xx.xx.xx.xx:5000/webhook`. There are tutorials online how to do this for your specific router 
* Under `Method`, choose `POST`
* Set `Content Type` to `text/plain`
* In the `Body` section type `{{TextField}}`

Create the service and go back to your pi for the next steps! 
## Setting up your pi Docker Containers

First, make sure to download this repository on your raspberry pi. Once you do, navigate to the downloaded folder in the terminal:

```
cd ~/path/to/directory
```
Inside the directory there is a file called Dockerfile, this instructs Docker what to do in order to build your environment perfectly. 

Use the following command to build the docker image (you may need sudo)
```
docker build --tag bartender
```
This will likely take a bit, so go grab yourself some coffee

Once docker has completed building your own bartender container, run the following command to start the web server:
```
docker run -p 5000:5000 -v $PWD:/app -d --name Bartender --privileged bartender
```
Now that your bartender is running, you can now start your local webhook relay client if you're using the service

Run the following command too install and run the webhook relay client. This only has to be done once.
```
docker run --name whr-relayd --net host --restart always -d webhookrelay/webhookrelayd-arm:latest --bucket bucket-name -k your-key -s your-secret
```
Copy your key and secret codes into the part of the command at the end where it says `your-key` and `your-secret` and change `bucket-name` to the bucket name you specified

The webhook relay should always run on startup. you can check that by rebooting your pi and seeing if your webhook relay dashboard says that a relay is connected without needing a command. 


To make the bartender container run on startup as well, use the following command:
```
docker update --restart always Bartender
```
### Setting a static IP
Setting a static IP will be helpful in making sure that the Bartender and webhook clients always communicate when the bartender is booted. 

This static IP will need to be removed if the Bartender is ever connected to a new internet network.

* Use the command `sudo nano /etc/dhcpd.conf` to open the static IP settings
* Add the following lines to the text file:
     * ```
       interface wlan0
       static ip_address=your.local.ip.address
       static routers=your.router.ip.address
       static domain_name_servers=your.router.ip.address
       ```
### Configure Bartender to Boot to Command Line
* Use the command `sudo raspi-config` to open the configuration screen
* Navigate to `Boot Options`
* Select `Desktop / CLI`
* Select `Console Autologin`
* When you're finished, select `Finish` to reboot

To switch back to booting to a desktop screen, just select `Desktop Autologin` instead of `Console Autologin`

### Useful Docker Commands
* Use `docker ps` to see what containers are currently running
* Use `docker start CONTAINER-NAME` to start a container and `docker stop CONTAINER-NAME` to stop one 

### How it Works / Read this for info on how to edit config files
Before making changes, Run `docker stop Bartender`, and remember to run `docker start Bartender` when changes are saved

There are two files that support the bartender.py file:

#### drinks.py
Holds all of the possible drink options. Drinks are filtered by the values in the pump configuration. If you want to add more drinks, add more entries to `drinks_list`. If you want to add more pump beverage options, add more entries to the `drink_options`.

`drinks_list` entries have the following format:

```
{
		"name": "gin and tonic",
		"ingredients": {
			"gin": 50,
			"tonic": 150
		}
	}
```

`name` specifies a name that will be searched for by the flask server when you make a request. It is best to use lowercase and no symbols. A good way to determine what name to use is to use the `google assistant` app on your phone and tell the app to `make me a ___`. Whatever the app types to the screen, match the case/spelling.
 
 This name has to be unique to help the app identify which drink has been selected. `ingredients` contains a map of beverage options that are available in `drink_options`. Each key represents a possible drink option. The value is the amount of liquid in mL. *Note: you might need a higher value for carbonated beverages since some of the CO2 might come out of solution while pumping the liquid.*

`drink_options` entries have the following format:

```
{"name": "Gin", "value": "gin"}
```

The name will be displayed on the pump configuration menu and the value will be assigned to the pump. The pump values will filter out drinks that the user can't make with the current pump configuration. 

### pump_config.json
The pump configuration persists information about pumps and the liquids that they are assigned to. An pump entry looks like this:

```
"pump_1": {
		"name": "Pump 1",
		"pin": 17, 
		"value": "gin"
	}
```

Each pump key needs to be unique. It is comprised of `name`, `pin`, and `value`. `name` is the display name shown to the user on the pump configuration menu, `pin` is the GPIO pin attached to the relay for that particular pump, and `value` is the current selected drink. `value` doesn't need to be set initially, but it will be changed once you select an option from the configuration menu.

My bartender uses all 8 pumps, although the original version from HackerShack only had 6. Pump 7 is attached to GPIO 16, and pump 8 is GPIO 12 
### A Note on Cleaning
After you use the bartender, you'll want to flush out the pump tubes in order to avoid bacteria growth. 

I added a function to my flask app for this feature. Simply create another IFTTT applet where the command is `Clean the Bartender` and the webhook is configured the same way except the `body` field contains `a clean`

The reason for the `a` is because of the bug i mentioned earlier in the IFTTT setup section. If the bug is ever fixed I will update this section of the guide as well.


