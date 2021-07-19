# Is The Rock Wet?

Is The Rock Wet? is a website that allows users to create weather "backcasts" for particular climbing locations, as well as a location selected from a map.

## Installation

Step 1: Download zip from github (https://github.com/ktkinsey37/capstone/archive/refs/heads/master.zip) and extract to directory

Step 2: Initiate python virtual environment

```bash
python -m venv venv
```

Step 3: Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies

```bash
pip install requirements.txt
```

Step 4: Initiate Flask
```bash
flask run
```

Step 5: Visit the correct port in your browser

## Usage
Navigate the website primarily through links and buttons. The homepage allows a user (without signing up) to select a location from the map (or a list of popular locations), designate whether it's sandstone or alpine, and create a weather backcast that shows the hour-by-hour history of precipitation. A user can also create an account in order to save their own locations. Backcasts can be saved and edited later by the user to compare accuracy (or for other activities like canyoneering, packrafting, biking, etc).



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors

Kevin Kinsey  
ktkinsey37@gmail.com