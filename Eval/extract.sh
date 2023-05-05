#! /bin/bash

USAGE='extract.sh [-g GRS_FILE] -c CORPUS [REQ_FILES]
Extracts the sentences of CORPUS having pattern given in REQ_FILES
  in a directory DIR per request file (erases the previous one).
Converts every .dep file in DIR to a png file with transparent background.

Options:
    -a            Only proceeds to the annotation phase
    -g GRS_FILE   Overwrites the input grs file. Default is fudia.grs
    -h, --help    Displays this help
    --no-png	  Does not creates dep and png files
    REQ_FILES     Overwrites the request files. Default request files are
    		    extract_Int_x.req for x in {1,2,3}
'

### Handling parameters

GRS="../fudia.grs" # grs default file name
SUF="Annotated"
REQ="extract_Int_1.req"
REQ2="extract_Int_2.req"
REQ3="extract_Int_3.req"
FIRST_REQ=true
REQ_FILES=("$REQ" "$REQ2" "$REQ3") # Default request files
PNG=true

while (( $# > 0 )) ; do
    case "$1" in
	"--help" | "-h" )     echo "$USAGE" ; exit ;;
	"--grs" | "-g" )      GRS="$2" ; shift ;;
	"--no-png" | "-n" )          PNG=false ;;
	"--corpus" | "-c" )   CORPUS="$2" ; shift ;;
	* )
	    if [[ $FIRST_REQ ]] ; then
		REQ_FILES=("$1") # Reinitializing REQ_FILES
		FIRST_REQ=false   
	    else
		REQ_FILES+=("$1") #Adding request file to a list
	    fi
	    ;;
    esac
    shift
done

if [[ "$GRS" != "../fudia.grs" ]] ; then
    SUF="${GRS##*/}"
    SUF="${SUF%.*}" # Name of the GRS file
fi

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

CDIR="${CORPUS%/*}" # Directory of Corpus
CORPUS="${CORPUS##*/}" # Name of Corpus in CDIR
OPWD=$(pwd)

###### Extraction

# Creating output files and directories
cd "$CDIR"
i=1
for FILE in "$OPWD/${REQ_FILES[@]}" ; do
    EXTRACTED="${CORPUS%.*}_$SUF_$i.json"
    OUTDIR="${CORPUS%.*}_$SUF_$i"
    [[ -d "$OUTDIR" ]] && rm -R "$OUTDIR"
    mkdir "$OUTDIR"

    # Running the request
    if [[ $PNG == "true" ]] ; then
	grew grep -request "$FILE" -i "$CORPUS" \
	     -html -dep_dir "$OUTDIR" > "$EXTRACTED"
    else
	grew grep -request "$FILE" -i "$CORPUS" -html
    fi

    i=$(($i + 1))
done

if [[ $PNG == "false" ]] ; then exit ; fi

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

# Applying conversion on all directories ending in _$SUF_x
# cd "$CDIR"
PREF="${CORPUS%.*}"
PREF="${PREF##*/}"
for DIR in $(ls -d */ | grep -E "$PREF""_$SUF_[0-9]+/") ; do
    cd "$DIR"
    echo "$DIR"
    dep2png
    cd ..
done
