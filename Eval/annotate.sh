#! /bin/bash

USAGE='annotate.sh [-g GRS_FILE] -c CORPUS
Creates a file with transformations given by the main strategy of the grs file,
(for each conllu file in CORPUS, one per line, if CORPUS is not a conllu file)

Options:
    -g GRS_FILE   Overwrites the input grs file. Default is fudia.grs
    -h, --help    Displays this help
'


### Handling parameters

GRS="../fudia.grs" # grs default file name
SUF="Annotated"

while (( $# > 0 )) ; do
    case "$1" in
	"--help" | "-h" )     echo "$USAGE" ; exit ;;
	"--grs" | "-g" )      GRS="$2" ; shift ;;
	"--corpus" | "-c" )   CORPUS="$2" ; shift ;;
	* )
	    echo "Wrong parameter $1" >&2 ; echo "$USAGE" ; exit 5 ;;
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


##### Annotation

CDIR="${CORPUS%/*}" # Directory of Corpus
OUTFILE="${CORPUS%.*}_${SUF}.${CORPUS##*.}" # name of annotated output file

[[ -f "$OUTFILE" ]] && rm "$OUTFILE"

if [[ "${CORPUS##*.}" = "conll"* ]] ; then
    grew transform -grs "$GRS" -i "$CORPUS" -o "$OUTFILE" -strat "main"
else
    CORPUS_LIST="$CORPUS"
    for CORPUS in $(cat "$CORPUS_LIST") ; do
	CDIR="${CORPUS_LIST%/*}" # Directory of Corpus
	CORPUS="$CDIR/$CORPUS"
	OUTFILE="${CORPUS%.*}_${SUF}.${CORPUS##*.}" # name of annotated output file
	echo "Annotating ${CORPUS##*/}..."
	grew transform -grs "$GRS" -i "$CORPUS" -o "$OUTFILE" -strat "main"
    done
fi



