dfiles=$(find . -type f -name "deploy.sh")
for d in $dfiles 
do
	echo "Executing $d"
	# Use dirname to get the base path
	fun_path=$(dirname $(realpath "$d"))
	cd $fun_path
	source deploy.sh
	cd -
done