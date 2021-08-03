# Plex-Trakt-Sync

![Python Versions][python-versions-badge]

This project adds a two-way-sync between trakt.tv and Plex Media Server. It
requires a trakt.tv account but no Plex premium and no Trakt VIP subscriptions,
unlike the Plex app provided by Trakt.

**To contribute, please find issues with the [`help-wanted`](https://github.com/Taxel/PlexTraktSync/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) label, thank you.**

[python-versions-badge]: https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue

## Features

 - Media in Plex are added to Trakt collection
 - Ratings are synced (if ratings differ, Trakt takes precedence)
 - Watched status are synced (dates are not reported from Trakt to Plex)
 - Liked lists in Trakt are downloaded and all movies in Plex belonging to that
   list are added
 - You can edit the [config file](https://github.com/Taxel/PlexTraktSync/blob/HEAD/config.default.json) to choose what to sync
 - None of the above requires a Plex Pass or Trakt VIP membership.
   Downside: Needs to be executed manually or via cronjob,
   can not use live data via webhooks.

## Pre-requisites

The script is known to work with Python 3.7-3.9 versions.

## Installing

To install this project, find out the latest release:
- https://github.com/Taxel/PlexTraktSync/releases

Download the `.tar`, or `.zip` or checkout the release with Git.

For example, the command to clone with Git:
```
git clone -b 0.7.19 --depth=1 https://github.com/Taxel/PlexTraktSync
```

In the extracted directory, install the required Python packages:
```
pip3 install -r requirements.txt
```

Alternatively you can use [pipenv]:
```
pip3 install pipenv
pipenv install
pipenv run python main.py
```

[pipenv]: https://pipenv.pypa.io/

## Setup

To connect to Trakt you need to create a new API app:
- Visit https://trakt.tv/oauth/applications/new
- Give it a meaningful name
- Enter `urn:ietf:wg:oauth:2.0:oob` as the redirect url
- You can leave Javascript origins and the Permissions checkboxes blank

Then, run `python3 main.py`.

At first run, you will be asked to setup Trakt and Plex access.
Follow the instructions, your credentials and API keys will be stored in
`.env` and `.pytrakt.json` files.

If you have [2 Factor Authentication enabled on Plex][2fa], you can append the code to your password.

[2fa]: https://support.plex.tv/articles/two-factor-authentication/#toc-1:~:text=Old%20Third%2DParty%20Apps%20%26%20Tools

You can take a look at the progress in the `last_update.log` file which will
be created. 

To set up to run this script in a cronjob every two hours,
type `crontab -e` in the terminal.

```
0 */2 * * * cd ~/path/to/this/repo && ./plex_trakt_sync.sh
```

## Sync options

The `sync` subcommand supports `--sync=tv` and `--sync=movies` options,
so you can sync only specific library types.

```
➔ ./plex_trakt_sync.sh sync --help
Usage: main.py sync [OPTIONS]

  Perform sync between Plex and Trakt

Options:
  --sync [all|movies|tv]  Specify what to sync  [default: all]
  --help                  Show this message and exit.
```

## Sync settings

To disable parts of the functionality of this software, look no further than
`config.json`. Here, in the sync section, you can disable the following things
by setting them from `true` to `false` in a text editor:

At first run, the script will create `config.json` based on `config.default.json`.
If you want to customize settings before first run (ex. you don't want full
sync) you can copy and edit `config.json` before launching the script.

 - Downloading liked lists from Trakt and adding them to Plex
 - Downloading your watchlist from Trakt and adding it to Plex
 - Syncing the watched status between Plex and Trakt
 - Syncing the collected status between Plex and Trakt

## The unmatched command

You can use `unmatched` command to scan your library and display unmatched movies.

Support for unmatched shows is not yet implemented.

## The watch command

You can use `watch` command to listen to events from Plex Media Server
and scrobble plays.

> What is scrobbling?
>
> _Scrobbling simply means automatically tracking what you’re watching. Instead
> of checking in from your phone of the website, this command runs in the
> background and automatically scrobbles back to Trakt while you enjoy watching
> your media_ - [Plex Scrobbler@blog.trakt.tv][plex-scrobbler]

[plex-scrobbler]: https://blog.trakt.tv/plex-scrobbler-52db9b016ead

```shell
$ ./plex_trakt_sync.sh watch
```

## Notes

 - The first execution of the script will (depending on your PMS library size)
   take a long time. After that, movie details and Trakt lists are cached, so
   it should run a lot quicker the second time. This does mean, however, that
   Trakt lists are not updated dynamically (which is fine for lists like "2018
   Academy Award Nominees" but might not be ideal for lists that are updated
   often). Here are the execution times on my Plex server: First run - 1228
   seconds, second run - 111 seconds

 - The PyTrakt API keys are not stored securely, so if you do not want to have
   a file containing those on your harddrive, you can not use this project.

## Docker

To build the image :
`docker build -t me/plextraktsync:latest .`
You can choose an image name as you want (me/plextraktsync:latest).

To create the container :
`docker create --name ptsync -e TZ=Europe/London --restart on-failure:2 twolaw/plextraktsync:latest`

You can choose a container name as you want (ptsync) and you can change the [timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) or remove it (it's UTC by default).

If you want easy access to config files, you can tweak the command to map a volume :
`docker create --name ptsync -v /home/ptsync:/usr/src/app -e TZ="Europe/London" --restart on-failure:2 twolaw/plextraktsync:latest`

In this case, the /home/ptsync (an example) folder on your system must contain all files of the PlexTraktSync github project (use `git clone https://github.com/Taxel/PlexTraktSync.git`).

To run the container :
`docker start -ia ptsync`

The first run must be interactive (docker run -it or docker start -ia) in order to setup your trakt and plex credentials.
