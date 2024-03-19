dfiles=$(find . -type f -name "update.sh")
for d in $dfiles 
do
	echo "Executing $d"
	# Use dirname to get the base path
	fun_path=$(dirname $(realpath "$d"))
	cd $fun_path
	source update.sh
	cd -
done