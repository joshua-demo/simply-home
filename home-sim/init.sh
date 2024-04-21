echo "init home-sim"
echo "note: this script should be run from the home-sim directory"

# if current directory is not home-sim, exit
# TODO

# copy over default.json to data.json
cp app/api/default.json app/api/data.json
echo "copied default.json to data.json"