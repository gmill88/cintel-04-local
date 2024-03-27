# cintel-04-local

## Publish Interactive Reactive App

### Virtual environment set up
- Create a repo in GitHub, clone it to down and create a local project virtual environment in the .venv folder using:

```bash
python3 -m venv .venv
```

- Activate .venv using:

```bash
source .venv/bin/activate
```
- Install all the packages needed for the project using the following commands:

```bash
py -m pip install --upgrade pip setuptools
py -m pip install --upgrade -r requirements.txt
```

### Run the App
After activating the virtual environment, run the app with live reloading using:

```bash 
shiny run --reload --launch-browser penguins/app.py
```
While the app is running you can no longer use that terminal, so you'll want to open a new terminal to run commands. 

### Build the app to the docs folder
With the virtual environment active, remove existing assests and use shinylive to export and build the app in the docs folder

```bash
shiny static-assets remove
shinylive export penguins docs
```

### Add a Custom Title to the App
Make changes to the title of the app to personalize your app

```html
    <title>PyShiny Penguins</title>
```

### Add a Favicon to your App
Add a Favicon image to the tab of your app

```html
    <link rel="icon" type="image/x-icon" href="./favicon.ico">
```

### When Finished Editing, Git Add/Commit?Push Changes to GitHub

When you are done editing use the following to update your GitHub repository

```bash
git add .
git commit -m "Your commit message"
git push -u origin main
```

### Publish the App with GitHub Pages
1. Go to the repository on GitHub and navigate to the **Settings** tab.
2. Scroll down and click the Pages section.
3. Select branch main as the source for the site.
4. Change from the root folder to the docs folder to publish from.
5. Click Save and wait for the site to build.
6. Edit the "About" section of the repository to include a link to the live app.