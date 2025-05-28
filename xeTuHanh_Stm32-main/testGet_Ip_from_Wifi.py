import socket
import fcntl
import struct

def get_wifi_ip(interface="wlan0"):
    try:
        # Tạo socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Lấy địa chỉ IP của giao diện mạng (wlan0)
        ip_address = socket.inet_ntoa(
            fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR: Lấy địa chỉ IP
                struct.pack('256s', interface[:15].encode('utf-8'))
            )[20:24]
        )
        return ip_address
    except Exception as e:
        return f"Không thể lấy địa chỉ IP của {interface}: {e}"

if __name__ == "__main__":
    interface = "wlan0"  # Giao diện WiFi mặc định
    ip = get_wifi_ip(interface)
    print(f"Địa chỉ IP WiFi ({interface}): {ip}")
