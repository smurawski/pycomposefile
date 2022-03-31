from decimal import Decimal
from .service_deploy import Deploy
from .service_credential_spec import CredentialSpec
from .compose_element import ComposeElement


class Service(ComposeElement):
    supported_keys = {
        "image": str,
        "container_name": str,
        "cpu_count": Decimal,
        "command": str,
        "deploy": Deploy.from_parsed_yaml,
        "ports": str,
        "expose": str,
        "cpus": Decimal,
        "credential_spec": CredentialSpec.from_parsed_yaml,
    }

    unsupported_keys = {
        "blkio_config": ("Azure ContainerApps does not support persistent storage",
                         "",
                         "https://github.com/compose-spec/compose-spec/blob/master/spec.md#blkio_config"),
        "cpu_percent": ("Azure ContainerApps only supports CPU configuration by vCPU Count.  Configure that via cpu_count or in deploy/resources",
                        "https://docs.microsoft.com/azure/container-apps/containers#configuration",
                        "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_percent"),
        "cpu_shares": ("Azure ContainerApps only supports CPU configuration by vCPU Count.  Configure that via cpu_count or in deploy/resources",
                       "https://docs.microsoft.com/azure/container-apps/containers#configuration",
                       "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_shares"),
        "cpu_period": ("Azure ContainerApps only supports CPU configuration by vCPU Count.  Configure that via cpu_count or in deploy/resources",
                       "https://docs.microsoft.com/azure/container-apps/containers#configuration",
                       "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_period"),
        "cpu_quota": ("Azure ContainerApps only supports CPU configuration by vCPU Count.  Configure that via cpu_count or in deploy/resources",
                      "https://docs.microsoft.com/azure/container-apps/containers#configuration",
                      "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_quota"),
        "cpu_rt_runtime": ("Azure ContainerApps only supports CPU configuration by vCPU Count.  Configure that via cpu_count or in deploy/resources",
                           "https://docs.microsoft.com/azure/container-apps/containers#configuration",
                           "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_rt_runtime"),
        "cpu_rt_period": ("Azure ContainerApps only supports CPU configuration by vCPU Count.  Configure that via cpu_count or in deploy/resources",
                          "https://docs.microsoft.com/azure/container-apps/containers#configuration",
                          "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_rt_period"),
        "cpuset": ("Azure ContainerApps only supports CPU configuration by vCPU Count.  Configure that via cpu_count or in deploy/resources",
                   "https://docs.microsoft.com/azure/container-apps/containers#configuration",
                   "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpuset"),
        "build": ("Deployment to Azure ContainerApps requires an image from a repository",
                  "https://docs.microsoft.com/en-us/azure/container-apps/containers#configuration",
                  "https://github.com/compose-spec/compose-spec/blob/master/build.md"),
        "cap_add": ("Capabilities are not exposed by Azure ContainerApps",
                    "",
                    "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cap_add"),
        "cap_drop": ("Capabilities are not exposed by Azure ContainerApps",
                     "",
                     "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cap_add"),
        "cgroup_parent": ("cgroup configuration is not supported by Azure ContainerApps",
                          "",
                          "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cgroup_parent"),
        "configs": ("Configs exposed through the filesystem are not supported by Azure ContainerApps. Environment variables and secrets can be used",
                    "https://docs.microsoft.com/en-us/azure/container-apps/secure-app?tabs=arm-template#using-secrets",
                    "https://github.com/compose-spec/compose-spec/blob/master/spec.md#configs"),
    }
