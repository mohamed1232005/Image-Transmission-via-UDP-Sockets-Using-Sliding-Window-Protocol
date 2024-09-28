# Libraries
import os
import math
import socket as net_sock
import time
import datetime
import cv2
import numpy as np

# Convert image file to a binary sequence
def img_to_bits(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    # Convert the image into bytes using JPEG format
    success, img_bytes = cv2.imencode('.jpeg', image)
    
    # Convert bytes to binary string representation
    if success:
        binary_stream = ''.join([format(byte, '08b') for byte in img_bytes.tobytes()])
        return binary_stream
    return ''



# Function to break the binary stream into packets
def create_packets(file_id, binary_data, chunk_size, total_chunks):
    packets = []
    # Iterating to create each packet with a unique ID and trailer
    for idx in range(math.ceil(total_chunks)):
        if idx != math.ceil(total_chunks) - 1:
            # Add metadata (packet ID, file ID, trailer) and a chunk of data
            packets.append(f"{bin(idx)[2:].zfill(16)}{bin(file_id)[2:].zfill(16)}{binary_data[:chunk_size]}{bin(0x0000)[2:].zfill(32)}")
        else:
            packets.append(f"{bin(idx)[2:].zfill(16)}{bin(file_id)[2:].zfill(16)}{binary_data[:chunk_size]}{bin(0xFFFF)[2:].zfill(32)}")
        binary_data = binary_data[chunk_size:]
    return packets



# Paths of images to be sent
img_paths = [
    "C:\\Users\\user\\Downloads\\small file.jpeg",
    "C:\\Users\\user\\Downloads\\medium file.jpeg",
    "C:\\Users\\user\\Downloads\\large file.jpeg"
]


# Set up the UDP socket
sock = net_sock.socket(net_sock.AF_INET, net_sock.SOCK_DGRAM)
port = 12345
receiver_addr = ('127.0.0.1', port)



# Parameters for transmission
win_size = [3, 5, 7]
timeouts = [0.5, 0.7, 0.9]
image_count = 0
resend_attempts = 0


for config_idx in range(3):
    for img_path in img_paths:
        # Convert the image to binary bits
        img_binary = img_to_bits(img_path)
        chunk_size = 1000
        file_id = 0
        chunk_total = len(img_binary) / chunk_size
        packet_list = create_packets(file_id, img_binary, chunk_size, chunk_total)

        base_index = 0
        next_pkt = 0


        # Start the transmission and measure time
        start_time = time.time()
        print(f"Sending image {image_count} with window size {win_size[config_idx]} and timeout {timeouts[config_idx]}")
        print(f"Transmission started at: {datetime.datetime.fromtimestamp(start_time)}")


        # Main loop for sending packets
        while base_index < len(packet_list):
            # Send packets in the window
            while next_pkt < base_index + win_size[config_idx] and next_pkt < len(packet_list):
                sock.sendto(packet_list[next_pkt].encode(), receiver_addr)
                next_pkt += 1


            # Acknowledgment loop or resend upon timeout
            while True:
                try:
                    sock.settimeout(timeouts[config_idx])
                    ack_data, _ = sock.recvfrom(4096)
                    ack_number = int(ack_data.decode())
                    if ack_number >= base_index:
                        base_index = ack_number + 1
                    if base_index == len(packet_list):
                        break
                except net_sock.timeout:
                    resend_attempts += 1
                    next_pkt = base_index  # Resend from the base if timeout occurs
                    break


        # Measure end time and calculate transmission stats
        end_time = time.time()
        print(f"End time: {datetime.datetime.fromtimestamp(end_time)}")
        print(f"Elapsed time: {end_time - start_time:.2f} seconds")
        print(f"Total number of packets: {chunk_total}")
        print(f"Resent packets: {resend_attempts}")
        print(f"Average rate: {chunk_total / (end_time - start_time + 0.000001)} packets/sec")

        image_count += 1

# Close the socket connection after the transfer
sock.close()
