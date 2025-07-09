locals {
  app = "${var.project}-picture"
}

data "kubernetes_service_account" "sa" {
  metadata {
    name      = "${var.project}-service-account"
    namespace = var.environment
  }
}

resource "kubernetes_deployment_v1" "picture_service" {
  metadata {
    name      = local.app
    namespace = var.environment
    labels = {
      app = local.app
      env = var.environment
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = local.app
        env = var.environment
      }
    }

    template {
      metadata {
        labels = {
          app = local.app
          env = var.environment
        }
      }

      spec {
        container {
          image = var.image
          name  = "${local.app}-cntr"

          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}
###############################################
# Picture K8S SERVICE
################################################
resource "kubernetes_service_v1" "picture_svc" {
  metadata {
    name      = "${local.app}-svc"
    namespace = var.environment
  }

  spec {
    selector = {
      app = kubernetes_deployment_v1.picture_service.spec[0].template[0].metadata[0].labels.app
      env = kubernetes_deployment_v1.picture_service.spec[0].template[0].metadata[0].labels.env
    }
    type = "ClusterIP"
    port {
      target_port = var.port
      port        = var.port
      protocol    = "TCP"
    }
  }
}
