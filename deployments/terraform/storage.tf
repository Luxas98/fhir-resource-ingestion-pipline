resource "google_storage_bucket" "ingestion-data-store" {
  provider = "google-beta"
  name = "${google_project.project.project_id}"
  location = "${var.region}"
  project = "${google_project.project.project_id}"
  storage_class = "REGIONAL"
  force_destroy = true
}

resource "google_storage_bucket_acl" "ingestion-data-acl" {
  bucket = "${google_storage_bucket.ingestion-data-store.name}"
  role_entity = [
    "OWNER:user-${google_service_account.client-sa.email}"
  ]

  depends_on = [google_service_account.client-sa, google_storage_bucket.ingestion-data-store]
}

output "bucket_id" {
  value = "${google_storage_bucket.ingestion-data-store.id}"
}
