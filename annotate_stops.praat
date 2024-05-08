## Lenition labelling script ##
## James Tanner ##
## May 2024 ##

## point to the directory containing
## the wavs and CSV file
## and path to previous annotation session
form Process files...
	text path
	text outpath
	text prev_session_path
endform

## check if no session path was provided and make fresh table
if prev_session_path$ == ""
	Create Table with column names: "output", 0, { "filename", "label" }
## otherwise load the previous session's CSV if exists
else
	Read Table from comma-separated file: prev_session_path$
	Rename: "output"
endif

## get the wav directory path
wavs$# = fileNames$# (path$ + "wavs/" + "*.wav")

## start iterating through the stops
for i to size (wavs$#)
	basename$ = wavs$# [i] - ".wav"

	## check if the stop has already been annotated
	## e.g. in a previous session
	selectObject: "Table output"
	search_check$ = Search column: "filename", "'basename$'"
	search_value = extractNumber(search_check$, "")

	## if there's no record of the stop
	## initialise the annotation
	if search_value == 0
		Read from file: path$ + "wavs/" + wavs$# [i]
		## prompt user for stop annotation
		select Sound 'basename$'
		View & Edit
		beginPause: "Provide Label"
			comment: "Realised with a burst?"
		result = endPause: "Save progress & exit", "Burst", "No Burst", 0

		## convert user result to 0/1
		if result = 3
			stop_label = 1
		elsif result = 2
			stop_label = 0

		## save current set of annotations
		## and quit
		elsif result = 1
			selectObject: "Table output"
			Save as comma-separated file: outpath$
			select all
			Remove
			exitScript("Progress saved")
		endif

		## write the annotation to the table
		selectObject: "Table output"
			Append row
			row = Get number of rows
			Set string value: row, "filename", basename$
			Set numeric value: row, "label", stop_label
	
		removeObject: "Sound 'basename$'"
	endif
endfor

## once all of the stops in the session
## have been annotated, write out the table
selectObject: "Table output"
Save as comma-separated file: outpath$
select all
Remove
exitScript("All stops annotated! Written annotations to output CSV")
