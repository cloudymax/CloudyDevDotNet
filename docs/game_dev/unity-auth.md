# Using Selenium to authorize Unity Personal Licenses

This program uses selenium and a headless firefox browser to automate the process of authorizing Unity Personal Edition licenses with the Unity CLI since Unity wont let us use the API

- You can find the repo [Here](https://github.com/cloudymax/unity-self-auth)

    ???+ Warning 

        WIP project for a game jam, only 'mostly' works




## Usage

1. follow the setup guide first

2. navigate to the program directory and run the program 

    ```bash
    cd program

    python3 license.py license/Unity_v2020.3.10f1.alf config/config.json

    python3 script <path/to/file.alf> <path/to/config.json>
    ```

## Program dependencies

- Install the gekko web driver

latest build url <a>https://github.com/mozilla/geckodriver/releases/latest</a>

??? Tip "On Linux"

    ```bash
    export gekko_version="0.29.1"
    export gekko_url=$(echo "https://github.com/mozilla/geckodriver/releases/download/v${gekko_version}/geckodriver-v${gekko_version}-linux64.tar.gz")
    wget "${gekko_url}"
    tar xvfz geckodriver-v"${gekko_version}"-linux64.tar.gz
    rm geckodriver-v"${gekko_version}"-linux64.tar.gz
    mv geckodriver ~/.local/bin #linux
    ```

??? Tip "On Mac"

    ```bash
    export gekko_version="0.29.1"
    export gekko_url=$(echo "https://github.com/mozilla/geckodriver/releases/download/v${gekko_version}/geckodriver-v${gekko_version}-macos.tar.gz")
    wget "${gekko_url}"
    tar xvfz geckodriver-v"${gekko_version}"-macos.tar.gz
    rm geckodriver-v"${gekko_version}"-macos.tar.gz
    mv geckodriver /usr/local/bin
    geckodriver -V
    ```

- Install selenium

    ```bash
    pip install selenium
    pip install -U selenium
    pip freeze | grep selenium
    #export PATH=$PATH:/home/max/.local/bin
    ```

- install firefox

    ```bash
    # I already have installed here on my mac
    ls /Applications/Firefox.app/Contents/MacOS/firefox
    > /Applications/Firefox.app/Contents/MacOS/firefox -v
    > Mozilla Firefox 89.0.2
    ```

## Machine Setup

- I really need to automate this with ansible

    ??? Warning
    
        notes, not code - it probably wont run right now

- install Docker

    ```zsh
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo \
      "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```

- install pip

    ```zsh

    sudo apt-get install python3-pip

    ```

- install brew

    ```zsh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /home/max/.profile
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    ```

- install Unity Hub, and set env vars

    - Download url <a>https://public-cdn.cloud.unity3d.com/hub/prod/UnityHub.AppImage</a>

    ```zsh
    chmod +x UnityHub.AppImage

    export VERSION="2020.3.10f1"
    export APPDIR=~/Unity/Hub/Editor/$VERSION/Editor
    export USN="email"
    export PSWD="password"
    export LICENSE_NAME="Unity_v${VERSION}.alf"
    ```


- generate liscence file

    ```zsh
    cd "${APPDIR}"

    Unity -quit -batchmode -nographics -logFile /dev/stdout \
        -createManualActivationFile \
        -username "${USN}" \
        -password "${PSWD}"

    cp "${LICENSE_NAME}" "${APPDIR}"/"${LICENSE_NAME}"
    ```


- Desktop Icons

- Create a .desktop file

    ```zsh
    
    touch hub.desktop
    
    ```

- Add the follwing to the file:

    ```yaml
    [Desktop Entry]
    Name=UnityHub
    Comment=Unity Hub
    Exec=UnityHub.AppImage
    Icon=UnityIcon.png
    Terminal=false
    Type=Application
    Categories=Development
    ```

- Set permissions and owner

    ```zsh
    chown max:max hub.desktop
    chmod +x hub.desktop
    ```

## Maintenance

1. Configuration_settings:

    - <b>elements</b>: the names of html elements to search for
    - <b>urls</b>: the web urls of pages to load
    - <b>radio buttons</b>: button selection options + xpaths

2. html_references:

    - where I save out html copies of the websites so you can sanity-check the search params if needed in case they change down the line

3. license:

    - put your .alf here

4. logs:

    - self explanitory

5. template_config:

    - example config file

???+ Todo

    - clean this up as a profile pack for my ansible runner provisioner or make it serverless
    - unity login
    - use selenium to get the latest gekko version
    - encrypt sensitive data, store in k8s or cloud (moving data to config file, then encryption can be done)
    - logging