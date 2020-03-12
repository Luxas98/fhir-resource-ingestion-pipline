provider "google-beta" {
  alias = "google-beta"
  region = "${var.region}"
  credentials="${file("../../tf-admin.json")}"
}

provider "kubernetes" {
  alias = "primary"
  host = "${google_container_cluster.primary.endpoint}"
  cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
}