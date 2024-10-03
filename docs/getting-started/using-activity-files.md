# Using Activity Files

Outdoor activities are usually recorded as `.GPX` or `.FIT` files. Some apps like [OsmAnd](https://osmand.net/) give you these files.

## Supported file formats

- FIT
- GPX
- TCX
- KML
- KMZ
- [Simra](https://www.digital-future.berlin/forschung/projekte/simra/) CSV export

# Add Activity Files

Before starting the service you need to create a folder for your activities and put at least one activity file in there.

Create a `Playground` folder on your storage somewhere and add a subfolder `Activities`. There you can add your activity files.  
For example:
```
~/
├─ Documents[or other location]/
│  ├─ Playground/
│  │  ├─ Activities/
│  │  │  ├─ 2024-03-03-17-42-10 Home to Bakery.gpx
```
The program will treat the files as read-only and does not modify them.  

You can extend the directory structure to sort them by different categories, see [Advanced Metadata Extraction](https://martin-ueding.github.io/geo-activity-playground/getting-started/using-activity-files/#advanced-metadata-extraction).
Once the service is running you can use the [Uploader](https://martin-ueding.github.io/geo-activity-playground/features/upload/) to avoid needing to restart.

# Metadata extraction

Most activity file formats contain basic data like date, time and track points.  
Each activity in geo-activity-playground has the metadata fields `kind`, `equipment` and `name`. These can be extracted for files that contain those.  

If no metadata is found, `kind` and `equipment` default to “Unknown”. The `name` is then extracted from the file name (without the suffix).  
So for `2024-03-03-17-42-10 Home to Bakery.gpx` the name is `2024-03-03-17-42-10 Home to Bakery`.

## Advanced Metadata extraction

Change how the name is read from file name by Regex expression

You can also add metadata via the file name and by putting files into respective directories.

If you want, you can use a naming and directory structure to fill in more meta data using regular expressions.

Using a regular expression with named capture groups one can extract these fields also from the files.

I for instance have the following file paths:

```
Activities/
├─ Ride/
│  ├─ Trekking Bike/
│  │  ├─ 2024-03-03-17-42-10.fit
├─ Hike/
│  ├─ Hiking Boots 2019/
│  │  ├─ 2024-03-03-11-03-18 Some nice place with Alice and Bob.fit
```

My structure is built such that the first directory level corresponds to the activity kind. The second level is the equipment used. Unique activities are directly in there as files. But there can also be a directory for the name and then just files with only the date as name. This way I can just put a lot of similar commutes there without having to name the files. In the first example I want it to take the name from the third directory. In either case I don't want to have the date to be part of the name.

In order to extract this data, I specify a list of regular expressions with named capture groups like `(?P<name>…)` where `name` is the field that you want to populate and `…` some regular expression. The program will try to _search_ (not _match_) the whole relative path of the activity to the regular expressions in the order given in the list. When it finds a match, it will take the capture groups, populate the metadata and stop evaluating more of the expressions. In my case they look like this:

```
(?P<kind>[^/]+)/(?P<equipment>[^/]+)/(?P<name>[^/]+)/
(?P<kind>[^/]+)/(?P<equipment>[^/]+)/[-\d_ ]+(?P<name>[^/]+)(?:\.\w+)+$
(?P<kind>[^/]+)/[-\d_ ]+(?P<name>[^/]+)(?:\.\w+)+$
```

Put something like that at the top of your `config.json` in your Playground folder.
 in order to extract metadata from the files and have it override metadata from the within the files.

## OsmAnd name format

### Extract name including weekday after date and time, as created by OSMAnd with added comment
```
re.search(r'(?P<kind>[^/]+)/(?P<equipment>[^/]+)/\d{4}-\d{2}-\d{2}_\d{2}-\d{2}_(?P<name>[^/.]*)', '/Ride/Trekkingrad/2024-09-25_10-28_Wed Zum Zahnarzt.gpx').groupdict()
{'kind': 'Ride', 'equipment': 'Trekkingrad', 'name': 'Wed Zum Zahnarzt'}
```

### Extract name after date, time and weekday, as created by OSMAnd with added comment
```
re.search(r'(?P<kind>[^/]+)/(?P<equipment>[^/]+)/\S+ ?(?P<name>[^/\.]*)', '/Ride/Trekkingrad/2024-09-25_10-28_Wed Zum Zahnarzt.gpx').groupdict()
{'kind': 'Ride', 'equipment': 'Trekkingrad', 'name': 'Zum Zahnarzt'}
```

### Extract name from file name
```
'(?P<kind>[^/]+)/(?P<equipment>[^/]+)/(?P<name>[^/.]+)'

'/Ride/Trekkingrad/2024-09-25_10-28_Wed Zum Zahnarzt.gpx'
{'kind': 'Ride',
 'equipment': 'Trekkingrad',
 'name': '2024-09-25_10-28_Wed Zum Zahnarzt'}

(?P<kind>[^/]+)/(?P<equipment>[^/]+)/(?P<name>[^/.]+)
```

## Next steps

Once you have your files put into the directory, you're all set and can proceed with the next steps.