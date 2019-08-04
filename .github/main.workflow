workflow "Build and Push to GCR" {
  resolves = ["Build Image", "Push Image to GCR"]
  on = "push"
}

action "Build Docker Image" {
  uses = "actions/docker/cli@master"
  args = "build -t battlesnake/play ."
}

action "Master Branch Only" {
  uses = "actions/bin/filter@master"
  needs = ["Build Docker Image"]
  args = "branch master"
}

action "Tag Image for GCR" {
  uses = "actions/docker/tag@master"
  needs = ["Master Branch Only"]
  args = "battlesnake/play gcr.io/battlesnake-com/battlesnake/play"
}

action "Google Cloud Auth" {
  uses = "actions/gcloud/auth@master"
  needs = ["Master Branch Only"]
  secrets = ["GCLOUD_AUTH"]
}

action "Add GCR to Docker" {
  uses = "actions/gcloud/cli@master"
  needs = ["Google Cloud Auth"]
  args = "auth configure-docker --quiet"
}

action "Push Image to GCR" {
  uses = "actions/gcloud/cli@master"
  needs = ["Add GCR to Docker", "Tag Image for GCR"]
  runs = "sh -c"
  args = ["docker push gcr.io/battlesnake-com/battlesnake/play"]
}
