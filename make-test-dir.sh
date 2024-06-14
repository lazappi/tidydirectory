TEST_DIR="test-dir/"
ARCHIVE_DIR="$TEST_DIR/archive/"
DOCS_ARCHIVE="$ARCHIVE_DIR/documents/"
IMAGES_ARCHIVE="$ARCHIVE_DIR/images/"
DATA_ARCHIVE="$ARCHIVE_DIR/data/"
OTHER_ARCHIVE="$ARCHIVE_DIR/other/"
DIRS_ARCHIVE="$ARCHIVE_DIR/directories/"

if [[ $OSTYPE == 'darwin'* ]]; then
    OLD_TIME=$(date -v -10d '+%Y%m%d%H%M')
    EXPIRED_TIME=$(date -v -35d '+%Y%m%d%H%M')
else
    OLD_TIME=$(date --date="10 days ago" '+%Y%m%d%H%M')
    EXPIRED_TIME=$(date --date="35 days ago" '+%Y%m%d%H%M')
fi

if [ -d $TEST_DIR ]; then
    echo "Removing existing test directory..."
    rm -rf $TEST_DIR
fi
echo "Creating new test directory..."
mkdir $TEST_DIR
mkdir $ARCHIVE_DIR
mkdir $DOCS_ARCHIVE
mkdir $IMAGES_ARCHIVE
mkdir $DATA_ARCHIVE
mkdir $OTHER_ARCHIVE
mkdir $DIRS_ARCHIVE

# Make new files
echo "Adding new files..."
touch $TEST_DIR/new-document.txt
touch $TEST_DIR/new-image.jpg
touch $TEST_DIR/new-data.csv
touch $TEST_DIR/new-other.unknown
mkdir $TEST_DIR/new-directory
touch $TEST_DIR/new-directory/new-directory.file

# Make old files. These should be archived.
echo "Adding old files..."
touch -t $OLD_TIME $TEST_DIR/old-document.txt
touch -t $OLD_TIME $TEST_DIR/old-image.jpg
touch -t $OLD_TIME $TEST_DIR/old-data.csv
touch -t $OLD_TIME $TEST_DIR/old-other.unknown
mkdir $TEST_DIR/old-directory
touch -t $OLD_TIME $TEST_DIR/old-directory/old-directory.file

# Make archived files
echo "Adding archived files..."
touch $DOCS_ARCHIVE/archived-document.txt
touch $IMAGES_ARCHIVE/archived-image.jpg
touch $DATA_ARCHIVE/archived-data.csv
touch $OTHER_ARCHIVE/archived-other.unknown
mkdir $DIRS_ARCHIVE/archived-directory
touch $DIRS_ARCHIVE/archived-directory/archived-directory.file

# Make expired files. These should be deleted.
echo "Adding expired files..."
touch -t $EXPIRED_TIME $DOCS_ARCHIVE/expired-document.txt
touch -t $EXPIRED_TIME $IMAGES_ARCHIVE/expired-image.txt
touch -t $EXPIRED_TIME $DATA_ARCHIVE/expired-data.csv
touch -t $EXPIRED_TIME $OTHER_ARCHIVE/expired-other.unknown
mkdir $DIRS_ARCHIVE/expired-directory
touch -t $EXPIRED_TIME $DIRS_ARCHIVE/expired-directory/expired-directory.file
