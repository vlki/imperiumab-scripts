# Imperium AB scripts

Management scripts for the (Imperium AB database)[https://imperiumab.investigace.cz/]. **Do not use as of yet, work in progress!**

## Setup

```
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

Plus create `.env` file and add to it your Imperium AB MediaWiki username and password.

```
WIKI_USERNAME=user
WIKI_PASSWORD=password
```

## Available scripts

### Import Czech subsidies from CEDR, SZIF and EU funds registers

To be able to run this script, you need to first download data from CEDR, SZIF and EU funds registers via (kokes/od)[https://github.com/kokes/od] project done by Ondřej Kokeš. Follow their instructions and download cedr, eufondy and szif datasets to your local PostgreSQL database.

When download, you can run the script which then searches those datasets for subsidies of Czech companies in Imperium AB database. When found, those subsidies are then imported to the Imperium AB database.

To run the script, you only need to pass the database connection string of `kokes/od` database. Eg.:

```
python3 import_czech_subsidies.py --connstring postgresql://localhost/od
```

## License

MIT