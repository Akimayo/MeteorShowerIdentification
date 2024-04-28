# 🌠 `MeteorShowerIdentificationConsole`
Console app for meteor shower association and finding new showers

# Running
## Running with Python
The entry point of the application is [`__main__.py`](./__main__.py). Run it using a Python interpreter of version **3.<span>*</span>** (built and tested on Python 3.12).

Running with no arguments will yield an error and a hint to use the `--help` flag, or you can run it with `--help` right away. The help text should be sufficient to get you started, but you can look at the [examples](#examples). Run with
```sh
python __main__.py <options>
```

## Running as an executable
Get the [latest executable](https://github.com/Akimayo/MeteorShowerIdentification/releases/latest) from GitHub Releases or use **pyinstaller** to build it yourself. Make sure to have it installed and then run
```sh
pyinstaller meteors.spec
```

Then find the `meteors.exe` file and run
```sh
meteors.exe <options>
```

## Examples
### Get help
```sh
meteors.exe --help
```

### Compare a single orbit with default meteor shower orbits
The `default` option tells the program to get the reference orbits from its internal meteor shower database.

Use
```sh
meteors.exe -q 1.0 -e 0.9 -w 87.6 -O 54.3 -i 2.1 default
```
or
```sh
meteors.exe -a 2.3 -e 0.9 -w 87.6 -O 54.3 -i 2.1 default
```

### Compare a file of compared orbits with file of reference orbits and write results into a file
```sh
meteors.exe compared.dat reference.dat -o output.txt
```

### Configuration files
Generate a configuration file for the current working directory by running
```sh
meteors.exe --config
```

This will generate a `.meteorrc` file in the current working directory. The file is a YAML file with a defined schema, so it's recommended to use a smart editor to fill it out. Otherwise, you can study the [schema](https://raw.githubusercontent.com/Akimayo/MeteorShowerIdentification/master/MeteorShowerIdentificationConsole/constants/meteorrc-schema.json) and fill it out manually.

The `.meteorrc` file will be used for all program runs from this working directory. The options inside can be overriden by command-line arguments and or completely ignored by running the program with the `-0` argument
```sh
meteors.exe compared.dat reference.dat -o output.txt -0
```