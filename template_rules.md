# Template rules

## Columns 

The first column is the data type or is for human organization. `NEGATIVE_KEYWORDS` is a specially handled section. All other first column entries are ignored. In the normal case, the next columns are processed as keyword information.

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
 - Due to the word match policy, entries with a space included must have quotation marks around them.
 <!-- - All keywords must be in separate columns, or they will be interpreted as text match. -->

## Location replacement

Before filtering into adgroups, all locations are replaced with LOCATION.

## Resulting CSV data file

For every adgroup, every search phrase will be listed as follows, in order of frequency:
`[template] [phrase] [frequency]`