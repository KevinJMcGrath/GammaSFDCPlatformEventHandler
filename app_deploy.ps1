docker build . -t kevinmcgrath/gamma-tenant-manager:latest -t kevinmcgrath/gamma-tenant-manager:0.1.3

docker push kevinmcgrath/gamma-tenant-manager:latest
docker push kevinmcgrath/gamma-tenant-manager:0.1.3

# On the VM:
# docker-compose up -d --build gamma-tenant
 #>