#! /bin/bash


USAGE='baseline_sent_ids.sh -b BASELINE -c CORPUS
Gets the sentence ids of the corpora annotated with BASELINE,
(for each conllu file in CORPUS, one per line, if CORPUS is not a conllu file)

Options:
    -h, --help    Displays this help
'


### Handling parameters

BASELINE="baseline1"

while (( $# > 0 )) ; do
    case "$1" in
	"--help" | "-h" )     echo "$USAGE" ; exit ;;
	"--baseline" | "-b" ) BASELINE="$2" ; shift ;;
	"--corpus" | "-c" )   CORPUS="$2" ; shift ;;
	* )
	    echo "Wrong parameter $1" >&2 ; echo "$USAGE" ; exit 5 ;;
    esac
    shift
done

# Testing if the files exist
if [[ ! -f "$CORPUS" ]] ; then
    echo "Wrong or missing corpus $CORPUS" >&2
    exit 2
fi

##### Retrieving ids

if [[ "${CORPUS##*.}" = "conll"* ]] ; then
    grep "# sent_id" "$CORPUS" | sed -E 's/# sent_id = (.*)/\1/g'
else
    CORPUS_LIST="$CORPUS"
    for CORPUS in $(cat "$CORPUS_LIST") ; do
	CDIR="${CORPUS_LIST%/*}" # Directory of Corpus
	# name of annotated output file
	CORPUS="$CDIR/${CORPUS%.*}_${BASELINE}.${CORPUS##*.}"
	echo "Getting ids from ${CORPUS##*/}..." >&2
	grep "# sent_id" "$CORPUS" | sed -E 's/# sent_id = (.*)/\1/g'
    done
fi
