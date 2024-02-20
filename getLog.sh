
dfiles=$(find . -maxdepth 1 -type d -name "MS*Entry" -exec basename {} \;)
folder_name="logs"
if [ ! -d "$folder_name" ]; then
    mkdir "$folder_name"
    echo "Folder created: $folder_name"
else
    echo "Folder already exists: $folder_name"
fi

for d in $dfiles 
do
	echo "Retreiving log of function $d"
	gcloud functions logs read $d  --gen2 --project=modellearning --region=northamerica-northeast1  --limit=1000 | grep "cpu" > "$folder_name/$d.csv"
done 