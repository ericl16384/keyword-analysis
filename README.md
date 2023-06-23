# keyword-analysis

<!-- (I don't really intend to work to hard on the README.) -->

Attempting to automate a solution for Jake's problem.

<!-- I will use Python to start because it is the easiest, but perhaps I will switch to JavaScript so it is more portable and works better with his workflow. -->

https://youtu.be/AOO_u33z7LE

<!-- *There are still a number of TODO items*

Please try each command. I am still working on implementing them, and some of them may just say "TODO." -->

## Columns 

Except for the fitst column, columns are processed as keyword information.

## Search order

Mr. Barr requested that there be no duplicates across the lists formed. Therefore, the priority order is the ranking of the keyword, followed by its specificity. This means that if a row has empty places at the beginning, it is interpreted as belonging to the nearest row above it that contains `1` less empty place.

### Example
```
abortion		
	     finder	
	     pill	
		        cost
		        free
```
The above will be ordered as the following adgroups:
```
abortion finder
abortion pill cost
abortion pill free
abortion pill
abortion
```

## Word match and exact match

Text-match example: `butterflies` or `nice` will hit the phrase `butterflies are nice`, but `butter` or `flies` or `ice` will also.
Word-match example: `"butterflies"` or `"nice"` will hit the phrase `butterflies are nice`, not `butter` or `flies` or `ice`.

## Keyword information

 - No capitalization was found in keywords.csv, so capitalization is ignored.
 - By default, keywords are searched by text-match, not word match. To search by word-match, place `"` quotation marks (not `“` or `”`) around the entire entry. Variations from this should raise an error.
   - IMPORTANT: This is not yet implemented. It currently searches by text-match only.
 <!-- - Due to the word-match policy, entries with a space included must have quotation marks around them. -->
 <!-- - All keywords must be in separate columns, or they will be interpreted as text match. -->

## Location replacement

Before filtering into adgroups, all locations are replaced with LOCATION. Locations are replaced with word-match to improve performance. This is disabled by default in config.

## Resulting CSV data file

For every adgroup, every search phrase will be listed as follows, in order of frequency:
`[adgroup] [phrase] [frequency]`

## Config

See `config.json`. Rerun the program after editing and saving.

## Data sources

https://data.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000%40public/export/?disjunctive.cou_name_en
for city data

https://gist.github.com/keeguon/2310008
for country data

https://gist.github.com/mshafrir/2646763
for state data

https://github.com/getify/dwordly-game/blob/main/
for six, five, four, three, and two letter words

