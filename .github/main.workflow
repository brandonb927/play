workflow "Build Image" {
  resolves = [
    "Run Docker Build",
  ]
  on = "push"
}

action "Run Docker Build" {
  uses = "actions/docker/cli@master"
  args = "build -t battlesnake/play ."
}

workflow "Release to GCR" {
  resolves = [
    "Push Image to GCR",
  ]
  on = "release"
}

action "Tags Only" {
  uses = "actions/bin/filter@master"
  args = "tag v*"
  needs = ["Run Docker Build"]
}

action "Tag Image for GCR" {
  uses = "actions/docker/tag@master"
  args = "battlesnake/play gcr.io/battlesnake-com/battlesnake/play"
  needs = ["Tags Only"]
}

action "Auth Google Cloud" {
  uses = "actions/gcloud/auth@master"
  secrets = ["GCLOUD_AUTH"]
  needs = ["Tags Only"]
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
