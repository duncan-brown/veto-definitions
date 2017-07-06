# Documenting flag generation using `/scripts/`

The `/scripts/` directory should be used to contain command-line executable codes that can exactly reproduce the segments stored in the segment database for a given GPS `[start, end)` interval.

## Functionality

Each script should be executable as follows

```
./script-name {GPSSTART} {GPSEND} [.. options]
```

and should write out a `LIGO_LW`-format XML file with segment tables (either to a given file name, or to the screen) that contain the known and active segments that define a flag.

## Naming conventions

Each script should be stored in a dedicated directory named for the flag it was used to create, as follows

```
/scripts/{FLAG_NAME}/{script-name}
```

where `{FLAG_NAME}` should be, e.g, `DCH-MY_FLAG_NAME`, and should no include the `IFO` prefix or the version number suffix. The script itself should have a sensible name, that describes the purpose whilst not being too verbose.

In all, you might end up with something like

```
/scripts/DCH-EX_SUSRACK_MAG_GLITCHES/find-susrack-glitches
```

## Linking other scripts

There is no requirement that the script be a unique bit of code that operates specifically for this flag, It could be a simple shell script that calls out to something else with specific arguments, as long as it exactly reproduces the segments in the database.
