# Trying to build with both tags at once. Didn't work as I expected it to.
# docker build . -t kevinmcgrath/gamma-tenant-manager:latest -t kevinmcgrath/gamma-tenant-manager:0.1.5

docker build . -t kevinmcgrath/gamma-tenant-manager:0.1.8

docker tag kevinmcgrath/gamma-tenant-manager:0.1.8 kevinmcgrath/gamma-tenant-manager:latest

docker push kevinmcgrath/gamma-tenant-manager:latest
docker push kevinmcgrath/gamma-tenant-manager:0.1.8

# On the VM:
# Update ~/docker/configs/config.json if changes were made
#
# docker image pull kevinmcgrath/gamma-tenant-manager:latest
# docker-compose up -d --build gamma-tenant
 #>