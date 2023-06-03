trap 'kill %1; kill %2; kill %3; kill %4; kill %5; kill %6; kill %7; kill %8' SIGINT
python3 serv0.py & \
python3 serv1.py & \
# python3 serv2.py & \
python3 serv3.py & \
# python3 serv4.py & \
# python3 serv5.py & \
# python3 serv6.py & \
# python3 serv7.py & \
# python3 serv8.py & \
# python3 serv9.py