# Word Art Generator

A Fun command line app to make word art using figlet

## Usage

1. clone the repo from [here](https://github.com/cloudymax/art_generator)

2. install pip deps

```zsh
cd art_generator
pip install -r requirements.txt
```
3. run the script

```zsh
export FONT="poison"
export TEXT_COLOR="ansimagenta"
export BG_COLOR="ansigreen"
export PAYLOAD="Poison"

python3 art_generator.py $FONT $TEXT_COLOR $BG_COLOR $PAYLOAD

python3 art_generator.py "poison" "ansimagenta" "ansigreen" "Poison"
```

## Example

![Example](https://github.com/cloudymax/art_generator/blob/main/example.png?raw=true)