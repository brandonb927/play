workflow "Build Docker Image" {
  resolves = [
    "Run Docker Build",
  ]
  on = "push"
}

action "Run Docker Build" {
  uses = "actions/docker/cli@master"
  args = "build -t battlesnake/play ."
}

workflow "Push Release Image to GCR" {
  resolves = [
    "Push Image to GCR",
  ]
  on = "release"
}

action "Master Branch Only" {
  uses = "actions/bin/filter@master"
  args = "branch master"
  needs = ["Run Docker Build"]
}

action "Tag Image for GCR" {
  uses = "actions/docker/tag@master"
  needs = ["Master Branch Only"]
  args = "battlesnake/play gcr.io/battlesnake-com/battlesnake/play"
}

action "Auth Google Cloud" {
  uses = "actions/gcloud/auth@master"
  needs = ["Master Branch Only"]
  secrets = ["GCLOUD_AUTH"]
}

action "Add GCR to Docker" {
  uses = "actions/gcloud/cli@master"
  args = "auth configure-docker --quiet"
  needs = ["Auth Google Cloud"]
}

action "Push Image to GCR" {
  uses = "actions/gcloud/cli@master"
  needs = ["Add GCR to Docker", "Tag Image for GCR"]
  runs = "sh -c"
  args = ["docker push gcr.io/battlesnake-com/battlesnake/play"]
}

