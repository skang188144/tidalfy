<div align="center">
  <h1 align="center">tidalfy</h1>

  <p align="center">
    A tool for the migration of Daily Mix playlists from Spotify to TIDAL.
    <br />
  </p>

</div>

[![GitHub Contributors](https://img.shields.io/github/contributors/skang188144/tidalfy.svg?label=Contributors)](https://github.com/skang188144/tidalfy/graphs/contributors) [![GitHub Forks](https://img.shields.io/github/forks/skang188144/tidalfy.svg?label=Forks)](https://github.com/skang188144/tidafy/forks) [![GitHub Stars](https://img.shields.io/github/stars/skang188144/tidalfy.svg?label=Stars)](https://github.com/skang188144/tidalfy/stargazers) [![GitHub Issues](https://img.shields.io/github/issues/skang188144/tidalfy.svg?label=Issues)](https://github.com/skang188144/tidalfy/issues) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

tidalfy is a Python script with the goal of providing a seamless migration from Spotify to TIDAL. The script, written in Python, utilizes tidalapi and spotipy to provide Daily Mix migration. Additional features are TBA. 

## Key Features

- **Daily Mix Migration:** Move your Daily Mix Spotify playlists to TIDAL automatically.

## Usage

1. Fork the repository. More instructions can be found [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#forking-a-repository "here").

2. Clone your forked repository:
   ```bash
   git clone https://github.com/-USERNAME-/tidalfy.git
   ```

3. Navigate to the project directory:
   ```bash
   cd tidalfy
   ```
4. Edit the spotify_session_config.yml file with your Spotify credentials and Daily Mix playlist URIs. More instructions can be found [here](https://github.com/skang188144/tidalfy#creating-a-spotify-api-app--retrieving-your-client-id-and-secret "here").

5. Run tidalfy.py, and follow the TIDAL authorization prompts:
	```
	"PROMPT: Please login with your web browser: link.tidal.com/sample_code"
	```

6. Allow the script to finish executing. This may take a few minutes, depending on the number and size of your Daily Mix playlists.

7. Once the script has finished, push the changes to your GitHub repository:
   ```bash
   git add .
   git commit -m "-MY COMMIT MESSAGE-"
   git push
   ```
   
8. Navigate to the "Actions" tab of your GitHub repository, and click "set up a workflow yourself".

9. Look over the provided GitHub Actions main.yml template.

   ```
   name: tidalfy

	on:
	  schedule:
	  - cron: "* * * * *" 
	  	# in cron syntax, "* * * * *" means "every minute"
		# to create your own cron syntax, visit https://crontab.guru

	jobs:
	  build:
		runs-on: ubuntu-latest
		steps:
		  - name: Checkout repository contents
			uses: actions/checkout@v4

		  - name: Setup Python Version
			uses: actions/setup-python@v5
			with:
			  python-version: 3.11.2 
			  # 3.11.2 is currently stable
			  # you may replace it with your own Python version, if you desire.

		  - name: Install Python Dependencies
			run: |
			  python -m pip install --upgrade pip
			  pip install -r requirements.txt

		  - name: Execute Code
			run: python tidalfy.py

		  - name: Commit Files
			run: |
			  git config --local user.name "-YOUR_GITHUB_USERNAME-"
			  git config --local user.email "-YOUR_GITHUB_EMAIL-"
			  git add --all
			  git commit -am "GitHub Action: Daily tidalfy execution"
			  git push origin main
			env:
			  REPO_KEY: ${{secrets.GITHUB_TOKEN}}
			  username: github-actions

		  - name: Push Changes
			uses: ad-m/github-push-action@v0.8.0
			with:
			  github_token: ${{secrets.GITHUB_TOKEN}}
			  branch: main
   ```

10. Replace the boilerplate text from the main.yml template with your own cron time, Python version, and GitHub username and email.

11. Paste the modified template into your own main.yml file.

12. Stage, commit, and push your changes to your GitHub repository.

## Creating a Spotify API App & Retrieving Your Client ID and secret
1. Login to Spotify Web.

2. Go to [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard "https://developer.spotify.com/dashboard"), and click "Create app".

3. Create an app name, enter http://localhost:8888/callback for the redirect URI, check all API/SDKs, and click "Save" (note: copy the redirect URI for your spotify session config file).

4. Navigate to your app in your Spotify Developer Dashboard.

5. Click on "Settings"

6. There, you will find your Spotify client ID and client secret (once you press "View client secret").

## Retrieving Your Spotify Username
1. Login to Spotify Web, and navigate to the Web Player.

2. Click on your profile image, and select "Account".

3. Select "Edit profile".

4. There, you will find your Spotify username.

## Retrieving Your Daily Mix Playlist URIs
1. Login to Spotify Web, and navigate to the Web Player.

2. Navigate to the appropriate Daily Mix playlist.

3. Click on the three dots.

4. While holding control (CTRL), select "Share" and then "Copy Spotify URI".

## License

tidalfy is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact

For inquiries or suggestions, contact the developer at skang188144@gmail.com.
