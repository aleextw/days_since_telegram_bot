# days_since_telegram_bot

Simple bot to track the number of days since a specified event

## Installation

Create a new virtual environment:

```shell
python3 -m venv venv
```

Activate the virtual environment.

If you are on Windows:

```shell
./venv/Scripts/activate
```

If you are on MacOS / Linux:

```shell
source ./venv/bin/activate
```

Install the requirements:

```shell
pip install -r requirements.txt
```

Set your bot token in the `config.py` file, and modify the other options as necessary.

- `TOKEN`: Your bot token
- `EVENT_NAME`: The text displayed when the cron job triggers ('It has been {} days since {EVENT_NAME}')
- `COMMAND`: The text of the command used to reset the counter ('/{COMMAND}')
- `REMINDER`: Set according to cron schedule expressions

## Commands

- `/start` or `/help`: Shows available commands
- `/set`: Starts the event tracking
- `/unset`: Stops the event tracking
- `/{CONFIG['COMMAND']}`: Resets the event tracking date
