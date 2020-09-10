# Trying to build with both tags at once. Didn't work as I expected it to.
# docker build . -t kevinmcgrath/gamma-tenant-manager:latest -t kevinmcgrath/gamma-tenant-manager:0.1.5

docker build . -t kevinmcgrath/gamma-tenant-manager:0.1.6

docker tag kevinmcgrath/gamma-tenant-manager:0.1.6 kevinmcgrath/gamma-tenant-manager:latest

docker push kevinmcgrath/gamma-tenant-manager:latest
docker push kevinmcgrath/gamma-tenant-manager:0.1.6

# On the VM:
# docker-compose up -d --build gamma-tenant
 #>