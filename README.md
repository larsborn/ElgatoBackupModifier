# ElgatoBackupModifier

The script in this directory allows you to modify an Elgato StreamDeck backup file. Technically, those backups are just
ZIP files but with a file extension of `.streamDeckProfilesBackup`. The only supported use case for the script is to
mass-edit the output sound device of Soundboard tiles. I wrote the script this script because for some unknown reasons
— potentially related to me playing around with virtual sound devices — my StreamDeck switched the output device to 
"Default" for all Soundboard tiles. This was particularly annoying because I use a different (virtual) sound device to 
allow other to hear the annoying sound board effects.

You can create a backup by opening the settings, switching to the "Profiles" tab and hitting the small down-arrow at
the bottom in the middle. In the menu select "Export..." and choose a file name. You can pass the name of the resulting
file to the `main.py` script and print all sound device names:

```bash
./main.py input.streamDeckProfile output.streamDeckProfile --print-output-type
```

Take note of the GUID you want to use for all sound tiles and pass it to the script like so: 

```bash
./main.py input.streamDeckProfile output.streamDeckProfile --set-output-type "{0.0.0.00000000}.{91e09dfe-17fa-4a4a-9962-f7b00ec861c4}"
```

Now import `output.streamDeckProfile` to your StreamDeck software and delete your old profile.
