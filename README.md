# multiturtle

Collaborative drawing application, built on Python turtle and websockets.

## Running the program

### Prerequisites

Some dependencies are required to run either the client or server. To install these dependencies, run `pip3 install -r requirements.txt`.

There are also some settings in `main.py` that you may want to edit; for example if you're on a Unix-based OS, you might need to edit the `PRECISION` variable to avoid recursion errors.

### Using the publicly-hosted server

The publicly hosted server will be taken down `2021-12-01`. If you're here before that date, you can simply run `main.py`, as the `INSTANCE` variable is set to it already.

Note that the drawings on the public instance are not moderated in any way, and there can also be lag issues if there are a lot of drawings, due to turtle/tkinter limits.

### Hosting your own instance

Run `server.py`. Then, change the `INSTANCE` variable in `main.py` with the IP of the machine running `server.py`. You may have to forward port `8765`. After doing that, you can run `main.py`.

### Offline mode

Set the `OFFLINE` variable in `main.py` to `True`. Then, run `main.py`.

## Using the program

Simply just start using it like any drawing program.

### Keyboard shortcuts

| Key                              | Action           |
| -------------------------------- | ---------------- |
| Scroll or Up/Down Arrow          | Change pen size  |
| <kbd>Ctrl</kbd> + <kbd>Z</kbd>   | Undo             |
| <kbd>C</kbd>                     | Choose pen color |
| <kbd>Ctrl</kbd> + <kbd>Del</kbd> | Clear board      |

## Why turtle?

This was a school project, and using turtle was part of the requirements. There are also a few bugs with this program, but unfortunately they are not going to be fixed, as because this is a school project, I'm no longer working on it after the due date.
