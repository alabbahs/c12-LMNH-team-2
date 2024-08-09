#!/bin/bash

REPOSITORY_NAME=c12-joshua-archive-ecs
REGION=eu-west-2
IMAGE_TAG=latest
ECR_URL=129033205317.dkr.ecr.eu-west-2.amazonaws.com
SUBDIR=archive

# Step 1: Check if the image already exists in the ECR repository (optional for logging purposes)
echo "Checking if the Docker image already exists in Amazon ECR..."
IMAGE_EXISTS=$(aws ecr describe-images --repository-name $REPOSITORY_NAME --region $REGION --query "imageDetails[?imageTags[?contains(@, '$IMAGE_TAG')]].imageTags[]" --output text)

if [[ "$IMAGE_EXISTS" == *"$IMAGE_TAG"* ]]; then
    echo "Image with tag '$IMAGE_TAG' already exists in the repository '$REPOSITORY_NAME'."
else
    echo "Image with tag '$IMAGE_TAG' does not exist in the repository '$REPOSITORY_NAME'."
fi

# Step 2: Copy requirements.txt into the archive directory
echo "Copying requirements.txt into the $SUBDIR directory..."
cp requirements.txt $SUBDIR/
if [ $? -ne 0 ]; then
    echo "Failed to copy requirements.txt."
    exit 1
fi
echo "requirements.txt copied successfully."

# Step 3: Login to ECR
echo "Logging in to Amazon ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_URL/$REPOSITORY_NAME
if [ $? -ne 0 ]; then
    echo "Failed to login to Amazon ECR."
    exit 1
fi
echo "Login succeeded."

# Step 4: Build the Docker image
echo "Building the Docker image..."
docker build -t archive:$IMAGE_TAG -f $SUBDIR/Dockerfile $SUBDIR --platform "linux/amd64"
if [ $? -ne 0 ]; then
    echo "Docker build failed."
    exit 1
fi
echo "Docker build succeeded."

# Step 5: Tag the Docker image
echo "Tagging the Docker image..."
docker tag archive:$IMAGE_TAG $ECR_URL/$REPOSITORY_NAME:$IMAGE_TAG
if [ $? -ne 0 ]; then
    echo "Failed to tag the Docker image."
    exit 1
fi
echo "Docker image tagged successfully."

# Step 6: Push the Docker image to ECR
echo "Pushing the Docker image to Amazon ECR..."
docker push $ECR_URL/$REPOSITORY_NAME:$IMAGE_TAG
if [ $? -ne 0 ]; then
    echo "Failed to push the Docker image to Amazon ECR."
    exit 1
fi
echo "Docker image pushed to Amazon ECR successfully."

# Step 7: Clean up copied requirements.txt from archive directory
echo "Cleaning up requirements.txt from the $SUBDIR directory..."
rm $SUBDIR/requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to clean up requirements.txt."
    exit 1
fi
echo "Clean up succeeded."
