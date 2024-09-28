# Libraries
import socket as rcv_sock
import copy
import random
import datetime
import cv2
import numpy as np

# Extract packet ID, file ID, and trailer from the packet data
def extract_packet_data(packet):
    pkt_id = packet[0:16]
    file_id = packet[16:32]
    trailer = packet[-32:]
    return pkt_id, file_id, trailer


# Extract binary message content from packet
def get_packet_content(packet):
    return packet[32:-32]


# Function to convert binary data to image
def binary_to_image(binary_data, width, height):
    byte_sequence = bytearray(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))
    np_img = np.frombuffer(byte_sequence, dtype=np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR).reshape(height, width, 3)
    return image


# Initialize variables for image reconstruction
current_img_data = ''
last_acknowledgment = -1



# Create UDP socket for receiving packets
sock = rcv_sock.socket(rcv_sock.AF_INET, rcv_sock.SOCK_DGRAM)
sock.bind(('127.0.0.1', 12345))



# Predefined dimensions for images
image_sizes = [(800, 500), (1280, 720), (1280, 853), (800, 500), (1280, 720), (1280, 853)]


# Loop through multiple images
for img_idx in range(9):
    lost_packets = [random.randint(0, 399) for _ in range(55)]
    lost_packet_copy = copy.deepcopy(lost_packets)
    expected_pkt = 0



    # Loop for receiving packets
    while True:
        packet, sender_addr = sock.recvfrom(4096)
        pkt_id, file_id, trailer = extract_packet_data(packet.decode())
        pkt_id = int(pkt_id, 2)
        

        # If packet was marked as lost, skip it
        if pkt_id in lost_packets:
            lost_packets.remove(pkt_id)
            continue
        

        # If packet is the expected one, process it
        if pkt_id == expected_pkt:
            last_acknowledgment = expected_pkt
            expected_pkt += 1
            current_img_data += get_packet_content(packet.decode())

        # Send acknowledgment for received packets
        ack_msg = f"{last_acknowledgment}"
        sock.sendto(ack_msg.encode(), sender_addr)

        # Break if the last packet is detected
        if trailer == '00000000000000001111111111111111':
            break


    # Convert binary data back to image and save
    img_width, img_height = image_sizes[img_idx % len(image_sizes)]
    reconstructed_img = binary_to_image(current_img_data, img_width, img_height)
    output_name = f"reconstructed_image_{img_idx}.png"
    cv2.imwrite(output_name, reconstructed_img)
    print(f"Image saved as: {output_name}")


    # Reset the image data for the next image
    current_img_data = ''

# Close the receiving socket
sock.close()
