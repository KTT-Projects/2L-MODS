import stun
 
 
def get_public_ip_and_port():
    nat_type, external_ip, external_port = stun.get_ip_info()
    return nat_type, external_ip, external_port
 
 
if __name__ == "__main__":
    nat_type, public_ip, public_port = get_public_ip_and_port()
    print(f"Public IP: {public_ip}")
    print(f"Public UDP Port: {public_port}")
    print(f"NAT Type: {nat_type}")
