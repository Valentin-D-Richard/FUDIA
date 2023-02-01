#! /bin/bash

USAGE='annotate_int [-a] [-g GRS_FILE] -c CORPUS [REQ_FILES]
Creates a file with transformations given by the main strategy of the grs file.
Extracts the sentences of CORPUS having pattern given in REQ_FILES
  in a directory DIR per request file (erases the previous one).
Converts every .dep file in DIR to a png file with transparent background.

Options:
    -a            Only proceeds to the annotation phase
    -g GRS_FILE   Overwrites the input grs file. Default is fudia.grs
    -h, --help    Displays this help
    REQ_FILES     Overwrites the request files. Default request files are
    		    extract_Int_x.req for x in {1,2,3}
'

### Handling parameters

GRS="fudia.grs" # grs default file name
REQ="extract_Int_1.req"
REQ2="extract_Int_2.req"
REQ3="extract_Int_3.req"
REQ_FILES=("$REQ" "$REQ2" "$REQ3") # Default request files
ANNOTATE_ONLY=false

while (( $# > 0 )) ; do
    case "$1" in
	"--help" | "-h" )     echo "$USAGE" ; exit ;;
	"--annotate" | "-a")  ANNOTATE_ONLY=true ;;
	"--grs" | "-g" )      GRS="$2" ; shift ;;
	"--corpus" | "-c" )   CORPUS="$2" ; shift ;;
	* )                   REQ_FILES+=("$1") ;; #Adding request file to a list
    esac
    shift
done

# Testing if the files exist
if [[ ! -f "$CORPUS" ]] ; then
    echo "Wrong or missing corpus $CORPUS" >&2
    exit 2
fi

if (( ${#REQ_FILES[@]} == 0 )) ; then
    echo "No request file given" >&2
    exit 3
fi

for FILE in "${REQ_FILES[@]}" ; do
    if [[ ! -f "$FILE" ]] ; then
	echo "Non-existing request file $FILE" >&2
	exit 1
    fi
done


##### Annotation

CDIR="${CORPUS%/*}" # Directory of Corpus
OUTFILE="${CORPUS%.*}_Annotated.${CORPUS##*.}" # name of annotated output file

[[ -f "$OUTFILE" ]] && rm "$OUTFILE"

grew transform -grs "$GRS" -i "$CORPUS" -o "$OUTFILE" -strat "main"

if $ANNOTATE_ONLY ; then exit ; fi

###### Extraction

# Creating output files and directories
i=1
for FILE in "${REQ_FILES[@]}" ; do
    EXTRACTED="${CORPUS%.*}_Int_$i.json"
    OUTDIR="${CORPUS%.*}_Int_$i"
    [[ -d "$OUTDIR" ]] && rm -R "$OUTDIR"
    mkdir "$OUTDIR"

    # Running the request
    grew grep -request "$FILE" -i "$OUTFILE" \
	 -html -dep_dir "$OUTDIR" > "$EXTRACTED"

    i=$(($i + 1))
done

##### Convertion into png

function dep2png() {
    for FILE in * ; do
	if [[ $FILE =~ .*\.dep ]] ; then
	    PNGFILE="${FILE%.*}.png"
	    dep2pict "$FILE" "$PNGFILE"
	    # Tranforms transparent into white
	    convert "$PNGFILE" -background white -alpha remove -flatten -alpha off "$PNGFILE"
	fi
    done
}

# Applying conversion on all directories ending in _Int_x
cd "$CDIR"
PREF="${CORPUS%.*}"
PREF="${PREF##*/}"
for DIR in $(ls -d */ | grep -E "$PREF""_Int_[0-9]+/") ; do
    cd "$DIR"
    echo "$DIR"
    dep2png
    cd ..
done

