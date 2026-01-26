# Go to test directory
 cd "$1"


# Build Docker images
docker compose build

# Get variables
results_path="${PWD}/results"
undo_path="${PWD}/results_undo"
git_root=$(git rev-parse --show-toplevel)
dir_name=$(basename "$PWD")
service_count=$(docker compose config --services | wc -l)


 #Run tests
 cd "$git_root"
 poetry run container-diffoscope "${dir_name}-base"  "${dir_name}-modified" --output-dir "$results_path"

# Cleanup Docker images
images_to_remove=$(docker images --format "{{.Repository}}" | grep "$dir_name"| sort)
images_array=($images_to_remove)


# Remove each image from the array
for image in "${images_array[@]}"; do
    echo "Removing image: $image"
    docker rmi "$image"
done