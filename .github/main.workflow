workflow "Build and Push to GCR" {
  resolves = ["Tag Image for GCR"]
  on = "push"
}

action "Build Docker Image" {
  uses = "actions/docker/cli@master"
  args = "build -t $CONTAINER_NAME ."
  env = {
    CONTAINER_NAME = "battlesnake/play"
  }
}

action "Tag Image for GCR" {
  uses = "actions/docker/tag@master"
  needs = ["Build Docker Image"]
  args = "$CONTAINER_NAME gcr.io/$GCLOUD_PROJECT_ID/$CONTAINER_NAME"
  env = {
    GCLOUD_PROJECT_ID = "battlesnake-io"
  }
}
