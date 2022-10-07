# systemd files for ticticthaum

Assumes tictacthaum is installed under user pi at /home/pi/tictacthaum.

Start script is installed under user pi at /home/pi/

If you have a different setup you'll need to adjust tictacthaum.service accordingly.

## systemd
Download the systemd files to the locations shown:

```
tictacthaum.service   => /etc/systemd/system/tictacthaum.service
```

Next, make necessary modifications (if any) then notify systemd:
```sh
sudo systemctl daemon-reload
```

Finally, enable and start the `tictacthaum` service:

```sh
# Enable tictacthaum service
sudo systemctl enable tictacthaum

# and start it
sudo systemctl start tictacthaum
```
