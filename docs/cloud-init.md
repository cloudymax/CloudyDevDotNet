# Cloud-Init Tools

I'm a huge fan of Cloud-init as an Ansible replacement and maintain a set of tools that lets me provision bare-metal, VMs, and cloud-instances with it. I find it to be the easiest way to declaratively set up a machine that you have pre-boot access to. If you cant used cloud-init because the machine was handed to you in an already provisioned state, thats when you can considder Ansible.

In addition to the tools below, all of my Terraform projects also accept cloud-init as a configuration option.

## Templating
- [Cloud-Init Templates](https://github.com/buildstar-online/cloud-init-templates)
- [Cloud-Init Generator](https://github.com/buildstar-online/cloud-init-generator)

## Bare-Metal

- [PXEless](https://github.com/cloudymax/pxeless/)

## Virtual Machines

- [Scrap-Metal](https://github.com/cloudymax/Scrap-Metal)
- [Kubevirt Charts](https://github.com/cloudymax/kubevirt-charts)
