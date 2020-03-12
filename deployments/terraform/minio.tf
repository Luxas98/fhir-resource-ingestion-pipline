# Seems easier to setup through terraform then manually + kustomize
resource "google_service_account" "gcs-minio-admin" {
  project = "${google_project.project.project_id}"
  account_id   = "minio-admin"
  display_name = "GCS service account for min.io"
}

resource "google_service_account_key" "gcs-minio-admin-key" {
  service_account_id = "${google_service_account.gcs-minio-admin.name}"
}

resource "kubernetes_namespace" "minio" {
  provider = "kubernetes.primary"
  metadata {
    name = "minio"
  }
}

resource "kubernetes_secret" "gcs-minio-secret" {
  provider = "kubernetes.primary"
  metadata {
    name = "minio-gcs-credentials"
    namespace = kubernetes_namespace.minio.metadata.0.name
  }
  type = "Opaque"
  data = {
    "minio_gcs_credentials.json": base64decode(google_service_account_key.gcs-minio-admin-key.private_key)
  }
}

resource "random_password" "password" {
  length = 16
  special = true
  override_special = "_%@"
}

locals {
 secret_key = random_password.password.result
 access_key = "minio"
}

resource "kubernetes_secret" "minio-credentials" {
  provider = "kubernetes.primary"
  metadata {
    name = "minio-secret"
    namespace = kubernetes_namespace.minio.metadata.0.name
  }

  data = {
    MINIO_SECRET_KEY = local.secret_key
    MINIO_ACCESS_KEY = local.access_key
  }
}

resource "google_project_iam_member" "project" {
  project = "${google_project.project.project_id}"
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.gcs-minio-admin.email}"
}