from sshtunnel import SSHTunnelForwarder

def create_tunnel(ip: str, username: str, password: str, local_port: str, remote_port: int) -> SSHTunnelForwarder:
    server = SSHTunnelForwarder(
        ip,
        ssh_username=username,
        ssh_password=password,
        remote_bind_address=('0.0.0.0', remote_port)
    )
    server.start()
    return server
